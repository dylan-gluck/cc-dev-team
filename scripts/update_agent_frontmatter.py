#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "pyyaml>=6.0",
#     "rich>=13.0",
# ]
# ///
"""
Update agent definition frontmatter names to match filenames.

This script finds all .md files in .claude/agents/ and updates the 'name:' field
in their YAML frontmatter to match their filename (without .md extension).

Usage:
    python update_agent_frontmatter.py
    # or if executable:
    ./update_agent_frontmatter.py
"""

import sys
import logging
from pathlib import Path
from typing import List, Tuple, Optional
import re

import yaml
from rich.console import Console
from rich.progress import Progress, TaskID
from rich.table import Table
from rich import print as rprint

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

console = Console()


def extract_frontmatter(content: str) -> Tuple[Optional[dict], str, str]:
    """
    Extract YAML frontmatter from markdown content.
    
    Returns:
        tuple: (frontmatter_dict, frontmatter_text, body_content)
    """
    # Match frontmatter pattern: --- at start, content, --- (with optional newlines)
    pattern = r'^---\s*\n(.*?)\n---\s*\n(.*)'
    match = re.match(pattern, content, re.DOTALL)
    
    if not match:
        return None, "", content
    
    frontmatter_text = match.group(1)
    body_content = match.group(2)
    
    try:
        frontmatter_dict = yaml.safe_load(frontmatter_text)
        return frontmatter_dict, frontmatter_text, body_content
    except yaml.YAMLError as e:
        logger.warning(f"Failed to parse YAML frontmatter: {e}")
        return None, frontmatter_text, body_content


def update_frontmatter_name(frontmatter_dict: dict, new_name: str) -> dict:
    """Update the name field in frontmatter dictionary."""
    updated = frontmatter_dict.copy()
    updated['name'] = new_name
    return updated


def serialize_frontmatter(frontmatter_dict: dict) -> str:
    """Serialize frontmatter dictionary back to YAML string."""
    return yaml.dump(frontmatter_dict, default_flow_style=False, sort_keys=False).strip()


def process_agent_file(file_path: Path) -> Tuple[bool, str]:
    """
    Process a single agent file and update its frontmatter.
    
    Returns:
        tuple: (was_changed, status_message)
    """
    try:
        # Extract expected name from filename
        expected_name = file_path.stem  # filename without .md extension
        
        # Read file content
        content = file_path.read_text(encoding='utf-8')
        
        # Extract frontmatter
        frontmatter_dict, frontmatter_text, body_content = extract_frontmatter(content)
        
        if frontmatter_dict is None:
            return False, f"No valid frontmatter found"
        
        # Check current name
        current_name = frontmatter_dict.get('name')
        if current_name == expected_name:
            return False, f"Name already matches: {current_name}"
        
        # Update frontmatter
        updated_frontmatter = update_frontmatter_name(frontmatter_dict, expected_name)
        
        # Serialize updated frontmatter
        new_frontmatter_text = serialize_frontmatter(updated_frontmatter)
        
        # Reconstruct file content
        new_content = f"---\n{new_frontmatter_text}\n---\n{body_content}"
        
        # Write back to file
        file_path.write_text(new_content, encoding='utf-8')
        
        return True, f"Updated: {current_name} → {expected_name}"
        
    except Exception as e:
        logger.error(f"Error processing {file_path}: {e}")
        return False, f"Error: {str(e)}"


def find_agent_files() -> List[Path]:
    """Find all agent definition files in .claude/agents/."""
    agents_dir = Path(".claude/agents")
    
    if not agents_dir.exists():
        raise FileNotFoundError(f"Directory not found: {agents_dir}")
    
    if not agents_dir.is_dir():
        raise NotADirectoryError(f"Not a directory: {agents_dir}")
    
    # Find all .md files
    agent_files = list(agents_dir.glob("*.md"))
    
    if not agent_files:
        raise FileNotFoundError(f"No .md files found in {agents_dir}")
    
    return sorted(agent_files)


def main() -> int:
    """Main execution function."""
    try:
        console.print("\n[bold blue]Agent Frontmatter Updater[/bold blue]")
        console.print("Updating name fields to match filenames...\n")
        
        # Find agent files
        agent_files = find_agent_files()
        console.print(f"Found {len(agent_files)} agent files to process\n")
        
        # Process files with progress tracking
        results = []
        changed_count = 0
        
        with Progress() as progress:
            task = progress.add_task("Processing files...", total=len(agent_files))
            
            for file_path in agent_files:
                was_changed, message = process_agent_file(file_path)
                results.append((file_path.name, was_changed, message))
                
                if was_changed:
                    changed_count += 1
                
                progress.update(task, advance=1)
        
        # Display results in a table
        table = Table(title="Processing Results")
        table.add_column("File", style="cyan")
        table.add_column("Status", style="green")
        table.add_column("Details", style="yellow")
        
        for filename, was_changed, message in results:
            status = "✅ Changed" if was_changed else "ℹ️  Skipped"
            table.add_row(filename, status, message)
        
        console.print(table)
        
        # Summary
        console.print(f"\n[bold green]Summary:[/bold green]")
        console.print(f"  Files processed: {len(agent_files)}")
        console.print(f"  Files changed: {changed_count}")
        console.print(f"  Files skipped: {len(agent_files) - changed_count}")
        
        if changed_count > 0:
            console.print(f"\n[bold yellow]✨ Successfully updated {changed_count} agent files![/bold yellow]")
        else:
            console.print(f"\n[bold blue]ℹ️  All agent files already have correct names.[/bold blue]")
        
        return 0
        
    except FileNotFoundError as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        return 1
    except Exception as e:
        logger.error(f"Script failed: {e}")
        console.print(f"[bold red]Error:[/bold red] {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())