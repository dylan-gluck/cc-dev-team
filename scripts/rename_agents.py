#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "rich>=13.0",
# ]
# ///
"""
Agent renaming script for .claude/agents/ directory.

This script renames agent files according to a predefined mapping and updates
all references to these agents throughout the directory structure.

Usage:
    python rename_agents.py
    # or if executable:
    ./rename_agents.py
"""

import os
import re
import sys
import logging
from pathlib import Path
from typing import Dict, Set, Tuple
from rich.console import Console
from rich.progress import Progress, TaskID
from rich.table import Table

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize rich console
console = Console()

# Agent renaming mapping
AGENT_MAPPING = {
    "research-ai": "research-ai",
    "engineering-api": "engineering-api",
    "meta-script-bun": "meta-script-bun",
    "product-analyst": "product-analyst",
    "devops-cicd": "devops-cicd",
    "engineering-cleanup": "engineering-cleanup",
    "meta-command": "meta-command",
    "meta-config": "meta-config",
    "marketing-content": "marketing-content",
    "creative-copywriter": "creative-creative-copywriter",
    "creative-director": "creative-director",  # no change
    "data-scientist": "data-scientist",  # no change
    "research-deep": "research-deep",
    "devops-manager": "devops-manager",  # no change
    "engineering-docs": "engineering-docs",
    "engineering-writer": "engineering-writer",
    "engineering-director": "engineering-director",  # no change
    "engineering-manager": "engineering-manager",  # no change
    "engineering-fullstack": "engineering-fullstack",
    "meta-commit": "meta-commit",
    "creative-illustrator": "creative-creative-illustrator",
    "devops-infrastructure": "devops-infrastructure",
    "creative-logo": "creative-logo",
    "marketing-director": "marketing-director",  # no change
    "meta-agent": "meta-agent",  # no change
    "creative-photographer": "creative-creative-photographer",
    "product-director": "product-director",  # no change
    "product-manager": "product-manager",  # no change
    "qa-analyst": "qa-analyst",  # no change
    "qa-director": "qa-director",  # no change
    "qa-e2e": "qa-e2e",
    "qa-scripts": "qa-scripts",
    "meta-readme": "meta-readme",
    "devops-release": "devops-release",
    "marketing-seo-analyst": "marketing-marketing-seo-analyst",
    "marketing-seo-engineer": "marketing-marketing-seo-engineer",
    "marketing-seo-researcher": "marketing-marketing-seo-researcher",
    "data-analytics": "data-analytics",
    "engineering-lead": "engineering-lead",
    "engineering-test": "engineering-test",
    "meta-script-uv": "meta-script-uv",
    "engineering-ux": "engineering-ux",
    "creative-ux-lead": "creative-creative-ux-lead",
    "creative-wireframe": "creative-wireframe",
    "meta-summary": "meta-summary",
}


def get_agents_directory() -> Path:
    """Get the .claude/agents directory path."""
    return Path(".claude/agents")


def get_files_that_need_renaming(agents_dir: Path) -> Dict[str, str]:
    """Find agent files that need renaming based on the mapping."""
    files_to_rename = {}
    
    for old_name, new_name in AGENT_MAPPING.items():
        if old_name != new_name:  # Only rename if names are different
            old_file = agents_dir / f"{old_name}.md"
            new_file = agents_dir / f"{new_name}.md"
            
            if old_file.exists():
                files_to_rename[str(old_file)] = str(new_file)
    
    return files_to_rename


def rename_agent_files(files_to_rename: Dict[str, str]) -> Tuple[int, int]:
    """Rename agent files according to the mapping."""
    success_count = 0
    error_count = 0
    
    console.print("\n[bold blue]Renaming agent files...[/bold blue]")
    
    for old_path, new_path in files_to_rename.items():
        try:
            old_file = Path(old_path)
            new_file = Path(new_path)
            
            # Check if target already exists
            if new_file.exists():
                console.print(f"[yellow]Warning: {new_file.name} already exists, skipping {old_file.name}[/yellow]")
                continue
            
            old_file.rename(new_file)
            console.print(f"[green]✓[/green] Renamed: {old_file.name} → {new_file.name}")
            success_count += 1
            
        except Exception as e:
            console.print(f"[red]✗[/red] Failed to rename {old_path}: {e}")
            error_count += 1
            logger.error(f"Failed to rename {old_path}: {e}")
    
    return success_count, error_count


