#!/usr/bin/env -S uv run --script
# /// script
# dependencies = ["pydantic", "rich"]
# ///

"""
Validation script for orchestration configuration files.
Ensures all configurations are valid and agent references are correct.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Set, Any, Optional
from pydantic import BaseModel, ValidationError, Field
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

# Configuration paths
CONFIG_DIR = Path(".claude/orchestration")
AGENTS_DIR = Path(".claude/agents")
TEAMS_CONFIG = CONFIG_DIR / "teams.json"
WORKFLOWS_CONFIG = CONFIG_DIR / "workflows.json"
SETTINGS_CONFIG = CONFIG_DIR / "settings.json"


class ValidationResult(BaseModel):
    """Result of a validation check."""
    file: str
    valid: bool
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)


class OrchestrationValidator:
    """Validates orchestration configuration files."""
    
    def __init__(self):
        """Initialize the validator."""
        self.results: List[ValidationResult] = []
        self.available_agents = self._get_available_agents()
    
    def _get_available_agents(self) -> Set[str]:
        """Get list of available agent names from .claude/agents/."""
        agents = set()
        if AGENTS_DIR.exists():
            for agent_file in AGENTS_DIR.glob("*.md"):
                # Agent name is the filename without extension
                agents.add(agent_file.stem)
        return agents
    
    def validate_json_syntax(self, file_path: Path) -> ValidationResult:
        """Validate JSON syntax of a file."""
        result = ValidationResult(file=str(file_path), valid=True)
        
        if not file_path.exists():
            result.valid = False
            result.errors.append(f"File not found: {file_path}")
            return result
        
        try:
            with open(file_path, 'r') as f:
                json.load(f)
        except json.JSONDecodeError as e:
            result.valid = False
            result.errors.append(f"Invalid JSON syntax: {e}")
        
        return result
    
    def validate_teams_config(self) -> ValidationResult:
        """Validate teams.json configuration."""
        result = self.validate_json_syntax(TEAMS_CONFIG)
        if not result.valid:
            return result
        
        with open(TEAMS_CONFIG, 'r') as f:
            config = json.load(f)
        
        # Check team structure
        teams = config.get("teams", {})
        for team_name, team_config in teams.items():
            # Check required fields
            if "name" not in team_config:
                result.errors.append(f"Team '{team_name}' missing 'name' field")
                result.valid = False
            
            if "members" not in team_config:
                result.errors.append(f"Team '{team_name}' missing 'members' field")
                result.valid = False
                continue
            
            # Check agent references
            for member in team_config.get("members", []):
                agent_name = member.get("agent")
                if agent_name:
                    # Build full agent name with team prefix
                    full_agent_name = f"{team_name}-{agent_name}"
                    
                    # Check if agent exists
                    if full_agent_name not in self.available_agents:
                        # Try without team prefix (for cross-team agents)
                        if agent_name not in self.available_agents:
                            result.warnings.append(
                                f"Agent '{agent_name}' in team '{team_name}' not found in .claude/agents/"
                            )
        
        # Check orchestration settings
        if "orchestration_settings" not in config:
            result.warnings.append("Missing 'orchestration_settings' section")
        
        return result
    
    def validate_workflows_config(self) -> ValidationResult:
        """Validate workflows.json configuration."""
        result = self.validate_json_syntax(WORKFLOWS_CONFIG)
        if not result.valid:
            return result
        
        with open(WORKFLOWS_CONFIG, 'r') as f:
            config = json.load(f)
        
        # Check workflows structure
        workflows = config.get("workflows", {})
        if not workflows:
            result.errors.append("No workflows defined")
            result.valid = False
        
        for workflow_name, workflow_config in workflows.items():
            # Check required fields
            if "description" not in workflow_config:
                result.warnings.append(f"Workflow '{workflow_name}' missing 'description'")
            
            # Check phases/types structure
            if "phases" not in workflow_config and "types" not in workflow_config:
                result.warnings.append(
                    f"Workflow '{workflow_name}' has neither 'phases' nor 'types'"
                )
        
        return result
    
    def validate_settings_config(self) -> ValidationResult:
        """Validate settings.json configuration."""
        result = self.validate_json_syntax(SETTINGS_CONFIG)
        if not result.valid:
            return result
        
        with open(SETTINGS_CONFIG, 'r') as f:
            config = json.load(f)
        
        # Check required sections
        required_sections = [
            "orchestration_mode",
            "resource_limits",
            "confirmation_settings",
            "slash_commands"
        ]
        
        for section in required_sections:
            if section not in config:
                result.warnings.append(f"Missing recommended section: '{section}'")
        
        # Validate orchestration mode
        mode_config = config.get("orchestration_mode", {})
        if mode_config.get("enabled", False) and mode_config.get("default_mode") == "full_auto":
            result.warnings.append(
                "Full auto mode is enabled - this can spawn many agents without consent"
            )
        
        return result
    
    def validate_agent_references(self) -> ValidationResult:
        """Cross-reference all agent mentions across configs."""
        result = ValidationResult(file="Agent References", valid=True)
        
        referenced_agents = set()
        
        # Collect references from teams.json
        if TEAMS_CONFIG.exists():
            with open(TEAMS_CONFIG, 'r') as f:
                teams_config = json.load(f)
                for team_name, team in teams_config.get("teams", {}).items():
                    for member in team.get("members", []):
                        if agent := member.get("agent"):
                            referenced_agents.add(agent)
        
        # Collect references from workflows.json
        if WORKFLOWS_CONFIG.exists():
            with open(WORKFLOWS_CONFIG, 'r') as f:
                workflows_config = json.load(f)
                # This would need more detailed parsing based on workflow structure
        
        # Check for orphaned references
        orphaned = referenced_agents - self.available_agents
        if orphaned:
            for agent in orphaned:
                result.warnings.append(f"Referenced agent '{agent}' not found in .claude/agents/")
        
        # Check for unused agents
        unused = self.available_agents - referenced_agents
        if unused and len(unused) < 10:  # Only warn if small number
            for agent in unused:
                result.warnings.append(f"Agent '{agent}' exists but is not referenced in configs")
        
        return result
    
    def run_all_validations(self) -> bool:
        """Run all validation checks."""
        console.print(Panel.fit("[bold]Validating Orchestration Configuration[/bold]", 
                               border_style="cyan"))
        
        # Run validations
        self.results.append(self.validate_teams_config())
        self.results.append(self.validate_workflows_config())
        self.results.append(self.validate_settings_config())
        self.results.append(self.validate_agent_references())
        
        # Display results
        all_valid = True
        for result in self.results:
            if result.valid and not result.errors and not result.warnings:
                console.print(f"✅ {result.file}: [green]Valid[/green]")
            elif result.valid and result.warnings:
                console.print(f"⚠️  {result.file}: [yellow]Valid with warnings[/yellow]")
                for warning in result.warnings:
                    console.print(f"   ⚠️  {warning}", style="yellow")
            else:
                console.print(f"❌ {result.file}: [red]Invalid[/red]")
                all_valid = False
                for error in result.errors:
                    console.print(f"   ❌ {error}", style="red")
                for warning in result.warnings:
                    console.print(f"   ⚠️  {warning}", style="yellow")
        
        # Summary
        console.print("\n" + "─" * 50)
        if all_valid:
            console.print("[bold green]✅ All configurations are valid![/bold green]")
        else:
            console.print("[bold red]❌ Some configurations have errors[/bold red]")
        
        warning_count = sum(len(r.warnings) for r in self.results)
        if warning_count > 0:
            console.print(f"[yellow]⚠️  {warning_count} warning(s) found[/yellow]")
        
        return all_valid


def main():
    """Main entry point."""
    validator = OrchestrationValidator()
    
    # Show available agents
    console.print(Panel.fit("[bold]Available Agents[/bold]", border_style="blue"))
    agents = sorted(validator.available_agents)
    if agents:
        # Group by team
        teams: Dict[str, List[str]] = {}
        for agent in agents:
            parts = agent.split("-", 1)
            if len(parts) == 2:
                team, name = parts
                if team not in teams:
                    teams[team] = []
                teams[team].append(name)
            else:
                if "other" not in teams:
                    teams["other"] = []
                teams["other"].append(agent)
        
        table = Table(show_header=True, header_style="bold blue")
        table.add_column("Team", style="cyan")
        table.add_column("Agents", style="white")
        
        for team, team_agents in sorted(teams.items()):
            table.add_row(team, ", ".join(sorted(team_agents)))
        
        console.print(table)
    else:
        console.print("[yellow]No agents found in .claude/agents/[/yellow]")
    
    console.print()
    
    # Run validations
    valid = validator.run_all_validations()
    
    # Exit with appropriate code
    sys.exit(0 if valid else 1)


if __name__ == "__main__":
    main()