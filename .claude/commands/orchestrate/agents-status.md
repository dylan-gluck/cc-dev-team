---
allowed-tools: Read, Bash(.claude/scripts/state_manager.py:*), Bash(.claude/scripts/observability.py:*), Bash(.claude/scripts/message_bus.py:*), Bash(.claude/scripts/event_stream.py:*), Bash(echo:*), Bash(ps:*), Bash(printf:*)
description: Show all active orchestration agents with detailed status
argument-hint: [--team team-name] [--format detailed|summary|json]
model: haiku
---

# Orchestration Agents Status

Display comprehensive status of all active orchestration agents.

## Arguments
- Team filter: --team [team-name] (optional)
- Format: --format detailed|summary|json (default: detailed)

## Agent Discovery

### 1. Get Active Agents
Retrieve all active agents:
- !`.claude/scripts/state_manager.py get agents.active`

### 2. Get Agent Processes
Check system processes if available:
- !`ps aux | grep -i claude | grep -v grep | wc -l`

### 3. Get Team Assignments
Map agents to teams:
- !`.claude/scripts/state_manager.py get teams.active`

## Agent Status Overview

### Summary Statistics

```
📊 Agent Overview
─────────────────────────────────────────
Total Active Agents: [count]
By Status:
  • 🟢 Busy: [count] agents
  • 🟡 Idle: [count] agents  
  • 🔴 Blocked: [count] agents
  • ⚫ Error: [count] agents

By Team:
  • Engineering: [count] agents
  • QA: [count] agents
  • DevOps: [count] agents
  • Product: [count] agents

Resource Usage:
  • Agents: [current]/[limit]
  • Tokens: [used]/[budget]
  • Runtime: [elapsed]/[limit]
```

## Detailed Agent List

### Orchestrator Agents

Display orchestrators with hierarchy:

```
🎯 ORCHESTRATORS
─────────────────────────────────────────

engineering-director [opus]
├── Status: Active
├── Session: session-abc123
├── Started: 2 hours ago
├── Current Focus: Sprint 3 coordination
├── Child Agents: 5
├── Tasks Managed: 12
├── Token Usage: 15,420
└── Last Update: 30 seconds ago

qa-director [opus]
├── Status: Active
├── Session: session-def456
├── Started: 1 hour ago
├── Current Focus: Test automation
├── Child Agents: 3
├── Tasks Managed: 6
├── Token Usage: 8,200
└── Last Update: 2 minutes ago
```

### Team Member Agents

Show all team members grouped by team:

```
👥 TEAM MEMBERS
─────────────────────────────────────────

ENGINEERING TEAM
────────────────
┌─────────────────────────────────────────────────────────┐
│ Agent ID                 │ Status │ Task      │ Duration │
├─────────────────────────────────────────────────────────┤
│ engineering-lead-1       │ Busy   │ task-15   │ 45 min   │
│ engineering-fullstack-1  │ Busy   │ task-12   │ 30 min   │
│ engineering-fullstack-2  │ Idle   │ -         │ -        │
│ engineering-ux-1         │ Busy   │ task-18   │ 15 min   │
│ engineering-test-1       │ Idle   │ -         │ -        │
└─────────────────────────────────────────────────────────┘

QA TEAM
────────
┌─────────────────────────────────────────────────────────┐
│ Agent ID                 │ Status │ Task      │ Duration │
├─────────────────────────────────────────────────────────┤
│ qa-e2e-1                │ Busy   │ task-20   │ 25 min   │
│ qa-scripts-1            │ Busy   │ task-21   │ 10 min   │
│ qa-analyst-1            │ Idle   │ -         │ -        │
└─────────────────────────────────────────────────────────┘
```

## Individual Agent Details

For each agent, show comprehensive information:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Agent: engineering-fullstack-1
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Identity:
  • Type: engineering-fullstack
  • Model: sonnet
  • Session: session-xyz789
  • Parent: engineering-director

Status:
  • Current: Busy 🟢
  • Task: task-12 (API endpoint implementation)
  • Progress: 75% complete
  • Duration: 30 minutes
  • Last Update: 1 minute ago

Performance:
  • Tasks Completed: 3
  • Average Duration: 42 minutes
  • Success Rate: 100%
  • Token Usage: 12,350
  • Token Rate: 412 tokens/minute

Work History:
  1. task-8: Database schema (✅ Completed - 45 min)
  2. task-10: API design (✅ Completed - 30 min)
  3. task-11: Unit tests (✅ Completed - 25 min)
  4. task-12: API implementation (🔄 In Progress - 30 min)

Communications:
  • Messages Sent: 5
  • Messages Received: 8
  • Questions Pending: 1
  • Last Communication: 5 minutes ago

Resources:
  • Working Directory: /Users/project
  • Worktree: feature/api-endpoints
  • Memory Usage: 256 MB
  • CPU Usage: 15%
```

## Agent Relationships

Show agent communication and dependencies:

```
🔗 Agent Relationships
─────────────────────────────────────────

Communication Flow:
┌──────────────────┐
│ eng-director     │──────┐
└──────────────────┘      │
         │                │
    ┌────┴────┬──────┐    │
    ▼         ▼      ▼    ▼
┌────────┐ ┌────────┐ ┌────────┐
│eng-lead│ │eng-fs-1│ │eng-fs-2│
└────────┘ └────────┘ └────────┘
    │          │           │
    └──────────┴───────────┘
              ▼
         ┌────────┐
         │qa-e2e-1│
         └────────┘

Active Handoffs:
• engineering-ux-1 → engineering-fullstack-1 (UI components)
• engineering-fullstack-1 → qa-e2e-1 (API ready for testing)

