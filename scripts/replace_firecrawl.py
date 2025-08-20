#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "rich>=13.0",
#     "typer>=0.9",
#     "pathlib>=1.0",
# ]
# ///
"""
Replace Firecrawl MCP tools with FreeCrawl equivalents across the codebase.

This script scans the codebase for Firecrawl tool references (mcp__firecrawl__*) 
and replaces them with corresponding FreeCrawl tool names, providing detailed 
logging and backup options.

Usage:
    # Dry run to preview changes
    python scripts/replace_firecrawl.py --dry-run
    
    # Execute replacements with backup
    python scripts/replace_firecrawl.py --backup
    
    # Execute replacements without backup
    python scripts/replace_firecrawl.py
"""

import sys
import re
import shutil
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import logging

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Confirm

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

console = Console()
app = typer.Typer(help="Replace Firecrawl MCP tools with FreeCrawl equivalents")

@dataclass
class Replacement:
    """Represents a single text replacement operation."""
    old_text: str
    new_text: str
    description: str

@dataclass
class FileChange:
    """Represents changes made to a single file."""
    file_path: Path
    replacements: List[Tuple[str, str, int]]  # (old, new, count)
    total_changes: int

class FirecrawlReplacer:
    """Main class for handling Firecrawl to FreeCrawl replacements."""
    
    def __init__(self, root_dir: Path, dry_run: bool = False, backup: bool = False, force: bool = False):
        self.root_dir = root_dir
        self.dry_run = dry_run
        self.backup = backup
        self.force = force
        self.file_changes: List[FileChange] = []
        
        # Define the mapping from Firecrawl to FreeCrawl tools
        self.tool_mappings = {
            'mcp__firecrawl__firecrawl_scrape': 'mcp__freecrawl__scrape',
            'mcp__firecrawl__firecrawl_batch_scrape': 'mcp__freecrawl__batch_scrape',
            'mcp__firecrawl__firecrawl_search': 'mcp__freecrawl__search',
            'mcp__firecrawl__firecrawl_extract': 'mcp__freecrawl__extract',
            'mcp__firecrawl__firecrawl_crawl': 'mcp__freecrawl__crawl',
            'mcp__firecrawl__firecrawl_map': 'mcp__freecrawl__map',
            'mcp__firecrawl__firecrawl_check_crawl_status': 'mcp__freecrawl__check_crawl_status',
            'mcp__firecrawl__firecrawl_deep_research': 'mcp__freecrawl__deep_research',
            'mcp__firecrawl__firecrawl_generate_llmstxt': 'mcp__freecrawl__generate_llmstxt',
        }
        
        # Wildcard patterns for general replacements
        self.wildcard_patterns = [
            (r'mcp__firecrawl__\*', 'mcp__freecrawl__*'),
            (r'mcp__firecrawl__firecrawl_([a-zA-Z_]+)', r'mcp__freecrawl__\1'),
        ]
    
    def find_target_files(self) -> List[Path]:
        """Find all files that might contain Firecrawl references."""
        target_patterns = [
            ".claude/agents/*.md",
            ".claude/commands/**/*.md",
            "ai_docs/*.md",
            "**/*.md"  # Catch any other markdown files
        ]
        
        files = set()
        for pattern in target_patterns:
            files.update(self.root_dir.glob(pattern))
        
        # Filter to only include files that actually contain mcp__firecrawl__
        filtered_files = []
        for file_path in files:
            try:
                content = file_path.read_text(encoding='utf-8')
                if 'mcp__firecrawl__' in content:
                    filtered_files.append(file_path)
            except (UnicodeDecodeError, PermissionError) as e:
                logger.warning(f"Skipping {file_path}: {e}")
        
        return sorted(filtered_files)
    
    def analyze_file(self, file_path: Path) -> Optional[FileChange]:
        """Analyze a file for potential replacements."""
        try:
            content = file_path.read_text(encoding='utf-8')
            original_content = content
            replacements = []
            
            # Apply direct tool mappings
            for old_tool, new_tool in self.tool_mappings.items():
                if old_tool in content:
                    count = content.count(old_tool)
                    content = content.replace(old_tool, new_tool)
                    replacements.append((old_tool, new_tool, count))
            
            # Apply wildcard pattern replacements
            for pattern, replacement in self.wildcard_patterns:
                matches = re.findall(pattern, content)
                if matches:
                    new_content = re.sub(pattern, replacement, content)
                    if new_content != content:
                        # Count approximate matches for reporting
                        count = len(matches)
                        replacements.append((pattern, replacement, count))
                        content = new_content
            
            if content != original_content:
                total_changes = sum(count for _, _, count in replacements)
                return FileChange(file_path, replacements, total_changes)
            
            return None
            
        except Exception as e:
            logger.error(f"Error analyzing {file_path}: {e}")
            return None
    
    def apply_changes(self, file_change: FileChange) -> bool:
        """Apply changes to a file."""
        try:
            # Create backup if requested
            if self.backup:
                backup_path = file_change.file_path.with_suffix(
                    file_change.file_path.suffix + '.backup'
                )
                shutil.copy2(file_change.file_path, backup_path)
                logger.info(f"Created backup: {backup_path}")
            
            # Read current content
            content = file_change.file_path.read_text(encoding='utf-8')
            
            # Apply all replacements
            for old_tool, new_tool in self.tool_mappings.items():
                content = content.replace(old_tool, new_tool)
            
            for pattern, replacement in self.wildcard_patterns:
                content = re.sub(pattern, replacement, content)
            
            if not self.dry_run:
                file_change.file_path.write_text(content, encoding='utf-8')
                logger.info(f"Updated {file_change.file_path}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error applying changes to {file_change.file_path}: {e}")
            return False
    
    def generate_summary_table(self) -> Table:
        """Generate a summary table of all changes."""
        table = Table(title="Firecrawl → FreeCrawl Replacement Summary")
        table.add_column("File", style="cyan")
        table.add_column("Changes", justify="right", style="green")
        table.add_column("Details", style="yellow")
        
        for file_change in self.file_changes:
            relative_path = file_change.file_path.relative_to(self.root_dir)
            details = ", ".join([
                f"{old} → {new} ({count}x)" 
                for old, new, count in file_change.replacements[:3]  # Show first 3
            ])
            if len(file_change.replacements) > 3:
                details += f" + {len(file_change.replacements) - 3} more"
            
            table.add_row(
                str(relative_path),
                str(file_change.total_changes),
                details
            )
        
        return table
    
    def run(self) -> int:
        """Execute the replacement process."""
        console.print(Panel.fit(
            "🔄 Firecrawl → FreeCrawl Tool Replacement",
            style="bold blue"
        ))
        
        if self.dry_run:
            console.print("🔍 Running in DRY RUN mode - no files will be modified")
        
        # Find target files
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Scanning for target files...", total=None)
            target_files = self.find_target_files()
            progress.update(task, completed=100)
        
        console.print(f"📁 Found {len(target_files)} files with Firecrawl references")
        
        if not target_files:
            console.print("✅ No files need updating!")
            return 0
        
        # Analyze files
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Analyzing files...", total=len(target_files))
            
            for file_path in target_files:
                file_change = self.analyze_file(file_path)
                if file_change:
                    self.file_changes.append(file_change)
                progress.advance(task)
        
        if not self.file_changes:
            console.print("✅ No changes needed!")
            return 0
        
        # Show summary
        console.print(self.generate_summary_table())
        
        total_files = len(self.file_changes)
        total_changes = sum(fc.total_changes for fc in self.file_changes)
        
        console.print(f"\n📊 Summary: {total_changes} changes across {total_files} files")
        
        # Confirm changes in non-dry-run mode
        if not self.dry_run and not self.force:
            if not Confirm.ask("Apply these changes?"):
                console.print("❌ Operation cancelled")
                return 1
        
        # Apply changes
        if not self.dry_run:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                task = progress.add_task("Applying changes...", total=len(self.file_changes))
                
                success_count = 0
                for file_change in self.file_changes:
                    if self.apply_changes(file_change):
                        success_count += 1
                    progress.advance(task)
            
            console.print(f"✅ Successfully updated {success_count}/{total_files} files")
            
            if self.backup:
                console.print("💾 Backup files created with .backup extension")
        else:
            console.print("🔍 Dry run complete - use without --dry-run to apply changes")
        
        return 0

