#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "rich>=13.7",
#     "click>=8.1",
#     "httpx>=0.24",
#     "python-dateutil>=2.8",
#     "tabulate>=0.9",
# ]
# ///
"""
Observability Dashboard for Claude Code Development Team

This script provides comprehensive monitoring and status tracking for the development team,
including agent status, task overview, sprint details, and system metrics.

Usage:
    ./observability.py status [--format=table|json|summary] [--agent=NAME]
    ./observability.py sprint [--current|--all] [--format=table|json]
    ./observability.py monitor [--interval=5] [--metrics=cpu,memory,tasks]
    ./observability.py metrics [--type=performance|quality|productivity]
"""

import sys
import json
import time
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple
from dataclasses import dataclass, field, asdict
from enum import Enum
import random  # For demo data generation

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.live import Live
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.columns import Columns
from rich.text import Text
from rich.align import Align
from rich.box import ROUNDED, DOUBLE
from rich import print as rprint
from dateutil import parser as date_parser
from tabulate import tabulate

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Rich console
console = Console()


# Data Models
class AgentStatus(Enum):
    """Agent status enumeration"""
    IDLE = "idle"
    ACTIVE = "active"
    BUSY = "busy"
    ERROR = "error"
    OFFLINE = "offline"


class TaskStatus(Enum):
    """Task status enumeration"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"


class TaskPriority(Enum):
    """Task priority levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class Agent:
    """Agent data model"""
    name: str
    team: str
    status: AgentStatus
    current_task: Optional[str] = None
    tasks_completed: int = 0
    tasks_failed: int = 0
    last_active: Optional[datetime] = None
    performance_score: float = 0.0
    specialization: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "name": self.name,
            "team": self.team,
            "status": self.status.value,
            "current_task": self.current_task,
            "tasks_completed": self.tasks_completed,
            "tasks_failed": self.tasks_failed,
            "last_active": self.last_active.isoformat() if self.last_active else None,
            "performance_score": self.performance_score,
            "specialization": self.specialization
        }


@dataclass
class Task:
    """Task data model"""
    id: str
    title: str
    description: str
    status: TaskStatus
    priority: TaskPriority
    assigned_to: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    estimated_hours: float = 0.0
    actual_hours: float = 0.0
    dependencies: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status.value,
            "priority": self.priority.value,
            "assigned_to": self.assigned_to,
            "created_at": self.created_at.isoformat(),
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "estimated_hours": self.estimated_hours,
            "actual_hours": self.actual_hours,
            "dependencies": self.dependencies,
            "tags": self.tags
        }


@dataclass
class Sprint:
    """Sprint data model"""
    id: str
    name: str
    start_date: datetime
    end_date: datetime
    goals: List[str]
    tasks: List[str]
    velocity: float = 0.0
    burndown_rate: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "goals": self.goals,
            "tasks": self.tasks,
            "velocity": self.velocity,
            "burndown_rate": self.burndown_rate
        }


@dataclass
class SystemMetrics:
    """System metrics data model"""
    timestamp: datetime
    cpu_usage: float
    memory_usage: float
    active_agents: int
    tasks_in_progress: int
    tasks_completed_today: int
    average_task_time: float
    error_rate: float
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "timestamp": self.timestamp.isoformat(),
            "cpu_usage": self.cpu_usage,
            "memory_usage": self.memory_usage,
            "active_agents": self.active_agents,
            "tasks_in_progress": self.tasks_in_progress,
            "tasks_completed_today": self.tasks_completed_today,
            "average_task_time": self.average_task_time,
            "error_rate": self.error_rate
        }


