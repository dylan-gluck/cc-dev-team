#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "click>=8.1",
#     "rich>=13.0",
#     "filelock>=3.12",
# ]
# ///
"""
Message Bus for Inter-Agent Communication.

A file-based message queue system for agents to communicate asynchronously.
Supports priority handling, message consumption/peeking, and broadcasting.

Usage:
    ./message_bus.py send <from_agent> <to_agent> <message_type> <payload> [--priority=normal]
    ./message_bus.py receive <agent_id> [--consume/--peek] [--format=table]
    ./message_bus.py broadcast <from_agent> <message_type> <payload> [--priority=normal]
    ./message_bus.py queue-status <agent_id>
"""

import json
import sys
import uuid
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import logging

import click
from rich.console import Console
from rich.table import Table
from rich.json import JSON
from filelock import FileLock

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize console for rich output
console = Console()

# Message queue directory
QUEUE_DIR = Path(".claude/messages")
LOCK_FILE = QUEUE_DIR / ".lock"


def ensure_queue_directory() -> None:
    """Ensure the message queue directory exists."""
    QUEUE_DIR.mkdir(parents=True, exist_ok=True)


def get_priority_weight(priority: str) -> int:
    """Convert priority string to numeric weight for sorting."""
    priority_map = {
        'critical': 0,
        'high': 1,
        'normal': 2,
        'low': 3
    }
    return priority_map.get(priority, 999)


def create_message(
    from_agent: str,
    to_agent: str,
    message_type: str,
    payload: str,
    priority: str = 'normal'
) -> Dict[str, Any]:
    """Create a structured message."""
    # Parse payload as JSON if it looks like JSON
    try:
        if payload.startswith('{') or payload.startswith('['):
            parsed_payload = json.loads(payload)
        else:
            parsed_payload = payload
    except json.JSONDecodeError:
        parsed_payload = payload
    
    return {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.now().isoformat(),
        "from": from_agent,
        "to": to_agent,
        "type": message_type,
        "payload": parsed_payload,
        "priority": priority
    }


def notify_agent(agent_id: str, message: Dict[str, Any]) -> None:
    """Notify agent of high-priority message."""
    console.print(
        f"[bold red]⚠️  High priority message for {agent_id}![/bold red]\n"
        f"  From: {message['from']}\n"
        f"  Type: {message['type']}\n"
        f"  Priority: {message['priority']}"
    )


@click.group()
def cli():
    """Message bus for inter-agent communication."""
    ensure_queue_directory()


@cli.command()
@click.argument('from_agent')
@click.argument('to_agent')
@click.argument('message_type')
@click.argument('payload')
@click.option(
    '--priority',
    type=click.Choice(['low', 'normal', 'high', 'critical']),
    default='normal',
    help='Message priority level'
)
def send(from_agent: str, to_agent: str, message_type: str, payload: str, priority: str):
    """Send message to a specific agent."""
    try:
        message = create_message(from_agent, to_agent, message_type, payload, priority)
        
        # Write message to queue with file locking
        msg_file = QUEUE_DIR / f"{to_agent}_{message['id']}.json"
        
        with FileLock(str(LOCK_FILE)):
            msg_file.write_text(json.dumps(message, indent=2))
        
        console.print(
            f"[green]✓[/green] Message sent successfully\n"
            f"  [cyan]From:[/cyan] {from_agent}\n"
            f"  [cyan]To:[/cyan] {to_agent}\n"
            f"  [cyan]Type:[/cyan] {message_type}\n"
            f"  [cyan]Priority:[/cyan] {priority}\n"
            f"  [dim]ID: {message['id']}[/dim]"
        )
        
        # Trigger notification for high priority messages
        if priority in ['high', 'critical']:
            notify_agent(to_agent, message)
        
        return 0
        
    except Exception as e:
        console.print(f"[red]✗[/red] Failed to send message: {e}")
        logger.error(f"Send failed: {e}")
        return 1


