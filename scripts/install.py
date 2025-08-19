#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "rich>=13.0",
# ]
# ///
"""
Claude Code Development Team Scaffolding Installer

This script copies the entire development team scaffolding directory structure
to a specified target path for setting up Claude Code configuration in new projects.

Features:
- Copy entire directory structure with preserved permissions
- Skip build artifacts and version control files
- Colored terminal output with progress indicators
- Dry-run mode for previewing changes
- Force mode for overwriting existing files
- Comprehensive error handling and validation

Usage:
    uv run scripts/install.py /path/to/project
    uv run scripts/install.py --dry-run /path/to/project
    uv run scripts/install.py --force /path/to/project
    uv run scripts/install.py --help
"""

import argparse
import os
import shutil
import sys
from pathlib import Path
from typing import List, Set, Tuple

from rich.console import Console
from rich.progress import Progress, TaskID
from rich.panel import Panel
from rich.table import Table
from rich import print as rprint

# Configure rich console
console = Console()

# Files and directories to skip during copy
SKIP_PATTERNS = {
    '.git',
    '__pycache__',
    '*.pyc',
    '*.pyo',
    '*.pyd',
    '.pytest_cache',
    '.coverage',
    '.tox',
    '.venv',
    'venv',
    '.env',
    'node_modules',
    '.DS_Store',
    '.ropeproject',
    'logs',
    'output'
}

# Extensions to skip
SKIP_EXTENSIONS = {'.pyc', '.pyo', '.pyd', '.so', '.dylib', '.dll'}


def should_skip_path(path: Path) -> bool:
    """Check if a path should be skipped during copy operation."""
    # Check if any part of the path matches skip patterns
    for part in path.parts:
        if part in SKIP_PATTERNS:
            return True
        if part.startswith('.') and part not in {'.claude', '.github', '.env.sample', '.mcp.json'}:
            return True

    # Check file extension
    if path.suffix in SKIP_EXTENSIONS:
        return True

    # Skip any file matching patterns
    name = path.name
    for pattern in SKIP_PATTERNS:
        if '*' in pattern:
            if pattern.replace('*', '') in name:
                return True
        elif name == pattern:
            return True

    return False


def get_files_to_copy(source_dir: Path) -> List[Tuple[Path, Path]]:
    """Get list of (source, relative_path) tuples for files to copy."""
    files_to_copy = []

    for root, dirs, files in os.walk(source_dir):
        root_path = Path(root)

        # Filter directories in-place to skip unwanted ones
        dirs[:] = [d for d in dirs if not should_skip_path(root_path / d)]

        for file in files:
            file_path = root_path / file
            if not should_skip_path(file_path):
                relative_path = file_path.relative_to(source_dir)
                files_to_copy.append((file_path, relative_path))

    return files_to_copy


def check_conflicts(target_dir: Path, files_to_copy: List[Tuple[Path, Path]]) -> List[Path]:
    """Check for existing files that would be overwritten."""
    conflicts = []

    for _, relative_path in files_to_copy:
        target_path = target_dir / relative_path
        if target_path.exists():
            conflicts.append(target_path)

    return conflicts


def copy_files(
    source_dir: Path,
    target_dir: Path,
    files_to_copy: List[Tuple[Path, Path]],
    dry_run: bool = False
) -> Tuple[int, int]:
    """Copy files from source to target directory."""
    copied_files = 0
    created_dirs = 0
    created_dir_set: Set[Path] = set()

    with Progress() as progress:
        task = progress.add_task("[green]Copying files...", total=len(files_to_copy))

        for source_path, relative_path in files_to_copy:
            target_path = target_dir / relative_path

            # Create parent directories if needed
            parent_dir = target_path.parent
            if parent_dir not in created_dir_set and not parent_dir.exists():
                if not dry_run:
                    parent_dir.mkdir(parents=True, exist_ok=True)
                created_dir_set.add(parent_dir)
                created_dirs += 1

            # Copy file
            if not dry_run:
                shutil.copy2(source_path, target_path)
                # Preserve permissions
                shutil.copystat(source_path, target_path)

            copied_files += 1
            progress.update(task, advance=1)

    return copied_files, created_dirs


