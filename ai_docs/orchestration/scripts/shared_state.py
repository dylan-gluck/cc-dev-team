#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "click>=8.1",
#     "rich>=13.7",
#     "filelock>=3.13",
#     "pyyaml>=6.0",
# ]
# ///
"""
Shared State Manager - Cross-session shared data for v2 orchestration.

Manages shared configurations, epic definitions, and sprint plans that persist across sessions.

Usage:
    uv run shared_state.py get-config KEY
    uv run shared_state.py set-config KEY VALUE
    uv run shared_state.py get-epic EPIC_ID
    uv run shared_state.py get-sprint SPRINT_ID
    uv run shared_state.py list-resources
    uv run shared_state.py import-epic --file epic.json
    uv run shared_state.py import-sprint --file sprint.json
"""

import json
import sys
import yaml
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime
from contextlib import contextmanager

import click
from filelock import FileLock, Timeout
from rich.console import Console
from rich.json import JSON
from rich.table import Table
from rich.panel import Panel
from rich import box
from rich.tree import Tree

console = Console()

# Base directories for shared state
SHARED_DIR = Path.cwd() / ".claude" / "shared"
CONFIG_FILE = SHARED_DIR / "config.json"
EPICS_DIR = SHARED_DIR / "epics"
SPRINTS_DIR = SHARED_DIR / "sprints"
TEMPLATES_DIR = SHARED_DIR / "templates"
LOCK_TIMEOUT = 5.0  # seconds


