#!/usr/bin/env -S uv run --script
# /// script
# dependencies = ["pydantic", "rich", "deepdiff"]
# ///

"""
Configuration management utilities for orchestration system.
Provides backup, restore, validation, and auto-fix capabilities.
"""

import json
import shutil
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from pydantic import BaseModel, Field
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.syntax import Syntax
from deepdiff import DeepDiff

console = Console()

# Configuration paths
CONFIG_DIR = Path(".claude/orchestration")
BACKUP_DIR = CONFIG_DIR / ".backups"
AGENTS_DIR = Path(".claude/agents")
STATE_FILE = Path(".claude/state/orchestration.json")

class ConfigBackup(BaseModel):
    """Backup metadata."""
    name: str
    timestamp: str
    files: Dict[str, str]  # filename -> checksum
    size_bytes: int
    version: Optional[str] = None
    description: Optional[str] = None

class ConfigManager:
    """Manages configuration operations."""
    
    def __init__(self):
        """Initialize configuration manager."""
        self.config_dir = CONFIG_DIR
        self.backup_dir = BACKUP_DIR
        self.ensure_directories()
    
    def ensure_directories(self):
        """Ensure required directories exist."""
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.config_dir.mkdir(parents=True, exist_ok=True)
    
    def get_file_checksum(self, filepath: Path) -> str:
        """Calculate SHA256 checksum of a file."""
        sha256 = hashlib.sha256()
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                sha256.update(chunk)
        return sha256.hexdigest()
    
    def create_backup(self, name: Optional[str] = None, description: Optional[str] = None) -> ConfigBackup:
        """Create a configuration backup."""
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup_name = name or f"backup-{timestamp}"
        backup_path = self.backup_dir / backup_name
        
        # Create backup directory
        backup_path.mkdir(parents=True, exist_ok=True)
        
        # Copy configuration files
        files = {}
        total_size = 0
        
        for config_file in self.config_dir.glob("*.json"):
            if config_file.is_file():
                dest = backup_path / config_file.name
                shutil.copy2(config_file, dest)
                files[config_file.name] = self.get_file_checksum(config_file)
                total_size += config_file.stat().st_size
        
        # Get version from settings if available
        version = None
        settings_file = self.config_dir / "settings.json"
        if settings_file.exists():
            try:
                with open(settings_file) as f:
                    settings = json.load(f)
                    version = settings.get("version")
            except:
                pass
        
        # Create manifest
        backup = ConfigBackup(
            name=backup_name,
            timestamp=timestamp,
            files=files,
            size_bytes=total_size,
            version=version,
            description=description
        )
        
        # Save manifest
        manifest_file = backup_path / "manifest.json"
        with open(manifest_file, 'w') as f:
            json.dump(backup.dict(), f, indent=2)
        
        return backup
    
    def list_backups(self) -> List[ConfigBackup]:
        """List all available backups."""
        backups = []
        
        if not self.backup_dir.exists():
            return backups
        
        for backup_path in sorted(self.backup_dir.iterdir(), reverse=True):
            if backup_path.is_dir():
                manifest_file = backup_path / "manifest.json"
                if manifest_file.exists():
                    try:
                        with open(manifest_file) as f:
                            manifest = json.load(f)
                            backups.append(ConfigBackup(**manifest))
                    except:
                        # Create basic backup info if manifest is corrupted
                        backups.append(ConfigBackup(
                            name=backup_path.name,
                            timestamp=backup_path.name.split('-', 1)[1] if '-' in backup_path.name else "unknown",
                            files={},
                            size_bytes=0
                        ))
        
        return backups
    
    def restore_backup(self, backup_name: str, create_safety_backup: bool = True) -> bool:
        """Restore configuration from backup."""
        backup_path = self.backup_dir / backup_name
        
        if not backup_path.exists():
            console.print(f"[red]Backup not found: {backup_name}[/red]")
            return False
        
        # Create safety backup if requested
        if create_safety_backup:
            safety_backup = self.create_backup(
                name=f"backup-pre-restore-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
                description=f"Safety backup before restoring {backup_name}"
            )
            console.print(f"[green]Safety backup created: {safety_backup.name}[/green]")
        
        # Restore files
        restored = []
        for config_file in backup_path.glob("*.json"):
            if config_file.name != "manifest.json":
                dest = self.config_dir / config_file.name
                shutil.copy2(config_file, dest)
                restored.append(config_file.name)
        
        console.print(f"[green]Restored {len(restored)} configuration files[/green]")
        return True
    
    def clean_old_backups(self, keep_count: int = 10, keep_days: int = 7) -> List[str]:
        """Clean old backups based on retention policy."""
        backups = self.list_backups()
        removed = []
        
        if len(backups) <= keep_count:
            return removed
        
        # Sort by timestamp
        backups.sort(key=lambda b: b.timestamp, reverse=True)
        
        # Keep recent backups
        cutoff_date = datetime.now() - timedelta(days=keep_days)
        
        for i, backup in enumerate(backups):
            # Keep first keep_count backups
            if i < keep_count:
                continue
            
            # Keep backups from last keep_days days
            try:
                backup_date = datetime.strptime(backup.timestamp, "%Y%m%d-%H%M%S")
                if backup_date > cutoff_date:
                    continue
            except:
                pass
            
            # Remove this backup
            backup_path = self.backup_dir / backup.name
            if backup_path.exists():
                shutil.rmtree(backup_path)
                removed.append(backup.name)
        
        return removed
    
    def validate_config(self, config_file: Path) -> Tuple[bool, List[str]]:
        """Validate a configuration file."""
        errors = []
        
        if not config_file.exists():
            return False, [f"File not found: {config_file}"]
        
        # Check JSON syntax
        try:
            with open(config_file) as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            return False, [f"JSON syntax error: {e}"]
        
        # File-specific validation
        if config_file.name == "teams.json":
            errors.extend(self._validate_teams(data))
        elif config_file.name == "workflows.json":
            errors.extend(self._validate_workflows(data))
        elif config_file.name == "settings.json":
            errors.extend(self._validate_settings(data))
        
        return len(errors) == 0, errors
    
    def _validate_teams(self, data: Dict) -> List[str]:
        """Validate teams configuration."""
        errors = []
        
        if "teams" not in data:
            errors.append("Missing 'teams' field")
            return errors
        
        # Check each team
        for team_name, team_config in data["teams"].items():
            if "description" not in team_config:
                errors.append(f"Team '{team_name}' missing description")
            
            if "lead" not in team_config:
                errors.append(f"Team '{team_name}' missing lead agent")
            elif not self._agent_exists(team_config["lead"]):
                errors.append(f"Team '{team_name}' lead agent '{team_config['lead']}' not found")
            
            if "members" in team_config:
                for member in team_config["members"]:
                    if "agent" not in member:
                        errors.append(f"Team '{team_name}' member missing agent field")
                    elif not self._agent_exists(member["agent"]):
                        errors.append(f"Team '{team_name}' member agent '{member['agent']}' not found")
        
        return errors
    
    def _validate_workflows(self, data: Dict) -> List[str]:
        """Validate workflows configuration."""
        errors = []
        
        if "workflows" not in data:
            errors.append("Missing 'workflows' field")
            return errors
        
        # Check each workflow
        for workflow_name, workflow_config in data["workflows"].items():
            if "triggers" not in workflow_config:
                errors.append(f"Workflow '{workflow_name}' missing triggers")
            
            if "delegation" not in workflow_config:
                errors.append(f"Workflow '{workflow_name}' missing delegation")
            else:
                delegation = workflow_config["delegation"]
                if "team" in delegation:
                    # Validate team exists (would need teams.json loaded)
                    pass
                elif "agent" in delegation:
                    if not self._agent_exists(delegation["agent"]):
                        errors.append(f"Workflow '{workflow_name}' agent '{delegation['agent']}' not found")
        
        return errors
    
    def _validate_settings(self, data: Dict) -> List[str]:
        """Validate settings configuration."""
        errors = []
        
        # Check required fields
        required_fields = ["version"]
        for field in required_fields:
            if field not in data:
                errors.append(f"Missing required field: {field}")
        
        return errors
    
    def _agent_exists(self, agent_name: str) -> bool:
        """Check if an agent file exists."""
        agent_file = AGENTS_DIR / f"{agent_name}.md"
        return agent_file.exists()
    
    def auto_fix_config(self, config_file: Path, dry_run: bool = False) -> Dict[str, Any]:
        """Auto-fix common configuration issues."""
        fixes = {
            "file": str(config_file),
            "fixes_applied": [],
            "errors": []
        }
        
        try:
            with open(config_file) as f:
                data = json.load(f)
                original_data = json.dumps(data, indent=2)
        except json.JSONDecodeError as e:
            # Try to fix JSON syntax
            try:
                content = config_file.read_text()
                # Remove trailing commas
                import re
                content = re.sub(r',(\s*[}\]])', r'\1', content)
                data = json.loads(content)
                fixes["fixes_applied"].append("Fixed JSON syntax errors")
            except:
                fixes["errors"].append(f"Cannot fix JSON syntax: {e}")
                return fixes
        
        # Apply fixes based on file type
        if config_file.name == "settings.json":
            if "version" not in data:
                data["version"] = "1.0.0"
                fixes["fixes_applied"].append("Added missing version field")
        
        elif config_file.name == "teams.json":
            if "teams" in data:
                for team_name, team_config in data["teams"].items():
                    # Remove references to non-existent agents
                    if "lead" in team_config and not self._agent_exists(team_config["lead"]):
                        fixes["fixes_applied"].append(f"Removed invalid lead agent in team '{team_name}'")
                        del team_config["lead"]
                    
                    if "members" in team_config:
                        valid_members = []
                        for member in team_config["members"]:
                            if "agent" in member and self._agent_exists(member["agent"]):
                                valid_members.append(member)
                            else:
                                fixes["fixes_applied"].append(f"Removed invalid member in team '{team_name}'")
                        team_config["members"] = valid_members
        
        # Save fixed configuration
        if not dry_run and fixes["fixes_applied"]:
            # Create backup first
            self.create_backup(description="Auto-fix backup")
            
            # Write fixed configuration
            with open(config_file, 'w') as f:
                json.dump(data, f, indent=2)
        
        # Add diff to fixes
        if fixes["fixes_applied"]:
            new_data = json.dumps(data, indent=2)
            fixes["diff"] = DeepDiff(original_data, new_data, verbose_level=2).to_dict()
        
        return fixes


