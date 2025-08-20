---
allowed-tools: Bash(.claude/scripts/state_manager.py:*), Bash(jq:*), Read
description: Show all agent assignments, workload, and performance metrics
argument-hint: [--status <status>] [--team <team>] [--available]
model: haiku
---

# Agent Workforce Analysis

Display comprehensive agent status, assignments, and performance metrics.

## Context

Filter arguments: $ARGUMENTS
Current agent state: !`.claude/scripts/state_manager.py get agents --format json`

## Agent Analysis

### 1. Parse Filter Options

Extract filters from arguments:
- `--status`: Filter by status (idle, busy, blocked)
- `--team`: Filter by team (engineering, qa, devops, etc.)
- `--available`: Show only available agents
- `--overloaded`: Show agents at >80% capacity
- `--performance`: Include performance metrics

### 2. Agent Status Overview

Group agents by current status:

**🟢 Available (Idle)**
```
• engineering-fullstack-1: Ready for assignment
• qa-analyst-2: Completed task-5, available
• devops-cicd-1: Standby mode
```

**🟡 Busy (Working)**
```
• engineering-api-1: Working on task-3 (2h elapsed)
• qa-e2e-1: Testing feature-X (80% complete)
• engineering-ux-1: Implementing UI components
```

**🔴 Blocked**
```
• engineering-lead-1: Waiting for requirements
• qa-scripts-1: Environment setup needed
```

### 3. Agent Workload Table

Display detailed agent information:

| Agent ID | Team | Status | Current Task | Time on Task | Tasks Today | Utilization |
|----------|------|--------|--------------|--------------|-------------|-------------|
| eng-full-1 | Engineering | busy | task-15 | 2h 30m | 3 | 75% |
| qa-e2e-1 | QA | busy | task-8 | 45m | 2 | 60% |
| devops-1 | DevOps | idle | - | - | 1 | 20% |

### 4. Team Distribution

Show agent allocation by team:

```
Engineering Team (5 agents)
├─ Busy: 3 (60%)
├─ Idle: 1 (20%)
└─ Blocked: 1 (20%)

QA Team (3 agents)
├─ Busy: 2 (67%)
├─ Idle: 1 (33%)
└─ Blocked: 0 (0%)

DevOps Team (2 agents)
├─ Busy: 0 (0%)
├─ Idle: 2 (100%)
└─ Blocked: 0 (0%)
```

### 5. Performance Metrics

Calculate agent performance indicators:

**Productivity Metrics**:
- Tasks completed per day
- Average task completion time
- Success rate (completed vs abandoned)
- Time to first response

**Efficiency Indicators**:
- Utilization rate (busy time / total time)
- Context switching frequency
- Blocked time percentage
- Collaboration effectiveness

### 6. Workload Balance Analysis

Identify imbalances:

```
⚠️ WORKLOAD ALERTS
• engineering-api-1: 95% utilized (overloaded)
• devops-team: 10% utilized (underutilized)
• qa-e2e-1: 3 tasks queued (bottleneck)
```

### 7. Agent Availability Forecast

Predict when agents will be available:

```
UPCOMING AVAILABILITY
• qa-analyst-1: ~30 min (task-5 completion)
• engineering-ux-1: ~2 hours (UI implementation)
• engineering-fullstack-2: ~4 hours (feature development)
```

### 8. Skill Matrix

Show agent capabilities:

| Agent | Frontend | Backend | Testing | DevOps | Database |
|-------|----------|---------|---------|--------|----------|
| eng-full-1 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| eng-api-1 | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| qa-e2e-1 | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐ | ⭐⭐ |

## Agent Recommendations

### Optimization Suggestions

1. **Load Balancing**:
   - Reassign task-X from overloaded agent-A to idle agent-B
   - Distribute QA tasks across available testers

2. **Skill Matching**:
   - Assign database tasks to agents with DB expertise
   - Route UI tasks to frontend specialists

3. **Blocked Resolution**:
   - Prioritize unblocking agent-X (high-value contributor)
   - Resolve environment issues for qa-scripts-1

## Output Format

```
═══════════════════════════════════════════
           AGENT WORKFORCE STATUS
═══════════════════════════════════════════

📊 WORKFORCE SUMMARY
├─ Total Agents: 15
├─ Active: 8 (53%)
├─ Available: 5 (33%)
├─ Blocked: 2 (14%)
└─ Avg Utilization: 65%

👥 TEAM STATUS
[Team breakdown here]

⚡ IMMEDIATE ACTIONS
• Reassign tasks from eng-api-1 (overloaded)
• Utilize idle devops team members
• Resolve blocker for eng-lead-1

📈 PERFORMANCE HIGHLIGHTS
• Top Performer: qa-analyst-2 (8 tasks/day)
• Most Improved: eng-fullstack-3 (+25% velocity)
• Best Collaboration: eng-ux-1 & qa-e2e-1

🔄 CURRENT ASSIGNMENTS
[Detailed assignment table]

💡 OPTIMIZATION OPPORTUNITIES
1. Balance workload: 3 agents at >80% capacity
2. Skill gaps: Need more testing expertise
3. Cross-training: DevOps underutilized
```

## Interactive Commands

Provide management commands:
- "Update agent status: `!.claude/scripts/state_manager.py update-agent agent-1 --status busy`"
- "Assign task: `!.claude/scripts/state_manager.py update-agent agent-1 task-5`"
- "Clear assignment: `!.claude/scripts/state_manager.py update-agent agent-1 --clear-task`"
- "View agent details: `/state get agents.active.agent-1`"