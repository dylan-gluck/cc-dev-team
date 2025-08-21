# V2 Orchestration Performance Monitoring Strategy

## Executive Summary

This document defines comprehensive performance benchmarks, monitoring strategies, and optimization techniques for the v2 orchestration system. The strategy ensures real-time observability, predictive performance management, and continuous optimization of multi-agent development workflows.

## Performance Targets & Justifications

### Core System Performance Targets

| Component | Target | Justification | Measurement Method |
|-----------|---------|---------------|-------------------|
| **Session Initialization** | < 100ms | User experience - immediate feedback required | Time from `SessionStateManager.__init__()` to `status="active"` |
| **State Query** | < 50ms | Real-time dashboard updates without UI lag | JSONPath query execution time via `QueryAPI.query()` |
| **Hook Processing** | < 200ms | Maintain workflow momentum without blocking | Hook execution from trigger to completion |
| **Dashboard Refresh** | < 500ms | Acceptable for real-time monitoring interfaces | Full dashboard render including all metrics |
| **Agent Spawn** | < 1s | Balance speed vs proper initialization | From spawn request to agent ready state |

### Extended Performance Targets

| Component | Target | Justification |
|-----------|---------|---------------|
| **Event Processing** | < 25ms per event | High-frequency event streams need minimal latency |
| **State Persistence** | < 300ms | Background operation, should not block user actions |
| **Message Bus Delivery** | < 100ms | Critical for agent coordination |
| **Dependency Resolution** | < 150ms | Essential for task orchestration |
| **Recovery Time** | < 5s | System availability during failures |

### Quality & Reliability Targets

| Metric | Target | Justification |
|--------|---------|---------------|
| **System Availability** | 99.9% | Professional development environment requirement |
| **Data Consistency** | 100% | Critical for multi-agent coordination |
| **Memory Efficiency** | < 500MB per session | Resource conservation on developer machines |
| **Storage Growth** | < 10MB/day | Sustainable long-term usage |
| **Error Rate** | < 0.1% | High reliability for production development |

## Monitoring Strategy

### 1. Multi-Layer Monitoring Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Monitoring Control Plane                 │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │ Real-time   │  │ Predictive  │  │ Historical  │         │
│  │ Metrics     │  │ Analytics   │  │ Analysis    │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │ Component   │  │ System      │  │ Business    │         │
│  │ Telemetry   │  │ Health      │  │ KPIs        │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
├─────────────────────────────────────────────────────────────┤
│                    Data Collection Layer                    │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │ Event       │  │ Metrics     │  │ Traces      │         │
│  │ Streams     │  │ Collectors  │  │ & Logs      │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└─────────────────────────────────────────────────────────────┘
```

### 2. Key Metrics Collection

#### Performance Metrics Framework

```python
# .claude/scripts/performance_monitor.py
#!/usr/bin/env -S uv run --script
# /// script
# dependencies = [
#   "psutil",
#   "rich",
#   "click",
#   "prometheus-client",
# ]
# ///

import time
import psutil
import json
from datetime import datetime, timedelta
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional
import threading
from contextlib import contextmanager

@dataclass
class PerformanceMetrics:
    # System Performance
    cpu_usage_percent: float
    memory_usage_mb: float
    memory_usage_percent: float
    disk_io_read_mb: float
    disk_io_write_mb: float
    
    # Orchestration Performance
    session_init_time_ms: float
    state_query_avg_ms: float
    hook_processing_avg_ms: float
    agent_spawn_avg_ms: float
    dashboard_refresh_ms: float
    
    # Business Metrics
    active_agents: int
    tasks_completed_per_hour: float
    success_rate_percent: float
    error_rate_percent: float
    
    # Quality Metrics
    test_coverage_percent: float
    code_quality_score: float
    documentation_coverage: float
    
    # Resource Efficiency
    agent_utilization_percent: float
    parallel_execution_ratio: float
    resource_efficiency_score: float
    
    timestamp: str

