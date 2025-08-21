#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "click>=8.1",
#     "rich>=13.7",
#     "filelock>=3.13",
# ]
# ///
"""
Session Manager - Session lifecycle management for v2 orchestration.

Manages session creation, loading, saving, and expiration with proper file locking.

Usage:
    uv run session_manager.py create --mode development
    uv run session_manager.py load SESSION_ID
    uv run session_manager.py save SESSION_ID --state-file state.json
    uv run session_manager.py expire SESSION_ID
    uv run session_manager.py list-active
    uv run session_manager.py info SESSION_ID
"""

import json
import sys
import uuid
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from contextlib import contextmanager

import click
from filelock import FileLock, Timeout
from rich.console import Console
from rich.json import JSON
from rich.table import Table
from rich.panel import Panel
from rich import box
from rich.syntax import Syntax

console = Console()

# Base directory for state files
STATE_DIR = Path.cwd() / ".claude" / "state"
LOCK_TIMEOUT = 5.0  # seconds

# Session modes
VALID_MODES = ["development", "leadership", "config", "emergency"]


class SessionManager:
    """Manages session lifecycle operations."""
    
    def __init__(self):
        # Ensure directories exist
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        (STATE_DIR / "events").mkdir(exist_ok=True)
    
    @contextmanager
    def _acquire_lock(self, session_id: str):
        """Acquire exclusive lock on session."""
        lock_file = STATE_DIR / f"session-{session_id}.lock"
        lock = FileLock(lock_file, timeout=LOCK_TIMEOUT)
        try:
            with lock:
                yield
        except Timeout:
            console.print(f"[red]Error: Could not acquire lock for session {session_id}[/red]")
            sys.exit(1)
    
    def create_session(self, mode: str = "development") -> Dict:
        """Initialize new session."""
        if mode not in VALID_MODES:
            raise ValueError(f"Invalid mode: {mode}. Must be one of {VALID_MODES}")
        
        session_id = str(uuid.uuid4())
        state_file = STATE_DIR / f"session-{session_id}.json"
        event_log = STATE_DIR / "events" / f"session-{session_id}.jsonl"
        
        # Create initial state
        state = self._create_initial_state(session_id, mode)
        
        # Apply mode-specific initialization
        state = self._initialize_mode(state, mode)
        
        # Save state atomically
        try:
            temp_file = state_file.with_suffix('.tmp')
            with temp_file.open('w') as f:
                json.dump(state, f, indent=2, default=str)
            temp_file.replace(state_file)
            
            # Create event log
            event_log.touch()
            
            # Log creation event
            self._log_event(session_id, "session_created", {
                "mode": mode,
                "workspace": str(Path.cwd())
            })
            
            return state
            
        except Exception as e:
            console.print(f"[red]Error creating session: {e}[/red]")
            sys.exit(1)
    
    def load_session(self, session_id: str) -> Optional[Dict]:
        """Load existing session."""
        state_file = STATE_DIR / f"session-{session_id}.json"
        
        if not state_file.exists():
            console.print(f"[red]Error: Session {session_id} not found[/red]")
            return None
        
        with self._acquire_lock(session_id):
            try:
                with state_file.open('r') as f:
                    state = json.load(f)
                
                # Update last activity
                if "session" in state and "lifecycle" in state["session"]:
                    state["session"]["lifecycle"]["last_activity"] = datetime.now().isoformat()
                
                # Log load event
                self._log_event(session_id, "session_loaded", {})
                
                return state
                
            except json.JSONDecodeError as e:
                console.print(f"[red]Error: Invalid JSON in state file: {e}[/red]")
                return None
    
    def save_session(self, session_id: str, state: Dict) -> bool:
        """Persist state to disk."""
        state_file = STATE_DIR / f"session-{session_id}.json"
        
        with self._acquire_lock(session_id):
            try:
                # Update metadata
                if "session" in state:
                    state["session"]["updated_at"] = datetime.now().isoformat()
                    if "lifecycle" in state["session"]:
                        state["session"]["lifecycle"]["last_activity"] = datetime.now().isoformat()
                
                # Update persistence metadata
                if "persistence" in state and "checkpoint" in state["persistence"]:
                    checkpoint = state["persistence"]["checkpoint"]
                    checkpoint["last_saved"] = datetime.now().isoformat()
                    checkpoint["sequence"] = checkpoint.get("sequence", 0) + 1
                    checkpoint["size_bytes"] = len(json.dumps(state))
                
                # Save atomically
                temp_file = state_file.with_suffix('.tmp')
                with temp_file.open('w') as f:
                    json.dump(state, f, indent=2, default=str)
                temp_file.replace(state_file)
                
                # Log save event
                self._log_event(session_id, "session_saved", {
                    "checkpoint_sequence": state.get("persistence", {}).get("checkpoint", {}).get("sequence", 0)
                })
                
                return True
                
            except Exception as e:
                console.print(f"[red]Error saving session: {e}[/red]")
                return False
    
    def expire_session(self, session_id: str) -> bool:
        """Mark session for cleanup."""
        state_file = STATE_DIR / f"session-{session_id}.json"
        
        if not state_file.exists():
            console.print(f"[yellow]Warning: Session {session_id} not found[/yellow]")
            return True
        
        with self._acquire_lock(session_id):
            try:
                # Load state
                with state_file.open('r') as f:
                    state = json.load(f)
                
                # Update lifecycle
                if "session" in state and "lifecycle" in state["session"]:
                    state["session"]["lifecycle"]["status"] = "terminating"
                    state["session"]["lifecycle"]["expiry"] = datetime.now().isoformat()
                
                # Save changes
                temp_file = state_file.with_suffix('.tmp')
                with temp_file.open('w') as f:
                    json.dump(state, f, indent=2, default=str)
                temp_file.replace(state_file)
                
                # Log expiration event
                self._log_event(session_id, "session_expired", {})
                
                return True
                
            except Exception as e:
                console.print(f"[red]Error expiring session: {e}[/red]")
                return False
    
    def get_active_sessions(self) -> List[Dict]:
        """List active sessions."""
        sessions = []
        
        if not STATE_DIR.exists():
            return sessions
        
        for state_file in STATE_DIR.glob("session-*.json"):
            try:
                session_id = state_file.stem.replace("session-", "")
                
                with state_file.open('r') as f:
                    state = json.load(f)
                
                session_info = state.get("session", {})
                lifecycle = session_info.get("lifecycle", {})
                
                # Only include active sessions
                if lifecycle.get("status") in ["active", "initializing", "suspended"]:
                    sessions.append({
                        "id": session_id,
                        "mode": session_info.get("mode", "unknown"),
                        "status": lifecycle.get("status", "unknown"),
                        "created_at": session_info.get("created_at", ""),
                        "last_activity": lifecycle.get("last_activity", ""),
                        "workspace": session_info.get("user_context", {}).get("workspace_path", ""),
                        "tasks": len(state.get("execution", {}).get("tasks", {})),
                        "agents": len(state.get("execution", {}).get("agents", {}).get("active", {}))
                    })
                    
            except Exception as e:
                console.print(f"[yellow]Warning: Could not read session {session_id}: {e}[/yellow]")
        
        return sessions
    
    def _create_initial_state(self, session_id: str, mode: str) -> Dict:
        """Create initial state structure."""
        return {
            "session": {
                "id": session_id,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "mode": mode,
                "user_context": {
                    "workspace_path": str(Path.cwd()),
                    "project_name": Path.cwd().name,
                    "user_preferences": {
                        "max_parallel_agents": 5,
                        "auto_persistence_interval": 30,
                        "consent_mode": "explicit"
                    }
                },
                "lifecycle": {
                    "status": "initializing",
                    "last_activity": datetime.now().isoformat(),
                    "expiry": (datetime.now() + timedelta(hours=8)).isoformat(),
                    "auto_cleanup": True
                }
            },
            "organization": {
                "teams": {},
                "projects": {},
                "global_settings": {
                    "token_budget": 100000,
                    "time_budget_minutes": 480,
                    "max_concurrent_agents": 10
                }
            },
            "execution": {
                "agents": {"active": {}, "pool": {}},
                "tasks": {},
                "workflows": {"active_sprints": [], "epics": {}}
            },
            "communication": {
                "message_queues": {},
                "channels": {"broadcast": [], "emergency": [], "handoffs": []},
                "coordination": {
                    "locks": {},
                    "dependencies": {"graph": {"nodes": {}, "edges": []}, "blocks": []}
                }
            },
            "observability": {
                "metrics": {
                    "performance": {
                        "session_duration_seconds": 0,
                        "total_tokens_used": 0,
                        "average_response_time_ms": 0,
                        "agent_spawn_time_ms": 0
                    },
                    "utilization": {
                        "agent_utilization_rate": 0.0,
                        "memory_usage_mb": 0,
                        "cpu_usage_percent": 0,
                        "active_connections": 0
                    },
                    "quality": {
                        "task_completion_rate": 0.0,
                        "error_rate": 0.0,
                        "test_coverage_percent": 0,
                        "code_quality_score": 0
                    }
                },
                "events": {"recent": [], "event_stream_offset": 0},
                "health": {
                    "system_status": "healthy",
                    "checks": {}
                }
            },
            "persistence": {
                "checkpoint": {
                    "last_saved": datetime.now().isoformat(),
                    "sequence": 0,
                    "size_bytes": 0
                },
                "event_log": {
                    "current_offset": 0,
                    "total_events": 0,
                    "log_files": []
                }
            }
        }
    
    def _initialize_mode(self, state: Dict, mode: str) -> Dict:
        """Apply mode-specific initialization."""
        if mode == "development":
            # Load engineering team
            state["organization"]["teams"]["engineering"] = {
                "name": "Engineering Team",
                "orchestrator": "engineering-director",
                "members": [
                    {"agent_id": "engineering-lead", "role": "Technical Lead", "capacity": 1, "status": "available"},
                    {"agent_id": "engineering-fullstack", "role": "Full Stack Developer", "capacity": 3, "status": "available"},
                    {"agent_id": "engineering-test", "role": "QA Engineer", "capacity": 2, "status": "available"}
                ],
                "settings": {
                    "max_parallel": 5,
                    "require_approval": True,
                    "auto_scaling": False
                }
            }
            
        elif mode == "leadership":
            # Load all teams for cross-functional work
            teams = ["product", "engineering", "qa", "devops", "creative", "data"]
            for team in teams:
                state["organization"]["teams"][team] = {
                    "name": f"{team.title()} Team",
                    "orchestrator": f"{team}-director",
                    "members": [],
                    "settings": {
                        "max_parallel": 3,
                        "require_approval": True,
                        "auto_scaling": True
                    }
                }
        
        elif mode == "emergency":
            # Minimal setup for emergency response
            state["organization"]["global_settings"]["max_concurrent_agents"] = 20
            state["session"]["lifecycle"]["auto_cleanup"] = False
            state["session"]["user_context"]["user_preferences"]["consent_mode"] = "automatic"
        
        # Update status to active
        state["session"]["lifecycle"]["status"] = "active"
        
        return state
    
    def _log_event(self, session_id: str, event_type: str, data: Dict):
        """Log event to event store."""
        event_log = STATE_DIR / "events" / f"session-{session_id}.jsonl"
        
        event = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.now().isoformat(),
            "type": event_type,
            "source": "session_manager",
            "severity": "info",
            "data": data,
            "session_id": session_id
        }
        
        try:
            with event_log.open('a') as f:
                f.write(json.dumps(event, separators=(',', ':')) + '\n')
        except Exception:
            pass  # Silently fail event logging