class StateManager:
    """Manages state and data for the observability system"""
    
    def __init__(self):
        self.base_path = Path.home() / ".claude" / "orchestration" / "state"
        self.base_path.mkdir(parents=True, exist_ok=True)
        self.agents: Dict[str, Agent] = {}
        self.tasks: Dict[str, Task] = {}
        self.sprints: Dict[str, Sprint] = {}
        self.metrics: List[SystemMetrics] = []
        self._load_or_generate_data()
    
    def _load_or_generate_data(self):
        """Load existing data or generate demo data"""
        # For now, generate demo data
        self._generate_demo_agents()
        self._generate_demo_tasks()
        self._generate_demo_sprints()
        self._generate_demo_metrics()
    
    def _generate_demo_agents(self):
        """Generate demo agent data"""
        teams = {
            "engineering": ["fullstack", "api", "ux", "lead"],
            "qa": ["director", "analyst", "e2e", "scripts"],
            "devops": ["manager", "cicd", "infrastructure", "release"],
            "product": ["director", "manager", "analyst"],
            "research": ["ai", "deep"],
            "creative": ["director", "copywriter", "illustrator"],
            "data": ["scientist", "analytics"],
            "meta": ["agent", "summary", "readme", "commit"]
        }
        
        for team, members in teams.items():
            for member in members:
                agent_name = f"{team}-{member}"
                status = random.choice(list(AgentStatus))
                agent = Agent(
                    name=agent_name,
                    team=team,
                    status=status,
                    current_task=f"Task-{random.randint(100, 999)}" if status == AgentStatus.ACTIVE else None,
                    tasks_completed=random.randint(0, 50),
                    tasks_failed=random.randint(0, 5),
                    last_active=datetime.now() - timedelta(minutes=random.randint(0, 120)),
                    performance_score=random.uniform(0.7, 1.0),
                    specialization=member
                )
                self.agents[agent_name] = agent
    
    def _generate_demo_tasks(self):
        """Generate demo task data"""
        task_templates = [
            ("Implement authentication system", "Add OAuth2 authentication", ["security", "backend"]),
            ("Create dashboard UI", "Design and implement admin dashboard", ["frontend", "ux"]),
            ("Optimize database queries", "Improve query performance", ["backend", "performance"]),
            ("Write unit tests", "Add test coverage for core modules", ["testing", "quality"]),
            ("Deploy to production", "Release v2.1.0 to production", ["devops", "release"]),
            ("Code review", "Review pull requests", ["quality", "collaboration"]),
            ("Fix bug in payment flow", "Critical bug affecting payments", ["bug", "critical"]),
            ("Update documentation", "Update API documentation", ["docs", "maintenance"]),
            ("Refactor legacy code", "Clean up technical debt", ["refactoring", "maintenance"]),
            ("Performance monitoring", "Set up APM monitoring", ["monitoring", "devops"])
        ]
        
        for i, (title, desc, tags) in enumerate(task_templates * 3):  # Generate 30 tasks
            task_id = f"TASK-{1000 + i}"
            status = random.choice(list(TaskStatus))
            priority = random.choice(list(TaskPriority))
            
            task = Task(
                id=task_id,
                title=title,
                description=desc,
                status=status,
                priority=priority,
                assigned_to=random.choice(list(self.agents.keys())) if status != TaskStatus.PENDING else None,
                created_at=datetime.now() - timedelta(days=random.randint(0, 7)),
                started_at=datetime.now() - timedelta(hours=random.randint(1, 48)) if status in [TaskStatus.IN_PROGRESS, TaskStatus.COMPLETED] else None,
                completed_at=datetime.now() - timedelta(hours=random.randint(0, 24)) if status == TaskStatus.COMPLETED else None,
                estimated_hours=random.uniform(1, 16),
                actual_hours=random.uniform(1, 20) if status == TaskStatus.COMPLETED else 0,
                tags=tags
            )
            self.tasks[task_id] = task
    
    def _generate_demo_sprints(self):
        """Generate demo sprint data"""
        for i in range(3):
            sprint_id = f"SPRINT-{i+1}"
            start_date = datetime.now() - timedelta(weeks=2-i)
            end_date = start_date + timedelta(weeks=2)
            
            sprint = Sprint(
                id=sprint_id,
                name=f"Sprint {i+1}: {'Current' if i == 1 else 'Past' if i == 0 else 'Upcoming'}",
                start_date=start_date,
                end_date=end_date,
                goals=[
                    f"Complete feature {chr(65+i*3+j)}" for j in range(3)
                ],
                tasks=random.sample(list(self.tasks.keys()), min(10, len(self.tasks))),
                velocity=random.uniform(20, 40),
                burndown_rate=random.uniform(0.6, 0.9)
            )
            self.sprints[sprint_id] = sprint
    
    def _generate_demo_metrics(self):
        """Generate demo metrics data"""
        for i in range(24):  # Last 24 hours
            timestamp = datetime.now() - timedelta(hours=23-i)
            metrics = SystemMetrics(
                timestamp=timestamp,
                cpu_usage=random.uniform(20, 80),
                memory_usage=random.uniform(30, 70),
                active_agents=random.randint(5, 20),
                tasks_in_progress=random.randint(10, 30),
                tasks_completed_today=random.randint(5, 15),
                average_task_time=random.uniform(2, 8),
                error_rate=random.uniform(0, 0.05)
            )
            self.metrics.append(metrics)
    
    def get_agents(self, team: Optional[str] = None, status: Optional[AgentStatus] = None) -> List[Agent]:
        """Get agents filtered by team and/or status"""
        agents = list(self.agents.values())
        if team:
            agents = [a for a in agents if a.team == team]
        if status:
            agents = [a for a in agents if a.status == status]
        return agents
    
    def get_tasks(self, status: Optional[TaskStatus] = None, assigned_to: Optional[str] = None) -> List[Task]:
        """Get tasks filtered by status and/or assignee"""
        tasks = list(self.tasks.values())
        if status:
            tasks = [t for t in tasks if t.status == status]
        if assigned_to:
            tasks = [t for t in tasks if t.assigned_to == assigned_to]
        return tasks
    
    def get_current_sprint(self) -> Optional[Sprint]:
        """Get the current active sprint"""
        now = datetime.now()
        for sprint in self.sprints.values():
            if sprint.start_date <= now <= sprint.end_date:
                return sprint
        return None
    
    def get_latest_metrics(self) -> Optional[SystemMetrics]:
        """Get the most recent system metrics"""
        return self.metrics[-1] if self.metrics else None
    
    def update_metrics(self):
        """Update system metrics with current values"""
        active_agents = len([a for a in self.agents.values() if a.status == AgentStatus.ACTIVE])
        tasks_in_progress = len([t for t in self.tasks.values() if t.status == TaskStatus.IN_PROGRESS])
        
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        tasks_completed_today = len([
            t for t in self.tasks.values() 
            if t.completed_at and t.completed_at >= today_start
        ])
        
        completed_tasks = [t for t in self.tasks.values() if t.status == TaskStatus.COMPLETED and t.actual_hours > 0]
        avg_task_time = sum(t.actual_hours for t in completed_tasks) / len(completed_tasks) if completed_tasks else 0
        
        failed_tasks = len([t for t in self.tasks.values() if t.status == TaskStatus.FAILED])
        total_tasks = len(self.tasks)
        error_rate = failed_tasks / total_tasks if total_tasks > 0 else 0
        
        metrics = SystemMetrics(
            timestamp=datetime.now(),
            cpu_usage=random.uniform(20, 80),  # Would be actual system metrics in production
            memory_usage=random.uniform(30, 70),
            active_agents=active_agents,
            tasks_in_progress=tasks_in_progress,
            tasks_completed_today=tasks_completed_today,
            average_task_time=avg_task_time,
            error_rate=error_rate
        )
        self.metrics.append(metrics)
        
        # Keep only last 24 hours of metrics
        cutoff = datetime.now() - timedelta(hours=24)
        self.metrics = [m for m in self.metrics if m.timestamp >= cutoff]