@cli.command()
@click.argument('agent_id')
@click.option(
    '--consume/--peek',
    default=True,
    help='Consume messages (delete after reading) or just peek'
)
@click.option(
    '--format',
    type=click.Choice(['json', 'table']),
    default='table',
    help='Output format'
)
@click.option(
    '--priority',
    type=click.Choice(['low', 'normal', 'high', 'critical', 'all']),
    default='all',
    help='Filter by priority level'
)
def receive(agent_id: str, consume: bool, format: str, priority: str):
    """Receive messages for an agent."""
    try:
        pattern = f"{agent_id}_*.json"
        messages = []
        
        with FileLock(str(LOCK_FILE)):
            for msg_file in sorted(QUEUE_DIR.glob(pattern)):
                try:
                    message = json.loads(msg_file.read_text())
                    
                    # Filter by priority if specified
                    if priority != 'all' and message.get('priority') != priority:
                        continue
                    
                    messages.append(message)
                    
                    if consume:
                        msg_file.unlink()
                        
                except (json.JSONDecodeError, IOError) as e:
                    logger.error(f"Error reading message {msg_file}: {e}")
                    continue
        
        # Sort by priority (critical first) then by timestamp
        messages.sort(
            key=lambda m: (
                get_priority_weight(m.get('priority', 'normal')),
                m.get('timestamp', '')
            )
        )
        
        if not messages:
            console.print(f"[yellow]No messages for {agent_id}[/yellow]")
            return 0
        
        # Display messages
        if format == 'table':
            table = Table(
                title=f"Messages for {agent_id} ({'consumed' if consume else 'peeked'})",
                show_lines=True
            )
            table.add_column("From", style="cyan", no_wrap=True)
            table.add_column("Type", style="yellow")
            table.add_column("Priority", style="magenta")
            table.add_column("Time", style="dim")
            table.add_column("Payload", style="green", overflow="fold")
            
            for msg in messages:
                # Format timestamp
                timestamp = datetime.fromisoformat(msg['timestamp'])
                time_str = timestamp.strftime("%H:%M:%S")
                
                # Format payload
                if isinstance(msg['payload'], (dict, list)):
                    payload_str = json.dumps(msg['payload'], indent=2)
                else:
                    payload_str = str(msg['payload'])
                
                # Color priority
                priority_str = msg['priority']
                if msg['priority'] == 'critical':
                    priority_str = f"[bold red]{priority_str}[/bold red]"
                elif msg['priority'] == 'high':
                    priority_str = f"[red]{priority_str}[/red]"
                
                table.add_row(
                    msg['from'],
                    msg['type'],
                    priority_str,
                    time_str,
                    payload_str
                )
            
            console.print(table)
            console.print(f"\n[dim]Total: {len(messages)} message(s)[/dim]")
        else:
            # JSON output
            console.print(JSON.from_data(messages))
        
        return 0
        
    except Exception as e:
        console.print(f"[red]✗[/red] Failed to receive messages: {e}")
        logger.error(f"Receive failed: {e}")
        return 1