class PerformanceMonitor:
    def __init__(self, workspace_path: str):
        self.workspace_path = Path(workspace_path)
        self.metrics_dir = self.workspace_path / ".claude" / "metrics"
        self.metrics_dir.mkdir(parents=True, exist_ok=True)
        
        # Performance tracking
        self.timers = {}
        self.counters = {}
        self.gauges = {}
        
        # Collection intervals
        self.system_metrics_interval = 30  # seconds
        self.business_metrics_interval = 60  # seconds
        
        # Performance baselines
        self.baselines = self.load_baselines()
        
        # Start background collection
        self._start_background_collection()
    
    @contextmanager
    def timer(self, operation: str):
        """Context manager for timing operations"""
        start_time = time.time()
        try:
            yield
        finally:
            duration_ms = (time.time() - start_time) * 1000
            self._record_timing(operation, duration_ms)
    
    def _record_timing(self, operation: str, duration_ms: float):
        """Record timing measurement"""
        if operation not in self.timers:
            self.timers[operation] = []
        
        self.timers[operation].append({
            "duration_ms": duration_ms,
            "timestamp": datetime.now().isoformat()
        })
        
        # Keep only last 100 measurements per operation
        if len(self.timers[operation]) > 100:
            self.timers[operation].pop(0)
    
    def increment_counter(self, metric: str, value: int = 1):
        """Increment a counter metric"""
        self.counters[metric] = self.counters.get(metric, 0) + value
    
    def set_gauge(self, metric: str, value: float):
        """Set a gauge metric value"""
        self.gauges[metric] = value
    
    def collect_current_metrics(self) -> PerformanceMetrics:
        """Collect all current performance metrics"""
        # System metrics
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk_io = psutil.disk_io_counters()
        
        # Calculate averages from timers
        session_init_avg = self._get_average_timing("session_init", 100.0)
        state_query_avg = self._get_average_timing("state_query", 50.0)
        hook_processing_avg = self._get_average_timing("hook_processing", 200.0)
        agent_spawn_avg = self._get_average_timing("agent_spawn", 1000.0)
        dashboard_refresh_avg = self._get_average_timing("dashboard_refresh", 500.0)
        
        # Business metrics from state
        state_metrics = self._get_state_metrics()
        
        return PerformanceMetrics(
            cpu_usage_percent=cpu_percent,
            memory_usage_mb=memory.used / (1024 * 1024),
            memory_usage_percent=memory.percent,
            disk_io_read_mb=disk_io.read_bytes / (1024 * 1024) if disk_io else 0,
            disk_io_write_mb=disk_io.write_bytes / (1024 * 1024) if disk_io else 0,
            
            session_init_time_ms=session_init_avg,
            state_query_avg_ms=state_query_avg,
            hook_processing_avg_ms=hook_processing_avg,
            agent_spawn_avg_ms=agent_spawn_avg,
            dashboard_refresh_ms=dashboard_refresh_avg,
            
            active_agents=state_metrics.get("active_agents", 0),
            tasks_completed_per_hour=state_metrics.get("tasks_per_hour", 0.0),
            success_rate_percent=state_metrics.get("success_rate", 0.0) * 100,
            error_rate_percent=state_metrics.get("error_rate", 0.0) * 100,
            
            test_coverage_percent=state_metrics.get("test_coverage", 0.0) * 100,
            code_quality_score=state_metrics.get("code_quality", 0.0),
            documentation_coverage=state_metrics.get("doc_coverage", 0.0) * 100,
            
            agent_utilization_percent=state_metrics.get("agent_utilization", 0.0) * 100,
            parallel_execution_ratio=state_metrics.get("parallel_ratio", 0.0),
            resource_efficiency_score=state_metrics.get("resource_efficiency", 0.0),
            
            timestamp=datetime.now().isoformat()
        )
    
    def _get_average_timing(self, operation: str, fallback: float) -> float:
        """Get average timing for an operation"""
        if operation not in self.timers or not self.timers[operation]:
            return fallback
        
        recent_timings = self.timers[operation][-10:]  # Last 10 measurements
        return sum(t["duration_ms"] for t in recent_timings) / len(recent_timings)
    
    def _get_state_metrics(self) -> Dict:
        """Extract metrics from orchestration state"""
        state_file = self.workspace_path / ".claude" / "state" / "orchestration.json"
        
        if not state_file.exists():
            return {}
        
        try:
            with state_file.open() as f:
                state = json.load(f)
            
            # Extract relevant metrics
            agents = state.get("execution", {}).get("agents", {}).get("active", {})
            tasks = state.get("execution", {}).get("tasks", {})
            metrics = state.get("observability", {}).get("metrics", {})
            
            # Calculate derived metrics
            active_agents = len(agents)
            completed_tasks = sum(1 for t in tasks.values() if t.get("status") == "completed")
            total_tasks = len(tasks)
            
            return {
                "active_agents": active_agents,
                "tasks_per_hour": completed_tasks * 6,  # Extrapolate from 10-min window
                "success_rate": metrics.get("quality", {}).get("task_completion_rate", 0.0),
                "error_rate": metrics.get("quality", {}).get("error_rate", 0.0),
                "test_coverage": metrics.get("quality", {}).get("test_coverage_percent", 0.0) / 100,
                "code_quality": metrics.get("quality", {}).get("code_quality_score", 0.0),
                "doc_coverage": metrics.get("quality", {}).get("documentation_coverage", 0.0),
                "agent_utilization": metrics.get("utilization", {}).get("agent_utilization_rate", 0.0),
                "parallel_ratio": metrics.get("utilization", {}).get("parallel_execution_ratio", 0.0),
                "resource_efficiency": metrics.get("utilization", {}).get("resource_efficiency_score", 0.0)
            }
            
        except (json.JSONDecodeError, KeyError):
            return {}
    
    def load_baselines(self) -> Dict:
        """Load performance baselines"""
        baseline_file = self.metrics_dir / "baselines.json"
        
        if baseline_file.exists():
            with baseline_file.open() as f:
                return json.load(f)
        
        # Default baselines
        return {
            "session_init_time_ms": 100.0,
            "state_query_avg_ms": 50.0,
            "hook_processing_avg_ms": 200.0,
            "agent_spawn_avg_ms": 1000.0,
            "dashboard_refresh_ms": 500.0,
            "cpu_usage_percent": 50.0,
            "memory_usage_percent": 60.0,
            "success_rate_percent": 95.0
        }
    
    def save_baselines(self, metrics: PerformanceMetrics):
        """Save current metrics as new baselines"""
        baseline_file = self.metrics_dir / "baselines.json"
        
        with baseline_file.open('w') as f:
            json.dump(asdict(metrics), f, indent=2)
    
    def _start_background_collection(self):
        """Start background metric collection"""
        def collect_system_metrics():
            while True:
                metrics = self.collect_current_metrics()
                self._save_metrics(metrics)
                time.sleep(self.system_metrics_interval)
        
        thread = threading.Thread(target=collect_system_metrics, daemon=True)
        thread.start()
    
    def _save_metrics(self, metrics: PerformanceMetrics):
        """Save metrics to time-series file"""
        metrics_file = self.metrics_dir / f"metrics-{datetime.now().strftime('%Y-%m-%d')}.jsonl"
        
        with metrics_file.open('a') as f:
            f.write(json.dumps(asdict(metrics)) + '\n')

# Global monitor instance
_monitor = None

def get_monitor(workspace_path: str = ".") -> PerformanceMonitor:
    """Get the global performance monitor instance"""
    global _monitor
    if _monitor is None:
        _monitor = PerformanceMonitor(workspace_path)
    return _monitor

