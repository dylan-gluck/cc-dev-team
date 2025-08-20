---
allowed-tools: Bash(python:*), Read, Task
description: Current sprint burndown, velocity, and progress tracking
argument-hint: [sprint-id] [--detailed]
model: haiku
---

# Sprint Progress Monitor

Track current sprint progress with burndown charts, velocity metrics, and goal completion status.

## Context
- Sprint data: !`python .claude/scripts/observability.py sprint --current --format=json`
- Sprint filter: $ARGUMENTS

## Sprint Dashboard

### 1. Sprint Overview
```
╭──────────────── SPRINT 2: CURRENT ────────────────╮
│                                                    │
│  Duration:    Aug 12 - Aug 26 (14 days)          │
│  Progress:    Day 8 of 14 (57% time elapsed)     │
│  Status:      ⚠️ Behind Schedule                  │
│                                                    │
│  Completed:   45/89 tasks (51% done)             │
│  In Progress: 12 tasks (8 agents active)         │
│  Blocked:     5 tasks                            │
│  Remaining:   27 tasks                           │
│                                                    │
╰────────────────────────────────────────────────────╯
```

### 2. Burndown Chart
```
📉 SPRINT BURNDOWN
Points
100 ┤ ████████████
 90 ┤ ████████████╲
 80 ┤ ████████████ ╲ Ideal
 70 ┤ ████████████  ╲
 60 ┤ ████████████   ╲___
 50 ┤ ████████████    ╲  ╲___  Actual
 40 ┤ ████████████     ╲     ╲___
 30 ┤ ████████████      ╲        ╲___
 20 ┤ ████████████       ╲           ╲
 10 ┤ ████████████        ╲
  0 ┤ ████████████         ╲___________
    └────────────────────────────────────
    Day 1  2  3  4  5  6  7  8  9  10 11 12 13 14

Legend: ████ Complete  ░░░░ Remaining  ╲ Ideal  ╲ Actual
```

### 3. Velocity Metrics
```
📊 VELOCITY ANALYSIS
┌──────────────────────┬─────────┬─────────┬──────────┐
│ Metric               │ Current │ Target  │ Status   │
├──────────────────────┼─────────┼─────────┼──────────┤
│ Daily Velocity       │ 5.6 pts │ 7.1 pts │ ⚠️ -21%  │
│ Completion Rate      │ 51%     │ 57%     │ ⚠️ -6%   │
│ Avg Task Time        │ 3.2h    │ 2.5h    │ ⚠️ +28%  │
│ Burndown Rate        │ 72%     │ 85%     │ ⚠️ -13%  │
│ Projected Completion │ 82%     │ 100%    │ 🔴 -18%  │
└──────────────────────┴─────────┴─────────┴──────────┘
```

### 4. Sprint Goals Status
```
🎯 SPRINT GOALS
┌─────────────────────────────────────────────┬────────┐
│ Goal                                        │ Status │
├─────────────────────────────────────────────┼────────┤
│ ✅ Complete authentication system           │ 100%   │
│ 🔄 Implement payment processing            │ 65%    │
│ 🔄 Deploy monitoring dashboard             │ 40%    │
│ ⏸️ Migrate database to new schema          │ 15%    │
│ ❌ Complete API documentation              │ 0%     │
└─────────────────────────────────────────────┴────────┘

Overall Goal Completion: 44% (Target: 57%)
```

### 5. Task Breakdown by Status
```
📋 TASK STATUS DISTRIBUTION
┌──────────────┬───────┬────────────────────────────┐
│ Status       │ Count │ Visual                     │
├──────────────┼───────┼────────────────────────────┤
│ Completed    │  45   │ ████████████████████       │
│ In Progress  │  12   │ █████                      │
│ Pending      │  27   │ ████████████               │
│ Blocked      │   5   │ ██                         │
│ Total        │  89   │ ████████████████████████   │
└──────────────┴───────┴────────────────────────────┘
```