class DashboardRenderer:
    """Renders various dashboard views"""
    
    def __init__(self, state_manager: StateManager):
        self.state = state_manager
        self.console = Console()
    
    def render_agent_status_table(self, agents: Optional[List[Agent]] = None) -> Table:
        """Render agent status table"""
        if agents is None:
            agents = list(self.state.agents.values())
        
        table = Table(title="Agent Status", box=ROUNDED)
        table.add_column("Agent", style="cyan", no_wrap=True)
        table.add_column("Team", style="magenta")
        table.add_column("Status", justify="center")
        table.add_column("Current Task", style="yellow")
        table.add_column("Completed", justify="right", style="green")
        table.add_column("Failed", justify="right", style="red")
        table.add_column("Performance", justify="center")
        table.add_column("Last Active", style="dim")
        
        for agent in sorted(agents, key=lambda a: (a.team, a.name)):
            status_color = {
                AgentStatus.ACTIVE: "green",
                AgentStatus.BUSY: "yellow",
                AgentStatus.IDLE: "blue",
                AgentStatus.ERROR: "red",
                AgentStatus.OFFLINE: "dim"
            }.get(agent.status, "white")
            
            perf_color = "green" if agent.performance_score >= 0.9 else "yellow" if agent.performance_score >= 0.7 else "red"
            
            last_active = agent.last_active.strftime("%H:%M") if agent.last_active else "N/A"
            
            table.add_row(
                agent.name,
                agent.team,
                f"[{status_color}]{agent.status.value}[/{status_color}]",
                agent.current_task or "-",
                str(agent.tasks_completed),
                str(agent.tasks_failed),
                f"[{perf_color}]{agent.performance_score:.0%}[/{perf_color}]",
                last_active
            )
        
        return table
    
    def render_task_overview_panel(self) -> Panel:
        """Render task overview panel"""
        tasks = list(self.state.tasks.values())
        
        status_counts = {}
        for status in TaskStatus:
            count = len([t for t in tasks if t.status == status])
            status_counts[status] = count
        
        priority_counts = {}
        for priority in TaskPriority:
            count = len([t for t in tasks if t.priority == priority])
            priority_counts[priority] = count
        
        content = Table.grid(padding=1)
        content.add_column(style="bold cyan", justify="right")
        content.add_column()
        
        # Status breakdown
        content.add_row("Task Status", "")
        for status, count in status_counts.items():
            color = {
                TaskStatus.PENDING: "yellow",
                TaskStatus.IN_PROGRESS: "blue",
                TaskStatus.COMPLETED: "green",
                TaskStatus.FAILED: "red",
                TaskStatus.BLOCKED: "magenta"
            }.get(status, "white")
            content.add_row(f"  {status.value.replace('_', ' ').title()}:", f"[{color}]{count}[/{color}]")
        
        content.add_row("", "")
        
        # Priority breakdown
        content.add_row("Priority Levels", "")
        for priority, count in priority_counts.items():
            color = {
                TaskPriority.CRITICAL: "red",
                TaskPriority.HIGH: "yellow",
                TaskPriority.MEDIUM: "blue",
                TaskPriority.LOW: "green"
            }.get(priority, "white")
            content.add_row(f"  {priority.value.title()}:", f"[{color}]{count}[/{color}]")
        
        return Panel(content, title="Task Overview", box=DOUBLE)
    
    def render_sprint_details(self, sprint: Sprint) -> Panel:
        """Render sprint details panel"""
        days_remaining = (sprint.end_date - datetime.now()).days
        progress = 1 - (days_remaining / (sprint.end_date - sprint.start_date).days)
        
        sprint_tasks = [self.state.tasks.get(tid) for tid in sprint.tasks if tid in self.state.tasks]
        completed = len([t for t in sprint_tasks if t and t.status == TaskStatus.COMPLETED])
        total = len(sprint_tasks)
        
        content = Table.grid(padding=1)
        content.add_column(style="bold cyan", justify="right")
        content.add_column()
        
        content.add_row("Sprint:", sprint.name)
        content.add_row("Duration:", f"{sprint.start_date.strftime('%Y-%m-%d')} to {sprint.end_date.strftime('%Y-%m-%d')}")
        content.add_row("Days Remaining:", f"[{'red' if days_remaining < 3 else 'yellow' if days_remaining < 7 else 'green'}]{days_remaining}[/]")
        content.add_row("Progress:", f"[cyan]{progress:.0%}[/cyan]")
        content.add_row("Tasks Completed:", f"[green]{completed}/{total}[/green]")
        content.add_row("Velocity:", f"[blue]{sprint.velocity:.1f} points/day[/blue]")
        content.add_row("Burndown Rate:", f"[{'green' if sprint.burndown_rate > 0.8 else 'yellow' if sprint.burndown_rate > 0.6 else 'red'}]{sprint.burndown_rate:.0%}[/]")
        
        content.add_row("", "")
        content.add_row("Goals:", "")
        for goal in sprint.goals:
            content.add_row("", f"• {goal}")
        
        return Panel(content, title=f"Sprint Details - {sprint.id}", box=DOUBLE)
    
    def render_metrics_dashboard(self) -> Layout:
        """Render full metrics dashboard"""
        layout = Layout()
        
        # Get latest metrics
        metrics = self.state.get_latest_metrics()
        if not metrics:
            return layout
        
        # Create layout structure
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="body"),
            Layout(name="footer", size=3)
        )
        
        # Header
        header_text = Text("System Metrics Dashboard", style="bold cyan", justify="center")
        layout["header"].update(Panel(header_text, box=ROUNDED))
        
        # Body - split into columns
        layout["body"].split_row(
            Layout(name="system", ratio=1),
            Layout(name="agents", ratio=1),
            Layout(name="tasks", ratio=1)
        )
        
        # System metrics
        system_table = Table.grid(padding=1)
        system_table.add_column(justify="right")
        system_table.add_column()
        system_table.add_row("CPU Usage:", f"[{'red' if metrics.cpu_usage > 80 else 'yellow' if metrics.cpu_usage > 60 else 'green'}]{metrics.cpu_usage:.1f}%[/]")
        system_table.add_row("Memory Usage:", f"[{'red' if metrics.memory_usage > 80 else 'yellow' if metrics.memory_usage > 60 else 'green'}]{metrics.memory_usage:.1f}%[/]")
        system_table.add_row("Error Rate:", f"[{'red' if metrics.error_rate > 0.05 else 'yellow' if metrics.error_rate > 0.02 else 'green'}]{metrics.error_rate:.1%}[/]")
        layout["system"].update(Panel(system_table, title="System", box=ROUNDED))
        
        # Agent metrics
        agent_table = Table.grid(padding=1)
        agent_table.add_column(justify="right")
        agent_table.add_column()
        agent_table.add_row("Active Agents:", f"[cyan]{metrics.active_agents}[/cyan]")
        agent_table.add_row("Total Agents:", f"[blue]{len(self.state.agents)}[/blue]")
        utilization = metrics.active_agents / len(self.state.agents) if self.state.agents else 0
        agent_table.add_row("Utilization:", f"[{'green' if utilization > 0.7 else 'yellow' if utilization > 0.5 else 'red'}]{utilization:.0%}[/]")
        layout["agents"].update(Panel(agent_table, title="Agents", box=ROUNDED))
        
        # Task metrics
        task_table = Table.grid(padding=1)
        task_table.add_column(justify="right")
        task_table.add_column()
        task_table.add_row("In Progress:", f"[yellow]{metrics.tasks_in_progress}[/yellow]")
        task_table.add_row("Completed Today:", f"[green]{metrics.tasks_completed_today}[/green]")
        task_table.add_row("Avg Task Time:", f"[blue]{metrics.average_task_time:.1f}h[/blue]")
        layout["tasks"].update(Panel(task_table, title="Tasks", box=ROUNDED))
        
        # Footer
        footer_text = Text(f"Last Updated: {metrics.timestamp.strftime('%Y-%m-%d %H:%M:%S')}", style="dim", justify="center")
        layout["footer"].update(Panel(footer_text, box=ROUNDED))
        
        return layout
    
    def render_json_output(self, data: Any) -> str:
        """Render data as JSON"""
        if hasattr(data, 'to_dict'):
            data = data.to_dict()
        elif isinstance(data, list) and data and hasattr(data[0], 'to_dict'):
            data = [item.to_dict() for item in data]
        elif isinstance(data, dict):
            # Convert any nested objects
            processed = {}
            for key, value in data.items():
                if hasattr(value, 'to_dict'):
                    processed[key] = value.to_dict()
                elif isinstance(value, list) and value and hasattr(value[0], 'to_dict'):
                    processed[key] = [item.to_dict() for item in value]
                else:
                    processed[key] = value
            data = processed
        
        return json.dumps(data, indent=2, default=str)
    
    def render_summary(self) -> str:
        """Render a text summary of the current state"""
        agents = list(self.state.agents.values())
        tasks = list(self.state.tasks.values())
        sprint = self.state.get_current_sprint()
        metrics = self.state.get_latest_metrics()
        
        summary = []
        summary.append("=== SYSTEM SUMMARY ===\n")
        
        # Agent summary
        active_agents = [a for a in agents if a.status == AgentStatus.ACTIVE]
        summary.append(f"Agents: {len(active_agents)}/{len(agents)} active")
        
        # Task summary
        in_progress = [t for t in tasks if t.status == TaskStatus.IN_PROGRESS]
        completed = [t for t in tasks if t.status == TaskStatus.COMPLETED]
        summary.append(f"Tasks: {len(in_progress)} in progress, {len(completed)} completed")
        
        # Sprint summary
        if sprint:
            days_left = (sprint.end_date - datetime.now()).days
            summary.append(f"Current Sprint: {sprint.name} ({days_left} days remaining)")
        
        # Metrics summary
        if metrics:
            summary.append(f"System Load: CPU {metrics.cpu_usage:.1f}%, Memory {metrics.memory_usage:.1f}%")
            summary.append(f"Today's Completions: {metrics.tasks_completed_today} tasks")
        
        return "\n".join(summary)


