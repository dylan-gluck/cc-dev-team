---
allowed-tools: Bash(.claude/scripts/state_manager.py:*), Bash(jq:*), Read
description: High-level orchestration state overview with insights
model: sonnet
---

# Orchestration State Summary

Generate a comprehensive overview of the current orchestration state with actionable insights.

## Context

Full state data: !`.claude/scripts/state_manager.py get --format json`

## Analysis Sections

### 1. Organization Overview
- Active projects and their health status
- Resource allocation across projects
- Strategic alignment metrics

### 2. Sprint Analytics
```bash
# Analyze sprint progress
- Current sprint velocity vs target
- Burndown rate and projections
- Task completion trends
- Blocker identification
```

### 3. Task Intelligence
```bash
# Task distribution analysis
- Status distribution (pie chart data)
- Age of pending tasks
- Blocked task dependencies
- Priority vs progress matrix
- Estimation accuracy
```

### 4. Agent Performance
```bash
# Agent utilization metrics
- Current workload distribution
- Idle vs busy ratio
- Task completion rates per agent
- Specialization effectiveness
- Collaboration patterns
```

### 5. Flow Metrics
```bash
# Development flow analysis
- Cycle time by task type
- Lead time trends
- Work in progress limits
- Bottleneck identification
- Throughput measurements
```

### 6. Health Indicators

Calculate and display health scores:

**Project Health Score** (0-100):
- Task completion rate (30%)
- Sprint velocity achievement (25%)
- Blocker resolution time (20%)
- Agent utilization balance (15%)
- Communication effectiveness (10%)

**Risk Indicators**:
- 🔴 **Critical**: Blocked tasks > 20%
- 🟡 **Warning**: Agent utilization > 80%
- 🟢 **Healthy**: Velocity within 10% of target

### 7. Predictive Insights

Based on current trends:
- Sprint completion probability
- Resource bottleneck predictions
- Optimal task assignments
- Recommended interventions

### 8. Communication Status
```bash
# Analyze communication patterns
- Unanswered questions count
- Handoff completion rate
- Average response time
- Collaboration frequency
```

## Visualization Format

Create Rich-formatted output with:

1. **Executive Dashboard**:
   - Key metrics in card layout
   - Traffic light status indicators
   - Trend arrows (↑ ↓ →)

2. **Detailed Tables**:
   - Sprint progress table
   - Agent workload matrix
   - Task aging report
   - Blocker dependency tree

3. **Charts** (ASCII representation):
   - Task status distribution
   - Sprint burndown
   - Agent utilization
   - Velocity trend

4. **Alerts Section**:
   - Critical issues requiring attention
   - Performance degradation warnings
   - Opportunity notifications

## Recommendations Engine

Generate actionable recommendations:

1. **Task Redistribution**:
   - Identify overloaded agents
   - Suggest task reassignments
   - Balance workload optimally

2. **Process Improvements**:
   - Bottleneck resolution steps
   - Workflow optimization suggestions
   - Automation opportunities

3. **Resource Planning**:
   - Additional agent needs
   - Skill gap identification
   - Training recommendations

## Time-based Analysis

Compare current state with:
- Previous sprint performance
- Week-over-week trends
- Daily velocity changes
- Historical patterns

## Output Structure

```
═══════════════════════════════════════════
       ORCHESTRATION STATE SUMMARY
═══════════════════════════════════════════

📊 EXECUTIVE METRICS
├─ Projects: X active, Y% on track
├─ Tasks: X total, Y% completed
├─ Agents: X active, Y% utilized
└─ Health Score: XX/100 [status]

🎯 CURRENT SPRINT (Sprint-X)
├─ Progress: ████████░░ 80%
├─ Velocity: 15/18 points
├─ Days Remaining: 3
└─ Completion Probability: 92%

⚠️ REQUIRES ATTENTION
• 3 tasks blocked for >24 hours
• Agent-X at 95% capacity
• Sprint-Y behind schedule

💡 RECOMMENDATIONS
1. Reassign task-X from Agent-Y to Agent-Z
2. Unblock task-A by completing dependency
3. Add QA resource for testing bottleneck

📈 TRENDS
• Velocity: ↑ 12% vs last sprint
• Cycle Time: ↓ 8% improvement
• Blockers: → stable at 2-3/sprint
```

## Interactive Elements

Provide commands for drill-down:
- "View blocked tasks: `/state get 'tasks | map(select(.status == \"blocked\"))'"
- "Check agent details: `/state agents`"
- "Sprint details: `/state sprints`"