@click.group()
def cli():
    """Session Manager - Session lifecycle management for v2 orchestration."""
    pass


@cli.command()
@click.option('--mode', default='development', type=click.Choice(VALID_MODES), help='Orchestration mode')
def create(mode: str):
    """Initialize new session."""
    manager = SessionManager()
    state = manager.create_session(mode)
    
    session_id = state["session"]["id"]
    console.print(Panel(
        f"[green]✓ Session created successfully[/green]\n\n"
        f"[cyan]Session ID:[/cyan] {session_id}\n"
        f"[cyan]Mode:[/cyan] {mode}\n"
        f"[cyan]Workspace:[/cyan] {Path.cwd()}\n"
        f"[cyan]Expiry:[/cyan] {state['session']['lifecycle']['expiry'].split('T')[0]}",
        title="New Session",
        box=box.ROUNDED
    ))
    
    # Show session ID for easy copying
    console.print(f"\n[dim]Use this ID for further operations:[/dim]\n{session_id}")


@cli.command()
@click.argument('session_id')
def load(session_id: str):
    """Load existing session."""
    manager = SessionManager()
    state = manager.load_session(session_id)
    
    if state:
        session_info = state.get("session", {})
        lifecycle = session_info.get("lifecycle", {})
        execution = state.get("execution", {})
        
        console.print(Panel(
            f"[green]✓ Session loaded successfully[/green]\n\n"
            f"[cyan]Mode:[/cyan] {session_info.get('mode', 'unknown')}\n"
            f"[cyan]Status:[/cyan] {lifecycle.get('status', 'unknown')}\n"
            f"[cyan]Created:[/cyan] {session_info.get('created_at', '').split('T')[0]}\n"
            f"[cyan]Tasks:[/cyan] {len(execution.get('tasks', {}))}\n"
            f"[cyan]Active Agents:[/cyan] {len(execution.get('agents', {}).get('active', {}))}",
            title=f"Session {session_id[:8]}...",
            box=box.ROUNDED
        ))
        
        # Show recent events
        events = state.get("observability", {}).get("events", {}).get("recent", [])
        if events:
            console.print("\n[bold]Recent Events:[/bold]")
            for event in events[-5:]:
                console.print(f"  • [{event['severity']}] {event['type']} - {event['timestamp'].split('T')[1].split('.')[0]}")


