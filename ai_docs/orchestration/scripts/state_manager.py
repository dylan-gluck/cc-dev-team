#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "click>=8.1",
#     "rich>=13.7",
#     "jsonpath-ng>=1.6",
#     "filelock>=3.13",
# ]
# ///
"""
State Manager - Core state operations for v2 orchestration.

Provides JSONPath-based queries and updates for session state with atomic file operations.

Usage:
    uv run state_manager.py get SESSION_ID PATH
    uv run state_manager.py set SESSION_ID PATH VALUE
    uv run state_manager.py merge SESSION_ID PATH --data '{"key": "value"}'
    uv run state_manager.py delete SESSION_ID PATH
    uv run state_manager.py list-sessions
    uv run state_manager.py cleanup-expired
"""

import json
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta
from contextlib import contextmanager

import click
from filelock import FileLock, Timeout
from jsonpath_ng import parse as jsonpath_parse
from rich.console import Console
from rich.json import JSON
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console()

# Base directory for state files
STATE_DIR = Path.cwd() / ".claude" / "state"
LOCK_TIMEOUT = 5.0  # seconds


class StateManager:
    """Manages session state with atomic operations and file locking."""
    
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.state_file = STATE_DIR / f"session-{session_id}.json"
        self.lock_file = STATE_DIR / f"session-{session_id}.lock"
        
        # Ensure directories exist
        STATE_DIR.mkdir(parents=True, exist_ok=True)
    
    @contextmanager
    def _acquire_lock(self):
        """Acquire exclusive lock on state file."""
        lock = FileLock(self.lock_file, timeout=LOCK_TIMEOUT)
        try:
            with lock:
                yield
        except Timeout:
            console.print(f"[red]Error: Could not acquire lock for session {self.session_id}[/red]")
            sys.exit(1)
    
    def _load_state(self) -> Dict:
        """Load state from disk."""
        if not self.state_file.exists():
            console.print(f"[yellow]Warning: Session {self.session_id} not found[/yellow]")
            return {}
        
        try:
            with self.state_file.open('r') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            console.print(f"[red]Error: Invalid JSON in state file: {e}[/red]")
            return {}
    
    def _save_state(self, state: Dict) -> bool:
        """Save state to disk atomically."""
        try:
            # Update metadata
            if "session" in state:
                state["session"]["updated_at"] = datetime.now().isoformat()
                if "lifecycle" in state["session"]:
                    state["session"]["lifecycle"]["last_activity"] = datetime.now().isoformat()
            
            # Write to temporary file first
            temp_file = self.state_file.with_suffix('.tmp')
            with temp_file.open('w') as f:
                json.dump(state, f, indent=2, default=str)
            
            # Atomic replace
            temp_file.replace(self.state_file)
            return True
            
        except Exception as e:
            console.print(f"[red]Error saving state: {e}[/red]")
            return False
    
    def get(self, path: str) -> Any:
        """Get value at JSONPath."""
        with self._acquire_lock():
            state = self._load_state()
            
            if not state:
                return None
            
            if not path or path == '$':
                return state
            
            try:
                # Use JSONPath for complex queries
                if path.startswith('$'):
                    jsonpath_expr = jsonpath_parse(path)
                    matches = jsonpath_expr.find(state)
                    if matches:
                        # Return single value if one match, list if multiple
                        if len(matches) == 1:
                            return matches[0].value
                        return [match.value for match in matches]
                    return None
                else:
                    # Simple dot notation
                    parts = path.split('.')
                    current = state
                    for part in parts:
                        if isinstance(current, dict):
                            current = current.get(part)
                        else:
                            return None
                        if current is None:
                            return None
                    return current
                    
            except Exception as e:
                console.print(f"[red]Error querying path '{path}': {e}[/red]")
                return None
    
    def set(self, path: str, value: Any) -> bool:
        """Set value at JSONPath."""
        with self._acquire_lock():
            state = self._load_state()
            
            if not state:
                console.print("[yellow]Warning: Creating new state structure[/yellow]")
                state = self._create_initial_state()
            
            try:
                # Parse path
                parts = path.split('.')
                
                # Navigate to parent
                current = state
                for part in parts[:-1]:
                    if part not in current:
                        current[part] = {}
                    current = current[part]
                
                # Set value
                current[parts[-1]] = value
                
                return self._save_state(state)
                
            except Exception as e:
                console.print(f"[red]Error setting value at '{path}': {e}[/red]")
                return False
    
    def merge(self, path: str, data: Dict) -> bool:
        """Merge data at JSONPath."""
        with self._acquire_lock():
            state = self._load_state()
            
            if not state:
                console.print("[yellow]Warning: Creating new state structure[/yellow]")
                state = self._create_initial_state()
            
            try:
                # Navigate to target
                parts = path.split('.') if path else []
                current = state
                
                for part in parts[:-1]:
                    if part not in current:
                        current[part] = {}
                    current = current[part]
                
                # Get target object
                if parts:
                    target = current.get(parts[-1], {})
                    if not isinstance(target, dict):
                        console.print(f"[red]Error: Path '{path}' is not an object[/red]")
                        return False
                    
                    # Merge data
                    target.update(data)
                    current[parts[-1]] = target
                else:
                    # Merge at root
                    state.update(data)
                
                return self._save_state(state)
                
            except Exception as e:
                console.print(f"[red]Error merging data at '{path}': {e}[/red]")
                return False
    
    def delete(self, path: str) -> bool:
        """Delete value at JSONPath."""
        with self._acquire_lock():
            state = self._load_state()
            
            if not state:
                return True  # Nothing to delete
            
            try:
                parts = path.split('.')
                
                # Navigate to parent
                current = state
                for part in parts[:-1]:
                    if isinstance(current, dict):
                        current = current.get(part)
                    else:
                        return True  # Path doesn't exist
                    if current is None:
                        return True  # Path doesn't exist
                
                # Delete key
                if isinstance(current, dict) and parts[-1] in current:
                    del current[parts[-1]]
                    return self._save_state(state)
                
                return True  # Key didn't exist
                
            except Exception as e:
                console.print(f"[red]Error deleting '{path}': {e}[/red]")
                return False
    
    def _create_initial_state(self) -> Dict:
        """Create initial state structure."""
        return {
            "session": {
                "id": self.session_id,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "mode": "development",
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
                    "status": "active",
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
                "coordination": {"locks": {}, "dependencies": {"graph": {"nodes": {}, "edges": []}, "blocks": []}}
            },
            "observability": {
                "metrics": {
                    "performance": {"session_duration_seconds": 0, "total_tokens_used": 0},
                    "utilization": {"agent_utilization_rate": 0.0, "memory_usage_mb": 0},
                    "quality": {"task_completion_rate": 0.0, "error_rate": 0.0}
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


def list_sessions() -> List[Dict]:
    """List all active sessions."""
    if not STATE_DIR.exists():
        return []
    
    sessions = []
    for state_file in STATE_DIR.glob("session-*.json"):
        try:
            session_id = state_file.stem.replace("session-", "")
            manager = StateManager(session_id)
            state = manager.get("$")
            
            if state and "session" in state:
                session_info = state["session"]
                sessions.append({
                    "id": session_id,
                    "mode": session_info.get("mode", "unknown"),
                    "status": session_info.get("lifecycle", {}).get("status", "unknown"),
                    "created_at": session_info.get("created_at", ""),
                    "last_activity": session_info.get("lifecycle", {}).get("last_activity", ""),
                    "expiry": session_info.get("lifecycle", {}).get("expiry", ""),
                    "tasks": len(state.get("execution", {}).get("tasks", {})),
                    "agents": len(state.get("execution", {}).get("agents", {}).get("active", {}))
                })
        except Exception as e:
            console.print(f"[yellow]Warning: Could not read session {session_id}: {e}[/yellow]")
    
    return sessions


def cleanup_expired() -> int:
    """Remove expired sessions."""
    if not STATE_DIR.exists():
        return 0
    
    cleaned = 0
    now = datetime.now()
    
    for state_file in STATE_DIR.glob("session-*.json"):
        try:
            session_id = state_file.stem.replace("session-", "")
            manager = StateManager(session_id)
            
            expiry_str = manager.get("session.lifecycle.expiry")
            auto_cleanup = manager.get("session.lifecycle.auto_cleanup")
            
            if expiry_str and auto_cleanup:
                expiry = datetime.fromisoformat(expiry_str.replace('Z', '+00:00'))
                if expiry < now:
                    # Remove state file
                    state_file.unlink()
                    
                    # Remove lock file if exists
                    lock_file = STATE_DIR / f"session-{session_id}.lock"
                    if lock_file.exists():
                        lock_file.unlink()
                    
                    cleaned += 1
                    console.print(f"[green]Cleaned up expired session: {session_id}[/green]")
                    
        except Exception as e:
            console.print(f"[yellow]Warning: Could not check session expiry: {e}[/yellow]")
    
    return cleaned


@click.group()
def cli():
    """State Manager - Core state operations for v2 orchestration."""
    pass


@cli.command()
@click.argument('session_id')
@click.argument('path', default='$')
def get(session_id: str, path: str):
    """Query state at JSONPath."""
    manager = StateManager(session_id)
    value = manager.get(path)
    
    if value is not None:
        if isinstance(value, (dict, list)):
            console.print(Panel(JSON(json.dumps(value)), title=f"Value at '{path}'", box=box.ROUNDED))
        else:
            console.print(Panel(str(value), title=f"Value at '{path}'", box=box.ROUNDED))
    else:
        console.print(f"[yellow]No value found at path: {path}[/yellow]")


@cli.command()
@click.argument('session_id')
@click.argument('path')
@click.argument('value')
@click.option('--json-value', '-j', is_flag=True, help='Parse value as JSON')
def set(session_id: str, path: str, value: str, json_value: bool):
    """Update state value at path."""
    manager = StateManager(session_id)
    
    # Parse value if JSON flag is set
    if json_value:
        try:
            value = json.loads(value)
        except json.JSONDecodeError:
            console.print("[red]Error: Invalid JSON value[/red]")
            sys.exit(1)
    
    if manager.set(path, value):
        console.print(f"[green]✓ Updated '{path}' in session {session_id}[/green]")
    else:
        console.print(f"[red]✗ Failed to update '{path}'[/red]")
        sys.exit(1)


@cli.command()
@click.argument('session_id')
@click.argument('path')
@click.option('--data', required=True, help='JSON data to merge')
def merge(session_id: str, path: str, data: str):
    """Merge data at path."""
    manager = StateManager(session_id)
    
    try:
        merge_data = json.loads(data)
    except json.JSONDecodeError:
        console.print("[red]Error: Invalid JSON data[/red]")
        sys.exit(1)
    
    if not isinstance(merge_data, dict):
        console.print("[red]Error: Merge data must be an object[/red]")
        sys.exit(1)
    
    if manager.merge(path, merge_data):
        console.print(f"[green]✓ Merged data at '{path}' in session {session_id}[/green]")
    else:
        console.print(f"[red]✗ Failed to merge data at '{path}'[/red]")
        sys.exit(1)


@cli.command()
@click.argument('session_id')
@click.argument('path')
def delete(session_id: str, path: str):
    """Remove state key at path."""
    manager = StateManager(session_id)
    
    if manager.delete(path):
        console.print(f"[green]✓ Deleted '{path}' from session {session_id}[/green]")
    else:
        console.print(f"[red]✗ Failed to delete '{path}'[/red]")
        sys.exit(1)


@cli.command('list-sessions')
def list_sessions_cmd():
    """Show active sessions."""
    sessions = list_sessions()
    
    if not sessions:
        console.print("[yellow]No active sessions found[/yellow]")
        return
    
    table = Table(title="Active Sessions", box=box.ROUNDED)
    table.add_column("Session ID", style="cyan")
    table.add_column("Mode", style="magenta")
    table.add_column("Status", style="green")
    table.add_column("Tasks", justify="right")
    table.add_column("Agents", justify="right")
    table.add_column("Last Activity", style="yellow")
    
    for session in sessions:
        status_color = "green" if session["status"] == "active" else "yellow"
        table.add_row(
            session["id"][:8] + "...",
            session["mode"],
            f"[{status_color}]{session['status']}[/{status_color}]",
            str(session["tasks"]),
            str(session["agents"]),
            session["last_activity"].split('T')[0] if session["last_activity"] else "N/A"
        )
    
    console.print(table)


@cli.command('cleanup-expired')
def cleanup_expired_cmd():
    """Remove old sessions."""
    cleaned = cleanup_expired()
    
    if cleaned > 0:
        console.print(f"[green]✓ Cleaned up {cleaned} expired session(s)[/green]")
    else:
        console.print("[yellow]No expired sessions to clean up[/yellow]")


if __name__ == "__main__":
    cli()