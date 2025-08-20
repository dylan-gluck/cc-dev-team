---
allowed-tools: Bash(.claude/scripts/state_manager.py:*), Bash(.claude/scripts/event_stream.py:*), Bash(jq:*), Read
description: Query state change history and analyze trends
argument-hint: [--path <path>] [--since <time>] [--limit <n>]
model: sonnet
---

# State History & Trends Analysis

Query historical state changes and analyze trends over time.

## Context

History arguments: $ARGUMENTS
Recent events: !`.claude/scripts/event_stream.py query --type state_updated --limit 10`

## History Analysis

### 1. Parse Query Parameters

Extract history filters:
- `--path <path>`: Filter by state path (e.g., "tasks.task-1")
- `--since <time>`: Time range (1h, 24h, 7d, 2024-08-20)
- `--until <time>`: End time for range
- `--limit <n>`: Maximum events to analyze
- `--type <type>`: Event type filter
- `--aggregate`: Show aggregated statistics

### 2. Change Timeline

Display chronological state changes:

```
STATE CHANGE TIMELINE
═══════════════════════════════════════════

2024-08-20 14:30:00 → Present

14:32:15 │ tasks.task-5.status
         │ "in_progress" → "completed"
         │ Source: engineering-fullstack-1
         │
14:31:45 │ agents.active.agent-3.status
         │ "idle" → "busy"
         │ Source: orchestrator
         │
14:31:00 │ tasks.task-5.assigned_to
         │ null → "agent-3"
         │ Source: task_manager
         │
14:30:22 │ sprints.sprint-3.metrics.velocity
         │ 15 → 16
         │ Source: sprint_tracker
         │
14:29:10 │ tasks.task-3.status
         │ "in_progress" → "completed"
         │ Source: qa-analyst-2
```

### 3. Path-Specific History

Track changes for specific paths:

```bash
# Query: /state history --path tasks.task-5

TASK-5 HISTORY
═══════════════════════════════════════════

Created: 2024-08-18 09:00:00
Total Changes: 12
Last Modified: 2024-08-20 14:32:15

Status Transitions:
├─ 08-18 09:00 : created → pending
├─ 08-19 10:30 : pending → in_progress
├─ 08-19 15:45 : in_progress → blocked
├─ 08-20 09:15 : blocked → in_progress
└─ 08-20 14:32 : in_progress → completed

Assignments:
├─ 08-19 10:30 : assigned to eng-fullstack-1
├─ 08-19 15:45 : reassigned to qa-analyst-1
└─ 08-20 09:15 : reassigned to eng-fullstack-1

Time Spent:
├─ Pending: 1d 1h 30m
├─ In Progress: 9h 32m
├─ Blocked: 17h 30m
└─ Total: 2d 5h 32m
```

### 4. Trend Analysis

Analyze patterns over time:

```
TREND ANALYSIS (Last 7 Days)
═══════════════════════════════════════════

Task Completion Rate:
Mon ████████░░ 80%
Tue ██████░░░░ 60%
Wed █████████░ 90%
Thu ███████░░░ 70%
Fri ████████░░ 85%
Sat ████░░░░░░ 40%
Sun ██████░░░░ 65%

Average: 70% | Trend: ↓ declining

Agent Utilization:
Mon ███████░░░ 75%
Tue ████████░░ 82%
Wed █████████░ 91%
Thu ████████░░ 85%
Fri ███████░░░ 78%
Sat █████░░░░░ 50%
Sun ██████░░░░ 60%

Average: 74% | Trend: ↓ weekend dip

Blocker Frequency:
This Week: 12 blockers (avg 1.7/day)
Last Week: 8 blockers (avg 1.1/day)
Change: ↑ 50% increase
```

### 5. State Replay

Reconstruct state at any point in time:

```bash
# Query: /state history --replay "2024-08-19 15:00"

STATE SNAPSHOT @ 2024-08-19 15:00:00
═══════════════════════════════════════════

Tasks:
├─ Total: 12
├─ Completed: 3 (25%)
├─ In Progress: 5 (42%)
├─ Blocked: 1 (8%)
└─ Pending: 3 (25%)

Agents:
├─ Total: 8
├─ Busy: 5 (63%)
├─ Idle: 2 (25%)
└─ Blocked: 1 (12%)

Sprint Progress:
├─ Sprint-3: Day 3/10 (30% time)
├─ Completed: 8/25 points (32%)
└─ On Track: ✓ Yes
```