# Decorators for easy instrumentation
def timed(operation_name: str):
    """Decorator to time function execution"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            monitor = get_monitor()
            with monitor.timer(operation_name):
                return func(*args, **kwargs)
        return wrapper
    return decorator

@timed("session_init")
def monitored_session_init():
    """Example of monitored session initialization"""
    pass

if __name__ == "__main__":
    import click
    
    @click.group()
    def cli():
        """Performance monitoring CLI"""
        pass
    
    @cli.command()
    @click.option('--format', type=click.Choice(['json', 'table']), default='table')
    def current(format):
        """Show current performance metrics"""
        monitor = get_monitor()
        metrics = monitor.collect_current_metrics()
        
        if format == 'json':
            print(json.dumps(asdict(metrics), indent=2))
        else:
            # Table format
            from rich.console import Console
            from rich.table import Table
            
            console = Console()
            table = Table(title="Current Performance Metrics")
            table.add_column("Metric", style="cyan")
            table.add_column("Value", style="green")
            table.add_column("Target", style="yellow")
            table.add_column("Status", style="bold")
            
            baselines = monitor.baselines
            
            def status_indicator(current, target, higher_is_better=True):
                if higher_is_better:
                    return "✅" if current >= target else "⚠️" if current >= target * 0.8 else "🔴"
                else:
                    return "✅" if current <= target else "⚠️" if current <= target * 1.2 else "🔴"
            
            # Performance metrics
            table.add_row("Session Init Time", f"{metrics.session_init_time_ms:.1f}ms", 
                         f"{baselines['session_init_time_ms']:.0f}ms",
                         status_indicator(metrics.session_init_time_ms, baselines['session_init_time_ms'], False))
            
            table.add_row("State Query Time", f"{metrics.state_query_avg_ms:.1f}ms",
                         f"{baselines['state_query_avg_ms']:.0f}ms", 
                         status_indicator(metrics.state_query_avg_ms, baselines['state_query_avg_ms'], False))
            
            table.add_row("Hook Processing", f"{metrics.hook_processing_avg_ms:.1f}ms",
                         f"{baselines['hook_processing_avg_ms']:.0f}ms",
                         status_indicator(metrics.hook_processing_avg_ms, baselines['hook_processing_avg_ms'], False))
            
            table.add_row("Agent Spawn Time", f"{metrics.agent_spawn_avg_ms:.1f}ms",
                         f"{baselines['agent_spawn_avg_ms']:.0f}ms",
                         status_indicator(metrics.agent_spawn_avg_ms, baselines['agent_spawn_avg_ms'], False))
            
            table.add_row("Dashboard Refresh", f"{metrics.dashboard_refresh_ms:.1f}ms",
                         f"{baselines['dashboard_refresh_ms']:.0f}ms",
                         status_indicator(metrics.dashboard_refresh_ms, baselines['dashboard_refresh_ms'], False))
            
            # Resource metrics
            table.add_row("CPU Usage", f"{metrics.cpu_usage_percent:.1f}%",
                         f"{baselines['cpu_usage_percent']:.0f}%",
                         status_indicator(metrics.cpu_usage_percent, baselines['cpu_usage_percent'], False))
            
            table.add_row("Memory Usage", f"{metrics.memory_usage_percent:.1f}%",
                         f"{baselines['memory_usage_percent']:.0f}%",
                         status_indicator(metrics.memory_usage_percent, baselines['memory_usage_percent'], False))
            
            # Business metrics
            table.add_row("Success Rate", f"{metrics.success_rate_percent:.1f}%",
                         f"{baselines['success_rate_percent']:.0f}%",
                         status_indicator(metrics.success_rate_percent, baselines['success_rate_percent']))
            
            console.print(table)
    
    @cli.command()
    def baseline(operation):
        """Set new performance baselines"""
        monitor = get_monitor()
        metrics = monitor.collect_current_metrics()
        monitor.save_baselines(metrics)
        print("✅ New performance baselines saved")
    
    cli()
```

### 3. Real-Time Dashboard Integration

#### Enhanced Observability Script

```python
# Enhancement to existing .claude/scripts/observability.py
class RealtimeDashboard:
    def __init__(self, session_manager):
        self.session_manager = session_manager
        self.performance_monitor = get_monitor()
        self.alert_thresholds = self.load_alert_thresholds()
    
    def generate_performance_dashboard(self):
        """Generate comprehensive performance dashboard"""
        metrics = self.performance_monitor.collect_current_metrics()
        
        layout = Layout()
        layout.split_column(
            Layout(name="header", size=5),
            Layout(name="main"),
            Layout(name="alerts", size=6)
        )
        
        # Header with system status
        status = self.get_system_status(metrics)
        layout["header"].update(Panel(
            f"[bold]V2 Orchestration Performance Dashboard[/bold]\n"
            f"Status: {status['indicator']} {status['message']}\n"
            f"Uptime: {status['uptime']} | Active Agents: {metrics.active_agents}\n"
            f"Last Updated: {datetime.now().strftime('%H:%M:%S')}"
        ))
        
        # Main dashboard content
        main_layout = Layout()
        main_layout.split_row(
            Layout(name="performance"),
            Layout(name="resources"),
            Layout(name="business")
        )
        
        # Performance metrics table
        perf_table = self.create_performance_table(metrics)
        main_layout["performance"].update(perf_table)
        
        # Resource utilization
        resource_table = self.create_resource_table(metrics)
        main_layout["resources"].update(resource_table)
        
        # Business KPIs
        business_table = self.create_business_table(metrics)
        main_layout["business"].update(business_table)
        
        layout["main"].update(main_layout)
        
        # Alerts and warnings
        alerts = self.check_alerts(metrics)
        layout["alerts"].update(self.create_alerts_panel(alerts))
        
        return layout
    
    def create_performance_table(self, metrics: PerformanceMetrics) -> Table:
        """Create performance metrics table"""
        table = Table(title="⚡ Performance Metrics")
        table.add_column("Component", style="cyan")
        table.add_column("Current", style="green")
        table.add_column("Target", style="yellow")
        table.add_column("Trend", style="blue")
        table.add_column("Status", style="bold")
        
        baselines = self.performance_monitor.baselines
        
        performance_metrics = [
            ("Session Init", metrics.session_init_time_ms, baselines["session_init_time_ms"], "ms", False),
            ("State Query", metrics.state_query_avg_ms, baselines["state_query_avg_ms"], "ms", False),
            ("Hook Processing", metrics.hook_processing_avg_ms, baselines["hook_processing_avg_ms"], "ms", False),
            ("Agent Spawn", metrics.agent_spawn_avg_ms, baselines["agent_spawn_avg_ms"], "ms", False),
            ("Dashboard Refresh", metrics.dashboard_refresh_ms, baselines["dashboard_refresh_ms"], "ms", False)
        ]
        
        for name, current, target, unit, higher_is_better in performance_metrics:
            trend = self.get_trend_indicator(name, current)
            status = self.get_status_indicator(current, target, higher_is_better)
            
            table.add_row(
                name,
                f"{current:.1f}{unit}",
                f"{target:.0f}{unit}",
                trend,
                status
            )
        
        return table
    
    def create_resource_table(self, metrics: PerformanceMetrics) -> Table:
        """Create resource utilization table"""
        table = Table(title="💻 Resource Utilization")
        table.add_column("Resource", style="cyan")
        table.add_column("Usage", style="green")
        table.add_column("Limit", style="yellow")
        table.add_column("Efficiency", style="blue")
        
        # CPU usage bar
        cpu_bar = self.create_usage_bar(metrics.cpu_usage_percent, 100)
        table.add_row("CPU", f"{metrics.cpu_usage_percent:.1f}%", "< 80%", cpu_bar)
        
        # Memory usage bar
        memory_bar = self.create_usage_bar(metrics.memory_usage_percent, 100)
        table.add_row("Memory", f"{metrics.memory_usage_mb:.0f}MB ({metrics.memory_usage_percent:.1f}%)", "< 75%", memory_bar)
        
        # Agent utilization
        agent_bar = self.create_usage_bar(metrics.agent_utilization_percent, 100)
        table.add_row("Agents", f"{metrics.agent_utilization_percent:.1f}%", "> 70%", agent_bar)
        
        # Parallel execution
        parallel_bar = self.create_usage_bar(metrics.parallel_execution_ratio * 100, 100)
        table.add_row("Parallel Exec", f"{metrics.parallel_execution_ratio * 100:.1f}%", "> 60%", parallel_bar)
        
        return table
    
    def create_business_table(self, metrics: PerformanceMetrics) -> Table:
        """Create business KPIs table"""
        table = Table(title="📊 Business KPIs")
        table.add_column("KPI", style="cyan")
        table.add_column("Current", style="green")
        table.add_column("Target", style="yellow")
        table.add_column("Impact", style="blue")
        
        table.add_row("Success Rate", f"{metrics.success_rate_percent:.1f}%", "> 95%", "🎯")
        table.add_row("Error Rate", f"{metrics.error_rate_percent:.2f}%", "< 1%", "🔍")
        table.add_row("Test Coverage", f"{metrics.test_coverage_percent:.1f}%", "> 80%", "🛡️")
        table.add_row("Code Quality", f"{metrics.code_quality_score:.1f}/10", "> 8.0", "⭐")
        table.add_row("Tasks/Hour", f"{metrics.tasks_completed_per_hour:.1f}", "> 20", "🚀")
        
        return table
    
    def create_usage_bar(self, current: float, maximum: float, width: int = 10) -> str:
        """Create a visual usage bar"""
        filled = int((current / maximum) * width)
        bar = "█" * filled + "░" * (width - filled)
        
        if current > 90:
            color = "red"
        elif current > 75:
            color = "yellow"
        else:
            color = "green"
        
        return f"[{color}]{bar}[/{color}] {current:.0f}%"
    
    def get_status_indicator(self, current: float, target: float, higher_is_better: bool) -> str:
        """Get status indicator for a metric"""
        if higher_is_better:
            if current >= target:
                return "✅"
            elif current >= target * 0.8:
                return "⚠️"
            else:
                return "🔴"
        else:
            if current <= target:
                return "✅"
            elif current <= target * 1.2:
                return "⚠️"
            else:
                return "🔴"
    
    def get_trend_indicator(self, metric_name: str, current_value: float) -> str:
        """Get trend indicator for a metric"""
        # Get historical data (simplified implementation)
        trend_data = self.get_historical_trend(metric_name)
        
        if not trend_data or len(trend_data) < 2:
            return "➡️"
        
        recent_avg = sum(trend_data[-3:]) / len(trend_data[-3:])
        older_avg = sum(trend_data[-6:-3]) / len(trend_data[-6:-3]) if len(trend_data) >= 6 else recent_avg
        
        if recent_avg > older_avg * 1.05:
            return "📈"
        elif recent_avg < older_avg * 0.95:
            return "📉"
        else:
            return "➡️"
    
    def check_alerts(self, metrics: PerformanceMetrics) -> List[Dict]:
        """Check for alert conditions"""
        alerts = []
        
        # Performance alerts
        if metrics.session_init_time_ms > 150:
            alerts.append({
                "level": "warning",
                "metric": "Session Init Time",
                "message": f"Slow session initialization: {metrics.session_init_time_ms:.1f}ms",
                "recommendation": "Check system resources and restart if needed"
            })
        
        if metrics.state_query_avg_ms > 75:
            alerts.append({
                "level": "warning", 
                "metric": "State Query",
                "message": f"Slow state queries: {metrics.state_query_avg_ms:.1f}ms",
                "recommendation": "Consider state cleanup or caching optimization"
            })
        
        # Resource alerts
        if metrics.cpu_usage_percent > 85:
            alerts.append({
                "level": "critical",
                "metric": "CPU Usage",
                "message": f"High CPU usage: {metrics.cpu_usage_percent:.1f}%",
                "recommendation": "Reduce agent concurrency or optimize workflows"
            })
        
        if metrics.memory_usage_percent > 80:
            alerts.append({
                "level": "critical",
                "metric": "Memory Usage", 
                "message": f"High memory usage: {metrics.memory_usage_percent:.1f}%",
                "recommendation": "Run cleanup operations and reduce session size"
            })
        
        # Business alerts
        if metrics.success_rate_percent < 90:
            alerts.append({
                "level": "warning",
                "metric": "Success Rate",
                "message": f"Low success rate: {metrics.success_rate_percent:.1f}%",
                "recommendation": "Review error patterns and improve workflows"
            })
        
        if metrics.error_rate_percent > 2:
            alerts.append({
                "level": "critical",
                "metric": "Error Rate",
                "message": f"High error rate: {metrics.error_rate_percent:.2f}%", 
                "recommendation": "Investigate and fix critical issues immediately"
            })
        
        return alerts
    
    def create_alerts_panel(self, alerts: List[Dict]) -> Panel:
        """Create alerts panel"""
        if not alerts:
            return Panel("[green]✅ All systems operating within normal parameters[/green]", 
                        title="🛡️ System Health")
        
        alert_text = ""
        for alert in alerts:
            level_icon = "🔴" if alert["level"] == "critical" else "⚠️"
            alert_text += f"{level_icon} {alert['metric']}: {alert['message']}\n"
            alert_text += f"   💡 {alert['recommendation']}\n\n"
        
        title_color = "red" if any(a["level"] == "critical" for a in alerts) else "yellow"
        return Panel(alert_text.strip(), title=f"[{title_color}]🚨 Active Alerts ({len(alerts)})[/{title_color}]")
```

## Benchmark Suite

### 1. Component Benchmarking Framework

```python
# .claude/scripts/benchmark.py
#!/usr/bin/env -S uv run --script
# /// script
# dependencies = [
#   "click",
#   "rich",
#   "statistics",
#   "concurrent.futures",
# ]
# ///

import time
import json
import statistics
import concurrent.futures
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Callable, Any
from dataclasses import dataclass

@dataclass
class BenchmarkResult:
    operation: str
    iterations: int
    mean_ms: float
    median_ms: float
    std_dev_ms: float
    min_ms: float
    max_ms: float
    percentile_95_ms: float
    percentile_99_ms: float
    success_rate: float
    timestamp: str

class BenchmarkSuite:
    def __init__(self, workspace_path: str):
        self.workspace_path = Path(workspace_path)
        self.results_dir = self.workspace_path / ".claude" / "benchmarks"
        self.results_dir.mkdir(parents=True, exist_ok=True)
        
    def run_benchmark(self, operation_name: str, operation_func: Callable, 
                     iterations: int = 100, warmup: int = 10) -> BenchmarkResult:
        """Run a benchmark for a specific operation"""
        print(f"🏃 Running benchmark: {operation_name} ({iterations} iterations)")
        
        # Warmup runs
        for _ in range(warmup):
            try:
                operation_func()
            except Exception:
                pass
        
        # Actual benchmark runs
        timings = []
        successes = 0
        
        for i in range(iterations):
            start_time = time.perf_counter()
            
            try:
                operation_func()
                success = True
                successes += 1
            except Exception as e:
                success = False
                print(f"❌ Iteration {i+1} failed: {e}")
            
            end_time = time.perf_counter()
            timings.append((end_time - start_time) * 1000)  # Convert to ms
        
        # Calculate statistics
        if not timings:
            raise ValueError("No successful benchmark runs")
        
        mean_ms = statistics.mean(timings)
        median_ms = statistics.median(timings)
        std_dev_ms = statistics.stdev(timings) if len(timings) > 1 else 0
        min_ms = min(timings)
        max_ms = max(timings)
        
        # Calculate percentiles
        sorted_timings = sorted(timings)
        percentile_95_ms = sorted_timings[int(0.95 * len(sorted_timings))]
        percentile_99_ms = sorted_timings[int(0.99 * len(sorted_timings))]
        
        success_rate = successes / iterations
        
        result = BenchmarkResult(
            operation=operation_name,
            iterations=iterations,
            mean_ms=mean_ms,
            median_ms=median_ms,
            std_dev_ms=std_dev_ms,
            min_ms=min_ms,
            max_ms=max_ms,
            percentile_95_ms=percentile_95_ms,
            percentile_99_ms=percentile_99_ms,
            success_rate=success_rate,
            timestamp=datetime.now().isoformat()
        )
        
        self.save_result(result)
        return result
    
    def run_session_initialization_benchmark(self) -> BenchmarkResult:
        """Benchmark session initialization"""
        def init_session():
            from .state_manager import SessionStateManager
            manager = SessionStateManager(str(self.workspace_path), "benchmark")
            manager.cleanup()  # Clean up after each run
        
        return self.run_benchmark("session_initialization", init_session, iterations=50)
    
    def run_state_query_benchmark(self) -> BenchmarkResult:
        """Benchmark state queries"""
        # Setup test state
        from .state_manager import SessionStateManager
        manager = SessionStateManager(str(self.workspace_path), "benchmark")
        
        # Add test data
        test_data = {
            "test_agents": {f"agent-{i}": {"status": "active"} for i in range(100)},
            "test_tasks": {f"task-{i}": {"status": "completed"} for i in range(500)}
        }
        manager.set("execution.agents.active", test_data["test_agents"])
        manager.set("execution.tasks", test_data["test_tasks"])
        
        def query_state():
            result1 = manager.get("execution.agents.active")
            result2 = manager.get("execution.tasks")
            result3 = manager.get("execution.agents.active.agent-50")
            return result1, result2, result3
        
        return self.run_benchmark("state_query", query_state, iterations=200)
    
    def run_hook_processing_benchmark(self) -> BenchmarkResult:
        """Benchmark hook processing"""
        def process_hook():
            # Simulate hook processing
            import subprocess
            result = subprocess.run(
                ["echo", "test hook processing"],
                capture_output=True,
                text=True
            )
            return result.stdout
        
        return self.run_benchmark("hook_processing", process_hook, iterations=100)
    
    def run_agent_spawn_benchmark(self) -> BenchmarkResult:
        """Benchmark agent spawning simulation"""
        def spawn_agent():
            # Simulate agent spawn process (without actual Claude Code invocation)
            import time
            time.sleep(0.1)  # Simulate initialization time
            
            # Simulate state updates
            agent_data = {
                "session_id": "benchmark",
                "agent_type": "test-agent",
                "spawned_at": datetime.now().isoformat(),
                "status": "initializing"
            }
            return agent_data
        
        return self.run_benchmark("agent_spawn_simulation", spawn_agent, iterations=20)
    
    def run_dashboard_refresh_benchmark(self) -> BenchmarkResult:
        """Benchmark dashboard refresh"""
        def refresh_dashboard():
            # Simulate dashboard data collection and rendering
            from .observability import get_state
            
            state = get_state()
            
            # Simulate metrics calculation
            agents = state.get("execution", {}).get("agents", {}).get("active", {})
            tasks = state.get("execution", {}).get("tasks", {})
            
            metrics = {
                "active_agents": len(agents),
                "total_tasks": len(tasks),
                "completed_tasks": sum(1 for t in tasks.values() if t.get("status") == "completed")
            }
            
            return metrics
        
        return self.run_benchmark("dashboard_refresh", refresh_dashboard, iterations=50)
    
    def run_load_test(self, concurrent_operations: int = 10) -> Dict[str, BenchmarkResult]:
        """Run load testing with concurrent operations"""
        print(f"🔥 Running load test with {concurrent_operations} concurrent operations")
        
        operations = [
            ("state_query", self.run_state_query_benchmark),
            ("hook_processing", self.run_hook_processing_benchmark),
            ("dashboard_refresh", self.run_dashboard_refresh_benchmark)
        ]
        
        results = {}
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=concurrent_operations) as executor:
            futures = {}
            
            for op_name, op_func in operations:
                for i in range(concurrent_operations):
                    future = executor.submit(op_func)
                    futures[future] = f"{op_name}_concurrent_{i}"
            
            for future in concurrent.futures.as_completed(futures):
                op_id = futures[future]
                try:
                    result = future.result()
                    results[op_id] = result
                    print(f"✅ Completed {op_id}")
                except Exception as e:
                    print(f"❌ Failed {op_id}: {e}")
        
        return results
    
    def run_stress_test(self, duration_minutes: int = 5) -> Dict[str, List[BenchmarkResult]]:
        """Run stress test for specified duration"""
        print(f"💪 Running stress test for {duration_minutes} minutes")
        
        start_time = time.time()
        end_time = start_time + (duration_minutes * 60)
        
        results = {
            "state_queries": [],
            "hook_processes": [],
            "dashboard_refreshes": []
        }
        
        while time.time() < end_time:
            # Run quick benchmarks
            try:
                query_result = self.run_benchmark("stress_state_query", 
                                                lambda: self.workspace_path.exists(), 
                                                iterations=10)
                results["state_queries"].append(query_result)
                
                hook_result = self.run_benchmark("stress_hook_process",
                                               lambda: time.sleep(0.01),
                                               iterations=10) 
                results["hook_processes"].append(hook_result)
                
                dashboard_result = self.run_benchmark("stress_dashboard",
                                                    lambda: {"timestamp": time.time()},
                                                    iterations=10)
                results["dashboard_refreshes"].append(dashboard_result)
                
            except Exception as e:
                print(f"⚠️ Stress test iteration failed: {e}")
        
        return results
    
    def save_result(self, result: BenchmarkResult):
        """Save benchmark result to file"""
        result_file = self.results_dir / f"benchmark-{datetime.now().strftime('%Y%m%d')}.jsonl"
        
        with result_file.open('a') as f:
            f.write(json.dumps(result.__dict__) + '\n')
    
    def compare_with_baseline(self, result: BenchmarkResult) -> Dict[str, Any]:
        """Compare result with historical baseline"""
        baseline_file = self.results_dir / "baselines.json"
        
        if not baseline_file.exists():
            return {"status": "no_baseline", "message": "No baseline found for comparison"}
        
        with baseline_file.open() as f:
            baselines = json.load(f)
        
        if result.operation not in baselines:
            return {"status": "no_baseline", "message": f"No baseline for {result.operation}"}
        
        baseline = baselines[result.operation]
        baseline_mean = baseline["mean_ms"]
        
        improvement_percent = ((baseline_mean - result.mean_ms) / baseline_mean) * 100
        
        if improvement_percent > 10:
            status = "significant_improvement"
        elif improvement_percent > 0:
            status = "improvement"
        elif improvement_percent > -10:
            status = "stable"
        else:
            status = "regression"
        
        return {
            "status": status,
            "improvement_percent": improvement_percent,
            "baseline_mean_ms": baseline_mean,
            "current_mean_ms": result.mean_ms,
            "message": f"Performance {status}: {improvement_percent:+.1f}%"
        }

if __name__ == "__main__":
    import click
    from rich.console import Console
    from rich.table import Table
    
    console = Console()
    
    @click.group()
    def cli():
        """Benchmark suite for V2 orchestration system"""
        pass
    
    @cli.command()
    @click.option('--component', type=click.Choice(['session', 'state', 'hook', 'agent', 'dashboard', 'all']), default='all')
    @click.option('--iterations', type=int, default=100)
    def run(component, iterations):
        """Run benchmarks"""
        suite = BenchmarkSuite('.')
        
        components = {
            'session': suite.run_session_initialization_benchmark,
            'state': suite.run_state_query_benchmark,
            'hook': suite.run_hook_processing_benchmark,
            'agent': suite.run_agent_spawn_benchmark,
            'dashboard': suite.run_dashboard_refresh_benchmark
        }
        
        if component == 'all':
            results = {}
            for comp_name, comp_func in components.items():
                console.print(f"Running {comp_name} benchmark...")
                results[comp_name] = comp_func()
        else:
            results = {component: components[component]()}
        
        # Display results
        table = Table(title="Benchmark Results")
        table.add_column("Component", style="cyan")
        table.add_column("Mean (ms)", style="green")
        table.add_column("P95 (ms)", style="yellow")
        table.add_column("Success Rate", style="blue")
        table.add_column("Status", style="bold")
        
        for comp_name, result in results.items():
            status = "✅" if result.mean_ms < 1000 else "⚠️" if result.mean_ms < 2000 else "🔴"
            table.add_row(
                comp_name.title(),
                f"{result.mean_ms:.1f}",
                f"{result.percentile_95_ms:.1f}",
                f"{result.success_rate * 100:.1f}%",
                status
            )
        
        console.print(table)
    
    @cli.command()
    @click.option('--concurrent', type=int, default=10)
    def load(concurrent):
        """Run load testing"""
        suite = BenchmarkSuite('.')
        results = suite.run_load_test(concurrent)
        console.print(f"✅ Load test completed with {len(results)} operations")
    
    @cli.command() 
    @click.option('--duration', type=int, default=5)
    def stress(duration):
        """Run stress testing"""
        suite = BenchmarkSuite('.')
        results = suite.run_stress_test(duration)
        
        for test_type, test_results in results.items():
            if test_results:
                avg_mean = sum(r.mean_ms for r in test_results) / len(test_results)
                console.print(f"{test_type}: {len(test_results)} runs, avg {avg_mean:.1f}ms")
    
    cli()
```

## Optimization Techniques

### 1. Caching Strategies

#### Intelligent State Caching

```python
# .claude/optimization/state_cache.py
class IntelligentStateCache:
    def __init__(self, max_size_mb: int = 50):
        self.max_size_mb = max_size_mb
        self.cache = {}
        self.access_times = {}
        self.cache_stats = {"hits": 0, "misses": 0, "evictions": 0}
        
    def get(self, key: str, generator_func: Callable = None):
        """Get from cache or generate if not present"""
        if key in self.cache:
            self.access_times[key] = time.time()
            self.cache_stats["hits"] += 1
            return self.cache[key]
        
        self.cache_stats["misses"] += 1
        
        if generator_func:
            value = generator_func()
            self.set(key, value)
            return value
        
        return None
    
    def set(self, key: str, value: Any):
        """Set cache value with intelligent eviction"""
        # Check size limits
        while self._get_cache_size_mb() > self.max_size_mb:
            self._evict_lru()
        
        self.cache[key] = value
        self.access_times[key] = time.time()
    
    def _get_cache_size_mb(self) -> float:
        """Estimate cache size in MB"""
        total_size = sum(len(str(v).encode('utf-8')) for v in self.cache.values())
        return total_size / (1024 * 1024)
    
    def _evict_lru(self):
        """Evict least recently used item"""
        if not self.access_times:
            return
        
        lru_key = min(self.access_times.keys(), key=lambda k: self.access_times[k])
        del self.cache[lru_key]
        del self.access_times[lru_key]
        self.cache_stats["evictions"] += 1
```

#### Query Optimization

```python
# .claude/optimization/query_optimizer.py
class QueryOptimizer:
    def __init__(self):
        self.query_patterns = {}
        self.index_cache = {}
    
    def optimize_jsonpath_query(self, path: str, state: Dict) -> Any:
        """Optimize JSONPath query execution"""
        # Check for cached indexes
        if path in self.index_cache:
            return self._execute_indexed_query(path, state)
        
        # Analyze query pattern
        pattern = self._analyze_pattern(path)
        
        if pattern["type"] == "array_filter":
            return self._optimize_array_filter(path, state, pattern)
        elif pattern["type"] == "deep_search":
            return self._optimize_deep_search(path, state, pattern)
        else:
            return self._execute_standard_query(path, state)
    
    def _analyze_pattern(self, path: str) -> Dict:
        """Analyze query pattern for optimization opportunities"""
        if "[" in path and "]" in path:
            return {"type": "array_filter", "complexity": "high"}
        elif path.count(".") > 5:
            return {"type": "deep_search", "complexity": "medium"}
        else:
            return {"type": "simple", "complexity": "low"}
    
    def _optimize_array_filter(self, path: str, state: Dict, pattern: Dict) -> Any:
        """Optimize array filtering operations"""
        # Build index for commonly queried arrays
        array_path = path.split("[")[0]
        if array_path not in self.index_cache:
            self._build_array_index(array_path, state)
        
        return self._execute_indexed_query(path, state)
```

### 2. Memory Management

#### Intelligent Memory Management

```python
# .claude/optimization/memory_manager.py
class MemoryManager:
    def __init__(self, max_memory_mb: int = 500):
        self.max_memory_mb = max_memory_mb
        self.memory_pools = {
            "state": [],
            "cache": [],
            "temp": []
        }
        
    def monitor_memory_usage(self):
        """Monitor and manage memory usage"""
        current_usage = self._get_memory_usage_mb()
        
        if current_usage > self.max_memory_mb * 0.8:
            self._trigger_cleanup()
        
        if current_usage > self.max_memory_mb * 0.95:
            self._aggressive_cleanup()
    
    def _get_memory_usage_mb(self) -> float:
        """Get current memory usage"""
        import psutil
        process = psutil.Process()
        return process.memory_info().rss / (1024 * 1024)
    
    def _trigger_cleanup(self):
        """Trigger standard cleanup operations"""
        # Clear temporary data
        self.memory_pools["temp"].clear()
        
        # Compress large objects
        self._compress_large_objects()
        
        # Run garbage collection
        import gc
        gc.collect()
    
    def _aggressive_cleanup(self):
        """Trigger aggressive cleanup when memory is critical"""
        self._trigger_cleanup()
        
        # Clear all caches
        self.memory_pools["cache"].clear()
        
        # Force state persistence
        # This would integrate with the state manager
        
        # Archive old data
        self._archive_old_data()
```

### 3. I/O Optimization

#### Asynchronous I/O Manager

```python
# .claude/optimization/async_io.py
import asyncio
import aiofiles
from concurrent.futures import ThreadPoolExecutor

class AsyncIOManager:
    def __init__(self, max_workers: int = 4):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.read_cache = {}
        
    async def read_file_async(self, file_path: Path) -> str:
        """Async file reading with caching"""
        cache_key = f"{file_path}:{file_path.stat().st_mtime}"
        
        if cache_key in self.read_cache:
            return self.read_cache[cache_key]
        
        async with aiofiles.open(file_path, 'r') as f:
            content = await f.read()
            self.read_cache[cache_key] = content
            return content
    
    async def write_file_async(self, file_path: Path, content: str):
        """Async file writing"""
        async with aiofiles.open(file_path, 'w') as f:
            await f.write(content)
    
    async def batch_read_files(self, file_paths: List[Path]) -> Dict[Path, str]:
        """Batch read multiple files asynchronously"""
        tasks = [self.read_file_async(path) for path in file_paths]
        results = await asyncio.gather(*tasks)
        
        return dict(zip(file_paths, results))
```

## Observability Integration

### 1. Metrics Export Framework

```python
# .claude/observability/metrics_exporter.py
class MetricsExporter:
    def __init__(self, export_formats: List[str] = None):
        self.export_formats = export_formats or ["prometheus", "json", "csv"]
        self.exporters = {
            "prometheus": self._export_prometheus,
            "json": self._export_json,
            "csv": self._export_csv,
            "grafana": self._export_grafana
        }
    
    def export_metrics(self, metrics: PerformanceMetrics, format: str = "json") -> str:
        """Export metrics in specified format"""
        if format not in self.exporters:
            raise ValueError(f"Unsupported export format: {format}")
        
        return self.exporters[format](metrics)
    
    def _export_prometheus(self, metrics: PerformanceMetrics) -> str:
        """Export metrics in Prometheus format"""
        return f"""
