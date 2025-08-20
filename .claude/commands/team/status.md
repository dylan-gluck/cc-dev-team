---
allowed-tools: Read, Task, Bash(jq:*)
description: Display detailed status of all teams and their current activities
model: haiku
---

# Team Status Report

Generate comprehensive status report for all teams and their current activities.

## Context
- Team configuration: @.claude/orchestration/teams.json
- Current state: @.claude/orchestration/team-state.json
- Timestamp: !`date +"%Y-%m-%d %H:%M:%S"`

## Status Report Generation

### 1. Engineering Team Status
```
🔧 ENGINEERING TEAM STATUS
━━━━━━━━━━━━━━━━━━━━━━━━━━━
Orchestrator: engineering-director
Model: opus
Capacity: X/9 utilized

Active Agents:
- engineering-lead: [status/task]
- engineering-fullstack: [status/task]
- engineering-ux: [status/task]
- engineering-test: [status/task]
- engineering-docs: [status/task]

Current Tasks:
1. [Task ID] - [Description] - [Agent] - [Progress]
2. ...

Settings:
- Max Parallel: 5
- Code Review: Required
- Test Coverage: 80%
- Auto Documentation: Enabled
```

### 2. Product Team Status
```
📊 PRODUCT TEAM STATUS
━━━━━━━━━━━━━━━━━━━━━━━━━━━
Orchestrator: product-director
Model: opus
Capacity: X/2 utilized

Active Agents:
- product-manager: [status/task]
- product-analyst: [status/task]

Current Tasks:
1. [Task ID] - [Description] - [Agent] - [Progress]

Settings:
- Max Parallel: 3
- Acceptance Criteria: Required
```

### 3. QA Team Status
```
✅ QA TEAM STATUS
━━━━━━━━━━━━━━━━━━━━━━━━━━━
Orchestrator: qa-director
Model: opus
Capacity: X/5 utilized

Active Agents:
- qa-e2e: [status/task]
- qa-scripts: [status/task]
- qa-analyst: [status/task]

Current Tasks:
1. [Task ID] - [Description] - [Agent] - [Progress]

Settings:
- Max Parallel: 4
- Test Plan: Required
- Regression Testing: Mandatory
```

### 4. DevOps Team Status
```
🚀 DEVOPS TEAM STATUS
━━━━━━━━━━━━━━━━━━━━━━━━━━━
Orchestrator: devops-manager
Model: opus
Capacity: X/3 utilized

Active Agents:
- devops-cicd: [status/task]
- devops-infrastructure: [status/task]
- devops-release: [status/task]

Current Tasks:
1. [Task ID] - [Description] - [Agent] - [Progress]

Settings:
- Max Parallel: 3
- Deployment Approval: Required
```

## Cross-Team Dependencies

### Active Handoffs
Display pending handoffs between teams:
```
🤝 Pending Handoffs:
1. [From Team] → [To Team]: [Context/Task]
   Status: [Waiting/In Progress]
   Created: [Timestamp]
```

### Blocked Items
Identify any blocked tasks:
```
⚠️ Blocked Tasks:
1. [Task] - Blocked by: [Dependency]
   Team: [Team Name]
   Duration: [Time blocked]
```

## Resource Utilization Summary

```
📊 OVERALL RESOURCE UTILIZATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Capacity:     19 agents
Currently Active:   X agents (Y%)
Available:         Z agents

By Team:
Engineering:  ████████░░ 80% (7/9)
Product:      ██████░░░░ 50% (1/2)
QA:           ████░░░░░░ 40% (2/5)
DevOps:       ██████░░░░ 66% (2/3)
```

## Recent Activity Log

Show last 10 team events:
```
📋 Recent Activity:
[Timestamp] [Team] [Event Type] [Description]
...
```

## Performance Indicators

### Team Velocity (Last 24 Hours)
```
Team         | Tasks Started | Tasks Completed | Success Rate
-------------|---------------|-----------------|-------------
Engineering  |       5       |       3         |    100%
Product      |       2       |       2         |    100%
QA           |       8       |       6         |     95%
DevOps       |       3       |       3         |    100%
```

## Alerts and Notifications

Highlight any issues requiring attention:
```
⚠️ Alerts:
- [Team]: [Alert description]
- ...

ℹ️ Notifications:
- [Team]: [Notification]
- ...
```

## Recommended Actions

Based on current status, suggest:
1. Teams that could take on more work
2. Teams that need assistance
3. Handoffs that should be initiated
4. Resources that could be reallocated

## Output Format

Present all information in a clear, scannable format with:
- Visual separators between sections
- Color-coded status indicators
- Progress bars for capacity
- Timestamp for report generation
- Actionable insights highlighted