Blocked Dependencies:
• qa-scripts-1 waiting on engineering-test-1 (test fixtures)
```

## Performance Metrics

### Agent Efficiency

```
📈 Performance Metrics
─────────────────────────────────────────

Agent Utilization:
Engineering: ████████████████░░░░ 80%
QA:          ████████████░░░░░░░░ 60%
DevOps:      ████████░░░░░░░░░░░░ 40%
Product:     ████░░░░░░░░░░░░░░░░ 20%

Task Throughput (last hour):
• Started: 8 tasks
• Completed: 5 tasks
• Failed: 0 tasks
• Blocked: 1 task

Average Task Duration:
• Simple tasks: 15 minutes
• Medium tasks: 45 minutes
• Complex tasks: 90 minutes

Token Efficiency:
• Average per task: 2,500 tokens
• Peak usage: 5,000 tokens (task-15)
• Most efficient: 800 tokens (task-7)
```

## Agent Health Monitoring

### Health Indicators

```
🏥 Agent Health Status
─────────────────────────────────────────

Healthy Agents (8):
✅ All responding normally
✅ Update frequency normal
✅ Token usage within limits

Warning Agents (2):
⚠️ engineering-fullstack-2: Idle for 45 minutes
⚠️ qa-analyst-1: High token usage (90% of limit)

Critical Issues (1):
❌ engineering-test-1: Not responding (last update 10 min ago)
   Action: May need restart

Blocked Agents (1):
🚫 qa-scripts-1: Waiting on dependency
   Blocking: task-21
   Duration: 15 minutes
   Dependency: test fixtures from engineering-test-1
```

## Communication Status

### Message Queues

```
📬 Communication Queues
─────────────────────────────────────────

Pending Messages by Priority:
• 🔴 Critical: 0
• 🟠 High: 2
• 🟡 Normal: 5
• 🟢 Low: 3

Pending Questions (3):
1. From: eng-fullstack-1 | To: eng-lead
   "Should we implement caching for this endpoint?"
   Age: 5 minutes

2. From: qa-e2e-1 | To: product-manager
   "Is this the expected behavior for edge case X?"
   Age: 12 minutes

3. From: eng-ux-1 | To: eng-lead
   "Can we use external component library?"
   Age: 20 minutes

Recent Communications (last 5):
• [2 min ago] eng-director → qa-director: "Ready for testing"
• [5 min ago] eng-fullstack-1 → eng-lead: "Code review needed"
• [8 min ago] qa-e2e-1 → eng-fullstack-1: "Found issue in API"
• [10 min ago] eng-lead → eng-team: "Sprint checkpoint"
• [15 min ago] product-manager → all: "Priority change"
```

## Resource Consumption

### Token Usage by Agent

```
💰 Token Consumption
─────────────────────────────────────────

Top Consumers (last hour):
1. engineering-director:    15,420 tokens
2. engineering-lead-1:      12,350 tokens  
3. qa-director:             8,200 tokens
4. engineering-fullstack-1: 6,500 tokens
5. engineering-ux-1:        4,200 tokens

Token Budget Status:
Used:      68,420 / 100,000 (68%)
Remaining: 31,580 tokens
Rate:      1,140 tokens/minute
Est. Exhaustion: 28 minutes

Token Usage Trend:
Hour -3: ████░░░░░░ 40%
Hour -2: ██████░░░░ 60%
Hour -1: ████████░░ 80%
Current: ███████░░░ 68%
```

## Quick Actions

Based on current status, suggest actions:

```
💡 Suggested Actions

1. 🔧 Resolve Blocker: engineering-test-1 not responding
   Command: /orchestrate agent restart engineering-test-1

2. 📞 Answer Questions: 3 pending questions
   Command: /orchestrate communication review

3. 🚀 Utilize Idle Agents: 3 agents available
   Command: /orchestrate task delegate

4. ⚠️ Monitor Token Usage: Approaching limit (68%)
   Command: /orchestrate budget review

5. 🔄 Restart Stalled Agent: engineering-test-1
   Command: /orchestrate agent restart engineering-test-1
```

## Export Options

```
📤 Export Agent Data

Available Formats:
1. JSON - Full agent state
2. CSV - Agent metrics table
3. Markdown - Formatted report
4. HTML - Interactive dashboard

Export command:
/orchestrate agents export --format [format]
```

## Live Monitoring Mode

If live monitoring requested:

```
🔴 LIVE MONITORING MODE
─────────────────────────────────────────
Refreshing every 10 seconds...
Press Ctrl+C to exit

[10:35:42] UPDATE: engineering-fullstack-1 completed task-12
[10:35:45] UPDATE: qa-e2e-1 started task-22
[10:35:48] WARNING: Token usage at 70%
[10:35:52] UPDATE: engineering-test-1 back online
```

## Agent Commands

Available agent management commands:

```
📝 Agent Management Commands

Individual Agent:
• /orchestrate agent restart [agent-id]
• /orchestrate agent stop [agent-id]
• /orchestrate agent reassign [agent-id] [new-task]
• /orchestrate agent communicate [agent-id] "[message]"

Bulk Operations:
• /orchestrate agents stop --team [team]
• /orchestrate agents restart --status blocked
• /orchestrate agents clear --status idle

Monitoring:
• /orchestrate agents watch [agent-id]
• /orchestrate agents trace [agent-id]
• /orchestrate agents profile [agent-id]
```

## Summary View (--format summary)

Condensed view:

```
Active: 11 agents (8 busy, 3 idle)
Teams: Engineering (5), QA (3), DevOps (2), Product (1)
Tasks: 8 in progress, 3 completed (last hour)
Health: 8 healthy, 2 warnings, 1 critical
Tokens: 68,420/100,000 (68%)
Runtime: 2.5 hours
```