### 6. Team Performance in Sprint
```
👥 TEAM CONTRIBUTIONS
┌──────────────┬──────────┬───────────┬────────────┐
│ Team         │ Assigned │ Completed │ Efficiency │
├──────────────┼──────────┼───────────┼────────────┤
│ Engineering  │    35    │    18     │ 51% ████   │
│ QA           │    20    │    12     │ 60% █████  │
│ DevOps       │    15    │     9     │ 60% █████  │
│ Product      │    10    │     4     │ 40% ███    │
│ Research     │     9    │     2     │ 22% ██     │
└──────────────┴──────────┴───────────┴────────────┘
```

### 7. Risk Assessment
```
⚠️ SPRINT RISKS & BLOCKERS
┌─────────────────────────────────────────────────────┐
│ High Risk Items:                                    │
│                                                      │
│ 🔴 Database migration blocking 3 tasks             │
│ 🔴 API documentation 0% complete (due in 6 days)   │
│ 🟡 Payment processing behind schedule              │
│ 🟡 5 tasks blocked > 24 hours                      │
│ 🟡 Velocity 21% below target                       │
│                                                      │
│ Mitigation Actions:                                 │
│ • Escalate database migration to DevOps            │
│ • Assign 2 agents to API documentation             │
│ • Unblock tasks through dependency resolution      │
│ • Consider scope adjustment for sprint             │
└─────────────────────────────────────────────────────┘
```

### 8. Daily Standup Summary
```
📅 TODAY'S SPRINT STATUS (Day 8)
┌─────────────────────────────────────────────────────┐
│ Yesterday:                                          │
│ • Completed 6 tasks (below target of 8)           │
│ • Resolved 2 blockers                             │
│ • Deployed monitoring v1.0                        │
│                                                     │
│ Today's Plan:                                      │
│ • Target: Complete 10 tasks                       │
│ • Focus: Payment processing integration           │
│ • Unblock: Database migration tasks               │
│                                                     │
│ Impediments:                                       │
│ • Database migration complexity underestimated    │
│ • Need additional QA resources                    │
│ • API documentation resource not available        │
└─────────────────────────────────────────────────────┘
```

### 9. Projected Outcomes
```
📈 SPRINT PROJECTIONS
Based on current velocity:

Optimistic (velocity improves 20%):
• 78 tasks completed (88% of sprint)
• 3 of 5 goals achieved
• 2 days schedule slip

Realistic (current velocity):
• 73 tasks completed (82% of sprint)
• 2 of 5 goals achieved
• 3 days schedule slip

Pessimistic (velocity drops 10%):
• 67 tasks completed (75% of sprint)
• 2 of 5 goals achieved
• 5 days schedule slip
```

## Commands

Current sprint overview:
```bash
python .claude/scripts/observability.py sprint --current
```

All sprints comparison:
```bash
python .claude/scripts/observability.py sprint --all
```

Detailed sprint metrics:
```bash
python .claude/scripts/observability.py sprint --current --format=json | jq
```

## Sprint Health Indicators

- 🟢 On Track: > 95% of ideal burndown
- 🟡 At Risk: 85-95% of ideal burndown
- 🔴 Behind: < 85% of ideal burndown

## Recommendations

### To Get Back on Track:
1. **Immediate Actions**
   - Resolve all blockers within 24h
   - Reassign idle agents to critical tasks
   - Daily check-ins on at-risk items

2. **Process Improvements**
   - Reduce task switching overhead
   - Improve estimation accuracy
   - Increase parallel execution

3. **Resource Optimization**
   - Add agents to bottleneck areas
   - Redistribute work from overloaded teams
   - Consider scope reduction if needed

## Export Options

- Sprint report (PDF)
- Burndown data (CSV)
- Velocity metrics (JSON)
- Executive summary (Markdown)

## Success Criteria

- [ ] Burndown chart accurate
- [ ] Velocity calculated correctly
- [ ] Goals tracked properly
- [ ] Risks identified
- [ ] Projections realistic
- [ ] Recommendations actionable