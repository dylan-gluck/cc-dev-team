---
allowed-tools: Read, LS, Task
description: Team management overview dashboard and coordination hub
model: sonnet
---

# Team Management Overview

Display comprehensive team management dashboard and coordination status.

## Context
- Team configuration: @.claude/orchestration/teams.json
- Current state: @.claude/orchestration/team-state.json
- Available agents: !`fd -t f . .claude/agents/ -e md | wc -l` agents total

## Dashboard Display

### 1. Team Overview
Create a visual team hierarchy showing:
```
🏢 Organization Structure
├── 🔧 Engineering Team (9 capacity)
│   ├── engineering-lead (Technical Leadership)
│   ├── engineering-fullstack (Full Stack x3)
│   ├── engineering-ux (UX Engineering x2)
│   ├── engineering-test (QA x2)
│   └── engineering-docs (Documentation)
├── 📊 Product Team (2 capacity)
│   ├── product-manager (Product Management)
│   └── product-analyst (Business Analysis)
├── ✅ QA Team (5 capacity)
│   ├── qa-e2e (E2E Testing x2)
│   ├── qa-scripts (Test Automation x2)
│   └── qa-analyst (Quality Analysis)
└── 🚀 DevOps Team (3 capacity)
    ├── devops-cicd (CI/CD Pipeline)
    ├── devops-infrastructure (Infrastructure)
    └── devops-release (Release Coordination)
```

### 2. Current Activity Status
Display for each team:
- Active teams and their current tasks
- Capacity utilization (used/total)
- Active assignments
- Pending handoffs
- Recent completions

### 3. Quick Actions Menu
```
Available Commands:
━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 /team status        - Detailed status of all teams
📈 /team capacity      - Capacity analysis and planning
👤 /team assign        - Assign agent to specific task
🤝 /team handoff       - Manage cross-team handoffs
⚡ /team activate      - Activate team for coordination
📋 /team list          - List all teams and agents
📉 /team performance   - Performance metrics dashboard
━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 4. Team Health Indicators
For each team show:
- ✅ Green: Operating normally (< 70% capacity)
- ⚠️ Yellow: High utilization (70-90% capacity)
- 🔴 Red: Over capacity (> 90% capacity)
- 💤 Idle: No active tasks

### 5. Recent Team Events
Display last 5 team events:
- Task assignments
- Handoff completions
- Team activations
- Performance milestones

## Orchestration Status

### Active Orchestrations
- Show any running team orchestrations
- Display progress indicators
- Estimate completion times

### Resource Allocation
```
Total Capacity: 19 agents
In Use: X agents (Y%)
Available: Z agents
```

## Recommendations

Based on current state, provide:
1. Suggested team optimizations
2. Capacity rebalancing recommendations
3. Cross-team collaboration opportunities
4. Performance improvement suggestions

## Interactive Help

Provide contextual help:
- "Need to start a new feature? Try `/team activate engineering`"
- "Want to check team performance? Use `/team performance`"
- "Ready to hand off work? Use `/team handoff`"

## Output Format

Present information in a clean, organized dashboard format with:
- Clear visual hierarchy
- Color-coded status indicators
- Actionable insights
- Quick command references

Make the overview immediately useful for understanding team state and taking action.