class ObservabilityDashboard:
    """Main observability dashboard controller"""
    
    def __init__(self):
        self.state = StateManager()
        self.renderer = DashboardRenderer(self.state)
    
    def show_status(self, format: str = "table", agent: Optional[str] = None):
        """Show agent and task status"""
        agents = self.state.get_agents()
        if agent:
            agents = [a for a in agents if agent.lower() in a.name.lower()]
        
        if format == "table":
            table = self.renderer.render_agent_status_table(agents)
            console.print(table)
            console.print()
            panel = self.renderer.render_task_overview_panel()
            console.print(panel)
        elif format == "json":
            data = {
                "agents": [a.to_dict() for a in agents],
                "task_summary": {
                    "total": len(self.state.tasks),
                    "by_status": {
                        status.value: len([t for t in self.state.tasks.values() if t.status == status])
                        for status in TaskStatus
                    }
                }
            }
            print(self.renderer.render_json_output(data))
        elif format == "summary":
            print(self.renderer.render_summary())
    
    def show_sprint(self, current: bool = True, all: bool = False, format: str = "table"):
        """Show sprint information"""
        if all:
            sprints = list(self.state.sprints.values())
        elif current:
            sprint = self.state.get_current_sprint()
            sprints = [sprint] if sprint else []
        else:
            sprints = list(self.state.sprints.values())[:1]
        
        if format == "table":
            for sprint in sprints:
                panel = self.renderer.render_sprint_details(sprint)
                console.print(panel)
                if sprint != sprints[-1]:
                    console.print()
        elif format == "json":
            data = [s.to_dict() for s in sprints]
            print(self.renderer.render_json_output(data))
    
    def monitor(self, interval: int = 5, metrics: str = "cpu,memory,tasks"):
        """Live monitoring dashboard"""
        metric_types = metrics.split(",")
        
        with Live(self.renderer.render_metrics_dashboard(), refresh_per_second=1) as live:
            try:
                while True:
                    # Update metrics
                    self.state.update_metrics()
                    
                    # Update display
                    live.update(self.renderer.render_metrics_dashboard())
                    
                    # Wait for next update
                    time.sleep(interval)
            except KeyboardInterrupt:
                console.print("\n[yellow]Monitoring stopped[/yellow]")
    
    def show_metrics(self, type: str = "performance"):
        """Show detailed metrics"""
        metrics = self.state.get_latest_metrics()
        if not metrics:
            console.print("[red]No metrics available[/red]")
            return
        
        if type == "performance":
            table = Table(title="Performance Metrics", box=ROUNDED)
            table.add_column("Metric", style="cyan")
            table.add_column("Value", justify="right")
            table.add_column("Status", justify="center")
            
            # CPU
            cpu_status = "🔴" if metrics.cpu_usage > 80 else "🟡" if metrics.cpu_usage > 60 else "🟢"
            table.add_row("CPU Usage", f"{metrics.cpu_usage:.1f}%", cpu_status)
            
            # Memory
            mem_status = "🔴" if metrics.memory_usage > 80 else "🟡" if metrics.memory_usage > 60 else "🟢"
            table.add_row("Memory Usage", f"{metrics.memory_usage:.1f}%", mem_status)
            
            # Task Time
            time_status = "🔴" if metrics.average_task_time > 8 else "🟡" if metrics.average_task_time > 4 else "🟢"
            table.add_row("Avg Task Time", f"{metrics.average_task_time:.1f} hours", time_status)
            
            console.print(table)
            
        elif type == "quality":
            table = Table(title="Quality Metrics", box=ROUNDED)
            table.add_column("Metric", style="cyan")
            table.add_column("Value", justify="right")
            table.add_column("Status", justify="center")
            
            # Error Rate
            error_status = "🔴" if metrics.error_rate > 0.05 else "🟡" if metrics.error_rate > 0.02 else "🟢"
            table.add_row("Error Rate", f"{metrics.error_rate:.1%}", error_status)
            
            # Task Success Rate
            success_rate = 1 - metrics.error_rate
            success_status = "🟢" if success_rate > 0.95 else "🟡" if success_rate > 0.90 else "🔴"
            table.add_row("Success Rate", f"{success_rate:.1%}", success_status)
            
            console.print(table)
            
        elif type == "productivity":
            table = Table(title="Productivity Metrics", box=ROUNDED)
            table.add_column("Metric", style="cyan")
            table.add_column("Value", justify="right")
            table.add_column("Trend", justify="center")
            
            table.add_row("Active Agents", str(metrics.active_agents), "📈")
            table.add_row("Tasks in Progress", str(metrics.tasks_in_progress), "📊")
            table.add_row("Completed Today", str(metrics.tasks_completed_today), "✅")
            
            # Calculate velocity
            if len(self.state.metrics) > 1:
                prev_completed = self.state.metrics[-2].tasks_completed_today
                trend = "📈" if metrics.tasks_completed_today > prev_completed else "📉" if metrics.tasks_completed_today < prev_completed else "➡️"
            else:
                trend = "➡️"
            
            table.add_row("Completion Trend", "", trend)
            
            console.print(table)