@app.command()
def main(
    dry_run: bool = typer.Option(
        False, 
        "--dry-run", 
        help="Preview changes without modifying files"
    ),
    backup: bool = typer.Option(
        False, 
        "--backup", 
        help="Create backup files before modification"
    ),
    force: bool = typer.Option(
        False,
        "--force",
        help="Skip confirmation prompt"
    ),
    root_dir: Optional[str] = typer.Option(
        None,
        "--root-dir",
        help="Root directory to search (defaults to current directory)"
    )
) -> None:
    """Replace Firecrawl MCP tools with FreeCrawl equivalents across the codebase."""
    
    # Determine root directory
    if root_dir:
        root_path = Path(root_dir).resolve()
    else:
        root_path = Path.cwd()
    
    if not root_path.exists():
        console.print(f"❌ Directory does not exist: {root_path}", style="red")
        raise typer.Exit(1)
    
    # Validate we're in the right place
    if not (root_path / ".claude").exists():
        console.print(
            f"⚠️  Warning: No .claude directory found in {root_path}\n"
            "This might not be a Claude Code project directory.",
            style="yellow"
        )
        if not Confirm.ask("Continue anyway?"):
            raise typer.Exit(1)
    
    try:
        replacer = FirecrawlReplacer(root_path, dry_run=dry_run, backup=backup, force=force)
        exit_code = replacer.run()
        sys.exit(exit_code)
        
    except KeyboardInterrupt:
        console.print("\n❌ Operation cancelled by user", style="red")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"❌ Error: {e}", style="red")
        logger.exception("Unexpected error occurred")
        raise typer.Exit(1)

if __name__ == "__main__":
    app()