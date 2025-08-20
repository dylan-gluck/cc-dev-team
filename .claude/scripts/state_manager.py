#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "click>=8.1",
#     "filelock>=3.12",
#     "rich>=13.0",
# ]
# ///
"""
State management system for orchestration.

This script provides a CLI interface for managing orchestration state with:
- JSON state storage with jq integration
- File locking for concurrent access
- Event emission for state changes
- Rich console output formatting
- Support for tasks, agents, and project hierarchy

Usage:
    ./state_manager.py get [PATH] [--format json|table]
    ./state_manager.py set PATH VALUE [--merge/--replace]
    ./state_manager.py update-task TASK_ID STATUS
    ./state_manager.py update-agent AGENT_ID [TASK_ID] [--status idle|busy|blocked]
"""

import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, Optional

import click
from filelock import FileLock
from rich.console import Console
from rich.table import Table
from rich.json import JSON

console = Console()
STATE_DIR = Path(".claude/state")
STATE_FILE = STATE_DIR / "orchestration.json"
LOCK_FILE = STATE_DIR / ".orchestration.lock"


def ensure_state_exists() -> None:
    """Ensure state file exists with default structure."""
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    
    if not STATE_FILE.exists():
        default_state = {
            "organization": {},
            "projects": {},
            "epics": {},
            "sprints": {},
            "tasks": {},
            "agents": {"active": {}},
            "communication": {"questions": [], "handoffs": []},
            "observability": {"metrics": {}, "events": []}
        }
        STATE_FILE.write_text(json.dumps(default_state, indent=2))
        console.print("[green]✓[/green] Created default state file")


def run_jq(expression: str, input_data: Dict[str, Any]) -> Optional[Any]:
    """Run jq command with given expression and input data."""
    try:
        result = subprocess.run(
            ['jq', expression],
            input=json.dumps(input_data),
            capture_output=True,
            text=True,
            check=False
        )
        
        if result.returncode != 0:
            console.print(f"[red]✗[/red] jq error: {result.stderr.strip()}")
            return None
            
        if result.stdout.strip():
            try:
                return json.loads(result.stdout)
            except json.JSONDecodeError:
                # Return as string if not valid JSON
                return result.stdout.strip()
        return None
        
    except FileNotFoundError:
        console.print("[red]✗[/red] jq not found. Please install jq to use this tool.")
        sys.exit(1)


def emit_event(event_type: str, data: Dict[str, Any]) -> None:
    """Emit event to event stream if event script exists."""
    event_script = Path(".claude/scripts/event_stream.py")
    
    if event_script.exists():
        try:
            subprocess.run(
                [str(event_script), 'emit', '--type', event_type, '--source', 'state_manager', '--data', json.dumps(data)],
                capture_output=True,
                text=True,
                check=False
            )
            console.print(f"[dim]→ Event emitted: {event_type}[/dim]")
        except Exception as e:
            console.print(f"[yellow]⚠[/yellow] Failed to emit event: {e}")


@click.group()
def cli():
    """State management for orchestration system."""
    ensure_state_exists()


@cli.command()
@click.argument('path', required=False)
@click.option('--format', 'output_format', type=click.Choice(['json', 'table']), default='json',
              help='Output format (json or table)')
def get(path: Optional[str], output_format: str) -> None:
    """Get state value at path using jq-style query.
    
    Examples:
        Get entire state: state_manager.py get
        Get tasks: state_manager.py get tasks
        Get specific task: state_manager.py get "tasks.task-3"
        Get with table format: state_manager.py get agents --format table
    """
    with FileLock(LOCK_FILE, timeout=10):
        state = json.loads(STATE_FILE.read_text())
        
        if path:
            # Build jq expression
            jq_expr = f'.{path}' if not path.startswith('.') else path
            value = run_jq(jq_expr, state)
            
            if value is None:
                console.print(f"[yellow]⚠[/yellow] Path '{path}' not found or empty")
                return
        else:
            value = state
        
        # Format output
        if output_format == 'table' and isinstance(value, dict):
            table = Table(title=f"State: {path or 'root'}")
            table.add_column("Key", style="cyan", no_wrap=True)
            table.add_column("Value", style="green")
            
            for k, v in value.items():
                if isinstance(v, (dict, list)):
                    value_str = json.dumps(v, indent=2)
                else:
                    value_str = str(v)
                table.add_row(k, value_str)
            
            console.print(table)
        else:
            # Use rich JSON formatting
            console.print(JSON.from_data(value))


