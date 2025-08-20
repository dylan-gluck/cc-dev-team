#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "click>=8.1",
#     "rich>=13.0",
#     "python-dateutil>=2.8",
# ]
# ///
"""
Event Stream System for Claude Code orchestration.

This script provides a simple append-only event log in JSONL format for tracking
orchestration events, agent communications, and system state changes.

Usage:
    # Emit an event
    ./event_stream.py emit --type task_start --source orchestrator --data '{"task": "build", "id": "123"}'
    
    # Stream all events
    ./event_stream.py stream
    
    # Stream with follow mode (like tail -f)
    ./event_stream.py stream --follow
    
    # Stream last N events
    ./event_stream.py stream --tail 10
"""

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional, Iterator
import logging

import click
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.layout import Layout
from rich.panel import Panel
from rich.syntax import Syntax
from rich.text import Text

# Configure logging
logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Rich console
console = Console()

# Event log file path
EVENT_LOG_DIR = Path(".claude/events")
EVENT_LOG_FILE = EVENT_LOG_DIR / "stream.jsonl"


class EventStream:
    """Manages the event stream operations."""
    
    def __init__(self, log_file: Path = EVENT_LOG_FILE):
        """Initialize the event stream.
        
        Args:
            log_file: Path to the JSONL event log file
        """
        self.log_file = log_file
        self._ensure_log_exists()
    
    def _ensure_log_exists(self) -> None:
        """Ensure the event log directory and file exist."""
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        if not self.log_file.exists():
            self.log_file.touch()
            logger.info(f"Created event log at {self.log_file}")
    
    def emit(self, event_type: str, source: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Emit a new event to the stream.
        
        Args:
            event_type: Type of event (e.g., task_start, agent_response)
            source: Source of the event (e.g., orchestrator, agent name)
            data: Event data as a dictionary
            
        Returns:
            The complete event object that was written
        """
        event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "type": event_type,
            "source": source,
            "data": data
        }
        
        # Append to JSONL file (one JSON object per line)
        with self.log_file.open("a", encoding="utf-8") as f:
            json.dump(event, f, ensure_ascii=False, separators=(",", ":"))
            f.write("\n")
        
        logger.info(f"Emitted event: {event_type} from {source}")
        return event
    
    def read_events(self, tail: Optional[int] = None) -> list[Dict[str, Any]]:
        """Read events from the log file.
        
        Args:
            tail: If specified, return only the last N events
            
        Returns:
            List of event dictionaries
        """
        if not self.log_file.exists():
            return []
        
        events = []
        with self.log_file.open("r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    try:
                        events.append(json.loads(line))
                    except json.JSONDecodeError as e:
                        logger.warning(f"Skipping malformed line: {e}")
        
        if tail and tail > 0:
            return events[-tail:]
        return events
    
    def stream_events(self, follow: bool = False, tail: Optional[int] = None) -> Iterator[Dict[str, Any]]:
        """Stream events from the log file.
        
        Args:
            follow: If True, continue streaming new events as they arrive
            tail: If specified, start with the last N events
            
        Yields:
            Event dictionaries as they are read
        """
        # First, yield existing events
        events = self.read_events(tail=tail)
        for event in events:
            yield event
        
        if not follow:
            return
        
        # Follow mode: watch for new events
        with self.log_file.open("r", encoding="utf-8") as f:
            # Move to end of file
            f.seek(0, 2)
            
            while True:
                line = f.readline()
                if line:
                    if line.strip():
                        try:
                            yield json.loads(line)
                        except json.JSONDecodeError as e:
                            logger.warning(f"Skipping malformed line: {e}")
                else:
                    time.sleep(0.1)  # Small delay when no new data


def format_event_table(events: list[Dict[str, Any]]) -> Table:
    """Format events as a Rich table.
    
    Args:
        events: List of event dictionaries
        
    Returns:
        Rich Table object
    """
    table = Table(title="Event Stream", show_header=True, header_style="bold magenta")
    table.add_column("Timestamp", style="cyan", no_wrap=True)
    table.add_column("Type", style="green")
    table.add_column("Source", style="yellow")
    table.add_column("Data", style="white")
    
    for event in events:
        # Format timestamp for display
        try:
            dt = datetime.fromisoformat(event["timestamp"])
            timestamp_str = dt.strftime("%Y-%m-%d %H:%M:%S")
        except (KeyError, ValueError):
            timestamp_str = event.get("timestamp", "N/A")
        
        # Format data as JSON
        data_str = json.dumps(event.get("data", {}), indent=2)
        if len(data_str) > 100:
            data_str = data_str[:97] + "..."
        
        table.add_row(
            timestamp_str,
            event.get("type", "N/A"),
            event.get("source", "N/A"),
            data_str
        )
    
    return table


def format_event_detail(event: Dict[str, Any]) -> Panel:
    """Format a single event with full details.
    
    Args:
        event: Event dictionary
        
    Returns:
        Rich Panel object
    """
    # Format timestamp
    try:
        dt = datetime.fromisoformat(event["timestamp"])
        timestamp_str = dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3] + " UTC"
    except (KeyError, ValueError):
        timestamp_str = event.get("timestamp", "N/A")
    
    # Create content
    content = Text()
    content.append("Timestamp: ", style="bold cyan")
    content.append(timestamp_str + "\n")
    content.append("Type: ", style="bold green")
    content.append(event.get("type", "N/A") + "\n")
    content.append("Source: ", style="bold yellow")
    content.append(event.get("source", "N/A") + "\n\n")
    content.append("Data:\n", style="bold white")
    
    # Format data as syntax-highlighted JSON
    data_json = json.dumps(event.get("data", {}), indent=2, ensure_ascii=False)
    
    # Create panel with syntax highlighting for data
    data_syntax = Syntax(data_json, "json", theme="monokai", line_numbers=False)
    
    layout = Layout()
    layout.split_column(
        Layout(content, size=4),
        Layout(data_syntax)
    )
    
    return Panel(layout, title=f"[bold blue]Event: {event.get('type', 'Unknown')}[/bold blue]", border_style="blue")


@click.group()
@click.version_option(version="1.0.0", prog_name="event_stream")
def cli():
    """Event Stream System for Claude Code orchestration."""
    pass


@cli.command()
@click.option("--type", "-t", "event_type", required=True, help="Event type (e.g., task_start, agent_response)")
@click.option("--source", "-s", required=True, help="Event source (e.g., orchestrator, agent name)")
@click.option("--data", "-d", required=True, help="Event data as JSON string")
def emit(event_type: str, source: str, data: str):
    """Emit a new event to the stream."""
    try:
        # Parse data as JSON
        data_dict = json.loads(data)
    except json.JSONDecodeError as e:
        console.print(f"[red]Error: Invalid JSON data: {e}[/red]")
        sys.exit(1)
    
    # Create event stream and emit event
    stream = EventStream()
    event = stream.emit(event_type, source, data_dict)
    
    # Display the emitted event
    console.print(format_event_detail(event))
    console.print("[green]✓ Event emitted successfully[/green]")


@cli.command()
@click.option("--follow", "-f", is_flag=True, help="Follow mode - stream new events as they arrive")
@click.option("--tail", "-n", type=int, help="Show only the last N events")
@click.option("--detailed", "-v", is_flag=True, help="Show detailed view of each event")
def stream(follow: bool, tail: Optional[int], detailed: bool):
    """Stream events from the log."""
    stream_obj = EventStream()
    
    if follow:
        console.print("[cyan]Streaming events (Ctrl+C to stop)...[/cyan]\n")
        
        try:
            for event in stream_obj.stream_events(follow=True, tail=tail):
                if detailed:
                    console.print(format_event_detail(event))
                    console.print()
                else:
                    # Simple one-line format for follow mode
                    try:
                        dt = datetime.fromisoformat(event["timestamp"])
                        timestamp_str = dt.strftime("%H:%M:%S")
                    except (KeyError, ValueError):
                        timestamp_str = "N/A"
                    
                    data_preview = json.dumps(event.get("data", {}))
                    if len(data_preview) > 50:
                        data_preview = data_preview[:47] + "..."
                    
                    console.print(
                        f"[cyan]{timestamp_str}[/cyan] "
                        f"[green]{event.get('type', 'N/A')}[/green] "
                        f"[yellow]{event.get('source', 'N/A')}[/yellow] "
                        f"{data_preview}"
                    )
        except KeyboardInterrupt:
            console.print("\n[yellow]Stream interrupted[/yellow]")
    else:
        # Static display of events
        events = stream_obj.read_events(tail=tail)
        
        if not events:
            console.print("[yellow]No events found[/yellow]")
            return
        
        if detailed:
            for event in events:
                console.print(format_event_detail(event))
                console.print()
        else:
            table = format_event_table(events)
            console.print(table)


@cli.command()
def clear():
    """Clear all events from the log (use with caution)."""
    if click.confirm("Are you sure you want to clear all events?"):
        stream = EventStream()
        
        # Backup existing events
        events = stream.read_events()
        if events:
            backup_file = stream.log_file.with_suffix(".jsonl.bak")
            with backup_file.open("w", encoding="utf-8") as f:
                for event in events:
                    json.dump(event, f, ensure_ascii=False)
                    f.write("\n")
            console.print(f"[yellow]Backed up {len(events)} events to {backup_file}[/yellow]")
        
        # Clear the log
        stream.log_file.write_text("")
        console.print("[green]✓ Event log cleared[/green]")
    else:
        console.print("[yellow]Clear operation cancelled[/yellow]")


@cli.command()
def stats():
    """Show statistics about the event stream."""
    stream = EventStream()
    events = stream.read_events()
    
    if not events:
        console.print("[yellow]No events found[/yellow]")
        return
    
    # Calculate statistics
    event_types = {}
    event_sources = {}
    
    for event in events:
        # Count by type
        evt_type = event.get("type", "unknown")
        event_types[evt_type] = event_types.get(evt_type, 0) + 1
        
        # Count by source
        evt_source = event.get("source", "unknown")
        event_sources[evt_source] = event_sources.get(evt_source, 0) + 1
    
    # Get time range
    try:
        first_time = datetime.fromisoformat(events[0]["timestamp"])
        last_time = datetime.fromisoformat(events[-1]["timestamp"])
        duration = last_time - first_time
    except (KeyError, ValueError):
        first_time = last_time = None
        duration = None
    
    # Create statistics table
    stats_table = Table(title="Event Stream Statistics", show_header=True, header_style="bold magenta")
    stats_table.add_column("Metric", style="cyan")
    stats_table.add_column("Value", style="white")
    
    stats_table.add_row("Total Events", str(len(events)))
    stats_table.add_row("Unique Event Types", str(len(event_types)))
    stats_table.add_row("Unique Sources", str(len(event_sources)))
    
    if first_time and last_time:
        stats_table.add_row("First Event", first_time.strftime("%Y-%m-%d %H:%M:%S"))
        stats_table.add_row("Last Event", last_time.strftime("%Y-%m-%d %H:%M:%S"))
        stats_table.add_row("Time Span", str(duration))
    
    console.print(stats_table)
    console.print()
    
    # Event types breakdown
    types_table = Table(title="Events by Type", show_header=True, header_style="bold green")
    types_table.add_column("Type", style="green")
    types_table.add_column("Count", style="white")
    types_table.add_column("Percentage", style="cyan")
    
    for evt_type, count in sorted(event_types.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / len(events)) * 100
        types_table.add_row(evt_type, str(count), f"{percentage:.1f}%")
    
    console.print(types_table)
    console.print()
    
    # Sources breakdown
    sources_table = Table(title="Events by Source", show_header=True, header_style="bold yellow")
    sources_table.add_column("Source", style="yellow")
    sources_table.add_column("Count", style="white")
    sources_table.add_column("Percentage", style="cyan")
    
    for source, count in sorted(event_sources.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / len(events)) * 100
        sources_table.add_row(source, str(count), f"{percentage:.1f}%")
    
    console.print(sources_table)


def main() -> int:
    """Main entry point."""
    try:
        cli()
        return 0
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        logger.exception("Unhandled exception")
        return 1


if __name__ == "__main__":
    sys.exit(main())