class SharedStateManager:
    """Manages cross-session shared data."""
    
    def __init__(self):
        # Ensure directories exist
        SHARED_DIR.mkdir(parents=True, exist_ok=True)
        EPICS_DIR.mkdir(exist_ok=True)
        SPRINTS_DIR.mkdir(exist_ok=True)
        TEMPLATES_DIR.mkdir(exist_ok=True)
        
        # Initialize config file if not exists
        if not CONFIG_FILE.exists():
            self._initialize_config()
    
    @contextmanager
    def _acquire_lock(self, resource: str = "config"):
        """Acquire exclusive lock on shared resource."""
        lock_file = SHARED_DIR / f"{resource}.lock"
        lock = FileLock(lock_file, timeout=LOCK_TIMEOUT)
        try:
            with lock:
                yield
        except Timeout:
            console.print(f"[red]Error: Could not acquire lock for {resource}[/red]")
            sys.exit(1)
    
    def _initialize_config(self):
        """Initialize default configuration."""
        default_config = {
            "version": "2.0.0",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "orchestration": {
                "default_mode": "development",
                "max_parallel_agents": 10,
                "session_timeout_hours": 8,
                "auto_cleanup_enabled": True
            },
            "teams": {
                "available": [
                    "engineering", "product", "qa", "devops", 
                    "creative", "data", "marketing", "research"
                ],
                "default_teams": {
                    "development": ["engineering", "qa"],
                    "leadership": ["product", "engineering", "qa", "devops", "creative"],
                    "config": ["devops"],
                    "emergency": ["engineering", "devops"]
                }
            },
            "workflows": {
                "sprint_duration_days": 14,
                "epic_max_duration_weeks": 12,
                "task_priorities": ["critical", "high", "medium", "low"],
                "task_types": ["feature", "bug", "tech_debt", "documentation", "testing"]
            },
            "resources": {
                "token_budget_default": 100000,
                "time_budget_minutes_default": 480,
                "memory_limit_mb": 1000
            }
        }
        
        with self._acquire_lock("config"):
            with CONFIG_FILE.open('w') as f:
                json.dump(default_config, f, indent=2)
    
    def get_config(self, key: str = None) -> Any:
        """Read shared configuration."""
        with self._acquire_lock("config"):
            if not CONFIG_FILE.exists():
                self._initialize_config()
            
            with CONFIG_FILE.open('r') as f:
                config = json.load(f)
            
            if key:
                # Navigate nested keys with dot notation
                parts = key.split('.')
                current = config
                for part in parts:
                    if isinstance(current, dict):
                        current = current.get(part)
                    else:
                        return None
                    if current is None:
                        return None
                return current
            
            return config
    
    def set_config(self, key: str, value: Any) -> bool:
        """Update shared configuration."""
        with self._acquire_lock("config"):
            try:
                # Load current config
                with CONFIG_FILE.open('r') as f:
                    config = json.load(f)
                
                # Navigate to parent and set value
                parts = key.split('.')
                current = config
                for part in parts[:-1]:
                    if part not in current:
                        current[part] = {}
                    current = current[part]
                
                current[parts[-1]] = value
                config["updated_at"] = datetime.now().isoformat()
                
                # Save atomically
                temp_file = CONFIG_FILE.with_suffix('.tmp')
                with temp_file.open('w') as f:
                    json.dump(config, f, indent=2)
                temp_file.replace(CONFIG_FILE)
                
                return True
                
            except Exception as e:
                console.print(f"[red]Error updating config: {e}[/red]")
                return False
    
    def get_epic(self, epic_id: str) -> Optional[Dict]:
        """Read epic definition."""
        epic_file = EPICS_DIR / f"{epic_id}.json"
        
        if not epic_file.exists():
            console.print(f"[yellow]Epic not found: {epic_id}[/yellow]")
            return None
        
        with self._acquire_lock(f"epic-{epic_id}"):
            try:
                with epic_file.open('r') as f:
                    return json.load(f)
            except json.JSONDecodeError as e:
                console.print(f"[red]Error reading epic: {e}[/red]")
                return None
    
    def save_epic(self, epic_id: str, epic_data: Dict) -> bool:
        """Save epic definition."""
        epic_file = EPICS_DIR / f"{epic_id}.json"
        
        with self._acquire_lock(f"epic-{epic_id}"):
            try:
                # Add metadata
                epic_data["id"] = epic_id
                epic_data["updated_at"] = datetime.now().isoformat()
                if "created_at" not in epic_data:
                    epic_data["created_at"] = datetime.now().isoformat()
                
                # Save atomically
                temp_file = epic_file.with_suffix('.tmp')
                with temp_file.open('w') as f:
                    json.dump(epic_data, f, indent=2)
                temp_file.replace(epic_file)
                
                return True
                
            except Exception as e:
                console.print(f"[red]Error saving epic: {e}[/red]")
                return False
    
    def get_sprint(self, sprint_id: str) -> Optional[Dict]:
        """Read sprint plan."""
        sprint_file = SPRINTS_DIR / f"{sprint_id}.json"
        
        if not sprint_file.exists():
            console.print(f"[yellow]Sprint not found: {sprint_id}[/yellow]")
            return None
        
        with self._acquire_lock(f"sprint-{sprint_id}"):
            try:
                with sprint_file.open('r') as f:
                    return json.load(f)
            except json.JSONDecodeError as e:
                console.print(f"[red]Error reading sprint: {e}[/red]")
                return None
    
    def save_sprint(self, sprint_id: str, sprint_data: Dict) -> bool:
        """Save sprint plan."""
        sprint_file = SPRINTS_DIR / f"{sprint_id}.json"
        
        with self._acquire_lock(f"sprint-{sprint_id}"):
            try:
                # Add metadata
                sprint_data["id"] = sprint_id
                sprint_data["updated_at"] = datetime.now().isoformat()
                if "created_at" not in sprint_data:
                    sprint_data["created_at"] = datetime.now().isoformat()
                
                # Save atomically
                temp_file = sprint_file.with_suffix('.tmp')
                with temp_file.open('w') as f:
                    json.dump(sprint_data, f, indent=2)
                temp_file.replace(sprint_file)
                
                return True
                
            except Exception as e:
                console.print(f"[red]Error saving sprint: {e}[/red]")
                return False
    
    def list_shared_resources(self) -> Dict[str, List[str]]:
        """Show available shared data."""
        resources = {
            "epics": [],
            "sprints": [],
            "templates": [],
            "config_keys": []
        }
        
        # List epics
        if EPICS_DIR.exists():
            for epic_file in EPICS_DIR.glob("*.json"):
                resources["epics"].append(epic_file.stem)
        
        # List sprints
        if SPRINTS_DIR.exists():
            for sprint_file in SPRINTS_DIR.glob("*.json"):
                resources["sprints"].append(sprint_file.stem)
        
        # List templates
        if TEMPLATES_DIR.exists():
            for template_file in TEMPLATES_DIR.glob("*.json"):
                resources["templates"].append(template_file.stem)
        
        # List config keys
        config = self.get_config()
        if config:
            resources["config_keys"] = list(config.keys())
        
        return resources
    
    def get_template(self, template_name: str) -> Optional[Dict]:
        """Load a template."""
        template_file = TEMPLATES_DIR / f"{template_name}.json"
        
        if not template_file.exists():
            # Try YAML format
            template_file = TEMPLATES_DIR / f"{template_name}.yaml"
            if not template_file.exists():
                return None
            
            with template_file.open('r') as f:
                return yaml.safe_load(f)
        
        with template_file.open('r') as f:
            return json.load(f)
    
    def save_template(self, template_name: str, template_data: Dict) -> bool:
        """Save a template."""
        template_file = TEMPLATES_DIR / f"{template_name}.json"
        
        try:
            with template_file.open('w') as f:
                json.dump(template_data, f, indent=2)
            return True
        except Exception as e:
            console.print(f"[red]Error saving template: {e}[/red]")
            return False


@click.group()
def cli():
    """Shared State Manager - Cross-session shared data for v2 orchestration."""
    pass


