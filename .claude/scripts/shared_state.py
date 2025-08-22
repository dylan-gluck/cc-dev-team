#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "click>=8.1",
#     "rich>=13.0",
#     "filelock>=3.12",
#     "pydantic>=2.0",
# ]
# ///
"""
Shared State Manager for V2 Orchestration System.

Manages project-level configuration, epics, sprints, and tool registry
that are shared across multiple sessions.

Usage:
    ./shared_state.py get-config PROJECT_ID
    ./shared_state.py set-config PROJECT_ID --data '{"key": "value"}'
    ./shared_state.py update-epic PROJECT_ID EPIC_ID --status completed
    ./shared_state.py list-sprints PROJECT_ID --status active
    ./shared_state.py list-tools
    ./shared_state.py register-tool --name "tool-name" --type "agent"
"""

import json
import sys
import tempfile
from pathlib import Path
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from enum import Enum
import logging

import click
from filelock import FileLock
from pydantic import BaseModel, Field
from rich.console import Console
from rich.table import Table
from rich.json import JSON as RichJSON

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Shared state directory configuration
SHARED_DIR = Path.home() / ".claude" / "state" / "shared"
SHARED_DIR.mkdir(parents=True, exist_ok=True)

console = Console()


class EpicStatus(str, Enum):
    """Epic status values."""
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    CANCELLED = "cancelled"


class SprintStatus(str, Enum):
    """Sprint status values."""
    PLANNED = "planned"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class ToolType(str, Enum):
    """Tool type values."""
    AGENT = "agent"
    COMMAND = "command"
    HOOK = "hook"
    WORKFLOW = "workflow"
    LIBRARY = "library"


class Epic(BaseModel):
    """Epic data model."""
    id: str
    title: str
    description: str = ""
    status: EpicStatus = EpicStatus.PLANNED
    priority: int = Field(ge=1, le=5, default=3)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    completed_at: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class Sprint(BaseModel):
    """Sprint data model."""
    id: str
    name: str
    epic_id: Optional[str] = None
    status: SprintStatus = SprintStatus.PLANNED
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    goals: List[str] = Field(default_factory=list)
    tasks: List[str] = Field(default_factory=list)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    metadata: Dict[str, Any] = Field(default_factory=dict)