# HELP session_init_time_ms Session initialization time in milliseconds
# TYPE session_init_time_ms gauge
session_init_time_ms {metrics.session_init_time_ms}

# HELP state_query_time_ms Average state query time in milliseconds
# TYPE state_query_time_ms gauge
state_query_time_ms {metrics.state_query_avg_ms}

# HELP active_agents Number of active agents
# TYPE active_agents gauge
active_agents {metrics.active_agents}

# HELP success_rate_percent Task success rate percentage
# TYPE success_rate_percent gauge
success_rate_percent {metrics.success_rate_percent}

# HELP cpu_usage_percent CPU usage percentage
# TYPE cpu_usage_percent gauge
cpu_usage_percent {metrics.cpu_usage_percent}

# HELP memory_usage_percent Memory usage percentage
# TYPE memory_usage_percent gauge
memory_usage_percent {metrics.memory_usage_percent}
        """.strip()
    
    def _export_json(self, metrics: PerformanceMetrics) -> str:
        """Export metrics in JSON format"""
        return json.dumps(asdict(metrics), indent=2)
    
    def _export_csv(self, metrics: PerformanceMetrics) -> str:
        """Export metrics in CSV format"""
        import csv
        import io
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Header
        writer.writerow(list(asdict(metrics).keys()))
        
        # Data
        writer.writerow(list(asdict(metrics).values()))
        
        return output.getvalue()
```

### 2. Status Line Integration

```python
# .claude/status/orchestration_status.py
def get_orchestration_status() -> Dict[str, Any]:
    """Generate orchestration status for status line"""
    try:
        monitor = get_monitor()
        metrics = monitor.collect_current_metrics()
        
        # Determine overall health
        health_score = calculate_health_score(metrics)
        health_indicator = "🟢" if health_score > 0.8 else "🟡" if health_score > 0.6 else "🔴"
        
        return {
            "health": {
                "indicator": health_indicator,
                "score": health_score,
                "status": "healthy" if health_score > 0.8 else "degraded" if health_score > 0.6 else "critical"
            },
            "performance": {
                "session_init": f"{metrics.session_init_time_ms:.0f}ms",
                "state_query": f"{metrics.state_query_avg_ms:.0f}ms",
                "agents": metrics.active_agents
            },
            "resources": {
                "cpu": f"{metrics.cpu_usage_percent:.0f}%",
                "memory": f"{metrics.memory_usage_percent:.0f}%",
                "efficiency": f"{metrics.resource_efficiency_score * 100:.0f}%"
            },
            "business": {
                "success_rate": f"{metrics.success_rate_percent:.0f}%",
                "tasks_per_hour": f"{metrics.tasks_completed_per_hour:.0f}",
                "quality": f"{metrics.code_quality_score:.1f}"
            }
        }
    except Exception as e:
        return {
            "health": {"indicator": "❓", "status": "unknown", "error": str(e)},
            "performance": {},
            "resources": {},
            "business": {}
        }

def calculate_health_score(metrics: PerformanceMetrics) -> float:
    """Calculate overall system health score (0-1)"""
    scores = []
    
    # Performance scores (higher is better for these metrics)
    if metrics.session_init_time_ms <= 100:
        scores.append(1.0)
    elif metrics.session_init_time_ms <= 200:
        scores.append(0.8)
    else:
        scores.append(0.5)
    
    if metrics.state_query_avg_ms <= 50:
        scores.append(1.0)
    elif metrics.state_query_avg_ms <= 100:
        scores.append(0.8)
    else:
        scores.append(0.5)
    
    # Resource scores (lower is better for usage percentages)
    if metrics.cpu_usage_percent <= 60:
        scores.append(1.0)
    elif metrics.cpu_usage_percent <= 80:
        scores.append(0.8)
    else:
        scores.append(0.5)
    
    if metrics.memory_usage_percent <= 60:
        scores.append(1.0)
    elif metrics.memory_usage_percent <= 80:
        scores.append(0.8)
    else:
        scores.append(0.5)
    
    # Business scores
    if metrics.success_rate_percent >= 95:
        scores.append(1.0)
    elif metrics.success_rate_percent >= 90:
        scores.append(0.8)
    else:
        scores.append(0.5)
    
    return sum(scores) / len(scores)
```

### 3. Event Stream Monitoring

```python
# .claude/observability/event_monitor.py
class EventStreamMonitor:
    def __init__(self, session_manager):
        self.session_manager = session_manager
        self.alert_rules = self.load_alert_rules()
        
    def monitor_event_stream(self):
        """Monitor event stream for patterns and anomalies"""
        event_log = self.session_manager.event_log
        
        if not event_log.exists():
            return
        
        # Read recent events
        recent_events = self._get_recent_events(minutes=10)
        
        # Check for patterns
        self._check_error_patterns(recent_events)
        self._check_performance_patterns(recent_events)
        self._check_resource_patterns(recent_events)
    
    def _get_recent_events(self, minutes: int = 10) -> List[Dict]:
        """Get events from the last N minutes"""
        cutoff_time = datetime.now() - timedelta(minutes=minutes)
        recent_events = []
        
        with self.session_manager.event_log.open('r') as f:
            for line in f:
                try:
                    event = json.loads(line.strip())
                    event_time = datetime.fromisoformat(event["timestamp"])
                    
                    if event_time >= cutoff_time:
                        recent_events.append(event)
                except (json.JSONDecodeError, KeyError):
                    continue
        
        return recent_events
    
    def _check_error_patterns(self, events: List[Dict]):
        """Check for error patterns in events"""
        error_events = [e for e in events if e.get("severity") in ["error", "critical"]]
        
        if len(error_events) > 5:  # More than 5 errors in 10 minutes
            self._emit_alert("high_error_rate", {
                "error_count": len(error_events),
                "time_window": "10 minutes",
                "recommendation": "Investigate recent changes and error patterns"
            })
    
    def _check_performance_patterns(self, events: List[Dict]):
        """Check for performance degradation patterns"""
        perf_events = [e for e in events if "time_ms" in e.get("data", {})]
        
        if perf_events:
            avg_time = sum(e["data"]["time_ms"] for e in perf_events) / len(perf_events)
            
            if avg_time > 1000:  # Average operation time > 1 second
                self._emit_alert("performance_degradation", {
                    "average_time_ms": avg_time,
                    "affected_operations": len(perf_events),
                    "recommendation": "Check system resources and optimize slow operations"
                })
    
    def _emit_alert(self, alert_type: str, data: Dict):
        """Emit an alert event"""
        self.session_manager._emit_event("performance_alert", {
            "alert_type": alert_type,
            "severity": "warning",
            "data": data,
            "timestamp": datetime.now().isoformat()
        })
```

## Performance Debugging Tools

### 1. Performance Profiler

```python
# .claude/debug/profiler.py
class PerformanceProfiler:
    def __init__(self):
        self.active_traces = {}
        self.completed_traces = []
        
    def start_trace(self, operation_id: str, operation_name: str):
        """Start tracing an operation"""
        self.active_traces[operation_id] = {
            "name": operation_name,
            "start_time": time.perf_counter(),
            "events": []
        }
    
    def add_event(self, operation_id: str, event_name: str, data: Dict = None):
        """Add an event to an active trace"""
        if operation_id in self.active_traces:
            self.active_traces[operation_id]["events"].append({
                "name": event_name,
                "timestamp": time.perf_counter(),
                "data": data or {}
            })
    
    def end_trace(self, operation_id: str):
        """End tracing and calculate metrics"""
        if operation_id not in self.active_traces:
            return None
        
        trace = self.active_traces.pop(operation_id)
        trace["end_time"] = time.perf_counter()
        trace["duration_ms"] = (trace["end_time"] - trace["start_time"]) * 1000
        
        self.completed_traces.append(trace)
        return trace
    
    def generate_flame_graph_data(self) -> Dict:
        """Generate data for flame graph visualization"""
        flame_data = []
        
        for trace in self.completed_traces:
            flame_entry = {
                "name": trace["name"],
                "duration": trace["duration_ms"],
                "children": []
            }
            
            # Add events as children
            for event in trace["events"]:
                event_duration = event.get("data", {}).get("duration_ms", 1)
                flame_entry["children"].append({
                    "name": event["name"],
                    "duration": event_duration
                })
            
            flame_data.append(flame_entry)
        
        return {"flame_graph": flame_data}
```

### 2. Real-time Performance Dashboard

```python
# .claude/debug/realtime_dashboard.py
class RealtimePerformanceDashboard:
    def __init__(self, refresh_interval: float = 1.0):
        self.refresh_interval = refresh_interval
        self.running = False
        
    def start_dashboard(self):
        """Start the real-time dashboard"""
        self.running = True
        
        with Live(self._generate_dashboard(), refresh_per_second=1/self.refresh_interval) as live:
            while self.running:
                time.sleep(self.refresh_interval)
                live.update(self._generate_dashboard())
    
    def stop_dashboard(self):
        """Stop the dashboard"""
        self.running = False
    
    def _generate_dashboard(self) -> Layout:
        """Generate the dashboard layout"""
        layout = Layout()
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="metrics", size=15),
            Layout(name="charts", size=10)
        )
        
        # Header
        layout["header"].update(Panel(
            f"[bold]Real-time Performance Dashboard[/bold] - {datetime.now().strftime('%H:%M:%S')}"
        ))
        
        # Metrics
        monitor = get_monitor()
        metrics = monitor.collect_current_metrics()
        
        metrics_layout = Layout()
        metrics_layout.split_row(
            Layout(name="performance"),
            Layout(name="resources"),
            Layout(name="business")
        )
        
        # Performance table
        perf_table = Table(title="⚡ Performance")
        perf_table.add_column("Metric")
        perf_table.add_column("Value")
        perf_table.add_column("Target")
        perf_table.add_column("Status")
        
        perf_metrics = [
            ("Session Init", f"{metrics.session_init_time_ms:.1f}ms", "< 100ms"),
            ("State Query", f"{metrics.state_query_avg_ms:.1f}ms", "< 50ms"),
            ("Hook Process", f"{metrics.hook_processing_avg_ms:.1f}ms", "< 200ms"),
            ("Agent Spawn", f"{metrics.agent_spawn_avg_ms:.1f}ms", "< 1000ms"),
            ("Dashboard", f"{metrics.dashboard_refresh_ms:.1f}ms", "< 500ms")
        ]
        
        for name, value, target in perf_metrics:
            # Extract numeric value for comparison
            numeric_value = float(value.replace('ms', ''))
            target_value = float(target.replace('< ', '').replace('ms', ''))
            
            status = "✅" if numeric_value <= target_value else "⚠️" if numeric_value <= target_value * 1.5 else "🔴"
            perf_table.add_row(name, value, target, status)
        
        metrics_layout["performance"].update(perf_table)
        
        # Resource table
        resource_table = Table(title="💻 Resources")
        resource_table.add_column("Resource")
        resource_table.add_column("Usage")
        resource_table.add_column("Status")
        
        resource_table.add_row("CPU", f"{metrics.cpu_usage_percent:.1f}%", 
                             "✅" if metrics.cpu_usage_percent < 80 else "🔴")
        resource_table.add_row("Memory", f"{metrics.memory_usage_percent:.1f}%",
                             "✅" if metrics.memory_usage_percent < 75 else "🔴")
        resource_table.add_row("Agents", f"{metrics.active_agents}",
                             "✅" if metrics.active_agents > 0 else "⚠️")
        
        metrics_layout["resources"].update(resource_table)
        
        # Business table
        business_table = Table(title="📊 Business")
        business_table.add_column("KPI")
        business_table.add_column("Value")
        business_table.add_column("Status")
        
        business_table.add_row("Success Rate", f"{metrics.success_rate_percent:.1f}%",
                             "✅" if metrics.success_rate_percent > 90 else "🔴")
        business_table.add_row("Tasks/Hour", f"{metrics.tasks_completed_per_hour:.0f}",
                             "✅" if metrics.tasks_completed_per_hour > 10 else "⚠️")
        business_table.add_row("Quality", f"{metrics.code_quality_score:.1f}/10",
                             "✅" if metrics.code_quality_score > 8 else "⚠️")
        
        metrics_layout["business"].update(business_table)
        
        layout["metrics"].update(metrics_layout)
        
        # Charts (simplified text-based charts)
        charts_panel = Panel(self._generate_ascii_charts(metrics), title="📈 Trends")
        layout["charts"].update(charts_panel)
        
        return layout
    
    def _generate_ascii_charts(self, metrics: PerformanceMetrics) -> str:
        """Generate simple ASCII charts"""
        return f"""
