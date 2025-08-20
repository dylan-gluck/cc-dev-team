---
allowed-tools: Read, Bash(.claude/scripts/state_manager.py:*), Bash(.claude/scripts/observability.py:*), Bash(.claude/scripts/message_bus.py:*), Bash(echo:*), Bash(printf:*)
description: Show current sprint progress, metrics, and team status
argument-hint: [sprint-id] [--format detailed|summary|json]
model: haiku
---

# Sprint Status Dashboard

Display comprehensive sprint progress, team status, and real-time metrics.

## Arguments
- Sprint ID: $ARGUMENTS (optional - defaults to active sprint)
- Format: --format detailed|summary|json (default: detailed)

## Sprint Discovery

Find the sprint to display:
1. If sprint ID provided, use it
2. Otherwise, find active sprint: !`.claude/scripts/state_manager.py get sprints`
3. If multiple active sprints, list them for selection

## Status Overview

### 📊 Sprint Summary
```
Sprint: [sprint-id]
Status: [active|planning|review|completed]
Progress: ████████░░ 75%
Day: 5 of 14
Velocity: 8 points/day
```

## Detailed Status Report

### 1. Task Progress
Display task breakdown by status:

```
Status       | Count | Tasks                          | Progress
-------------|-------|--------------------------------|----------
✅ Completed | 8     | task-1, task-2, task-3...     | 100%
🔄 Active    | 3     | task-4, task-5, task-6        | 45%
⏳ Queued    | 5     | task-7, task-8, task-9...     | 0%
🚫 Blocked   | 1     | task-10                       | 0%
-------------|-------|--------------------------------|----------
Total        | 17    |                                | 53%
```

### 2. Team Performance

Show performance by team:

```
Team         | Agents | Active Tasks | Completed | Velocity | Utilization
-------------|--------|--------------|-----------|----------|-------------
Engineering  | 5/5    | 2            | 6         | 8 pts    | 85%
QA           | 3/3    | 1            | 2         | 3 pts    | 75%
Product      | 1/2    | 0            | 1         | 2 pts    | 50%
```

### 3. Active Agents

List all active agents and their current work:

```
Agent                    | Status | Current Task | Duration | Last Update
-------------------------|--------|--------------|----------|-------------
engineering-fullstack-1  | busy   | task-4      | 15 min   | 2 min ago
engineering-fullstack-2  | busy   | task-5      | 8 min    | 1 min ago
engineering-ux-1        | idle   | -           | -        | 5 min ago
qa-e2e-1                | busy   | task-6      | 12 min   | 30 sec ago
qa-scripts-1            | idle   | -           | -        | 3 min ago
```

### 4. Sprint Burndown

Show burndown chart (text-based):

```
Points Remaining
100 |*
 90 |**
 80 | ***
 70 |  ****
 60 |    *****
 50 |      ******      <- Current (53 points)
 40 |         ********
 30 |            **********
 20 |                 ************
 10 |                      **************
  0 +----------------------------------------
    Day 1  2  3  4  5  6  7  8  9  10 11 12 13 14
                    ^
                  Today
    
Legend: * Actual | - Ideal
```

### 5. Blockers and Issues

Highlight any blockers or issues:

```
⚠️ Current Issues:

1. BLOCKED: task-10 - "Database migration dependency"
   - Blocking: task-11, task-12
   - Assigned: engineering-fullstack-1
   - Duration: 2 hours
   - Action: Awaiting DBA approval

2. WARNING: High token usage
   - Current: 72,000 / 100,000 (72%)
   - Rate: 15,000 tokens/hour
   - Estimated exhaustion: 2 hours

3. RISK: Test coverage below threshold
   - Current: 65%
   - Required: 80%
   - Gap: 15%
```

### 6. Key Metrics

Display sprint metrics:

```
Metric                  | Value    | Target  | Status
------------------------|----------|---------|--------
Sprint Velocity         | 8 pts    | 10 pts  | ⚠️
Task Completion Rate    | 47%      | 50%     | ⚠️
Test Coverage          | 65%      | 80%     | ❌
Build Success Rate     | 92%      | 95%     | ⚠️
Agent Utilization      | 73%      | 80%     | ⚠️
Average Task Duration  | 45 min   | 30 min  | ❌
Blocked Task Ratio     | 6%       | <5%     | ❌
```

### 7. Recent Events

Show last 5 sprint events:

```
Time     | Event                    | Details
---------|--------------------------|----------------------------------
2 min    | task_completed          | task-3 by engineering-fullstack-1
5 min    | agent_idle              | engineering-ux-1 completed task-2
8 min    | task_started            | task-6 by qa-e2e-1
15 min   | task_blocked            | task-10 - database dependency
22 min   | sprint_checkpoint       | Daily standup completed
```

### 8. Communication Queue

Show pending questions or handoffs:

```
📬 Pending Communications:

Questions (2):
1. FROM: engineering-fullstack-1 TO: engineering-lead
   "Should we use Redis or PostgreSQL for session storage?"
   Context: task-4 | Age: 10 min

2. FROM: qa-e2e-1 TO: product-manager
   "Need clarification on acceptance criteria for login flow"
   Context: task-6 | Age: 5 min

Handoffs (1):
1. FROM: engineering-ux-1 TO: engineering-fullstack-2
   "Login component ready for integration"
   Artifact: components/Login.tsx | Status: Ready
```

## Progress Indicators

### Visual Progress Bars

```
Overall Sprint Progress:
[████████████████░░░░░░░░░░░░] 53% (9/17 tasks)

By Priority:
High:    [████████████████████████] 100% (4/4)
Medium:  [████████░░░░░░░░░░░░░░░░] 33% (3/9)
Low:     [████████████░░░░░░░░░░░░] 50% (2/4)

By Team:
Engineering: [██████████████░░░░░░░] 67%
QA:          [████████░░░░░░░░░░░░░] 40%
Product:     [████████████████████░] 100%
```

## Quick Actions

Based on current status, suggest actions:

```
💡 Suggested Actions:

1. 🚨 Resolve Blocker: task-10 needs immediate attention
   Command: /orchestrate task unblock task-10

2. 📈 Improve Velocity: 3 agents are idle
   Command: /orchestrate task delegate

3. 🧪 Increase Coverage: Test coverage below threshold
   Command: /orchestrate team activate qa --focus testing

4. 💬 Answer Questions: 2 pending questions need responses
   Command: /orchestrate communication review
```

## Format Options

### Summary Format (--format summary)
Show only high-level metrics and progress

### JSON Format (--format json)
Output raw state data for processing

### Detailed Format (default)
Show comprehensive status as above

## Auto-Refresh Notice

If monitoring mode requested:
```
📍 Live Monitoring Active
   Refreshing every 30 seconds...
   Press Ctrl+C to stop

   Last update: 2 seconds ago
   Next update: in 28 seconds
```

## Sprint Health Assessment

Provide overall health score:

```
🏥 Sprint Health: MODERATE (72/100)

✅ Strengths:
• High task completion rate
• Good team coordination
• No critical errors

⚠️ Areas of Concern:
• Test coverage below target
• 1 task blocked for >2 hours
• Token usage approaching limit

📋 Recommendations:
1. Prioritize unblocking task-10
2. Increase QA agent allocation
3. Monitor token usage closely
```

## Export Options

Offer data export:
```
📤 Export Options:
• Generate sprint report: /orchestrate report generate
• Export metrics: /orchestrate metrics export
• Create burndown chart: /orchestrate chart burndown
• Send status email: /orchestrate notify team
```