---
allowed-tools: Bash(python:*), Read, Grep, Task
description: Team utilization, capacity planning, and resource optimization
argument-hint: [team-name] [--compare]
model: haiku
---

# Team Utilization & Capacity Monitor

Monitor team performance, utilization rates, capacity planning, and resource optimization across all development teams.

## Context
- Team data: !`python .claude/scripts/observability.py status --format=json | jq '.agents | group_by(.team)'`
- Team filter: $ARGUMENTS

## Team Dashboard

### 1. Team Overview Grid
```
╭────────────── TEAM UTILIZATION OVERVIEW ──────────────╮
│                                                        │
│  Active Teams: 8       Total Agents: 32              │
│  Overall Utilization: 68%    Efficiency: 89%         │
│  Tasks in Progress: 45       Completed Today: 123    │
│                                                        │
╰────────────────────────────────────────────────────────╯

┌──────────────┬────────┬──────────┬──────────┬────────┐
│ Team         │ Agents │ Util %   │ Tasks    │ Health │
├──────────────┼────────┼──────────┼──────────┼────────┤
│ Engineering  │   8    │ 75% ███  │ 23 active│   🟢   │
│ QA           │   4    │ 88% ████ │ 15 active│   🟢   │
│ DevOps       │   4    │ 92% ████ │ 12 active│   🟡   │
│ Product      │   3    │ 67% ██   │  8 active│   🟢   │
│ Research     │   2    │ 50% ██   │  5 active│   🟡   │
│ Creative     │   3    │ 33% █    │  3 active│   🔴   │
│ Data         │   2    │ 75% ███  │  6 active│   🟢   │
│ Meta         │   6    │ 17% ░    │  2 active│   🔴   │
└──────────────┴────────┴──────────┴──────────┴────────┘
```

### 2. Detailed Team Metrics

#### Engineering Team (8 agents)
```
👥 ENGINEERING TEAM DETAILS
┌────────────────────────────────────────────────────┐
│ Capacity:      160 hours/week                     │
│ Allocated:     120 hours (75%)                    │
│ Available:     40 hours (25%)                     │
│                                                    │
│ Current Load Distribution:                        │
│ • eng-fullstack:  95% ████████████████████       │
│ • eng-api:        88% ████████████████████       │
│ • eng-ux:         62% █████████████              │
│ • eng-lead:       90% ████████████████████       │
│ • eng-backend:    72% ████████████████           │
│ • eng-frontend:   58% █████████████              │
│ • eng-mobile:     45% ███████████                │
│ • eng-security:   80% ████████████████████       │
│                                                    │
│ Performance Metrics:                              │
│ • Avg Task Time: 2.8h (Target: 3h) ✅            │
│ • Success Rate: 94% (Target: 90%) ✅             │
│ • Velocity: 42 pts/day (Target: 40) ✅           │
└────────────────────────────────────────────────────┘
```

### 3. Capacity Planning Matrix
```
📊 CAPACITY PLANNING (Next 7 Days)
         Mon   Tue   Wed   Thu   Fri   Sat   Sun
Engin.   ███   ████  ████  ███   ██    █     █
QA       ████  ████  ███   ████  ███   ░     ░
DevOps   ████  ████  ████  ████  ███   ██    █
Product  ██    ███   ███   ██    ██    ░     ░
Research ██    ██    ███   ███   ██    ░     ░
Creative █     ██    ██    █     █     ░     ░
Data     ███   ███   ██    ███   ██    █     ░
Meta     █     █     █     █     █     ░     ░

Legend: ████ >90%  ███ 70-90%  ██ 50-70%  █ <50%  ░ Off
```

### 4. Team Workload Distribution
```
📈 WORKLOAD ANALYSIS
┌──────────────┬─────────┬──────────┬───────────┐
│ Team         │ Backlog │ Assigned │ Capacity  │
├──────────────┼─────────┼──────────┼───────────┤
│ Engineering  │   45    │    35    │    40     │
│ QA           │   28    │    22    │    25     │
│ DevOps       │   18    │    16    │    20     │
│ Product      │   12    │     8    │    15     │
│ Research     │    8    │     5    │    10     │
│ Creative     │   15    │     4    │    12     │
│ Data         │   10    │     6    │     8     │
│ Meta         │    5    │     2    │    10     │
├──────────────┼─────────┼──────────┼───────────┤
│ TOTAL        │  141    │    98    │   140     │
└──────────────┴─────────┴──────────┴───────────┘

⚠️ Warning: Engineering team over capacity by 5 tasks
⚠️ Warning: Creative team underutilized (33%)
```

### 5. Cross-Team Dependencies
```
🔗 TEAM DEPENDENCIES & HANDOFFS
┌─────────────────────────────────────────────────┐
│ Active Dependencies:                            │
│                                                  │
│ Engineering → QA:        12 tasks pending      │
│ QA → DevOps:             8 tasks pending       │
│ Product → Engineering:   5 requirements        │
│ Research → Engineering:  3 recommendations     │
│ DevOps → QA:            2 deployments          │
│                                                  │
│ Blocked Handoffs:                              │
│ • API specs from Engineering to QA (2 days)    │
│ • Test results from QA to DevOps (1 day)       │
│ • Requirements from Product (3 days)           │
└─────────────────────────────────────────────────┘
```

