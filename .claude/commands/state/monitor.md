---
allowed-tools: Bash(.claude/scripts/state_manager.py:*), Bash(.claude/scripts/event_stream.py:*), Bash(tail:*), Bash(watch:*)
description: Monitor real-time state changes and events
argument-hint: [--filter <type>] [--follow] [--interval <seconds>]
model: haiku
---

# Real-Time State Monitor

Monitor orchestration state changes and events in real-time with filtering and alerting.

## Context

Monitor arguments: $ARGUMENTS
Current event stream: !`.claude/scripts/event_stream.py tail --limit 5`

## Monitoring Modes

### 1. Parse Monitor Options

Extract monitoring parameters:
- `--filter <type>`: Filter events by type (task, agent, sprint, state)
- `--follow`: Continuous monitoring mode
- `--interval <seconds>`: Refresh interval (default: 5)
- `--alerts`: Show only critical alerts
- `--changes`: Show only state changes

### 2. Live Dashboard Display

Create real-time monitoring dashboard:

```
═══════════════════════════════════════════
     ORCHESTRATION STATE MONITOR
     [LIVE] Refresh: 5s | Events: 127
═══════════════════════════════════════════

📊 CURRENT METRICS
├─ Tasks: 15 total (3 active, 2 blocked)
├─ Agents: 8 online (5 busy, 3 idle)
├─ Sprint: Day 5/10 (45% complete)
└─ Health: 78/100 🟡

🔄 RECENT CHANGES (Last 5 min)
• [14:32:15] task-5: pending → in_progress
• [14:31:45] agent-3: idle → busy (assigned task-5)
• [14:30:22] sprint-3: velocity updated (15 → 16)
• [14:29:10] task-3: in_progress → completed
• [14:28:55] agent-1: busy → idle

⚡ ACTIVE OPERATIONS
├─ engineering-fullstack-1: Working on task-8 (15m)
├─ qa-analyst-2: Testing feature-X (5m)
└─ devops-cicd-1: Deploying service-Y (2m)

⚠️ ALERTS & WARNINGS
• task-15: Blocked for 3 hours (critical)
• agent-7: No heartbeat for 10 minutes
• sprint-3: Behind schedule by 2 days

📈 VELOCITY TRACKING
Hour  : ████████░░░░ 8 points
Day   : ████████████░░░░ 15 points
Sprint: ████░░░░░░░░ 45%
```

### 3. Event Stream Integration

Monitor event stream for state changes:

```bash
# Tail event stream with filtering
.claude/scripts/event_stream.py tail --follow --filter state_updated

# Parse events for state changes
Events show:
- Path modified
- Old value
- New value
- Timestamp
- Source (user/agent)
```

### 4. Change Detection

Track specific state changes:

**Task Status Changes**:
```
Task Status Flow (Last Hour):
pending (8) → in_progress (5) → completed (3)
                    ↓
                blocked (2)
```

**Agent Activity**:
```
Agent State Transitions:
idle → busy: 5 transitions
busy → idle: 3 transitions
busy → blocked: 1 transition
```

### 5. Alert Conditions

Monitor for critical conditions:

**Critical Alerts** 🔴:
- Task blocked > 4 hours
- Agent offline unexpectedly
- Sprint velocity < 50% of target
- Error rate > 5%

**Warnings** 🟡:
- Task age > 3 days
- Agent utilization > 90%
- Sprint behind by 1 day
- Queue depth > 10 tasks

**Info** 🔵:
- New task created
- Agent status change
- Sprint milestone reached

### 6. Performance Metrics

Real-time performance tracking:

```
PERFORMANCE METRICS (5-min window)
├─ Throughput: 3 tasks/hour ↑
├─ Cycle Time: 2.5 hours ↓
├─ Block Rate: 13% ↑
├─ Success Rate: 87% →
└─ Velocity: 1.5 pts/hour ↑

Trends: ↑ improving, ↓ degrading, → stable
```

### 7. Watchdog Features

Automated monitoring capabilities:

**Heartbeat Monitoring**:
- Check agent last_update timestamps
- Alert if no update > threshold
- Auto-mark as offline if unresponsive

**Deadlock Detection**:
- Identify circular task dependencies
- Alert on mutual blocking
- Suggest resolution order

**Capacity Monitoring**:
- Track WIP limits
- Alert on bottlenecks
- Suggest rebalancing

### 8. Filter Examples

Common monitoring filters:

```bash
# Monitor only task changes
/state monitor --filter task

# Watch specific agent
/state monitor --filter "agent:engineering-fullstack-1"

# Critical alerts only
/state monitor --alerts --filter critical

# Sprint progress
/state monitor --filter sprint --interval 30

# State mutations
/state monitor --changes
```

## Output Modes

### Compact Mode
Single-line updates for terminal monitoring:
```
[14:32:15] ✓ task-5 completed | ⚡ agent-3 assigned task-6 | 📊 velocity: 16
```

### Detailed Mode
Full event information with context:
```
═══════════════════════════════════════════
Event: state_updated
Time: 2024-08-20 14:32:15.234
Path: tasks.task-5.status
Old: "in_progress"
New: "completed"
Source: engineering-fullstack-1
Impact: Sprint progress +2 points
═══════════════════════════════════════════
```

### CSV Export Mode
For analysis and reporting:
```csv
timestamp,event_type,path,old_value,new_value,source
2024-08-20T14:32:15,state_updated,tasks.task-5.status,in_progress,completed,eng-1
```

## Interactive Commands

While monitoring, support commands:
- Press 'f' to change filter
- Press 'i' to change interval
- Press 'p' to pause/resume
- Press 'c' to clear screen
- Press 'e' to export events
- Press 'q' to quit monitoring

## Integration Points

Connect with other systems:

1. **Event Stream**: Real-time event consumption
2. **State Manager**: Direct state queries
3. **Observability**: Metrics and analytics
4. **Alerting**: Webhook/notification triggers
5. **Logging**: Audit trail maintenance

## Example Usage

```bash
# Basic monitoring
/state monitor

# Follow mode with 2-second refresh
/state monitor --follow --interval 2

# Monitor critical alerts only
/state monitor --alerts --filter critical

# Watch specific sprint
/state monitor --filter "sprint:sprint-3"

# Export changes to file
/state monitor --changes > state_changes.log
```