def get_all_files_to_update() -> Set[Path]:
    """Get all files that might contain agent references."""
    files_to_update = set()
    
    # Common file extensions that might contain agent references
    extensions = {'.md', '.txt', '.json', '.yaml', '.yml', '.toml', '.py', '.js', '.ts'}
    
    for root, dirs, files in os.walk('.'):
        # Skip hidden directories and common build/cache directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in {'node_modules', '__pycache__', 'target', 'build', 'dist'}]
        
        for file in files:
            file_path = Path(root) / file
            if file_path.suffix.lower() in extensions:
                files_to_update.add(file_path)
    
    return files_to_update


def update_file_references(file_path: Path, mapping: Dict[str, str]) -> Tuple[bool, int]:
    """Update agent references in a single file."""
    try:
        # Read file content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        replacements_made = 0
        
        # Sort by length (longest first) to avoid partial replacements
        sorted_mapping = sorted(mapping.items(), key=lambda x: len(x[0]), reverse=True)
        
        for old_name, new_name in sorted_mapping:
            if old_name != new_name:  # Only process if names are different
                # Use word boundaries to ensure exact matches
                pattern = r'\b' + re.escape(old_name) + r'\b'
                matches = re.findall(pattern, content)
                if matches:
                    content = re.sub(pattern, new_name, content)
                    replacements_made += len(matches)
        
        # Write back if changes were made
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, replacements_made
        
        return False, 0
        
    except Exception as e:
        logger.error(f"Failed to update {file_path}: {e}")
        return False, 0


def update_all_references(files_to_update: Set[Path], mapping: Dict[str, str]) -> Tuple[int, int]:
    """Update agent references in all files."""
    files_updated = 0
    total_replacements = 0
    
    console.print(f"\n[bold blue]Updating references in {len(files_to_update)} files...[/bold blue]")
    
    with Progress() as progress:
        task = progress.add_task("[green]Processing files...", total=len(files_to_update))
        
        for file_path in files_to_update:
            was_updated, replacements = update_file_references(file_path, mapping)
            
            if was_updated:
                files_updated += 1
                total_replacements += replacements
                console.print(f"[green]✓[/green] Updated {file_path} ({replacements} replacements)")
            
            progress.update(task, advance=1)
    
    return files_updated, total_replacements


def create_summary_table(rename_success: int, rename_errors: int, 
                        files_updated: int, total_replacements: int) -> None:
    """Create a summary table of the operation results."""
    table = Table(title="Agent Renaming Summary")
    table.add_column("Operation", style="cyan")
    table.add_column("Count", style="magenta")
    table.add_column("Status", style="green")
    
    table.add_row("Files renamed", str(rename_success), "✓ Success" if rename_errors == 0 else f"⚠ {rename_errors} errors")
    table.add_row("Files updated", str(files_updated), "✓ Complete")
    table.add_row("Total replacements", str(total_replacements), "✓ Complete")
    
    console.print("\n")
    console.print(table)


def main() -> int:
    """Main execution function."""
    try:
        console.print("[bold green]Agent Renaming Script[/bold green]")
        console.print("This script will rename agent files and update all references.\n")
        
        # Check if agents directory exists
        agents_dir = get_agents_directory()
        if not agents_dir.exists():
            console.print(f"[red]Error: {agents_dir} directory not found![/red]")
            return 1
        
        # Show mapping summary
        changes_only = {k: v for k, v in AGENT_MAPPING.items() if k != v}
        console.print(f"[bold]Found {len(changes_only)} agents that need renaming:[/bold]")
        for old, new in list(changes_only.items())[:5]:  # Show first 5
            console.print(f"  {old} → {new}")
        if len(changes_only) > 5:
            console.print(f"  ... and {len(changes_only) - 5} more")
        
        # Get files that need renaming
        files_to_rename = get_files_that_need_renaming(agents_dir)
        console.print(f"\n[bold]Found {len(files_to_rename)} agent files to rename[/bold]")
        
        # Rename agent files
        rename_success, rename_errors = rename_agent_files(files_to_rename)
        
        # Get all files to update
        files_to_update = get_all_files_to_update()
        
        # Update references
        files_updated, total_replacements = update_all_references(files_to_update, AGENT_MAPPING)
        
        # Show summary
        create_summary_table(rename_success, rename_errors, files_updated, total_replacements)
        
        if rename_errors > 0:
            console.print(f"\n[yellow]Warning: {rename_errors} files failed to rename[/yellow]")
            return 1
        
        console.print("\n[bold green]✓ Agent renaming completed successfully![/bold green]")
        return 0
        
    except Exception as e:
        console.print(f"[red]Script failed: {e}[/red]")
        logger.error(f"Script failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())