class Tool(BaseModel):
    """Tool registration model."""
    name: str
    type: ToolType
    version: str = "1.0.0"
    description: str = ""
    path: Optional[str] = None
    dependencies: List[str] = Field(default_factory=list)
    config: Dict[str, Any] = Field(default_factory=dict)
    registered_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class SharedStateManager:
    """Manages shared state across sessions."""
    
    def __init__(self):
        self.shared_dir = SHARED_DIR
        self.projects_dir = self.shared_dir / "projects"
        self.tools_file = self.shared_dir / "tools.json"
        self.projects_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_project_dir(self, project_id: str) -> Path:
        """Get project directory."""
        project_dir = self.projects_dir / project_id
        project_dir.mkdir(parents=True, exist_ok=True)
        return project_dir
    
    def _get_config_file(self, project_id: str) -> Path:
        """Get project config file path."""
        return self._get_project_dir(project_id) / "config.json"
    
    def _get_epics_file(self, project_id: str) -> Path:
        """Get project epics file path."""
        return self._get_project_dir(project_id) / "epics.json"
    
    def _get_sprints_file(self, project_id: str) -> Path:
        """Get project sprints file path."""
        return self._get_project_dir(project_id) / "sprints.json"
    
    def _get_lock_file(self, file_path: Path) -> Path:
        """Get lock file for a given file."""
        return file_path.with_suffix('.lock')
    
    def _load_json(self, file_path: Path) -> Dict[str, Any]:
        """Load JSON file with default empty dict."""
        if not file_path.exists():
            return {}
        
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading {file_path}: {e}")
            return {}
    
    def _save_json(self, file_path: Path, data: Dict[str, Any]) -> None:
        """Save JSON file atomically."""
        # Write to temporary file first
        with tempfile.NamedTemporaryFile(
            mode='w',
            dir=file_path.parent,
            prefix=f".{file_path.stem}.",
            suffix='.tmp',
            delete=False
        ) as tmp_file:
            json.dump(data, tmp_file, indent=2, default=str)
            tmp_path = Path(tmp_file.name)
        
        # Atomically replace the original file
        tmp_path.replace(file_path)
    
    def get_config(self, project_id: str) -> Dict[str, Any]:
        """Get project configuration."""
        config_file = self._get_config_file(project_id)
        lock_file = self._get_lock_file(config_file)
        
        with FileLock(lock_file, timeout=10):
            config = self._load_json(config_file)
            
            # Initialize default config if empty
            if not config:
                config = {
                    "project_id": project_id,
                    "created_at": datetime.now(timezone.utc).isoformat(),
                    "settings": {},
                    "team": {},
                    "environments": {},
                    "metadata": {}
                }
                self._save_json(config_file, config)
            
            return config
    
    def set_config(self, project_id: str, config_data: Dict[str, Any]) -> bool:
        """Set project configuration."""
        config_file = self._get_config_file(project_id)
        lock_file = self._get_lock_file(config_file)
        
        with FileLock(lock_file, timeout=10):
            config = self._load_json(config_file)
            
            # Merge with existing config
            config.update(config_data)
            config["updated_at"] = datetime.now(timezone.utc).isoformat()
            
            self._save_json(config_file, config)
            return True
    
    def update_epic(
        self,
        project_id: str,
        epic_id: str,
        status: Optional[EpicStatus] = None,
        updates: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Update epic status and data."""
        epics_file = self._get_epics_file(project_id)
        lock_file = self._get_lock_file(epics_file)
        
        with FileLock(lock_file, timeout=10):
            epics = self._load_json(epics_file)
            
            if epic_id not in epics:
                # Create new epic
                epic = Epic(
                    id=epic_id,
                    title=updates.get("title", f"Epic {epic_id}") if updates else f"Epic {epic_id}",
                    status=status or EpicStatus.PLANNED
                )
                epics[epic_id] = epic.model_dump()
            else:
                # Update existing epic
                if status:
                    epics[epic_id]["status"] = status.value
                    if status == EpicStatus.COMPLETED:
                        epics[epic_id]["completed_at"] = datetime.now(timezone.utc).isoformat()
                
                if updates:
                    epics[epic_id].update(updates)
                
                epics[epic_id]["updated_at"] = datetime.now(timezone.utc).isoformat()
            
            self._save_json(epics_file, epics)
            return True
    
    def list_epics(
        self,
        project_id: str,
        status: Optional[EpicStatus] = None
    ) -> List[Dict[str, Any]]:
        """List project epics with optional status filter."""
        epics_file = self._get_epics_file(project_id)
        epics = self._load_json(epics_file)
        
        result = []
        for epic_data in epics.values():
            if status and epic_data.get("status") != status.value:
                continue
            result.append(epic_data)
        
        # Sort by priority and created_at
        result.sort(key=lambda x: (x.get("priority", 3), x.get("created_at", "")))
        
        return result
    
    def create_sprint(
        self,
        project_id: str,
        sprint_id: str,
        name: str,
        epic_id: Optional[str] = None,
        sprint_data: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Create a new sprint."""
        sprints_file = self._get_sprints_file(project_id)
        lock_file = self._get_lock_file(sprints_file)
        
        with FileLock(lock_file, timeout=10):
            sprints = self._load_json(sprints_file)
            
            sprint = Sprint(
                id=sprint_id,
                name=name,
                epic_id=epic_id
            )
            
            if sprint_data:
                # Update sprint with additional data
                sprint_dict = sprint.model_dump()
                sprint_dict.update(sprint_data)
                sprints[sprint_id] = sprint_dict
            else:
                sprints[sprint_id] = sprint.model_dump()
            
            self._save_json(sprints_file, sprints)
            return True
    
    def list_sprints(
        self,
        project_id: str,
        status: Optional[SprintStatus] = None,
        epic_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """List project sprints with optional filters."""
        sprints_file = self._get_sprints_file(project_id)
        sprints = self._load_json(sprints_file)
        
        result = []
        for sprint_data in sprints.values():
            if status and sprint_data.get("status") != status.value:
                continue
            if epic_id and sprint_data.get("epic_id") != epic_id:
                continue
            result.append(sprint_data)
        
        # Sort by created_at
        result.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        
        return result
    
    def list_tools(self) -> List[Dict[str, Any]]:
        """List all registered tools."""
        lock_file = self._get_lock_file(self.tools_file)
        
        with FileLock(lock_file, timeout=10):
            tools = self._load_json(self.tools_file)
            
            result = []
            for tool_data in tools.values():
                result.append(tool_data)
            
            # Sort by type and name
            result.sort(key=lambda x: (x.get("type", ""), x.get("name", "")))
            
            return result
    
    def register_tool(
        self,
        name: str,
        tool_type: ToolType,
        version: str = "1.0.0",
        description: str = "",
        path: Optional[str] = None,
        dependencies: Optional[List[str]] = None,
        config: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Register a new tool or update existing one."""
        lock_file = self._get_lock_file(self.tools_file)
        
        with FileLock(lock_file, timeout=10):
            tools = self._load_json(self.tools_file)
            
            tool = Tool(
                name=name,
                type=tool_type,
                version=version,
                description=description,
                path=path,
                dependencies=dependencies or [],
                config=config or {}
            )
            
            if name in tools:
                tool.updated_at = datetime.now(timezone.utc).isoformat()
            
            tools[name] = tool.model_dump()
            
            self._save_json(self.tools_file, tools)
            return True
    
    def get_tool(self, name: str) -> Optional[Dict[str, Any]]:
        """Get tool information by name."""
        tools = self._load_json(self.tools_file)
        return tools.get(name)


@click.group()
def cli():
    """Shared State Manager for V2 Orchestration System."""
    pass


@cli.command('get-config')
@click.argument('project_id')
@click.option('--json-output', is_flag=True, help='Output as JSON')
def get_config(project_id: str, json_output: bool):
    """Get project configuration."""
    try:
        manager = SharedStateManager()
        config = manager.get_config(project_id)
        
        if json_output:
            print(json.dumps(config, indent=2))
        else:
            console.print(f"[bold cyan]Project Configuration: {project_id}[/bold cyan]")
            console.print(RichJSON(json.dumps(config, indent=2)))
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@cli.command('set-config')
@click.argument('project_id')
@click.option('--data', required=True, help='Configuration data as JSON')
def set_config(project_id: str, data: str):
    """Set project configuration."""
    try:
        manager = SharedStateManager()
        config_data = json.loads(data)
        
        success = manager.set_config(project_id, config_data)
        
        if success:
            console.print(f"[green]✓ Configuration updated for project {project_id}[/green]")
        else:
            console.print(f"[red]Failed to update configuration[/red]")
            sys.exit(1)
    except json.JSONDecodeError as e:
        console.print(f"[red]Invalid JSON data: {e}[/red]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@cli.command('update-epic')
@click.argument('project_id')
@click.argument('epic_id')
@click.option('--status', type=click.Choice(['planned', 'in_progress', 'completed', 'blocked', 'cancelled']))
@click.option('--title', help='Epic title')
@click.option('--description', help='Epic description')
@click.option('--priority', type=int, help='Priority (1-5)')
@click.option('--data', help='Additional data as JSON')
def update_epic(project_id: str, epic_id: str, status: Optional[str], title: Optional[str],
                description: Optional[str], priority: Optional[int], data: Optional[str]):
    """Update epic status and data."""
    try:
        manager = SharedStateManager()
        
        updates = {}
        if title:
            updates["title"] = title
        if description:
            updates["description"] = description
        if priority:
            updates["priority"] = priority
        
        if data:
            additional_data = json.loads(data)
            updates.update(additional_data)
        
        epic_status = EpicStatus(status) if status else None
        
        success = manager.update_epic(project_id, epic_id, epic_status, updates if updates else None)
        
        if success:
            console.print(f"[green]✓ Epic {epic_id} updated[/green]")
        else:
            console.print(f"[red]Failed to update epic[/red]")
            sys.exit(1)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@cli.command('list-epics')
@click.argument('project_id')
@click.option('--status', type=click.Choice(['planned', 'in_progress', 'completed', 'blocked', 'cancelled']))
@click.option('--json-output', is_flag=True, help='Output as JSON')
def list_epics(project_id: str, status: Optional[str], json_output: bool):
    """List project epics."""
    try:
        manager = SharedStateManager()
        epic_status = EpicStatus(status) if status else None
        epics = manager.list_epics(project_id, epic_status)
        
        if json_output:
            print(json.dumps(epics, indent=2))
        else:
            if epics:
                table = Table(title=f"Epics for {project_id}")
                table.add_column("ID", style="cyan")
                table.add_column("Title", style="white")
                table.add_column("Status", style="green")
                table.add_column("Priority", style="yellow")
                table.add_column("Created", style="dim")
                
                for epic in epics:
                    status_color = {
                        "planned": "yellow",
                        "in_progress": "blue",
                        "completed": "green",
                        "blocked": "red",
                        "cancelled": "dim"
                    }.get(epic["status"], "white")
                    
                    table.add_row(
                        epic["id"],
                        epic["title"],
                        f"[{status_color}]{epic['status']}[/{status_color}]",
                        str(epic.get("priority", 3)),
                        epic["created_at"][:10] if epic.get("created_at") else "N/A"
                    )
                
                console.print(table)
            else:
                console.print("[yellow]No epics found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@cli.command('create-sprint')
@click.argument('project_id')
@click.argument('sprint_id')
@click.argument('name')
@click.option('--epic-id', help='Associated epic ID')
@click.option('--data', help='Additional sprint data as JSON')
def create_sprint(project_id: str, sprint_id: str, name: str, epic_id: Optional[str], data: Optional[str]):
    """Create a new sprint."""
    try:
        manager = SharedStateManager()
        
        sprint_data = None
        if data:
            sprint_data = json.loads(data)
        
        success = manager.create_sprint(project_id, sprint_id, name, epic_id, sprint_data)
        
        if success:
            console.print(f"[green]✓ Sprint {sprint_id} created[/green]")
        else:
            console.print(f"[red]Failed to create sprint[/red]")
            sys.exit(1)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@cli.command('list-sprints')
@click.argument('project_id')
@click.option('--status', type=click.Choice(['planned', 'active', 'completed', 'cancelled']))
@click.option('--epic-id', help='Filter by epic ID')
@click.option('--json-output', is_flag=True, help='Output as JSON')
def list_sprints(project_id: str, status: Optional[str], epic_id: Optional[str], json_output: bool):
    """List project sprints."""
    try:
        manager = SharedStateManager()
        sprint_status = SprintStatus(status) if status else None
        sprints = manager.list_sprints(project_id, sprint_status, epic_id)
        
        if json_output:
            print(json.dumps(sprints, indent=2))
        else:
            if sprints:
                table = Table(title=f"Sprints for {project_id}")
                table.add_column("ID", style="cyan")
                table.add_column("Name", style="white")
                table.add_column("Status", style="green")
                table.add_column("Epic", style="blue")
                table.add_column("Tasks", style="yellow")
                table.add_column("Created", style="dim")
                
                for sprint in sprints:
                    status_color = {
                        "planned": "yellow",
                        "active": "green",
                        "completed": "blue",
                        "cancelled": "dim"
                    }.get(sprint["status"], "white")
                    
                    table.add_row(
                        sprint["id"],
                        sprint["name"],
                        f"[{status_color}]{sprint['status']}[/{status_color}]",
                        sprint.get("epic_id", "-"),
                        str(len(sprint.get("tasks", []))),
                        sprint["created_at"][:10] if sprint.get("created_at") else "N/A"
                    )
                
                console.print(table)
            else:
                console.print("[yellow]No sprints found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@cli.command('list-tools')
@click.option('--type', type=click.Choice(['agent', 'command', 'hook', 'workflow', 'library']),
              help='Filter by tool type')
@click.option('--json-output', is_flag=True, help='Output as JSON')
def list_tools(type: Optional[str], json_output: bool):
    """List registered tools."""
    try:
        manager = SharedStateManager()
        tools = manager.list_tools()
        
        # Filter by type if specified
        if type:
            tools = [t for t in tools if t.get("type") == type]
        
        if json_output:
            print(json.dumps(tools, indent=2))
        else:
            if tools:
                table = Table(title="Registered Tools")
                table.add_column("Name", style="cyan")
                table.add_column("Type", style="magenta")
                table.add_column("Version", style="yellow")
                table.add_column("Description", style="white")
                table.add_column("Registered", style="dim")
                
                for tool in tools:
                    table.add_row(
                        tool["name"],
                        tool["type"],
                        tool["version"],
                        tool.get("description", "")[:50] + "..." if len(tool.get("description", "")) > 50 else tool.get("description", ""),
                        tool["registered_at"][:10] if tool.get("registered_at") else "N/A"
                    )
                
                console.print(table)
            else:
                console.print("[yellow]No tools found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@cli.command('register-tool')
@click.option('--name', required=True, help='Tool name')
@click.option('--type', type=click.Choice(['agent', 'command', 'hook', 'workflow', 'library']),
              required=True, help='Tool type')
@click.option('--version', default='1.0.0', help='Tool version')
@click.option('--description', help='Tool description')
@click.option('--path', help='Tool path')
@click.option('--dependencies', help='Dependencies as JSON array')
@click.option('--config', help='Configuration as JSON')
def register_tool(name: str, type: str, version: str, description: Optional[str],
                  path: Optional[str], dependencies: Optional[str], config: Optional[str]):
    """Register a new tool."""
    try:
        manager = SharedStateManager()
        
        deps = []
        if dependencies:
            deps = json.loads(dependencies)
        
        cfg = {}
        if config:
            cfg = json.loads(config)
        
        success = manager.register_tool(
            name=name,
            tool_type=ToolType(type),
            version=version,
            description=description or "",
            path=path,
            dependencies=deps,
            config=cfg
        )
        
        if success:
            console.print(f"[green]✓ Tool {name} registered[/green]")
        else:
            console.print(f"[red]Failed to register tool[/red]")
            sys.exit(1)
    except json.JSONDecodeError as e:
        console.print(f"[red]Invalid JSON: {e}[/red]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@cli.command('get-tool')
@click.argument('name')
@click.option('--json-output', is_flag=True, help='Output as JSON')
def get_tool(name: str, json_output: bool):
    """Get tool information by name."""
    try:
        manager = SharedStateManager()
        tool = manager.get_tool(name)
        
        if tool:
            if json_output:
                print(json.dumps(tool, indent=2))
            else:
                console.print(f"[bold cyan]Tool: {tool['name']}[/bold cyan]")
                console.print(f"Type: {tool['type']}")
                console.print(f"Version: {tool['version']}")
                console.print(f"Description: {tool.get('description', 'N/A')}")
                if tool.get('path'):
                    console.print(f"Path: {tool['path']}")
                if tool.get('dependencies'):
                    console.print(f"Dependencies: {', '.join(tool['dependencies'])}")
                if tool.get('config'):
                    console.print("Configuration:")
                    console.print(RichJSON(json.dumps(tool['config'], indent=2)))
        else:
            console.print(f"[yellow]Tool not found: {name}[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    cli()