@cli.command()
@click.argument('session_id')
@click.option('--state-file', type=click.Path(exists=True), help='JSON file with state data')
def save(session_id: str, state_file: str):
    """Save session state."""
    manager = SessionManager()
    
    if state_file:
        # Load state from file
        try:
            with open(state_file, 'r') as f:
                state = json.load(f)
        except Exception as e:
            console.print(f"[red]Error reading state file: {e}[/red]")
            sys.exit(1)
    else:
        # Load current state
        state = manager.load_session(session_id)
        if not state:
            sys.exit(1)
    
    if manager.save_session(session_id, state):
        console.print(f"[green]✓ Session {session_id} saved successfully[/green]")
    else:
        console.print(f"[red]✗ Failed to save session[/red]")
        sys.exit(1)


@cli.command()
@click.argument('session_id')
def expire(session_id: str):
    """Mark session for cleanup."""
    manager = SessionManager()
    
    if manager.expire_session(session_id):
        console.print(f"[green]✓ Session {session_id} marked for expiration[/green]")
    else:
        console.print(f"[red]✗ Failed to expire session[/red]")
        sys.exit(1)


@cli.command('list-active')
def list_active():
    """List active sessions."""
    manager = SessionManager()
    sessions = manager.get_active_sessions()
    
    if not sessions:
        console.print("[yellow]No active sessions found[/yellow]")
        return
    
    table = Table(title="Active Sessions", box=box.ROUNDED)
    table.add_column("Session ID", style="cyan")
    table.add_column("Mode", style="magenta")
    table.add_column("Status", style="green")
    table.add_column("Workspace", style="blue")
    table.add_column("Tasks", justify="right")
    table.add_column("Agents", justify="right")
    table.add_column("Last Activity", style="yellow")
    
    for session in sessions:
        status_color = {
            "active": "green",
            "initializing": "yellow",
            "suspended": "red"
        }.get(session["status"], "white")
        
        workspace = Path(session["workspace"]).name if session["workspace"] else "N/A"
        
        table.add_row(
            session["id"][:8] + "...",
            session["mode"],
            f"[{status_color}]{session['status']}[/{status_color}]",
            workspace,
            str(session["tasks"]),
            str(session["agents"]),
            session["last_activity"].split('T')[0] if session["last_activity"] else "N/A"
        )
    
    console.print(table)