# CLI Commands
@click.group()
def cli():
    """Observability Dashboard for Claude Code Development Team"""
    pass


@cli.command()
@click.option('--format', type=click.Choice(['table', 'json', 'summary']), default='table', help='Output format')
@click.option('--agent', type=str, help='Filter by agent name')
def status(format: str, agent: Optional[str]):
    """Show current agent and task status"""
    dashboard = ObservabilityDashboard()
    dashboard.show_status(format=format, agent=agent)


@cli.command()
@click.option('--current', is_flag=True, default=True, help='Show current sprint only')
@click.option('--all', is_flag=True, help='Show all sprints')
@click.option('--format', type=click.Choice(['table', 'json']), default='table', help='Output format')
def sprint(current: bool, all: bool, format: str):
    """Show sprint information and progress"""
    dashboard = ObservabilityDashboard()
    dashboard.show_sprint(current=current, all=all, format=format)


@cli.command()
@click.option('--interval', type=int, default=5, help='Refresh interval in seconds')
@click.option('--metrics', type=str, default='cpu,memory,tasks', help='Metrics to monitor (comma-separated)')
def monitor(interval: int, metrics: str):
    """Live monitoring dashboard with real-time updates"""
    dashboard = ObservabilityDashboard()
    console.print(f"[cyan]Starting live monitoring (refresh every {interval}s)...[/cyan]")
    console.print("[dim]Press Ctrl+C to stop[/dim]\n")
    dashboard.monitor(interval=interval, metrics=metrics)


@cli.command()
@click.option('--type', type=click.Choice(['performance', 'quality', 'productivity']), default='performance', help='Type of metrics to show')
def metrics(type: str):
    """Show detailed system metrics and analytics"""
    dashboard = ObservabilityDashboard()
    dashboard.show_metrics(type=type)


def main() -> int:
    """Main entry point"""
    try:
        cli()
        return 0
    except Exception as e:
        logger.error(f"Dashboard error: {e}")
        console.print(f"[red]Error: {e}[/red]")
        return 1


if __name__ == "__main__":
    sys.exit(main())