CPU Usage Trend:     {self._create_sparkline([70, 65, 68, 72, 75, metrics.cpu_usage_percent])}
Memory Usage:        {self._create_sparkline([45, 48, 52, 55, 58, metrics.memory_usage_percent])}
Success Rate:        {self._create_sparkline([92, 94, 96, 95, 97, metrics.success_rate_percent])}
        """.strip()
    
    def _create_sparkline(self, values: List[float], width: int = 20) -> str:
        """Create a simple ASCII sparkline"""
        if not values:
            return "─" * width
        
        min_val = min(values)
        max_val = max(values)
        range_val = max_val - min_val or 1
        
        chars = "▁▂▃▄▅▆▇█"
        sparkline = ""
        
        for value in values[-width:]:
            normalized = (value - min_val) / range_val
            char_index = int(normalized * (len(chars) - 1))
            sparkline += chars[char_index]
        
        return sparkline
```

## Implementation Timeline

### Phase 1: Core Monitoring Infrastructure (Week 1-2)
- [ ] Implement `PerformanceMonitor` class
- [ ] Create basic metrics collection 
- [ ] Set up benchmark framework
- [ ] Integrate with existing observability script

### Phase 2: Dashboard & Real-time Monitoring (Week 3-4)
- [ ] Enhance dashboard with performance metrics
- [ ] Implement real-time monitoring
- [ ] Create alert system
- [ ] Add status line integration

### Phase 3: Optimization Tools (Week 5-6)
- [ ] Implement caching strategies
- [ ] Add memory management
- [ ] Create I/O optimization
- [ ] Build profiling tools

### Phase 4: Advanced Features (Week 7-8)
- [ ] Add predictive analytics
- [ ] Implement automated tuning
- [ ] Create performance regression detection
- [ ] Build comprehensive reporting

## Success Criteria

- [ ] All performance targets consistently met
- [ ] Real-time monitoring operational
- [ ] Automated alerting functional
- [ ] Optimization tools reducing bottlenecks
- [ ] Comprehensive benchmark suite running
- [ ] Performance regression detection working
- [ ] Status line integration complete
- [ ] Export formats operational

## Conclusion

This comprehensive performance monitoring strategy provides the foundation for maintaining optimal performance in the v2 orchestration system. By implementing proactive monitoring, intelligent optimization, and comprehensive benchmarking, the system can scale efficiently while maintaining the responsive user experience critical for development workflows.

The strategy balances real-time observability with predictive analytics, enabling both reactive problem-solving and proactive performance management. This ensures the orchestration system remains performant as complexity and usage grow.