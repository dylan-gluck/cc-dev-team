---
allowed-tools: Bash(.claude/scripts/state_manager.py:*), Bash(jq:*), Read
description: Show sprint status, progress metrics, and burndown analysis
argument-hint: [--sprint <sprint-id>] [--active] [--metrics]
model: sonnet
---

# Sprint Management Dashboard

Display comprehensive sprint information with progress tracking and predictive analytics.

## Context

Filter arguments: $ARGUMENTS
Current sprint state: !`.claude/scripts/state_manager.py get sprints --format json`

## Sprint Analysis

### 1. Parse Sprint Filters

Extract options from arguments:
- `--sprint`: Show specific sprint details
- `--active`: Show only active sprints
- `--completed`: Show completed sprints
- `--metrics`: Include detailed metrics
- `--burndown`: Generate burndown chart

### 2. Active Sprint Summary

For each active sprint, display:

**🏃 Sprint-X (Active)**
```
Duration: Day 5 of 10 (50% time elapsed)
Progress: ████████░░░░░░░░ 45% tasks complete
Velocity: 15/33 story points

Key Metrics:
├─ Planned: 20 tasks, 33 points
├─ Completed: 9 tasks, 15 points
├─ In Progress: 5 tasks, 10 points
├─ Blocked: 2 tasks, 3 points
└─ Remaining: 4 tasks, 5 points

Health: 🟡 At Risk (behind by 2 days)
```

### 3. Sprint Progress Table

| Sprint ID | Status | Start Date | End Date | Progress | Velocity | Health |
|-----------|--------|------------|----------|----------|----------|--------|
| sprint-3 | active | 2024-08-15 | 2024-08-25 | 45% | 15/33 | 🟡 At Risk |
| sprint-2 | completed | 2024-08-01 | 2024-08-14 | 100% | 28/30 | 🟢 Success |
| sprint-4 | planned | 2024-08-26 | 2024-09-08 | 0% | 0/35 | - |

### 4. Burndown Visualization

Generate ASCII burndown chart:

```
Sprint-3 Burndown Chart
Points
35 |*
30 |  *....... (ideal)
25 |    *     *
20 |      *     * (actual)
15 |        *     *
10 |          *     *---*
 5 |            *         *
 0 |________________________*
   |1 2 3 4 5 6 7 8 9 10    Days

Legend: * = Actual, . = Ideal
Status: Behind ideal by 5 points
```

### 5. Sprint Metrics Deep Dive

**Velocity Analysis**:
- Current velocity: X points/day
- Required velocity: Y points/day
- Historical average: Z points/day
- Velocity trend: ↑↓→

**Task Flow Metrics**:
```
Task Movement (Last 24h):
pending (5) → in_progress (3) → completed (2)
                    ↓
                blocked (1)
```

**Impediment Analysis**:
- Blockers: X tasks blocked for Y total hours
- Top blocker: "Waiting for API documentation"
- Resolution time: Average 2.5 days

### 6. Sprint Predictions

Based on current metrics:

**Completion Forecast**:
```
Scenario Analysis:
├─ Current pace: 65% completion by deadline
├─ Best case (+20%): 85% completion
├─ Worst case (-20%): 45% completion
└─ Recommended: Add 2 resources or extend 2 days
```

**Risk Assessment**:
- 🔴 High Risk: Blocked tasks not decreasing
- 🟡 Medium Risk: Velocity below planned
- 🟢 Low Risk: Team morale stable

### 7. Sprint Comparisons

Compare with previous sprints:

| Metric | Current | Previous | Avg (Last 5) | Trend |
|--------|---------|----------|--------------|-------|
| Velocity | 15 pts | 28 pts | 25 pts | ↓ -46% |
| Completion | 45% | 93% | 88% | ↓ -48% |
| Blockers | 2 | 1 | 1.5 | ↑ +100% |
| Cycle Time | 3.2d | 2.1d | 2.5d | ↑ +52% |

### 8. Sprint Goals & Outcomes

Track sprint goals:

**Sprint-3 Goals**:
- ✅ Complete authentication module
- 🔄 Deploy payment integration (60%)
- ❌ Launch beta testing (blocked)
- ✅ Fix critical bugs from sprint-2

**Delivery Confidence**: 65%

### 9. Team Performance in Sprint

Show team contributions:

```
Team Contributions:
Engineering: ████████░░ 80% of tasks
QA:         ███░░░░░░░ 30% of tasks
DevOps:     ██░░░░░░░░ 20% of tasks

Top Contributors:
1. eng-fullstack-1: 5 tasks completed
2. qa-analyst-2: 3 tasks completed
3. eng-api-1: 2 tasks completed
```

## Sprint Recommendations

### Immediate Actions

1. **Unblock Critical Path**:
   - Resolve "API documentation" blocker
   - Impacts 3 downstream tasks

2. **Resource Reallocation**:
   - Move idle DevOps resources to testing
   - Reassign low-priority tasks

3. **Scope Adjustment**:
   - Consider deferring feature-X to sprint-4
   - Focus on must-have deliverables

## Output Format

```
═══════════════════════════════════════════
           SPRINT DASHBOARD
═══════════════════════════════════════════

🎯 ACTIVE SPRINTS (1)
Sprint-3: "Payment Integration"
├─ Timeline: Day 5/10 (50%)
├─ Progress: 45% complete
├─ Velocity: 15/33 points
├─ Health: 🟡 At Risk
└─ Confidence: 65%

📊 BURNDOWN ANALYSIS
[Burndown chart here]

⚠️ CRITICAL ISSUES
• 2 tasks blocked for >48 hours
• Velocity 40% below target
• 3 must-have features at risk

📈 METRICS & TRENDS
[Metrics table here]

💡 RECOMMENDATIONS
1. Unblock task-15 immediately
2. Add QA resource from idle pool
3. Defer feature-X to maintain quality

🔄 RECENT ACTIVITY
• task-8: moved to completed (2h ago)
• task-15: blocked on dependencies (5h ago)
• sprint velocity updated: 15 points
```

## Interactive Commands

Sprint management commands:
- "Update sprint: `/state set sprints.sprint-3.status 'completed'`"
- "Add task to sprint: `/state set tasks.task-10.sprint_id 'sprint-3'`"
- "Update metrics: `/state set sprints.sprint-3.metrics.velocity 18 --merge`"
- "View sprint tasks: `/state get 'tasks | map(select(.sprint_id == \"sprint-3\"))'`"