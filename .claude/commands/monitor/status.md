---
allowed-tools: Bash(python:*), Read
description: Real-time system status overview with health indicators
argument-hint: [team|agent-name] [--json]
model: haiku
---

# System Status Overview

Display current system status with health indicators, agent states, and task summaries.

## Context
- Status check script: !`python .claude/scripts/observability.py status --format=summary`
- Filter criteria: $ARGUMENTS

## Status Report Sections

### 1. System Health Check
```
🏥 SYSTEM HEALTH STATUS
├─ Overall Health: [Healthy|Warning|Critical]
├─ Uptime: [duration]
├─ Last Check: [timestamp]
└─ Alert Count: [number]
```

### 2. Resource Utilization
```
📊 RESOURCE METRICS
├─ CPU Usage:    ████████░░ 78% ⚠️
├─ Memory:       ██████░░░░ 62% ✅
├─ Disk I/O:     ███░░░░░░░ 30% ✅
└─ Network:      ████░░░░░░ 45% ✅
```

### 3. Agent Fleet Status
```
🤖 AGENT STATUS (25 total)
├─ 🟢 Active:    12 agents (48%)
├─ 🔵 Idle:      8 agents (32%)
├─ 🟡 Busy:      3 agents (12%)
├─ 🔴 Error:     1 agent (4%)
└─ ⚫ Offline:   1 agent (4%)
```

### 4. Task Pipeline Status
```
📋 TASK PIPELINE
├─ Backlog:      34 tasks
├─ In Progress:  15 tasks (12 agents)
├─ Completed:    89 tasks today
├─ Failed:       3 tasks
└─ Blocked:      5 tasks
```

### 5. Team Performance
```
👥 TEAM PERFORMANCE
├─ Engineering:  85% utilization, 95% success
├─ QA:          72% utilization, 98% success
├─ DevOps:      91% utilization, 92% success
├─ Product:     68% utilization, 100% success
└─ Research:    55% utilization, 97% success
```

### 6. Critical Alerts
```
🚨 ACTIVE ALERTS
├─ ⚠️ High memory usage on devops-cicd (82%)
├─ 🔴 Agent engineering-api in error state
├─ ⚠️ Sprint velocity below target (65%)
└─ ⚠️ 5 tasks blocked > 2 hours
```

## Execution Commands

Basic status:
```bash
python .claude/scripts/observability.py status --format=table
```

Filtered by team:
```bash
python .claude/scripts/observability.py status --format=table --agent=$TEAM
```

JSON output:
```bash
python .claude/scripts/observability.py status --format=json
```

## Quick Actions

Based on status, suggest actions:

### If High Resource Usage:
- Scale down non-critical agents
- Clear completed task logs
- Optimize running processes

### If Agents in Error State:
- Check agent logs
- Restart failed agents
- Escalate to DevOps team

### If Tasks Blocked:
- Identify dependencies
- Reassign to available agents
- Clear blocking issues

## Status Indicators

Use consistent indicators:
- 🟢 Healthy/Good (>90%)
- 🔵 Idle/Available
- 🟡 Warning (70-90%)
- 🔴 Critical (<70%)
- ⚫ Offline/Disabled
- ✅ Success/Complete
- ❌ Failed/Error
- ⚠️ Warning/Attention
- 🚨 Alert/Critical

## Refresh Options

- Static snapshot (default)
- Auto-refresh every N seconds
- Watch mode for continuous monitoring

## Export Formats

- Console table (Rich formatted)
- JSON (machine readable)
- Summary text (human readable)
- CSV (for spreadsheets)

## Success Criteria

- [ ] All status sections displayed
- [ ] Health indicators accurate
- [ ] Alerts prominently shown
- [ ] Performance metrics calculated
- [ ] Team breakdown included
- [ ] Actionable recommendations provided