@cli.command('get-config')
@click.argument('key', required=False)
def get_config(key: Optional[str]):
    """Read shared configuration."""
    manager = SharedStateManager()
    value = manager.get_config(key)
    
    if value is not None:
        if isinstance(value, (dict, list)):
            console.print(Panel(
                JSON(json.dumps(value)),
                title=f"Config: {key if key else 'All'}",
                box=box.ROUNDED
            ))
        else:
            console.print(Panel(
                str(value),
                title=f"Config: {key}",
                box=box.ROUNDED
            ))
    else:
        console.print(f"[yellow]No configuration found for key: {key}[/yellow]")


@cli.command('set-config')
@click.argument('key')
@click.argument('value')
@click.option('--json-value', '-j', is_flag=True, help='Parse value as JSON')
def set_config(key: str, value: str, json_value: bool):
    """Update shared configuration."""
    manager = SharedStateManager()
    
    # Parse value if JSON
    if json_value:
        try:
            value = json.loads(value)
        except json.JSONDecodeError:
            console.print("[red]Error: Invalid JSON value[/red]")
            sys.exit(1)
    
    if manager.set_config(key, value):
        console.print(f"[green]✓ Updated config '{key}'[/green]")
    else:
        console.print(f"[red]✗ Failed to update config[/red]")
        sys.exit(1)


@cli.command('get-epic')
@click.argument('epic_id')
def get_epic(epic_id: str):
    """Read epic definition."""
    manager = SharedStateManager()
    epic = manager.get_epic(epic_id)
    
    if epic:
        console.print(Panel(
            f"[bold cyan]Epic: {epic.get('title', 'Untitled')}[/bold cyan]\n\n"
            f"[cyan]ID:[/cyan] {epic.get('id', epic_id)}\n"
            f"[cyan]Status:[/cyan] {epic.get('status', 'unknown')}\n"
            f"[cyan]Owner:[/cyan] {epic.get('owner', 'unassigned')}\n"
            f"[cyan]Description:[/cyan]\n{epic.get('description', 'No description')}\n\n"
            f"[cyan]Sprints:[/cyan] {len(epic.get('sprints', []))}\n"
            f"[cyan]Features:[/cyan] {len(epic.get('features', []))}",
            title=f"Epic {epic_id}",
            box=box.ROUNDED
        ))
        
        # Show success criteria
        criteria = epic.get('success_criteria', [])
        if criteria:
            console.print("\n[bold]Success Criteria:[/bold]")
            for criterion in criteria:
                console.print(f"  • {criterion}")


@cli.command('get-sprint')
@click.argument('sprint_id')
def get_sprint(sprint_id: str):
    """Read sprint plan."""
    manager = SharedStateManager()
    sprint = manager.get_sprint(sprint_id)
    
    if sprint:
        console.print(Panel(
            f"[bold cyan]Sprint: {sprint.get('name', 'Untitled')}[/bold cyan]\n\n"
            f"[cyan]ID:[/cyan] {sprint.get('id', sprint_id)}\n"
            f"[cyan]Epic:[/cyan] {sprint.get('epic_id', 'none')}\n"
            f"[cyan]Status:[/cyan] {sprint.get('status', 'unknown')}\n"
            f"[cyan]Start:[/cyan] {sprint.get('start_date', 'TBD')}\n"
            f"[cyan]End:[/cyan] {sprint.get('end_date', 'TBD')}",
            title=f"Sprint {sprint_id}",
            box=box.ROUNDED
        ))
        
        # Show goals
        goals = sprint.get('goals', [])
        if goals:
            console.print("\n[bold]Sprint Goals:[/bold]")
            for goal in goals:
                console.print(f"  • {goal}")
        
        # Show task summary
        task_categories = sprint.get('task_categories', {})
        if task_categories:
            console.print("\n[bold]Task Summary:[/bold]")
            for category, tasks in task_categories.items():
                console.print(f"  • {category}: {len(tasks)} tasks")


