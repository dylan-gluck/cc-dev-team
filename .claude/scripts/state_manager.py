#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "jsonpath-ng>=1.6",
#     "filelock>=3.12",
#     "click>=8.1",
#     "rich>=13.0",
# ]
# ///
"""
State Manager for V2 Orchestration System.

Provides atomic state operations with JSONPath query support and file locking
for concurrent access to session state files.

Usage:
    ./state_manager.py get SESSION_ID "path.to.value"
    ./state_manager.py set SESSION_ID "path.to.value" "new value"
    ./state_manager.py merge SESSION_ID "path" --data '{"key": "value"}'
    ./state_manager.py delete SESSION_ID "path.to.value"
    ./state_manager.py list-sessions
    ./state_manager.py cleanup-expired
"""

import json
import sys
import tempfile
from pathlib import Path
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Union
import logging

import click
from jsonpath_ng import parse
from jsonpath_ng.exceptions import JsonPathParserError
from filelock import FileLock
from rich.console import Console
from rich.json import JSON as RichJSON
from rich.table import Table

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


class StateManager:
    """Manages session state with atomic operations and file locking."""
    
    def __init__(self):
        self.state_dir = STATE_DIR
        
    def _get_state_file(self, session_id: str) -> Path:
        """Get the path to a session's state file."""
        return self.state_dir / f"{session_id}.json"
    
    def _get_lock_file(self, session_id: str) -> Path:
        """Get the path to a session's lock file."""
        return self.state_dir / f"{session_id}.lock"
    
    def _load_state(self, session_id: str) -> Dict[str, Any]:
        """Load state from file with locking."""
        state_file = self._get_state_file(session_id)
        
        if not state_file.exists():
            # Initialize with default structure
            return {
                "session": {
                    "id": session_id,
                    "mode": "development",
                    "created_at": datetime.now(timezone.utc).isoformat(),
                    "lifecycle": {
                        "status": "active",
                        "last_activity": datetime.now(timezone.utc).isoformat(),
                        "expiry": (datetime.now(timezone.utc) + timedelta(hours=24)).isoformat()
                    }
                },
                "execution": {
                    "agents": {},
                    "tasks": {},
                    "workflows": {}
                },
                "observability": {
                    "metrics": {},
                    "events": []
                }
            }
        
        with open(state_file, 'r') as f:
            return json.load(f)
    
    def _save_state(self, session_id: str, state: Dict[str, Any]) -> None:
        """Save state to file atomically with locking."""
        state_file = self._get_state_file(session_id)
        
        # Update last activity
        if "session" in state and "lifecycle" in state["session"]:
            state["session"]["lifecycle"]["last_activity"] = datetime.now(timezone.utc).isoformat()
        
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
    
    def get(self, session_id: str, path: str) -> Any:
        """Get value at path using JSONPath or dot notation."""
        lock_file = self._get_lock_file(session_id)
        
        with FileLock(lock_file, timeout=10):
            state = self._load_state(session_id)
            
            # Try JSONPath first (if it starts with $)
            if path.startswith('$'):
                try:
                    expr = parse(path)
                    matches = expr.find(state)
                    if matches:
                        # Return list if multiple matches, single value if one
                        if len(matches) == 1:
                            return matches[0].value
                        return [match.value for match in matches]
                    return None
                except JsonPathParserError as e:
                    logger.error(f"Invalid JSONPath: {e}")
                    return None
            
            # Fall back to dot notation
            keys = path.split('.')
            value = state
            
            for key in keys:
                if isinstance(value, dict) and key in value:
                    value = value[key]
                else:
                    return None
            
            return value
    
    def set(self, session_id: str, path: str, value: Any) -> bool:
        """Set value at path using dot notation."""
        lock_file = self._get_lock_file(session_id)
        
        with FileLock(lock_file, timeout=10):
            state = self._load_state(session_id)
            
            keys = path.split('.')
            current = state
            
            # Navigate to the parent of the target
            for key in keys[:-1]:
                if key not in current:
                    current[key] = {}
                current = current[key]
            
            # Set the value
            current[keys[-1]] = value
            
            self._save_state(session_id, state)
            return True
    
    def merge(self, session_id: str, path: str, data: Dict[str, Any]) -> bool:
        """Deep merge data at path."""
        lock_file = self._get_lock_file(session_id)
        
        with FileLock(lock_file, timeout=10):
            state = self._load_state(session_id)
            
            if path:
                keys = path.split('.')
                current = state
                
                # Navigate to the target
                for key in keys[:-1]:
                    if key not in current:
                        current[key] = {}
                    current = current[key]
                
                # Get or create the target dict
                if keys[-1] not in current:
                    current[keys[-1]] = {}
                
                # Deep merge
                self._deep_merge(current[keys[-1]], data)
            else:
                # Merge at root level
                self._deep_merge(state, data)
            
            self._save_state(session_id, state)
            return True
    
    def _deep_merge(self, target: Dict, source: Dict) -> None:
        """Deep merge source into target."""
        for key, value in source.items():
            if key in target and isinstance(target[key], dict) and isinstance(value, dict):
                self._deep_merge(target[key], value)
            else:
                target[key] = value
    
    def delete(self, session_id: str, path: str) -> bool:
        """Delete key at path."""
        lock_file = self._get_lock_file(session_id)
        
        with FileLock(lock_file, timeout=10):
            state = self._load_state(session_id)
            
            keys = path.split('.')
            current = state
            
            # Navigate to the parent of the target
            for key in keys[:-1]:
                if isinstance(current, dict) and key in current:
                    current = current[key]
                else:
                    return False
            
            # Delete the key
            if isinstance(current, dict) and keys[-1] in current:
                del current[keys[-1]]
                self._save_state(session_id, state)
                return True
            
            return False
    
    def list_sessions(self) -> List[Dict[str, Any]]:
        """List all sessions with their metadata."""
        sessions = []
        
        for state_file in self.state_dir.glob("*.json"):
            try:
                with open(state_file, 'r') as f:
                    state = json.load(f)
                    
                session_info = {
                    "id": state.get("session", {}).get("id", state_file.stem),
                    "mode": state.get("session", {}).get("mode", "unknown"),
                    "status": state.get("session", {}).get("lifecycle", {}).get("status", "unknown"),
                    "created_at": state.get("session", {}).get("created_at", ""),
                    "last_activity": state.get("session", {}).get("lifecycle", {}).get("last_activity", ""),
                    "expiry": state.get("session", {}).get("lifecycle", {}).get("expiry", "")
                }
                sessions.append(session_info)
            except Exception as e:
                logger.error(f"Error reading session {state_file.stem}: {e}")
        
        return sessions
    
    def cleanup_expired(self) -> List[str]:
        """Remove expired session files."""
        removed = []
        now = datetime.now(timezone.utc)
        
        for state_file in self.state_dir.glob("*.json"):
            try:
                with open(state_file, 'r') as f:
                    state = json.load(f)
                
                expiry_str = state.get("session", {}).get("lifecycle", {}).get("expiry")
                if expiry_str:
                    expiry = datetime.fromisoformat(expiry_str.replace('Z', '+00:00'))
                    if expiry < now:
                        # Remove state and lock files
                        session_id = state_file.stem
                        state_file.unlink()
                        lock_file = self._get_lock_file(session_id)
                        if lock_file.exists():
                            lock_file.unlink()
                        removed.append(session_id)
            except Exception as e:
                logger.error(f"Error processing session {state_file.stem}: {e}")
        
        return removed