@cli.command()
@click.argument('from_agent')
@click.argument('message_type')
@click.argument('payload')
@click.option(
    '--priority',
    type=click.Choice(['low', 'normal', 'high', 'critical']),
    default='normal',
    help='Message priority level'
)
@click.option(
    '--exclude',
    multiple=True,
    help='Agents to exclude from broadcast'
)
def broadcast(from_agent: str, message_type: str, payload: str, priority: str, exclude: tuple):
    """Broadcast message to all active agents."""
    try:
        # Try to get active agents from state manager
        state_script = Path(".claude/scripts/state_manager.py")
        active_agents = []
        
        if state_script.exists():
            result = subprocess.run(
                [sys.executable, str(state_script), 'get', 'agents.active'],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0 and result.stdout.strip():
                try:
                    agents_data = json.loads(result.stdout)
                    if isinstance(agents_data, dict):
                        active_agents = list(agents_data.keys())
                except json.JSONDecodeError:
                    logger.warning("Could not parse active agents from state manager")
        
        # If no active agents found, look for agent definitions
        if not active_agents:
            agents_dir = Path(".claude/agents")
            if agents_dir.exists():
                active_agents = [
                    f.stem for f in agents_dir.glob("*.md")
                    if not f.stem.startswith('_')
                ]
        
        if not active_agents:
            console.print("[yellow]⚠️  No active agents found for broadcast[/yellow]")
            return 0
        
        # Filter out sender and excluded agents
        exclude_set = set(exclude) | {from_agent}
        target_agents = [a for a in active_agents if a not in exclude_set]
        
        if not target_agents:
            console.print("[yellow]No agents to broadcast to after exclusions[/yellow]")
            return 0
        
        # Send to each agent
        success_count = 0
        failed_agents = []
        
        with FileLock(str(LOCK_FILE)):
            for agent_id in target_agents:
                try:
                    message = create_message(from_agent, agent_id, message_type, payload, priority)
                    msg_file = QUEUE_DIR / f"{agent_id}_{message['id']}.json"
                    msg_file.write_text(json.dumps(message, indent=2))
                    success_count += 1
                except Exception as e:
                    logger.error(f"Failed to send to {agent_id}: {e}")
                    failed_agents.append(agent_id)
        
        # Report results
        console.print(
            f"[green]✓[/green] Broadcast sent successfully\n"
            f"  [cyan]From:[/cyan] {from_agent}\n"
            f"  [cyan]Type:[/cyan] {message_type}\n"
            f"  [cyan]Priority:[/cyan] {priority}\n"
            f"  [cyan]Recipients:[/cyan] {success_count}/{len(target_agents)} agents"
        )
        
        if failed_agents:
            console.print(f"  [red]Failed:[/red] {', '.join(failed_agents)}")
        
        # Notify for high priority broadcasts
        if priority in ['high', 'critical']:
            console.print(f"\n[bold red]⚠️  High priority broadcast sent![/bold red]")
        
        return 0
        
    except Exception as e:
        console.print(f"[red]✗[/red] Broadcast failed: {e}")
        logger.error(f"Broadcast failed: {e}")
        return 1


@cli.command('queue-status')
@click.argument('agent_id', required=False)
@click.option(
    '--all',
    is_flag=True,
    help='Show status for all agents'
)
def queue_status(agent_id: Optional[str], all: bool):
    """Check message queue status for agent(s)."""
    try:
        if all or not agent_id:
            # Get all unique agent IDs from message files
            agent_messages = {}
            
            for msg_file in QUEUE_DIR.glob("*_*.json"):
                # Extract agent ID from filename
                agent = msg_file.stem.rsplit('_', 1)[0]
                if agent not in agent_messages:
                    agent_messages[agent] = []
                
                try:
                    message = json.loads(msg_file.read_text())
                    agent_messages[agent].append(message)
                except (json.JSONDecodeError, IOError):
                    continue
            
            if not agent_messages:
                console.print("[yellow]No messages in any queue[/yellow]")
                return 0
            
            # Display overall status
            table = Table(title="Message Queue Status", show_lines=True)
            table.add_column("Agent", style="cyan")
            table.add_column("Total", justify="right")
            table.add_column("Critical", justify="right", style="bold red")
            table.add_column("High", justify="right", style="red")
            table.add_column("Normal", justify="right", style="green")
            table.add_column("Low", justify="right", style="dim")
            
            for agent, messages in sorted(agent_messages.items()):
                priorities = {'critical': 0, 'high': 0, 'normal': 0, 'low': 0}
                for msg in messages:
                    priority = msg.get('priority', 'normal')
                    priorities[priority] = priorities.get(priority, 0) + 1
                
                table.add_row(
                    agent,
                    str(len(messages)),
                    str(priorities['critical']) if priorities['critical'] else "-",
                    str(priorities['high']) if priorities['high'] else "-",
                    str(priorities['normal']) if priorities['normal'] else "-",
                    str(priorities['low']) if priorities['low'] else "-"
                )
            
            console.print(table)
            
        else:
            # Show status for specific agent
            pattern = f"{agent_id}_*.json"
            messages = []
            
            for msg_file in QUEUE_DIR.glob(pattern):
                try:
                    message = json.loads(msg_file.read_text())
                    messages.append(message)
                except (json.JSONDecodeError, IOError):
                    continue
            
            console.print(f"\n[bold]Queue status for {agent_id}:[/bold]")
            console.print(f"  Total pending messages: {len(messages)}")
            
            if messages:
                # Count by priority
                priorities = {'critical': 0, 'high': 0, 'normal': 0, 'low': 0}
                types = {}
                senders = {}
                
                for msg in messages:
                    # Priority count
                    priority = msg.get('priority', 'normal')
                    priorities[priority] = priorities.get(priority, 0) + 1
                    
                    # Type count
                    msg_type = msg.get('type', 'unknown')
                    types[msg_type] = types.get(msg_type, 0) + 1
                    
                    # Sender count
                    sender = msg.get('from', 'unknown')
                    senders[sender] = senders.get(sender, 0) + 1
                
                # Display breakdown
                console.print("\n  [cyan]By Priority:[/cyan]")
                for priority in ['critical', 'high', 'normal', 'low']:
                    if priorities[priority] > 0:
                        if priority == 'critical':
                            console.print(f"    [bold red]{priority}:[/bold red] {priorities[priority]}")
                        elif priority == 'high':
                            console.print(f"    [red]{priority}:[/red] {priorities[priority]}")
                        else:
                            console.print(f"    {priority}: {priorities[priority]}")
                
                console.print("\n  [cyan]By Type:[/cyan]")
                for msg_type, count in sorted(types.items()):
                    console.print(f"    {msg_type}: {count}")
                
                console.print("\n  [cyan]By Sender:[/cyan]")
                for sender, count in sorted(senders.items()):
                    console.print(f"    {sender}: {count}")
                
                # Show oldest and newest message times
                messages.sort(key=lambda m: m.get('timestamp', ''))
                if messages:
                    oldest = datetime.fromisoformat(messages[0]['timestamp'])
                    newest = datetime.fromisoformat(messages[-1]['timestamp'])
                    console.print(f"\n  [dim]Oldest: {oldest.strftime('%Y-%m-%d %H:%M:%S')}[/dim]")
                    console.print(f"  [dim]Newest: {newest.strftime('%Y-%m-%d %H:%M:%S')}[/dim]")
            else:
                console.print("  [green]Queue is empty[/green]")
        
        return 0
        
    except Exception as e:
        console.print(f"[red]✗[/red] Failed to check queue status: {e}")
        logger.error(f"Queue status failed: {e}")
        return 1


def main() -> int:
    """Main entry point."""
    try:
        return cli()
    except Exception as e:
        console.print(f"[red]✗[/red] Unexpected error: {e}")
        logger.error(f"Unexpected error: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())