@cli.command()
@click.argument('path')
@click.argument('value')
@click.option('--merge/--replace', default=False,
              help='Merge with existing value (for objects) or replace entirely')
def set(path: str, value: str, merge: bool) -> None:
    """Set state value at path.
    
    Examples:
        Set simple value: state_manager.py set "agents.active.agent-1.status" '"busy"'
        Set object: state_manager.py set "tasks.task-5" '{"name": "New task", "status": "pending"}'
        Merge data: state_manager.py set "sprints.sprint-3.metrics" '{"velocity": 8}' --merge
    """
    with FileLock(LOCK_FILE, timeout=10):
        state = json.loads(STATE_FILE.read_text())
        
        # Parse value as JSON
        try:
            parsed_value = json.loads(value)
        except json.JSONDecodeError:
            # If not valid JSON, treat as string
            parsed_value = value
        
        # Build jq expression
        if merge:
            # Merge objects
            jq_expr = f'.{path} |= . + {json.dumps(parsed_value)}'
        else:
            # Replace value
            jq_expr = f'.{path} = {json.dumps(parsed_value)}'
        
        # Apply update
        new_state = run_jq(jq_expr, state)
        
        if new_state is not None:
            STATE_FILE.write_text(json.dumps(new_state, indent=2))
            console.print(f"[green]✓[/green] Updated {path}")
            
            # Emit event
            emit_event('state_updated', {
                'path': path,
                'value': parsed_value,
                'merge': merge,
                'timestamp': datetime.now().isoformat()
            })
        else:
            console.print(f"[red]✗[/red] Failed to update {path}")


@cli.command('update-task')
@click.argument('task_id')
@click.argument('status', type=click.Choice(['pending', 'in_progress', 'completed', 'blocked']))
@click.option('--assigned-to', help='Agent ID to assign the task to')
def update_task(task_id: str, status: str, assigned_to: Optional[str]) -> None:
    """Update task status and optionally assign to agent.
    
    Examples:
        Update status: state_manager.py update-task task-3 completed
        Assign task: state_manager.py update-task task-5 in_progress --assigned-to engineering-fullstack-1
    """
    with FileLock(LOCK_FILE, timeout=10):
        state = json.loads(STATE_FILE.read_text())
        
        # Initialize tasks if not present
        if 'tasks' not in state:
            state['tasks'] = {}
        
        # Update or create task
        if task_id not in state['tasks']:
            state['tasks'][task_id] = {
                'id': task_id,
                'created_at': datetime.now().isoformat()
            }
        
        task = state['tasks'][task_id]
        old_status = task.get('status', 'pending')
        
        # Update task fields
        task['status'] = status
        task['updated_at'] = datetime.now().isoformat()
        
        if assigned_to:
            task['assigned_to'] = assigned_to
        
        # Update sprint task lists if task is in a sprint
        for sprint_id, sprint in state.get('sprints', {}).items():
            sprint_tasks = sprint.get('tasks', {})
            
            # Remove from old status list
            for task_status, task_list in sprint_tasks.items():
                if task_id in task_list:
                    task_list.remove(task_id)
            
            # Add to new status list if task belongs to this sprint
            if task.get('sprint_id') == sprint_id:
                sprint_tasks.setdefault(status, []).append(task_id)
        
        # Save state
        STATE_FILE.write_text(json.dumps(state, indent=2))
        
        console.print(f"[green]✓[/green] Task {task_id}: {old_status} → {status}")
        
        if assigned_to:
            console.print(f"[green]✓[/green] Assigned to {assigned_to}")
        
        # Emit event
        emit_event('task_status_changed', {
            'task_id': task_id,
            'old_status': old_status,
            'new_status': status,
            'assigned_to': assigned_to,
            'timestamp': datetime.now().isoformat()
        })


