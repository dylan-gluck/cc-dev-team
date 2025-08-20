---
allowed-tools: Bash(python:*), Read, Task
description: Live monitoring mode with auto-refresh and real-time updates
argument-hint: [refresh-seconds] [panels]
model: haiku
---

# Live Monitoring Mode

Activate real-time monitoring with auto-refresh, streaming updates, and interactive dashboard panels.

## Context
- Refresh interval: $ARGUMENTS (default: 5 seconds)
- Monitoring script: @.claude/scripts/observability.py

## Live Dashboard Configuration

### Display Layout
```
╭────────────────── LIVE MONITORING ──────────────────╮
│ Refresh: Every 5s    Started: 14:32:15    ⚡ LIVE   │
╰──────────────────────────────────────────────────────╯

┌─────── System ────────┬──────── Agents ────────┐
│ CPU:    45% ████░░░░ │ Active:  15/32 (47%)   │
│ Memory: 62% ██████░░ │ Busy:    3 agents       │
│ Disk:   38% ███░░░░░ │ Idle:    12 agents      │
│ Net I/O: 125 MB/s    │ Error:   1 agent        │
└───────────────────────┴─────────────────────────┘

┌─────── Tasks ─────────┬──────── Sprint ────────┐
│ In Progress: 23       │ Day 8/14 (57%)         │
│ Completed:   198      │ Velocity: 5.6 pts/day  │
│ Failed:      3        │ Behind: -6%            │
│ Blocked:     5        │ At Risk: Yes           │
└───────────────────────┴─────────────────────────┘

┌──────────── Live Activity Feed ────────────────┐
│ [14:32:45] eng-fullstack completed TASK-142    │
│ [14:32:38] qa-analyst started TASK-201         │
│ [14:32:31] High memory warning (82%)           │
│ [14:32:24] eng-api failed TASK-155             │
│ [14:32:17] Sprint velocity updated             │
└─────────────────────────────────────────────────┘
```

## Live Monitoring Features

### 1. Auto-Refresh Control
```python
# Start live monitoring with custom interval
python .claude/scripts/observability.py monitor \
  --interval=${REFRESH:-5} \
  --metrics=cpu,memory,tasks,agents
```

### 2. Panel Selection
Available panels to display:
- `system` - System resources (CPU, Memory, Disk, Network)
- `agents` - Agent status and utilization
- `tasks` - Task pipeline and progress
- `sprint` - Sprint burndown and velocity
- `events` - Live event stream
- `alerts` - Critical alerts and warnings
- `metrics` - Performance KPIs
- `teams` - Team utilization

### 3. Interactive Controls
```
Keyboard Shortcuts:
  [Space]  - Pause/Resume updates
  [R]      - Force refresh now
  [F]      - Toggle fullscreen
  [↑/↓]    - Scroll event feed
  [1-8]    - Toggle panels on/off
  [Q]      - Quit monitoring
  [H]      - Show help
  [S]      - Save snapshot
  [E]      - Export data
```

### 4. Alert Notifications
```
🚨 REAL-TIME ALERTS
────────────────────────────────────────
⚠️ [14:32:31] Memory usage critical (82%)
🔴 [14:32:24] Agent eng-api error state
⚠️ [14:28:15] Database connection slow
🟡 [14:15:42] Sprint behind schedule
────────────────────────────────────────
Auto-dismiss after 30 seconds
```

### 5. Performance Graphs
```
CPU Usage (Last 60 seconds)
100% ┤
 80% ┤      ╱╲    ╱╲
 60% ┤   ╱╲╱  ╲╱╲╱  ╲
 40% ┤╱╲╱          ╲╱
 20% ┤
  0% └────────────────────
     -60s  -40s  -20s  Now

Memory Usage (Last 60 seconds)  
100% ┤
 80% ┤         ╱────────
 60% ┤   ╱────╱
 40% ┤──╱
 20% ┤
  0% └────────────────────
     -60s  -40s  -20s  Now
```

### 6. Status Indicators
```
Visual Status Indicators:
  🟢 Healthy    - All systems normal
  🟡 Warning    - Attention needed
  🔴 Critical   - Immediate action required
  🔵 Info       - Informational
  ⚡ Live       - Real-time data
  ⏸️ Paused     - Updates paused
  🔄 Refreshing - Updating data
  📡 Connected  - Stream active
  ❌ Error      - Connection lost
```

## Live Monitoring Modes

### Default Mode
Balanced view with all essential panels:
```bash
python .claude/scripts/observability.py monitor
```

### Performance Mode
Focus on system and agent performance:
```bash
python .claude/scripts/observability.py monitor \
  --interval=2 \
  --metrics=cpu,memory,agents
```

### Sprint Mode
Focus on sprint progress and tasks:
```bash
python .claude/scripts/observability.py monitor \
  --interval=10 \
  --metrics=tasks,sprint
```

### Alert Mode
Focus on events and alerts:
```bash
python .claude/scripts/observability.py monitor \
  --interval=1 \
  --metrics=events,alerts
```

## Data Export

### Live Export Options
- **Screenshot**: Save current dashboard state
- **JSON Stream**: Export live data feed
- **CSV Metrics**: Export performance data
- **PDF Report**: Generate monitoring report

### Export Commands
```bash
# Export current snapshot
[S] → saves to ~/monitoring-snapshot-{timestamp}.png

# Export data stream
[E] → saves to ~/monitoring-data-{timestamp}.json

# Generate report
[P] → creates ~/monitoring-report-{timestamp}.pdf
```

## Performance Optimization

### Refresh Strategy
- Fast refresh (1-2s): Critical monitoring
- Normal refresh (5s): Standard monitoring
- Slow refresh (10-30s): Resource conservation
- Adaptive: Adjust based on activity level

### Resource Management
- Limit panels to reduce load
- Use sampling for high-frequency data
- Cache static information
- Batch API calls

## Alert Configuration

### Alert Priorities
1. **Critical** - System failures, errors
2. **High** - Performance degradation
3. **Medium** - Capacity warnings
4. **Low** - Informational notices

### Alert Actions
- Visual highlight in dashboard
- Sound notification (if enabled)
- Log to file
- Send to external systems

## Troubleshooting

### Common Issues
- **High CPU**: Reduce refresh rate
- **Network lag**: Check connection
- **Missing data**: Verify data source
- **Display issues**: Resize terminal

### Debug Mode
```bash
python .claude/scripts/observability.py monitor \
  --debug \
  --log-level=DEBUG
```

## Integration Points

### External Systems
- Grafana dashboard export
- Prometheus metrics endpoint
- Slack notifications
- PagerDuty alerts
- Datadog integration

### API Endpoints
- `/metrics` - Prometheus format
- `/health` - Health check
- `/events` - Event stream
- `/snapshot` - Current state

## Success Criteria

- [ ] Live updates working smoothly
- [ ] All panels refreshing correctly
- [ ] Keyboard controls responsive
- [ ] Alerts displayed prominently
- [ ] Performance optimized
- [ ] Export functions operational