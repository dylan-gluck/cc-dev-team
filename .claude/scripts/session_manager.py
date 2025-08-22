#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "click>=8.1",
#     "rich>=13.0",
#     "filelock>=3.12",
# ]
# ///
"""
Session Manager for V2 Orchestration System.

Manages session lifecycle including creation, heartbeat, handoff, and recovery.
Supports different session modes and provides coordination between sessions.

Usage:
    ./session_manager.py create --mode development --project myapp
    ./session_manager.py heartbeat SESSION_ID
    ./session_manager.py handoff FROM_SESSION TO_SESSION
    ./session_manager.py list --active --project myapp
    ./session_manager.py recover SESSION_ID
"""

import json
import sys
import uuid
import tempfile
from pathlib import Path
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional
from enum import Enum
import logging

import click
from filelock import FileLock
from rich.console import Console
from rich.table import Table
from rich.json import JSON as RichJSON

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# State directory configuration
STATE_DIR = Path.home() / ".claude" / "state" / "sessions"
STATE_DIR.mkdir(parents=True, exist_ok=True)

console = Console()


class SessionMode(str, Enum):
    """Session execution modes."""
    DEVELOPMENT = "development"
    LEADERSHIP = "leadership"
    SPRINT = "sprint"
    CONFIG = "config"


class SessionStatus(str, Enum):
    """Session lifecycle status."""
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"


