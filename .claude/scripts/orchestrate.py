#!/usr/bin/env -S uv run --script
# /// script
# dependencies = ["pydantic", "rich", "typer"]
# ///

"""
Orchestration command handler for Claude Code.
Manages team coordination and multi-agent workflows.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum

import typer
from pydantic import BaseModel, Field
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Confirm

app = typer.Typer()
console = Console()

# Configuration paths
CONFIG_DIR = Path(".claude/orchestration")
STATE_DIR = Path(".claude/state")
TEAMS_CONFIG = CONFIG_DIR / "teams.json"
WORKFLOWS_CONFIG = CONFIG_DIR / "workflows.json"
SETTINGS_CONFIG = CONFIG_DIR / "settings.json"
STATE_FILE = STATE_DIR / "orchestration.json"


class OrchestrationMode(str, Enum):
    """Orchestration operation modes."""
    MANUAL = "manual"
    ASSISTED = "assisted"
    SEMI_AUTO = "semi_auto"
    FULL_AUTO = "full_auto"


class OrchestrationState(BaseModel):
    """Runtime state for orchestration."""
    session_id: str
    mode: OrchestrationMode = OrchestrationMode.MANUAL
    active_teams: List[str] = Field(default_factory=list)
    active_agents: List[str] = Field(default_factory=list)
    current_workflow: Optional[str] = None
    current_phase: Optional[str] = None
    token_usage: int = 0
    start_time: datetime = Field(default_factory=datetime.now)
    tasks_completed: int = 0
    tasks_pending: int = 0


class OrchestrationManager:
    """Manages orchestration operations."""
    
    def __init__(self):
        """Initialize the orchestration manager."""
        self.teams = self._load_config(TEAMS_CONFIG)
        self.workflows = self._load_config(WORKFLOWS_CONFIG)
        self.settings = self._load_config(SETTINGS_CONFIG)
        self.state = self._load_state()
    
    def _load_config(self, path: Path) -> Dict[str, Any]:
        """Load configuration from JSON file."""
        if not path.exists():
            console.print(f"[red]Configuration file not found: {path}[/red]")
            return {}
        
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            console.print(f"[red]Error loading {path}: {e}[/red]")
            return {}
    
    def _load_state(self) -> OrchestrationState:
        """Load or create orchestration state."""
        if STATE_FILE.exists():
            try:
                with open(STATE_FILE, 'r') as f:
                    data = json.load(f)
                    return OrchestrationState(**data)
            except Exception as e:
                console.print(f"[yellow]Creating new state file: {e}[/yellow]")
        
        # Create new state
        import uuid
        state = OrchestrationState(session_id=str(uuid.uuid4()))
        self._save_state(state)
        return state
    
    def _save_state(self, state: OrchestrationState):
        """Save orchestration state to file."""
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        with open(STATE_FILE, 'w') as f:
            json.dump(state.model_dump(mode='json'), f, indent=2, default=str)
    
    def show_preview(self, command: str, args: List[str]) -> bool:
        """Show preview and get confirmation for orchestration."""
        # Parse command and estimate resources
        agents_needed = self._estimate_agents(command, args)
        tokens_estimate = self._estimate_tokens(command, args)
        time_estimate = self._estimate_time(command, args)
        
        # Create preview table
        table = Table(title=f"Orchestration Preview: {command}")
        table.add_column("Resource", style="cyan")
        table.add_column("Estimate", style="yellow")
        table.add_column("Limit", style="green")
        
        table.add_row("Agents", str(agents_needed), 
                      str(self.settings.get("resource_limits", {}).get("max_agents_per_operation", 10)))
        table.add_row("Tokens", f"{tokens_estimate:,}", 
                      f"{self.settings.get('resource_limits', {}).get('max_tokens_per_session', 100000):,}")
        table.add_row("Time", f"{time_estimate} minutes", 
                      f"{self.settings.get('resource_limits', {}).get('max_runtime_minutes', 60)} minutes")
        
        console.print(table)
        
        # Check thresholds
        confirm_settings = self.settings.get("confirmation_settings", {})
        thresholds = confirm_settings.get("confirmation_thresholds", {})
        
        requires_confirmation = (
            agents_needed >= thresholds.get("agents", {}).get("require", 5) or
            tokens_estimate >= thresholds.get("tokens", {}).get("require", 50000) or
            time_estimate >= thresholds.get("time_minutes", {}).get("require", 30)
        )
        
        if requires_confirmation:
            return Confirm.ask("[bold yellow]This operation exceeds thresholds. Continue?[/bold yellow]")
        
        return True
    
    def _estimate_agents(self, command: str, args: List[str]) -> int:
        """Estimate number of agents needed."""
        # Simple estimation based on command type
        estimates = {
            "sprint start": 5,
            "epic plan": 8,
            "task delegate": 2,
            "team activate": 3,
        }
        return estimates.get(command, 1)
    
    def _estimate_tokens(self, command: str, args: List[str]) -> int:
        """Estimate token usage."""
        # Simple estimation based on command type
        estimates = {
            "sprint start": 25000,
            "epic plan": 50000,
            "task delegate": 5000,
            "team activate": 15000,
        }
        return estimates.get(command, 10000)
    
    def _estimate_time(self, command: str, args: List[str]) -> int:
        """Estimate time in minutes."""
        # Simple estimation based on command type
        estimates = {
            "sprint start": 20,
            "epic plan": 45,
            "task delegate": 5,
            "team activate": 10,
        }
        return estimates.get(command, 10)
    
    def execute_command(self, command: str, args: List[str]):
        """Execute an orchestration command."""
        console.print(f"[green]Executing: {command} {' '.join(args)}[/green]")
        
        # Update state
        self.state.current_workflow = command
        self._save_state(self.state)
        
        # Command execution would happen here
        # This is a placeholder for the actual orchestration logic
        console.print("[yellow]Note: This is a configuration placeholder.[/yellow]")
        console.print("[yellow]Actual orchestration would be triggered via Claude Code slash commands.[/yellow]")
        
        # Show success message
        console.print(f"[green]✓ Command '{command}' configured successfully[/green]")


@app.command()
def sprint(action: str = "start"):
    """Manage sprint orchestration."""
    manager = OrchestrationManager()
    
    if not manager.show_preview(f"sprint {action}", []):
        console.print("[red]Operation cancelled[/red]")
        return
    
    manager.execute_command(f"sprint {action}", [])


@app.command()
def epic(action: str = "plan"):
    """Manage epic orchestration."""
    manager = OrchestrationManager()
    
    if not manager.show_preview(f"epic {action}", []):
        console.print("[red]Operation cancelled[/red]")
        return
    
    manager.execute_command(f"epic {action}", [])


@app.command()
def task(action: str, task_id: Optional[str] = None):
    """Delegate tasks to teams."""
    manager = OrchestrationManager()
    args = [task_id] if task_id else []
    
    if not manager.show_preview(f"task {action}", args):
        console.print("[red]Operation cancelled[/red]")
        return
    
    manager.execute_command(f"task {action}", args)


@app.command()
def team(action: str, team_name: Optional[str] = None):
    """Activate and manage teams."""
    manager = OrchestrationManager()
    args = [team_name] if team_name else []
    
    if not manager.show_preview(f"team {action}", args):
        console.print("[red]Operation cancelled[/red]")
        return
    
    manager.execute_command(f"team {action}", args)


@app.command()
def status():
    """Show current orchestration status."""
    manager = OrchestrationManager()
    state = manager.state
    
    # Create status panel
    status_text = f"""