### 6. Change Frequency Analysis

Identify high-activity areas:

```
CHANGE FREQUENCY (Last 24h)
═══════════════════════════════════════════

Most Changed Paths:
1. tasks.task-8.status         : 8 changes
2. agents.active.eng-1.status  : 6 changes
3. sprints.sprint-3.metrics    : 5 changes
4. tasks.task-5.assigned_to    : 4 changes
5. communication.questions     : 4 changes

Hotspot Analysis:
• High Activity: task-8 (possible instability)
• Frequent Reassignment: task-5 (resource issue?)
• Metric Updates: sprint-3 (active monitoring)
```

### 7. Audit Trail

Detailed audit log with actor attribution:

```
AUDIT TRAIL
═══════════════════════════════════════════

Filter: --since 1h --type state_updated

Time     | Actor      | Action          | Path            | Change
---------|------------|-----------------|-----------------|------------------
14:32:15 | eng-full-1 | status_change   | tasks.task-5    | in_progress → completed
14:31:45 | system     | agent_assign    | agents.agent-3  | idle → busy
14:31:00 | pm-1       | task_assign     | tasks.task-5    | null → agent-3
14:30:22 | system     | metric_update   | sprints.sprint-3| velocity: 15 → 16
```

### 8. Statistical Analysis

Generate statistics from history:

```
HISTORICAL STATISTICS (30 days)
═══════════════════════════════════════════

Task Metrics:
├─ Total Created: 156
├─ Total Completed: 142 (91%)
├─ Avg Cycle Time: 2.3 days
├─ Avg Block Time: 4.5 hours
└─ Success Rate: 91%

Agent Performance:
├─ Avg Utilization: 72%
├─ Task/Agent/Day: 2.8
├─ Avg Response Time: 15 min
└─ Collaboration Rate: 34%

Sprint Performance:
├─ Sprints Completed: 3
├─ Avg Velocity: 28 points
├─ Predictability: 85%
└─ Scope Creep: 12%
```

### 9. Pattern Detection

Identify recurring patterns:

```
PATTERN ANALYSIS
═══════════════════════════════════════════

Detected Patterns:

📊 Daily Patterns:
• Peak activity: 10:00-12:00, 14:00-16:00
• Low activity: 12:00-13:00 (lunch)
• Task completion spike: 16:00-17:00

📈 Weekly Patterns:
• Monday: High planning activity
• Wednesday: Peak productivity
• Friday: High completion rate
• Weekend: Minimal activity

⚠️ Anomalies Detected:
• Unusual blocking pattern on task-15
• Agent-7 irregular status changes
• Sprint-3 velocity fluctuation
```

### 10. Comparison Analysis

Compare different time periods:

```bash
# Query: /state history --compare "last-week" "this-week"

COMPARATIVE ANALYSIS
═══════════════════════════════════════════

Metric          | Last Week | This Week | Change
----------------|-----------|-----------|----------
Tasks Completed | 28        | 35        | ↑ +25%
Avg Cycle Time  | 2.5 days  | 2.1 days  | ↓ -16%
Blockers        | 8         | 12        | ↑ +50%
Agent Util.     | 68%       | 74%       | ↑ +9%
Sprint Velocity | 25 pts    | 30 pts    | ↑ +20%

Summary: Increased productivity but more blockers
```

## Export Capabilities

Support various export formats:

```bash
# Export to CSV
/state history --since 7d --export csv > history.csv

# Export to JSON
/state history --path tasks --export json > tasks_history.json

# Export for visualization
/state history --aggregate --export chartjs > chart_data.js
```

## Interactive Queries

Provide drill-down capabilities:
- "View specific change: `/state history --event <event-id>`"
- "Track entity: `/state history --entity task-5`"
- "Compare periods: `/state history --compare yesterday today`"
- "Export range: `/state history --since 2024-08-01 --until 2024-08-20 --export csv`"