class SessionManager:
    """Manages session lifecycle and coordination."""
    
    def __init__(self):
        self.state_dir = STATE_DIR
    
    def _get_state_file(self, session_id: str) -> Path:
        """Get the path to a session's state file."""
        return self.state_dir / f"{session_id}.json"
    
    def _get_lock_file(self, session_id: str) -> Path:
        """Get the path to a session's lock file."""
        return self.state_dir / f"{session_id}.lock"
    
    def _load_state(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Load session state from file."""
        state_file = self._get_state_file(session_id)
        
        if not state_file.exists():
            return None
        
        try:
            with open(state_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading session {session_id}: {e}")
            return None
    
    def _save_state(self, session_id: str, state: Dict[str, Any]) -> None:
        """Save session state to file atomically."""
        state_file = self._get_state_file(session_id)
        
        # Write to temporary file first (atomic operation)
        with tempfile.NamedTemporaryFile(
            mode='w',
            dir=self.state_dir,
            prefix=f".{session_id}.",
            suffix='.tmp',
            delete=False
        ) as tmp_file:
            json.dump(state, tmp_file, indent=2, default=str)
            tmp_path = Path(tmp_file.name)
        
        # Atomically replace the original file
        tmp_path.replace(state_file)
    
    def create(
        self,
        mode: SessionMode,
        project: Optional[str] = None,
        parent_session: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """Create a new session with unique ID."""
        session_id = str(uuid.uuid4())
        now = datetime.now(timezone.utc)
        
        # Set expiry based on mode
        expiry_hours = {
            SessionMode.DEVELOPMENT: 24,
            SessionMode.LEADERSHIP: 48,
            SessionMode.SPRINT: 168,  # 1 week
            SessionMode.CONFIG: 1
        }
        
        expiry = now + timedelta(hours=expiry_hours.get(mode, 24))
        
        state = {
            "session": {
                "id": session_id,
                "mode": mode.value if isinstance(mode, SessionMode) else mode,
                "project": project,
                "parent_session": parent_session,
                "created_at": now.isoformat(),
                "created_by": "session_manager",
                "metadata": metadata or {},
                "lifecycle": {
                    "status": SessionStatus.ACTIVE.value,
                    "last_activity": now.isoformat(),
                    "heartbeat": now.isoformat(),
                    "expiry": expiry.isoformat()
                }
            },
            "execution": {
                "agents": {},
                "tasks": {},
                "workflows": {},
                "context": {
                    "project": project,
                    "parent_session": parent_session
                }
            },
            "observability": {
                "metrics": {
                    "start_time": now.isoformat(),
                    "heartbeat_count": 0,
                    "task_count": 0,
                    "agent_count": 0
                },
                "events": [
                    {
                        "timestamp": now.isoformat(),
                        "type": "session_created",
                        "data": {"mode": mode.value if isinstance(mode, SessionMode) else mode}
                    }
                ]
            }
        }
        
        lock_file = self._get_lock_file(session_id)
        with FileLock(lock_file, timeout=10):
            self._save_state(session_id, state)
        
        return session_id
    
    def heartbeat(self, session_id: str) -> bool:
        """Update session heartbeat and extend expiry."""
        lock_file = self._get_lock_file(session_id)
        
        with FileLock(lock_file, timeout=10):
            state = self._load_state(session_id)
            
            if not state:
                return False
            
            now = datetime.now(timezone.utc)
            
            # Update heartbeat and last activity
            state["session"]["lifecycle"]["heartbeat"] = now.isoformat()
            state["session"]["lifecycle"]["last_activity"] = now.isoformat()
            
            # Extend expiry based on mode
            mode = state["session"].get("mode", "development")
            expiry_hours = {
                "development": 24,
                "leadership": 48,
                "sprint": 168,
                "config": 1
            }
            
            new_expiry = now + timedelta(hours=expiry_hours.get(mode, 24))
            state["session"]["lifecycle"]["expiry"] = new_expiry.isoformat()
            
            # Update metrics
            if "metrics" in state["observability"]:
                state["observability"]["metrics"]["heartbeat_count"] = \
                    state["observability"]["metrics"].get("heartbeat_count", 0) + 1
            
            # Add heartbeat event
            state["observability"]["events"].append({
                "timestamp": now.isoformat(),
                "type": "heartbeat",
                "data": {"extended_expiry": new_expiry.isoformat()}
            })
            
            self._save_state(session_id, state)
            return True
    
    def handoff(
        self,
        from_session: str,
        to_session: str,
        handoff_data: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Hand off context from one session to another."""
        # Load source session
        from_state = self._load_state(from_session)
        if not from_state:
            return False
        
        # Load or create target session
        to_lock = self._get_lock_file(to_session)
        
        with FileLock(to_lock, timeout=10):
            to_state = self._load_state(to_session)
            
            if not to_state:
                # Create new session if it doesn't exist
                mode = from_state["session"].get("mode", "development")
                project = from_state["session"].get("project")
                to_session_id = self.create(
                    mode=SessionMode(mode),
                    project=project,
                    parent_session=from_session
                )
                to_state = self._load_state(to_session_id)
            
            now = datetime.now(timezone.utc)
            
            # Transfer execution context
            if "execution" in from_state:
                to_state["execution"]["inherited_context"] = {
                    "from_session": from_session,
                    "timestamp": now.isoformat(),
                    "context": from_state["execution"].get("context", {}),
                    "handoff_data": handoff_data or {}
                }
            
            # Add handoff event
            to_state["observability"]["events"].append({
                "timestamp": now.isoformat(),
                "type": "handoff_received",
                "data": {
                    "from_session": from_session,
                    "handoff_data": handoff_data
                }
            })
            
            self._save_state(to_session if to_state else to_session_id, to_state)
        
        # Mark source session as completed
        from_lock = self._get_lock_file(from_session)
        
        with FileLock(from_lock, timeout=10):
            from_state["session"]["lifecycle"]["status"] = SessionStatus.COMPLETED.value
            from_state["observability"]["events"].append({
                "timestamp": now.isoformat(),
                "type": "handoff_completed",
                "data": {"to_session": to_session}
            })
            self._save_state(from_session, from_state)
        
        return True
    
    def list(
        self,
        active_only: bool = False,
        project: Optional[str] = None,
        mode: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """List sessions with optional filters."""
        sessions = []
        
        for state_file in self.state_dir.glob("*.json"):
            try:
                with open(state_file, 'r') as f:
                    state = json.load(f)
                
                # Apply filters
                if active_only and state["session"]["lifecycle"]["status"] != SessionStatus.ACTIVE.value:
                    continue
                
                if project and state["session"].get("project") != project:
                    continue
                
                if mode and state["session"].get("mode") != mode:
                    continue
                
                session_info = {
                    "id": state["session"]["id"],
                    "mode": state["session"]["mode"],
                    "project": state["session"].get("project", ""),
                    "status": state["session"]["lifecycle"]["status"],
                    "created_at": state["session"]["created_at"],
                    "last_activity": state["session"]["lifecycle"]["last_activity"],
                    "heartbeat": state["session"]["lifecycle"].get("heartbeat", ""),
                    "expiry": state["session"]["lifecycle"]["expiry"],
                    "parent_session": state["session"].get("parent_session", ""),
                    "metrics": state["observability"].get("metrics", {})
                }
                sessions.append(session_info)
            except Exception as e:
                logger.error(f"Error reading session {state_file.stem}: {e}")
        
        # Sort by last activity (most recent first)
        sessions.sort(key=lambda x: x["last_activity"], reverse=True)
        
        return sessions
    
    def recover(self, session_id: str) -> bool:
        """Recover a failed or paused session."""
        lock_file = self._get_lock_file(session_id)
        
        with FileLock(lock_file, timeout=10):
            state = self._load_state(session_id)
            
            if not state:
                return False
            
            now = datetime.now(timezone.utc)
            
            # Update status to active
            state["session"]["lifecycle"]["status"] = SessionStatus.ACTIVE.value
            state["session"]["lifecycle"]["last_activity"] = now.isoformat()
            state["session"]["lifecycle"]["heartbeat"] = now.isoformat()
            
            # Extend expiry
            mode = state["session"].get("mode", "development")
            expiry_hours = {
                "development": 24,
                "leadership": 48,
                "sprint": 168,
                "config": 1
            }
            
            new_expiry = now + timedelta(hours=expiry_hours.get(mode, 24))
            state["session"]["lifecycle"]["expiry"] = new_expiry.isoformat()
            
            # Add recovery event
            state["observability"]["events"].append({
                "timestamp": now.isoformat(),
                "type": "session_recovered",
                "data": {"previous_status": state["session"]["lifecycle"].get("status")}
            })
            
            self._save_state(session_id, state)
            return True
    
    def get_info(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed session information."""
        state = self._load_state(session_id)
        if not state:
            return None
        
        return {
            "session": state["session"],
            "execution_summary": {
                "agent_count": len(state["execution"].get("agents", {})),
                "task_count": len(state["execution"].get("tasks", {})),
                "workflow_count": len(state["execution"].get("workflows", {}))
            },
            "metrics": state["observability"].get("metrics", {}),
            "recent_events": state["observability"].get("events", [])[-5:]  # Last 5 events
        }


@click.group()
def cli():
    """Session Manager for V2 Orchestration System."""
    pass


@cli.command()
@click.option('--mode', type=click.Choice(['development', 'leadership', 'sprint', 'config']),
              default='development', help='Session mode')
@click.option('--project', help='Project identifier')
@click.option('--parent-session', help='Parent session ID for inheritance')
@click.option('--metadata', help='Additional metadata as JSON')
@click.option('--json-output', is_flag=True, help='Output as JSON')
def create(mode: str, project: Optional[str], parent_session: Optional[str],
           metadata: Optional[str], json_output: bool):
    """Create a new session."""
    try:
        manager = SessionManager()
        
        # Parse metadata if provided
        meta_dict = None
        if metadata:
            meta_dict = json.loads(metadata)
        
        session_id = manager.create(
            mode=SessionMode(mode),
            project=project,
            parent_session=parent_session,
            metadata=meta_dict
        )
        
        if json_output:
            print(json.dumps({"session_id": session_id}))
        else:
            console.print(f"[green]✓ Created session: {session_id}[/green]")
            console.print(f"  Mode: {mode}")
            if project:
                console.print(f"  Project: {project}")
            if parent_session:
                console.print(f"  Parent: {parent_session}")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@cli.command()
@click.argument('session_id')
@click.option('--json-output', is_flag=True, help='Output as JSON')
def heartbeat(session_id: str, json_output: bool):
    """Send heartbeat to keep session alive."""
    try:
        manager = SessionManager()
        success = manager.heartbeat(session_id)
        
        if json_output:
            print(json.dumps({"success": success}))
        else:
            if success:
                console.print(f"[green]✓ Heartbeat sent for session {session_id}[/green]")
            else:
                console.print(f"[red]Session not found: {session_id}[/red]")
                sys.exit(1)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@cli.command()
@click.argument('from_session')
@click.argument('to_session')
@click.option('--data', help='Handoff data as JSON')
@click.option('--json-output', is_flag=True, help='Output as JSON')
def handoff(from_session: str, to_session: str, data: Optional[str], json_output: bool):
    """Hand off context from one session to another."""
    try:
        manager = SessionManager()
        
        # Parse handoff data if provided
        handoff_data = None
        if data:
            handoff_data = json.loads(data)
        
        success = manager.handoff(from_session, to_session, handoff_data)
        
        if json_output:
            print(json.dumps({"success": success}))
        else:
            if success:
                console.print(f"[green]✓ Handoff completed from {from_session} to {to_session}[/green]")
            else:
                console.print(f"[red]Handoff failed[/red]")
                sys.exit(1)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@cli.command()
@click.option('--active', is_flag=True, help='Show only active sessions')
@click.option('--project', help='Filter by project')
@click.option('--mode', type=click.Choice(['development', 'leadership', 'sprint', 'config']),
              help='Filter by mode')
@click.option('--json-output', is_flag=True, help='Output as JSON')
def list(active: bool, project: Optional[str], mode: Optional[str], json_output: bool):
    """List sessions with optional filters."""
    try:
        manager = SessionManager()
        sessions = manager.list(active_only=active, project=project, mode=mode)
        
        if json_output:
            print(json.dumps(sessions, indent=2))
        else:
            if sessions:
                table = Table(title="Sessions")
                table.add_column("Session ID", style="cyan", no_wrap=True)
                table.add_column("Mode", style="magenta")
                table.add_column("Project", style="blue")
                table.add_column("Status", style="green")
                table.add_column("Created", style="yellow")
                table.add_column("Last Activity", style="yellow")
                table.add_column("Tasks", style="white")
                
                for session in sessions:
                    status_color = {
                        "active": "green",
                        "paused": "yellow",
                        "completed": "blue",
                        "failed": "red"
                    }.get(session["status"], "white")
                    
                    table.add_row(
                        session["id"][:8] + "...",
                        session["mode"],
                        session["project"] or "-",
                        f"[{status_color}]{session['status']}[/{status_color}]",
                        session["created_at"][:19] if session["created_at"] else "N/A",
                        session["last_activity"][:19] if session["last_activity"] else "N/A",
                        str(session["metrics"].get("task_count", 0))
                    )
                
                console.print(table)
                console.print(f"\n[dim]Total: {len(sessions)} sessions[/dim]")
            else:
                console.print("[yellow]No sessions found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@cli.command()
@click.argument('session_id')
@click.option('--json-output', is_flag=True, help='Output as JSON')
def recover(session_id: str, json_output: bool):
    """Recover a failed or paused session."""
    try:
        manager = SessionManager()
        success = manager.recover(session_id)
        
        if json_output:
            print(json.dumps({"success": success}))
        else:
            if success:
                console.print(f"[green]✓ Session {session_id} recovered[/green]")
            else:
                console.print(f"[red]Failed to recover session {session_id}[/red]")
                sys.exit(1)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@cli.command()
@click.argument('session_id')
@click.option('--json-output', is_flag=True, help='Output as JSON')
def info(session_id: str, json_output: bool):
    """Get detailed session information."""
    try:
        manager = SessionManager()
        info = manager.get_info(session_id)
        
        if not info:
            console.print(f"[red]Session not found: {session_id}[/red]")
            sys.exit(1)
        
        if json_output:
            print(json.dumps(info, indent=2))
        else:
            console.print(f"[bold cyan]Session: {info['session']['id']}[/bold cyan]")
            console.print(f"Mode: {info['session']['mode']}")
            console.print(f"Status: {info['session']['lifecycle']['status']}")
            console.print(f"Project: {info['session'].get('project', 'N/A')}")
            console.print(f"Created: {info['session']['created_at']}")
            console.print(f"Expiry: {info['session']['lifecycle']['expiry']}")
            
            console.print("\n[bold]Execution Summary:[/bold]")
            console.print(f"  Agents: {info['execution_summary']['agent_count']}")
            console.print(f"  Tasks: {info['execution_summary']['task_count']}")
            console.print(f"  Workflows: {info['execution_summary']['workflow_count']}")
            
            if info['metrics']:
                console.print("\n[bold]Metrics:[/bold]")
                console.print(RichJSON(json.dumps(info['metrics'], indent=2)))
            
            if info['recent_events']:
                console.print("\n[bold]Recent Events:[/bold]")
                for event in info['recent_events']:
                    console.print(f"  [{event['timestamp'][:19]}] {event['type']}")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    cli()