def display_summary(
    source_dir: Path,
    target_dir: Path,
    files_to_copy: List[Tuple[Path, Path]],
    copied_files: int,
    created_dirs: int,
    dry_run: bool
):
    """Display operation summary."""
    table = Table(title="Installation Summary")
    table.add_column("Item", style="cyan")
    table.add_column("Count", style="green")

    table.add_row("Source Directory", str(source_dir))
    table.add_row("Target Directory", str(target_dir))
    table.add_row("Files to Copy", str(len(files_to_copy)))
    table.add_row("Directories Created", str(created_dirs))

    if dry_run:
        table.add_row("Mode", "[yellow]DRY RUN - No changes made[/yellow]")
    else:
        table.add_row("Files Copied", str(copied_files))
        table.add_row("Status", "[green]✓ Installation Complete[/green]")

    console.print(table)


def main() -> int:
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description="Install Claude Code development team scaffolding",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  uv run scripts/install.py /path/to/project
  uv run scripts/install.py --dry-run /path/to/project
  uv run scripts/install.py --force /path/to/project
  uv run scripts/install.py --help
        """
    )

    parser.add_argument(
        "target_path",
        nargs="?",
        help="Target directory path for installation"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be copied without making changes"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing files (default is to error on conflicts)"
    )

    # Parse arguments
    args = parser.parse_args()

    # Show help if no target path provided
    if not args.target_path:
        parser.print_help()
        return 0

    try:
        # Determine source directory (directory containing this script)
        script_dir = Path(__file__).parent
        source_dir = script_dir.parent  # Go up one level from scripts/

        # Validate source directory
        if not source_dir.exists():
            console.print(f"[red]✗ Source directory not found: {source_dir}[/red]")
            return 1

        if not (source_dir / ".claude").exists():
            console.print(f"[red]✗ Invalid source directory: .claude directory not found in {source_dir}[/red]")
            return 1

        # Process target path
        target_dir = Path(args.target_path).resolve()

        console.print(Panel.fit(
            f"[bold]Claude Code Development Team Scaffolding Installer[/bold]\n\n"
            f"Source: [cyan]{source_dir}[/cyan]\n"
            f"Target: [cyan]{target_dir}[/cyan]\n"
            f"Mode: [yellow]{'DRY RUN' if args.dry_run else 'INSTALL'}[/yellow]"
        ))

        # Create target directory if it doesn't exist
        if not target_dir.exists():
            if not args.dry_run:
                target_dir.mkdir(parents=True, exist_ok=True)
            console.print(f"[green]✓ Target directory will be created: {target_dir}[/green]")

        # Get files to copy
        console.print("[blue]Scanning source directory...[/blue]")
        files_to_copy = get_files_to_copy(source_dir)

        if not files_to_copy:
            console.print("[yellow]⚠ No files found to copy[/yellow]")
            return 0

        # Check for conflicts
        conflicts = check_conflicts(target_dir, files_to_copy)
        if conflicts and not args.force:
            console.print(f"[red]✗ Found {len(conflicts)} existing files that would be overwritten:[/red]")
            for conflict in conflicts[:10]:  # Show first 10 conflicts
                console.print(f"  [red]•[/red] {conflict}")
            if len(conflicts) > 10:
                console.print(f"  [red]... and {len(conflicts) - 10} more[/red]")
            console.print("\n[yellow]Use --force to overwrite existing files[/yellow]")
            return 1

        if conflicts and args.force:
            console.print(f"[yellow]⚠ Will overwrite {len(conflicts)} existing files (--force enabled)[/yellow]")

        # Perform copy operation
        copied_files, created_dirs = copy_files(source_dir, target_dir, files_to_copy, args.dry_run)

        # Display summary
        display_summary(source_dir, target_dir, files_to_copy, copied_files, created_dirs, args.dry_run)

        if not args.dry_run:
            console.print(f"\n[green]✓ Successfully installed Claude Code scaffolding to {target_dir}[/green]")
            console.print("\n[blue]Next steps:[/blue]")
            console.print("1. Navigate to your project directory")
            console.print("2. Review and customize .claude/agents/ configurations")
            console.print("3. Update .env.sample with your project-specific variables")
            console.print("4. Start using Claude Code with your development team!")

        return 0

    except KeyboardInterrupt:
        console.print("\n[yellow]Installation cancelled by user[/yellow]")
        return 130
    except PermissionError as e:
        console.print(f"[red]✗ Permission denied: {e}[/red]")
        return 1
    except OSError as e:
        console.print(f"[red]✗ File system error: {e}[/red]")
        return 1
    except Exception as e:
        console.print(f"[red]✗ Unexpected error: {e}[/red]")
        return 1


if __name__ == "__main__":
    sys.exit(main())