@cli.command()
@click.argument('session_id')
def info(session_id: str):
    """Show detailed session information."""
    manager = SessionManager()
    state = manager.load_session(session_id)
    
    if not state:
        sys.exit(1)
    
    # Display session overview
    session = state.get("session", {})
    lifecycle = session.get("lifecycle", {})
    
    console.print(Panel(
        f"[bold cyan]Session Information[/bold cyan]\n\n"
        f"ID: {session.get('id', 'unknown')}\n"
        f"Mode: {session.get('mode', 'unknown')}\n"
        f"Status: {lifecycle.get('status', 'unknown')}\n"
        f"Created: {session.get('created_at', '')}\n"
        f"Last Activity: {lifecycle.get('last_activity', '')}\n"
        f"Expiry: {lifecycle.get('expiry', '')}\n"
        f"Auto Cleanup: {lifecycle.get('auto_cleanup', False)}",
        title="Session Details",
        box=box.ROUNDED
    ))
    
    # Show metrics
    metrics = state.get("observability", {}).get("metrics", {})
    if metrics:
        console.print("\n[bold]Performance Metrics:[/bold]")
        perf = metrics.get("performance", {})
        console.print(f"  • Session Duration: {perf.get('session_duration_seconds', 0)}s")
        console.print(f"  • Total Tokens: {perf.get('total_tokens_used', 0)}")
        
        util = metrics.get("utilization", {})
        console.print(f"  • Agent Utilization: {util.get('agent_utilization_rate', 0):.1%}")
        console.print(f"  • Memory Usage: {util.get('memory_usage_mb', 0)} MB")
    
    # Show teams
    teams = state.get("organization", {}).get("teams", {})
    if teams:
        console.print("\n[bold]Teams:[/bold]")
        for team_id, team in teams.items():
            console.print(f"  • {team.get('name', team_id)}: {len(team.get('members', []))} members")


if __name__ == "__main__":
    cli()