### 6. Team Performance Comparison
```
🏆 TEAM PERFORMANCE RANKINGS
┌────┬──────────────┬──────┬─────────┬───────────┐
│ #  │ Team         │ Score│ Velocity│ Quality   │
├────┼──────────────┼──────┼─────────┼───────────┤
│ 1  │ QA           │ 96%  │ 38 pts  │ 98% ⭐⭐⭐⭐⭐│
│ 2  │ Engineering  │ 94%  │ 42 pts  │ 95% ⭐⭐⭐⭐⭐│
│ 3  │ DevOps       │ 92%  │ 35 pts  │ 92% ⭐⭐⭐⭐ │
│ 4  │ Data         │ 91%  │ 15 pts  │ 96% ⭐⭐⭐⭐⭐│
│ 5  │ Research     │ 88%  │ 12 pts  │ 97% ⭐⭐⭐⭐⭐│
│ 6  │ Product      │ 87%  │ 28 pts  │ 100% ⭐⭐⭐⭐⭐│
│ 7  │ Meta         │ 85%  │ 10 pts  │ 99% ⭐⭐⭐⭐⭐│
│ 8  │ Creative     │ 78%  │ 8 pts   │ 94% ⭐⭐⭐⭐ │
└────┴──────────────┴──────┴─────────┴───────────┘
```

### 7. Resource Optimization Recommendations
```
💡 OPTIMIZATION OPPORTUNITIES
┌─────────────────────────────────────────────────┐
│ Immediate Actions:                              │
│                                                  │
│ 1. Rebalance Engineering Load                  │
│    • Move 5 tasks to available teams           │
│    • Consider hiring or automation             │
│                                                  │
│ 2. Increase Creative Utilization               │
│    • Assign pending design tasks               │
│    • Cross-train for other skills              │
│                                                  │
│ 3. Resolve Dependency Bottlenecks              │
│    • Fast-track API spec completion            │
│    • Daily sync between dependent teams        │
│                                                  │
│ Strategic Recommendations:                      │
│                                                  │
│ • Scale QA team (consistently at 88%+)         │
│ • Automate Meta team tasks                     │
│ • Implement load balancing algorithm           │
│ • Create cross-functional pods                 │
└─────────────────────────────────────────────────┘
```

### 8. Team Health Indicators
```
🏥 TEAM HEALTH METRICS
┌──────────────┬────────┬────────┬─────────┬────────┐
│ Team         │ Morale │ Burnout│ Turnover│ Growth │
├──────────────┼────────┼────────┼─────────┼────────┤
│ Engineering  │   85%  │  Low   │   5%    │  +15%  │
│ QA           │   82%  │  Med   │   8%    │  +10%  │
│ DevOps       │   78%  │  High  │   12%   │  +5%   │
│ Product      │   90%  │  Low   │   3%    │  +20%  │
│ Research     │   88%  │  Low   │   2%    │  +8%   │
│ Creative     │   75%  │  Low   │   10%   │  0%    │
│ Data         │   86%  │  Med   │   6%    │  +12%  │
│ Meta         │   92%  │  Low   │   0%    │  +25%  │
└──────────────┴────────┴────────┴─────────┴────────┘

⚠️ Alert: DevOps showing high burnout risk
```

### 9. Capacity Forecast
```
📅 30-DAY CAPACITY FORECAST
┌──────────────┬──────┬──────┬──────┬──────────┐
│ Team         │ Week1│ Week2│ Week3│ Week4    │
├──────────────┼──────┼──────┼──────┼──────────┤
│ Engineering  │  75% │  82% │  88% │  92% 🔴  │
│ QA           │  88% │  85% │  90% │  95% 🔴  │
│ DevOps       │  92% │  88% │  85% │  80%     │
│ Product      │  67% │  72% │  75% │  78%     │
│ Research     │  50% │  55% │  60% │  58%     │
│ Creative     │  33% │  45% │  52% │  48%     │
│ Data         │  75% │  78% │  82% │  85% 🟡  │
│ Meta         │  17% │  22% │  25% │  28%     │
└──────────────┴──────┴──────┴──────┴──────────┘

Scaling Needed: Engineering, QA (Week 4)
```

## Team Management Commands

All teams overview:
```bash
python .claude/scripts/observability.py status --format=table
```

Specific team details:
```bash
python .claude/scripts/observability.py status --agent=$TEAM
```

Team comparison:
```bash
python .claude/scripts/observability.py metrics --type=productivity
```

## Optimization Strategies

### Load Balancing
- Redistribute tasks from overloaded teams
- Cross-train agents for flexibility
- Implement dynamic assignment

### Capacity Planning
- Forecast based on historical data
- Plan scaling 2 weeks ahead
- Monitor burnout indicators

### Performance Improvement
- Identify bottleneck teams
- Optimize workflows
- Automate repetitive tasks

## Alert Thresholds

- 🔴 Critical: Utilization > 90%
- 🟡 Warning: Utilization > 85%
- 🟡 Warning: Utilization < 30%
- 🔴 Critical: Burnout risk high
- 🟡 Warning: Dependencies blocked > 2 days

## Success Criteria

- [ ] All teams monitored
- [ ] Utilization calculated accurately
- [ ] Dependencies tracked
- [ ] Health metrics assessed
- [ ] Recommendations actionable
- [ ] Forecasts realistic