def main():
    """CLI interface for configuration manager."""
    import sys
    
    manager = ConfigManager()
    
    if len(sys.argv) < 2:
        console.print("[yellow]Usage: config_manager.py <command> [options][/yellow]")
        console.print("Commands: backup, restore, list, clean, validate, fix")
        return
    
    command = sys.argv[1]
    
    if command == "backup":
        description = sys.argv[2] if len(sys.argv) > 2 else None
        backup = manager.create_backup(description=description)
        console.print(f"[green]Backup created: {backup.name}[/green]")
    
    elif command == "list":
        backups = manager.list_backups()
        table = Table(title="Available Backups")
        table.add_column("Name")
        table.add_column("Timestamp")
        table.add_column("Files")
        table.add_column("Size")
        table.add_column("Description")
        
        for backup in backups:
            table.add_row(
                backup.name,
                backup.timestamp,
                str(len(backup.files)),
                f"{backup.size_bytes / 1024:.1f} KB",
                backup.description or ""
            )
        
        console.print(table)
    
    elif command == "restore":
        if len(sys.argv) < 3:
            console.print("[red]Please specify backup name[/red]")
            return
        
        backup_name = sys.argv[2]
        if manager.restore_backup(backup_name):
            console.print(f"[green]Successfully restored from {backup_name}[/green]")
    
    elif command == "clean":
        removed = manager.clean_old_backups()
        if removed:
            console.print(f"[yellow]Removed {len(removed)} old backups[/yellow]")
            for name in removed:
                console.print(f"  - {name}")
        else:
            console.print("[green]No backups to clean[/green]")
    
    elif command == "validate":
        for config_file in CONFIG_DIR.glob("*.json"):
            valid, errors = manager.validate_config(config_file)
            if valid:
                console.print(f"✅ {config_file.name}: Valid")
            else:
                console.print(f"❌ {config_file.name}: {len(errors)} errors")
                for error in errors:
                    console.print(f"   - {error}")
    
    elif command == "fix":
        dry_run = "--dry-run" in sys.argv
        
        for config_file in CONFIG_DIR.glob("*.json"):
            result = manager.auto_fix_config(config_file, dry_run=dry_run)
            
            if result["fixes_applied"]:
                console.print(f"\n[yellow]{config_file.name}:[/yellow]")
                for fix in result["fixes_applied"]:
                    console.print(f"  ✓ {fix}")
            
            if result["errors"]:
                for error in result["errors"]:
                    console.print(f"  ✗ {error}", style="red")
        
        if dry_run:
            console.print("\n[yellow]DRY RUN - No changes made[/yellow]")

if __name__ == "__main__":
    main()