@cli.command('update-agent')
@click.argument('agent_id')
@click.argument('task_id', required=False)
@click.option('--status', type=click.Choice(['idle', 'busy', 'blocked']),
              help='Agent status')
@click.option('--clear-task', is_flag=True,
              help='Clear current task assignment')
def update_agent(agent_id: str, task_id: Optional[str], status: Optional[str], clear_task: bool) -> None:
    """Update agent status and task assignment.
    
    Examples:
        Assign task: state_manager.py update-agent engineering-fullstack-1 task-5
        Update status: state_manager.py update-agent engineering-fullstack-1 --status busy
        Clear task: state_manager.py update-agent engineering-fullstack-1 --clear-task --status idle
    """
    with FileLock(LOCK_FILE, timeout=10):
        state = json.loads(STATE_FILE.read_text())
        
        # Initialize agent structure
        agents = state.setdefault('agents', {}).setdefault('active', {})
        agent = agents.setdefault(agent_id, {
            'id': agent_id,
            'created_at': datetime.now().isoformat()
        })
        
        # Store previous state for event
        previous_task = agent.get('current_task')
        previous_status = agent.get('status', 'idle')
        
        # Update agent fields
        if clear_task:
            agent.pop('current_task', None)
            console.print(f"[green]✓[/green] Cleared task assignment for {agent_id}")
        elif task_id:
            agent['current_task'] = task_id
            # Auto-set status to busy when task assigned
            if not status:
                agent['status'] = 'busy'
            console.print(f"[green]✓[/green] Assigned task {task_id} to {agent_id}")
        
        if status:
            agent['status'] = status
            console.print(f"[green]✓[/green] Agent {agent_id} status → {status}")
        
        agent['last_update'] = datetime.now().isoformat()
        
        # Save state
        STATE_FILE.write_text(json.dumps(state, indent=2))
        
        # Emit event
        emit_event('agent_status_changed', {
            'agent_id': agent_id,
            'previous_task': previous_task,
            'current_task': agent.get('current_task'),
            'previous_status': previous_status,
            'current_status': agent.get('status', 'idle'),
            'timestamp': datetime.now().isoformat()
        })


@cli.command()
def summary():
    """Display a summary of the current orchestration state."""
    with FileLock(LOCK_FILE, timeout=10):
        state = json.loads(STATE_FILE.read_text())
        
        # Create summary table
        table = Table(title="Orchestration State Summary")
        table.add_column("Category", style="cyan", no_wrap=True)
        table.add_column("Count", style="green", justify="right")
        table.add_column("Details", style="yellow")
        
        # Projects
        projects = state.get('projects', {})
        table.add_row("Projects", str(len(projects)), ", ".join(projects.keys())[:50] if projects else "None")
        
        # Tasks
        tasks = state.get('tasks', {})
        task_statuses = {}
        for task in tasks.values():
            status = task.get('status', 'unknown')
            task_statuses[status] = task_statuses.get(status, 0) + 1
        
        status_str = ", ".join([f"{s}: {c}" for s, c in task_statuses.items()])
        table.add_row("Tasks", str(len(tasks)), status_str or "None")
        
        # Agents
        agents = state.get('agents', {}).get('active', {})
        agent_statuses = {}
        for agent in agents.values():
            status = agent.get('status', 'unknown')
            agent_statuses[status] = agent_statuses.get(status, 0) + 1
        
        status_str = ", ".join([f"{s}: {c}" for s, c in agent_statuses.items()])
        table.add_row("Active Agents", str(len(agents)), status_str or "None")
        
        # Sprints
        sprints = state.get('sprints', {})
        active_sprints = [s for s in sprints.values() if s.get('status') == 'active']
        table.add_row("Sprints", str(len(sprints)), f"Active: {len(active_sprints)}")
        
        # Events
        events = state.get('observability', {}).get('events', [])
        recent_events = len([e for e in events if isinstance(e, dict)])
        table.add_row("Events", str(recent_events), "Recent events logged")
        
        console.print(table)


def main() -> int:
    """Main execution function."""
    try:
        cli()
        return 0
    except Exception as e:
        console.print(f"[red]✗[/red] Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())