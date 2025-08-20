---
allowed-tools: Bash(python:*), Read, Grep
description: Stream recent events and activity from the orchestration system
argument-hint: [filter-type] [--follow]
model: haiku
---

# Event Stream Monitor

Stream and monitor real-time events, activities, and system notifications from the orchestration platform.

## Context
- Event stream: !`tail -n 50 ~/.claude/orchestration/logs/events.log 2>/dev/null || echo "No events logged"`
- Filter: $ARGUMENTS

## Event Stream Dashboard

### 1. Live Event Feed
```
🔴 LIVE EVENT STREAM
─────────────────────────────────────────────────────────
[2025-08-20 14:32:45] [INFO]    Agent eng-fullstack started TASK-142
[2025-08-20 14:32:38] [SUCCESS] Agent qa-analyst completed TASK-198 (2.3h)
[2025-08-20 14:32:31] [WARNING] High memory usage detected (82%)
[2025-08-20 14:32:24] [ERROR]   Agent eng-api failed TASK-155: Timeout
[2025-08-20 14:32:17] [INFO]    Sprint velocity updated: 42 points/day
[2025-08-20 14:32:10] [SUCCESS] Deployment completed: v2.1.3
[2025-08-20 14:32:03] [INFO]    New task created: TASK-205 (Priority: High)
[2025-08-20 14:31:56] [WARNING] Agent devops-cicd idle for 30 minutes
[2025-08-20 14:31:49] [SUCCESS] Code review approved by eng-lead
[2025-08-20 14:31:42] [INFO]    Cache cleared successfully
─────────────────────────────────────────────────────────
```

### 2. Event Categories

#### System Events
```
⚙️ SYSTEM EVENTS (Last Hour)
├─ Startup/Shutdown:     3 events
├─ Configuration:        8 changes
├─ Resource Scaling:     2 events
├─ Cache Operations:     12 events
└─ Health Checks:        24 events
```

#### Agent Events
```
🤖 AGENT EVENTS (Last Hour)
├─ Task Assignments:     45 events
├─ Status Changes:       28 events
├─ Completions:         23 events
├─ Failures:            3 events
└─ Performance Updates:  15 events
```

#### Task Events
```
📋 TASK EVENTS (Last Hour)
├─ Created:             34 tasks
├─ Started:             42 tasks
├─ Completed:           38 tasks
├─ Failed:              3 tasks
└─ Blocked/Unblocked:   8 events
```

#### Deployment Events
```
🚀 DEPLOYMENT EVENTS (Last 24h)
├─ Builds Triggered:     12 events
├─ Tests Executed:       45 events
├─ Deployments:          3 events
├─ Rollbacks:           0 events
└─ Config Updates:       8 events
```

### 3. Event Timeline Visualization

```
📅 EVENT TIMELINE (Last 4 Hours)
         10:00    11:00    12:00    13:00    14:00
System    │░░░│    │▓▓▓│    │░░░│    │░░░│    │▓▓▓│
Agents    │▓▓▓│    │▓▓▓│    │███│    │▓▓▓│    │███│
Tasks     │▓▓▓│    │███│    │███│    │▓▓▓│    │▓▓▓│
Deploys   │░░░│    │░█░│    │░░░│    │░█░│    │░░░│
Errors    │░░░│    │░█░│    │░░░│    │░░░│    │░█░│

Legend: ░ Low  ▓ Medium  █ High Activity
```

### 4. Critical Event Alerts

```
🚨 CRITICAL EVENTS (Requires Attention)
┌─────────────────────────────────────────────────────┐
│ [14:32:24] ERROR: Agent eng-api failed repeatedly   │
│ [14:32:31] WARN:  Memory usage critical (82%)       │
│ [14:28:15] ERROR: Database connection timeout       │
│ [14:15:42] WARN:  Sprint behind schedule (3 days)  │
│ [13:45:20] ERROR: Security scan found vulnerability │
└─────────────────────────────────────────────────────┘
```

### 5. Event Statistics

```
📊 EVENT STATISTICS (24 Hour Summary)
┌──────────────────┬────────┬─────────┬──────────┐
│ Event Type       │ Count  │ Rate/hr │ Trend    │
├──────────────────┼────────┼─────────┼──────────┤
│ Task Created     │  234   │  9.75   │ ↑ +12%   │
│ Task Completed   │  198   │  8.25   │ ↑ +8%    │
│ Agent Started    │  456   │  19.00  │ → stable │
│ Agent Completed  │  423   │  17.63  │ → stable │
│ Errors          │   12   │  0.50   │ ↓ -25%   │
│ Warnings        │   34   │  1.42   │ ↑ +15%   │
│ Deployments     │    8   │  0.33   │ → stable │
└──────────────────┴────────┴─────────┴──────────┘
```

### 6. Event Patterns & Insights

```
🔍 PATTERN ANALYSIS
┌──────────────────────────────────────────────────┐
│ Detected Patterns:                               │
│                                                   │
│ • Peak activity: 10:00-11:00, 14:00-15:00       │
│ • Error spike correlation with deployments       │
│ • Increased task failures on Mondays            │
│ • Memory issues during batch processing         │
│ • Agent idle time increases after 17:00         │
│                                                   │
│ Recommendations:                                 │
│ • Schedule deployments during low activity       │
│ • Increase resources for batch jobs             │
│ • Implement predictive scaling for peak times    │
└──────────────────────────────────────────────────┘
```

## Event Filtering

### By Event Type
```bash
# System events only
grep "SYSTEM" ~/.claude/orchestration/logs/events.log

# Error events only
grep "ERROR" ~/.claude/orchestration/logs/events.log

# Agent events
grep "Agent" ~/.claude/orchestration/logs/events.log
```

### By Time Range
```bash
# Last hour
grep "$(date -v-1H '+%Y-%m-%d %H')" events.log

# Today's events
grep "$(date '+%Y-%m-%d')" events.log
```

### By Severity
```bash
# Critical and errors
grep -E "(CRITICAL|ERROR)" events.log

# Warnings and above
grep -E "(WARNING|ERROR|CRITICAL)" events.log
```

## Real-time Monitoring

Follow mode for continuous streaming:
```bash
tail -f ~/.claude/orchestration/logs/events.log
```

With filtering:
```bash
tail -f events.log | grep --line-buffered "ERROR"
```

## Event Notifications

### Slack Integration
- Critical errors → #alerts channel
- Deployments → #deployments channel
- Performance issues → #monitoring channel

### Email Alerts
- System failures → ops team
- Security events → security team
- Sprint issues → product team

## Event Correlation

Correlate events to identify root causes:
- Task failures + Agent errors = Agent issue
- Memory warnings + Slow performance = Resource issue
- Deploy event + Error spike = Deployment issue

## Export Options

- Stream view (real-time console)
- JSON events (structured data)
- CSV export (analysis)
- Syslog forward (SIEM integration)
- Webhook (external systems)

## Success Criteria

- [ ] Events streamed in real-time
- [ ] Filtering working correctly
- [ ] Statistics calculated accurately
- [ ] Patterns identified
- [ ] Critical events highlighted
- [ ] Export formats functional