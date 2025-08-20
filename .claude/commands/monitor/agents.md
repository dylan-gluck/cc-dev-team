---
allowed-tools: Bash(python:*), Read, Grep
description: Monitor active agents performance and utilization in real-time
argument-hint: [team-name] [--watch]
model: haiku
---

# Agent Monitoring Dashboard

Monitor all agents across teams with performance metrics, utilization, and task assignments.

## Context
- Agent status: !`python .claude/scripts/observability.py status --format=json | jq '.agents'`
- Team filter: $ARGUMENTS

## Agent Performance Dashboard

### 1. Agent Fleet Overview
```
╭──────────────── AGENT FLEET MONITOR ────────────────╮
│ Total Agents: 32    Active: 15    Utilization: 47%  │
│ Teams: 8            Idle: 12      Efficiency: 89%   │
│ Online: 30          Busy: 3       Success Rate: 94% │
╰──────────────────────────────────────────────────────╯
```

### 2. Team-by-Team Breakdown

#### Engineering Team (8 agents)
```
┌─────────────────┬────────┬─────────┬──────────┬───────────┬──────┐
│ Agent           │ Status │ Current │ Complete │ Perf Score│ Load │
├─────────────────┼────────┼─────────┼──────────┼───────────┼──────┤
│ eng-fullstack   │ 🟢 Active│ TASK-142│    45    │    95%    │ ████ │
│ eng-api         │ 🟢 Active│ TASK-156│    52    │    92%    │ ████ │
│ eng-ux          │ 🔵 Idle  │    -    │    38    │    88%    │ ░░░░ │
│ eng-lead        │ 🟡 Busy  │ Review  │    67    │    97%    │ ████ │
└─────────────────┴────────┴─────────┴──────────┴───────────┴──────┘
```

#### QA Team (4 agents)
```
┌─────────────────┬────────┬─────────┬──────────┬───────────┬──────┐
│ Agent           │ Status │ Current │ Complete │ Perf Score│ Load │
├─────────────────┼────────┼─────────┼──────────┼───────────┼──────┤
│ qa-director     │ 🟢 Active│ TASK-189│    34    │    96%    │ ███░ │
│ qa-analyst      │ 🟢 Active│ TASK-201│    41    │    94%    │ ████ │
│ qa-e2e          │ 🔵 Idle  │    -    │    29    │    91%    │ ░░░░ │
│ qa-scripts      │ 🟢 Active│ TASK-198│    38    │    89%    │ ██░░ │
└─────────────────┴────────┴─────────┴──────────┴───────────┴──────┘
```

### 3. Performance Metrics

#### Top Performers (by completion rate)
```
🏆 TOP PERFORMERS
1. eng-lead        - 67 tasks, 97% success, 2.3h avg
2. eng-api         - 52 tasks, 92% success, 3.1h avg
3. eng-fullstack   - 45 tasks, 95% success, 2.8h avg
4. qa-analyst      - 41 tasks, 94% success, 1.9h avg
5. qa-scripts      - 38 tasks, 89% success, 2.5h avg
```

#### Agents Needing Attention
```
⚠️ ATTENTION REQUIRED
• eng-backend     - Error state for 15 minutes
• devops-release  - 3 failed tasks in last hour
• data-scientist  - Idle for >2 hours
• creative-illustrator - Performance below 70%
```

### 4. Task Distribution

```
📊 TASK ASSIGNMENT MATRIX
                 Pending  Active  Complete  Failed
Engineering:        12      5       89        2
QA:                 8       3       45        1
DevOps:            5       2       38        0
Product:           3       1       29        0
Research:          6       2       18        0
Creative:          4       1       15        0
Data:              2       1       12        0
Meta:              1       0       8         0
```

### 5. Agent Utilization Timeline

```
📈 24-HOUR UTILIZATION
100% ┤
 90% ┤      ╭─╮    ╭───╮
 80% ┤   ╭──╯ ╰────╯   ╰─╮
 70% ┤ ╭─╯               ╰─╮
 60% ┤─╯                   ╰─────
 50% ┤
     └─────────────────────────────
     00:00  06:00  12:00  18:00  24:00
```

### 6. Real-time Activity Feed

```
🔄 LIVE AGENT ACTIVITY
[14:32:15] eng-fullstack completed TASK-142 (2.3h)
[14:31:42] qa-analyst started TASK-201
[14:30:28] eng-api failed TASK-155 (timeout)
[14:29:51] devops-cicd completed deployment
[14:28:33] eng-ux became idle
[14:27:19] product-manager assigned TASK-203
```

## Monitoring Commands

Full agent dashboard:
```bash
python .claude/scripts/observability.py status --format=table
```

Watch mode (auto-refresh):
```bash
python .claude/scripts/observability.py monitor --interval=5 --metrics=agents
```

Team-specific view:
```bash
python .claude/scripts/observability.py status --agent=$TEAM
```

## Alert Thresholds

- 🔴 Critical: Agent error state > 5 minutes
- 🟡 Warning: Performance < 80%
- 🟡 Warning: Idle time > 1 hour
- 🔴 Critical: Failed tasks > 5 in last hour
- 🟡 Warning: Utilization < 30% (team level)

## Optimization Recommendations

Based on current metrics:

### Load Balancing
- Redistribute tasks from busy agents
- Activate idle agents for pending work
- Scale teams with high utilization

### Performance Tuning
- Review agents with low scores
- Analyze failed task patterns
- Optimize task assignment algorithm

### Capacity Planning
- Identify bottleneck teams
- Forecast resource needs
- Plan agent scaling strategy

## Export Options

- Live dashboard (Rich formatted)
- JSON metrics (API integration)
- CSV report (analysis)
- Prometheus metrics (monitoring)

## Success Criteria

- [ ] All agents monitored
- [ ] Performance metrics accurate
- [ ] Utilization calculated correctly
- [ ] Alerts triggered appropriately
- [ ] Activity feed updated real-time
- [ ] Recommendations actionable