Session ID: {state.session_id}
Mode: {state.mode.value}
Active Teams: {', '.join(state.active_teams) if state.active_teams else 'None'}
Active Agents: {len(state.active_agents)}
Current Workflow: {state.current_workflow or 'None'}
Current Phase: {state.current_phase or 'None'}
Token Usage: {state.token_usage:,}
Tasks Completed: {state.tasks_completed}
Tasks Pending: {state.tasks_pending}
Start Time: {state.start_time.strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    panel = Panel(status_text, title="Orchestration Status", border_style="green")
    console.print(panel)


@app.command()
def config(action: str = "show"):
    """Manage orchestration configuration."""
    manager = OrchestrationManager()
    
    if action == "show":
        console.print(Panel.fit("Teams Configuration", border_style="cyan"))
        console.print(json.dumps(manager.teams.get("teams", {}), indent=2))
        
        console.print("\n")
        console.print(Panel.fit("Settings", border_style="cyan"))
        console.print(json.dumps(manager.settings, indent=2))
    
    elif action == "reload":
        manager = OrchestrationManager()
        console.print("[green]✓ Configuration reloaded[/green]")
    
    else:
        console.print(f"[red]Unknown action: {action}[/red]")


@app.command()
def stop():
    """Stop all orchestration activities."""
    if Confirm.ask("[bold red]Stop all orchestration activities?[/bold red]"):
        manager = OrchestrationManager()
        manager.state.active_teams = []
        manager.state.active_agents = []
        manager.state.current_workflow = None
        manager.state.current_phase = None
        manager._save_state(manager.state)
        console.print("[green]✓ All orchestration activities stopped[/green]")
    else:
        console.print("[yellow]Operation cancelled[/yellow]")


if __name__ == "__main__":
    app()