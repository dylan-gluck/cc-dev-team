---
allowed-tools: Bash(python:*), Read, Task
description: Main monitoring dashboard showing comprehensive system overview
argument-hint: [refresh-interval] [filter]
model: haiku
---

# System Monitoring Dashboard

Display comprehensive real-time monitoring dashboard with system metrics, agent status, and task overview.

## Context
- Observability script: @.claude/scripts/observability.py
- User preferences: $ARGUMENTS

## Dashboard Components

### 1. System Overview Panel
Display real-time system metrics:
- CPU and Memory usage with health indicators
- Active agents and utilization percentage
- Tasks in progress and completion rate
- Error rate and performance trends
- Last update timestamp

### 2. Agent Status Grid
Show all agents with:
- Current status (active/idle/busy/error/offline)
- Team affiliation and specialization
- Current task assignment
- Performance score
- Tasks completed/failed count
- Last active timestamp

### 3. Task Pipeline View
Visualize task flow:
- Pending tasks queue
- In-progress tasks with assignees
- Completed tasks today
- Failed/blocked tasks requiring attention
- Priority distribution

### 4. Sprint Progress
Current sprint information:
- Sprint name and timeline
- Days remaining with urgency indicator
- Task completion percentage
- Velocity and burndown rate
- Sprint goals checklist

## Execution

Run the observability dashboard with appropriate options:
```bash
python .claude/scripts/observability.py status --format=table
```

If refresh interval specified in $ARGUMENTS:
```bash
python .claude/scripts/observability.py monitor --interval=$INTERVAL
```

## Display Format

Use Rich formatting for beautiful console output:
- Color-coded status indicators (🟢 good, 🟡 warning, 🔴 critical)
- Box-drawing characters for panels
- Progress bars for completion metrics
- Aligned columns and grids
- Responsive layout

## Interactive Features

- Auto-refresh at specified intervals
- Filter by team or status if provided
- Highlight critical issues
- Show trend indicators (📈 📉 ➡️)

## Alert Conditions

Highlight when:
- CPU/Memory > 80% (critical)
- Error rate > 5% (critical)
- Agent utilization < 30% (warning)
- Sprint behind schedule (warning)
- Blocked tasks > 5 (warning)

## Export Options

Provide data in multiple formats:
- Table view (default) - Rich formatted console
- JSON export - For integration with other tools
- Summary text - Quick status overview

## Example Output

```
╭─────────────── System Metrics Dashboard ───────────────╮
│                                                         │
│  System          Agents          Tasks                 │
│  CPU: 45.2% 🟢   Active: 12/25   In Progress: 15      │
│  Mem: 62.1% 🟡   Util: 48% 🟡    Completed: 23 ✅     │
│  Err: 0.8% 🟢    Teams: 8        Avg Time: 3.2h       │
│                                                         │
╰────────── Last Updated: 2025-08-20 14:32:15 ──────────╯
```

## Success Criteria

- [ ] All metrics displayed clearly
- [ ] Real-time updates working
- [ ] Color coding applied correctly
- [ ] Responsive to terminal size
- [ ] Performance optimized
- [ ] Alerts visible for critical issues