@cli.command('list-resources')
def list_resources():
    """Show available shared resources."""
    manager = SharedStateManager()
    resources = manager.list_shared_resources()
    
    # Create tree view
    tree = Tree("[bold cyan]Shared Resources[/bold cyan]")
    
    # Add epics
    if resources["epics"]:
        epics_branch = tree.add("[magenta]Epics[/magenta]")
        for epic_id in sorted(resources["epics"]):
            epic = manager.get_epic(epic_id)
            title = epic.get("title", "Untitled") if epic else "???"
            epics_branch.add(f"{epic_id}: {title}")
    
    # Add sprints
    if resources["sprints"]:
        sprints_branch = tree.add("[green]Sprints[/green]")
        for sprint_id in sorted(resources["sprints"]):
            sprint = manager.get_sprint(sprint_id)
            name = sprint.get("name", "Untitled") if sprint else "???"
            sprints_branch.add(f"{sprint_id}: {name}")
    
    # Add templates
    if resources["templates"]:
        templates_branch = tree.add("[yellow]Templates[/yellow]")
        for template in sorted(resources["templates"]):
            templates_branch.add(template)
    
    # Add config keys
    if resources["config_keys"]:
        config_branch = tree.add("[blue]Configuration[/blue]")
        for key in sorted(resources["config_keys"]):
            if key not in ["created_at", "updated_at", "version"]:
                config_branch.add(key)
    
    console.print(tree)
    
    # Show summary
    console.print(Panel(
        f"[cyan]Epics:[/cyan] {len(resources['epics'])}\n"
        f"[cyan]Sprints:[/cyan] {len(resources['sprints'])}\n"
        f"[cyan]Templates:[/cyan] {len(resources['templates'])}\n"
        f"[cyan]Config Keys:[/cyan] {len(resources['config_keys'])}",
        title="Summary",
        box=box.ROUNDED
    ))


@cli.command('import-epic')
@click.option('--file', required=True, type=click.Path(exists=True), help='Epic JSON file')
@click.option('--epic-id', help='Override epic ID')
def import_epic(file: str, epic_id: Optional[str]):
    """Import epic from file."""
    manager = SharedStateManager()
    
    try:
        with open(file, 'r') as f:
            epic_data = json.load(f)
        
        # Use provided ID or extract from data
        if not epic_id:
            epic_id = epic_data.get('id')
            if not epic_id:
                console.print("[red]Error: Epic ID not found in file and not provided[/red]")
                sys.exit(1)
        
        if manager.save_epic(epic_id, epic_data):
            console.print(f"[green]✓ Imported epic: {epic_id}[/green]")
        else:
            console.print(f"[red]✗ Failed to import epic[/red]")
            sys.exit(1)
            
    except Exception as e:
        console.print(f"[red]Error importing epic: {e}[/red]")
        sys.exit(1)


@cli.command('import-sprint')
@click.option('--file', required=True, type=click.Path(exists=True), help='Sprint JSON file')
@click.option('--sprint-id', help='Override sprint ID')
def import_sprint(file: str, sprint_id: Optional[str]):
    """Import sprint from file."""
    manager = SharedStateManager()
    
    try:
        with open(file, 'r') as f:
            sprint_data = json.load(f)
        
        # Use provided ID or extract from data
        if not sprint_id:
            sprint_id = sprint_data.get('id')
            if not sprint_id:
                console.print("[red]Error: Sprint ID not found in file and not provided[/red]")
                sys.exit(1)
        
        if manager.save_sprint(sprint_id, sprint_data):
            console.print(f"[green]✓ Imported sprint: {sprint_id}[/green]")
        else:
            console.print(f"[red]✗ Failed to import sprint[/red]")
            sys.exit(1)
            
    except Exception as e:
        console.print(f"[red]Error importing sprint: {e}[/red]")
        sys.exit(1)


@cli.command('create-template')
@click.argument('template_name')
@click.option('--type', 'template_type', type=click.Choice(['epic', 'sprint', 'task']), required=True, help='Template type')
def create_template(template_name: str, template_type: str):
    """Create a new template."""
    manager = SharedStateManager()
    
    # Create template based on type
    if template_type == 'epic':
        template = {
            "type": "epic",
            "title": "Epic Template",
            "description": "Template for creating new epics",
            "status": "draft",
            "owner": "",
            "sprints": [],
            "features": [],
            "success_criteria": [],
            "timeline": {
                "estimated_weeks": 4,
                "actual_weeks": None
            }
        }
    elif template_type == 'sprint':
        template = {
            "type": "sprint",
            "name": "Sprint Template",
            "epic_id": "",
            "status": "planning",
            "start_date": "",
            "end_date": "",
            "team_assignments": {},
            "goals": [],
            "task_categories": {
                "pending": [],
                "in_progress": [],
                "completed": [],
                "blocked": []
            },
            "metrics": {
                "velocity": 0,
                "completion_rate": 0,
                "blocked_ratio": 0
            }
        }
    else:  # task
        template = {
            "type": "task",
            "title": "Task Template",
            "status": "pending",
            "priority": "medium",
            "assignee": None,
            "dependencies": [],
            "blocking": [],
            "estimated_effort": 1,
            "actual_effort": None,
            "artifacts": [],
            "context": {
                "epic_id": None,
                "sprint_id": None,
                "team": "",
                "requirements": "",
                "acceptance_criteria": []
            }
        }
    
    if manager.save_template(template_name, template):
        console.print(f"[green]✓ Created template: {template_name}[/green]")
    else:
        console.print(f"[red]✗ Failed to create template[/red]")
        sys.exit(1)


if __name__ == "__main__":
    cli()