@click.group()
def cli():
    """State Manager for V2 Orchestration System."""
    pass


@cli.command()
@click.argument('session_id')
@click.argument('path')
@click.option('--json-output', is_flag=True, help='Output as JSON')
def get(session_id: str, path: str, json_output: bool):
    """Get value at path from session state."""
    try:
        manager = StateManager()
        value = manager.get(session_id, path)
        
        if json_output:
            print(json.dumps(value, indent=2, default=str))
        else:
            if value is not None:
                if isinstance(value, (dict, list)):
                    console.print(RichJSON(json.dumps(value, default=str)))
                else:
                    console.print(value)
            else:
                console.print(f"[yellow]No value found at path: {path}[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@cli.command()
@click.argument('session_id')
@click.argument('path')
@click.argument('value')
@click.option('--json-value', is_flag=True, help='Parse value as JSON')
def set(session_id: str, path: str, value: str, json_value: bool):
    """Set value at path in session state."""
    try:
        manager = StateManager()
        
        # Parse value if JSON flag is set
        if json_value:
            value = json.loads(value)
        
        success = manager.set(session_id, path, value)
        
        if success:
            console.print(f"[green]✓ Value set at {path}[/green]")
        else:
            console.print(f"[red]Failed to set value at {path}[/red]")
            sys.exit(1)
    except json.JSONDecodeError as e:
        console.print(f"[red]Invalid JSON value: {e}[/red]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@cli.command()
@click.argument('session_id')
@click.argument('path')
@click.option('--data', required=True, help='JSON data to merge')
def merge(session_id: str, path: str, data: str):
    """Deep merge data at path in session state."""
    try:
        manager = StateManager()
        
        # Parse JSON data
        merge_data = json.loads(data)
        
        if not isinstance(merge_data, dict):
            console.print("[red]Data must be a JSON object[/red]")
            sys.exit(1)
        
        success = manager.merge(session_id, path, merge_data)
        
        if success:
            console.print(f"[green]✓ Data merged at {path}[/green]")
        else:
            console.print(f"[red]Failed to merge data at {path}[/red]")
            sys.exit(1)
    except json.JSONDecodeError as e:
        console.print(f"[red]Invalid JSON data: {e}[/red]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@cli.command()
@click.argument('session_id')
@click.argument('path')
def delete(session_id: str, path: str):
    """Delete key at path from session state."""
    try:
        manager = StateManager()
        success = manager.delete(session_id, path)
        
        if success:
            console.print(f"[green]✓ Deleted {path}[/green]")
        else:
            console.print(f"[yellow]Key not found at path: {path}[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@cli.command('list-sessions')
@click.option('--json-output', is_flag=True, help='Output as JSON')
def list_sessions(json_output: bool):
    """List all sessions with metadata."""
    try:
        manager = StateManager()
        sessions = manager.list_sessions()
        
        if json_output:
            print(json.dumps(sessions, indent=2))
        else:
            if sessions:
                table = Table(title="Active Sessions")
                table.add_column("Session ID", style="cyan")
                table.add_column("Mode", style="magenta")
                table.add_column("Status", style="green")
                table.add_column("Created", style="yellow")
                table.add_column("Last Activity", style="yellow")
                
                for session in sessions:
                    table.add_row(
                        session["id"],
                        session["mode"],
                        session["status"],
                        session["created_at"][:19] if session["created_at"] else "N/A",
                        session["last_activity"][:19] if session["last_activity"] else "N/A"
                    )
                
                console.print(table)
            else:
                console.print("[yellow]No sessions found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@cli.command('cleanup-expired')
@click.option('--dry-run', is_flag=True, help='Show what would be removed without removing')
def cleanup_expired(dry_run: bool):
    """Remove expired session files."""
    try:
        manager = StateManager()
        
        if dry_run:
            sessions = manager.list_sessions()
            now = datetime.now(timezone.utc)
            expired = []
            
            for session in sessions:
                if session["expiry"]:
                    expiry = datetime.fromisoformat(session["expiry"].replace('Z', '+00:00'))
                    if expiry < now:
                        expired.append(session["id"])
            
            if expired:
                console.print("[yellow]Would remove expired sessions:[/yellow]")
                for session_id in expired:
                    console.print(f"  - {session_id}")
            else:
                console.print("[green]No expired sessions found[/green]")
        else:
            removed = manager.cleanup_expired()
            
            if removed:
                console.print(f"[green]✓ Removed {len(removed)} expired sessions:[/green]")
                for session_id in removed:
                    console.print(f"  - {session_id}")
            else:
                console.print("[green]No expired sessions found[/green]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    cli()