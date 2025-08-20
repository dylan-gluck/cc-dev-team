---
allowed-tools: Bash(python:*), Read, Task
description: Performance metrics and KPIs dashboard with trends and analysis
argument-hint: [metric-type] [time-range]
model: haiku
---

# Performance Metrics Dashboard

Display comprehensive KPIs, performance metrics, and trend analysis for the development team.

## Context
- Metrics data: !`python .claude/scripts/observability.py metrics --type=performance`
- Analysis period: $ARGUMENTS

## Metrics Dashboard Layout

### 1. Executive Summary
```
╭────────────── PERFORMANCE METRICS SUMMARY ──────────────╮
│                                                          │
│  Period: Last 24 Hours        Status: ✅ Healthy        │
│  ────────────────────────────────────────────────────   │
│  Throughput:     234 tasks    ↑ 12% from yesterday      │
│  Success Rate:   94.2%        ↑ 2.1% from last week     │
│  Avg Response:   2.8 hours    ↓ 15% improvement         │
│  Team Velocity:  42 pts/day   ↑ 8% from sprint avg      │
│                                                          │
╰──────────────────────────────────────────────────────────╯
```

### 2. Key Performance Indicators

#### Efficiency Metrics
```
📊 EFFICIENCY KPIs
┌──────────────────────┬─────────┬─────────┬──────────┐
│ Metric               │ Current │ Target  │ Status   │
├──────────────────────┼─────────┼─────────┼──────────┤
│ Task Completion Rate │  94.2%  │  90%    │ ✅ +4.2% │
│ First-Time Success   │  87.5%  │  85%    │ ✅ +2.5% │
│ Rework Rate          │  12.5%  │  <15%   │ ✅ -2.5% │
│ Automation Coverage  │  78.3%  │  75%    │ ✅ +3.3% │
│ Code Review Time     │  1.2h   │  <2h    │ ✅ -0.8h │
└──────────────────────┴─────────┴─────────┴──────────┘
```

#### Quality Metrics
```
📈 QUALITY KPIs
┌──────────────────────┬─────────┬─────────┬──────────┐
│ Metric               │ Current │ Target  │ Status   │
├──────────────────────┼─────────┼─────────┼──────────┤
│ Defect Escape Rate   │  2.1%   │  <5%    │ ✅ -2.9% │
│ Test Coverage        │  82.4%  │  80%    │ ✅ +2.4% │
│ Code Quality Score   │  8.7/10 │  8.0    │ ✅ +0.7  │
│ Documentation Score  │  91%    │  85%    │ ✅ +6%   │
│ Security Score       │  A-     │  B+     │ ✅ ↑     │
└──────────────────────┴─────────┴─────────┴──────────┘
```

#### Productivity Metrics
```
📉 PRODUCTIVITY KPIs
┌──────────────────────┬─────────┬─────────┬──────────┐
│ Metric               │ Current │ Target  │ Status   │
├──────────────────────┼─────────┼─────────┼──────────┤
│ Sprint Velocity      │  42 pts │  40 pts │ ✅ +2    │
│ Cycle Time           │  2.8h   │  3h     │ ✅ -0.2h │
│ Lead Time            │  5.2h   │  6h     │ ✅ -0.8h │
│ Throughput           │  234/d  │  200/d  │ ✅ +34   │
│ WIP Limit Adherence  │  95%    │  90%    │ ✅ +5%   │
└──────────────────────┴─────────┴─────────┴──────────┘
```

### 3. Trend Analysis

#### Weekly Performance Trend
```
📊 7-DAY PERFORMANCE TREND
100% ┤                    ╭───
 95% ┤             ╭─────╯
 90% ┤      ╭─────╯
 85% ┤ ────╯
 80% ┤
     └───────────────────────
     Mon  Tue  Wed  Thu  Fri  Sat  Sun
     
Legend: ─── Success Rate  ╌╌╌ Target (90%)
```

#### Task Completion Velocity
```
📈 DAILY TASK VELOCITY
300 ┤           ╭╮
250 ┤       ╭──╯ ╰╮  ╭───
200 ┤   ╭──╯      ╰──╯
150 ┤ ──╯
100 ┤
    └────────────────────────
    Week 1   Week 2   Week 3   Week 4
```

### 4. Team Performance Comparison

```
👥 TEAM PERFORMANCE MATRIX
                 Tasks  Success  Velocity  Quality
Engineering      ████   95%     42 pts    A-
QA              ███░   98%     38 pts    A
DevOps          ███░   92%     35 pts    B+
Product         ██░░   100%    28 pts    A
Research        ██░░   97%     25 pts    A-
Creative        █░░░   94%     18 pts    B+
Data            █░░░   96%     15 pts    A-
Meta            █░░░   99%     12 pts    A
```

### 5. Resource Utilization

```
💪 RESOURCE EFFICIENCY
┌─────────────────────────────────────────────┐
│ CPU Utilization     ████████░░  78% (Good)  │
│ Memory Usage        ██████░░░░  62% (Good)  │
│ Agent Utilization   █████░░░░░  47% (Low)   │
│ Task Queue Depth    ███░░░░░░░  34 tasks    │
│ Parallel Execution  ███████░░░  72% (Good)  │
└─────────────────────────────────────────────┘
```

### 6. Cost & Efficiency Analysis

```
💰 COST EFFICIENCY METRICS
┌──────────────────────┬──────────┬───────────┐
│ Metric               │ This Week│ Last Week │
├──────────────────────┼──────────┼───────────┤
│ Cost per Task        │ $0.42    │ $0.48     │
│ ROI                  │ 312%     │ 287%      │
│ Resource Efficiency  │ 89%      │ 84%       │
│ Waste Reduction      │ 23%      │ 18%       │
│ Time Saved           │ 142h     │ 118h      │
└──────────────────────┴──────────┴───────────┘
```

## Detailed Metrics Commands

Performance metrics:
```bash
python .claude/scripts/observability.py metrics --type=performance
```

Quality metrics:
```bash
python .claude/scripts/observability.py metrics --type=quality
```

Productivity metrics:
```bash
python .claude/scripts/observability.py metrics --type=productivity
```

## Alert Conditions

Metrics requiring attention:
- ⚠️ Success rate < 85%
- 🔴 Defect escape > 10%
- ⚠️ Velocity < 80% of target
- 🔴 Resource utilization > 90%
- ⚠️ Cost per task increasing > 20%

## Improvement Recommendations

Based on current metrics:

### Quick Wins
- Increase parallel execution (currently 72%)
- Reduce idle agent time
- Optimize task assignment algorithm

### Strategic Improvements
- Implement predictive scaling
- Enhance automated testing
- Improve documentation automation

### Risk Mitigation
- Monitor declining metrics
- Plan capacity for peak loads
- Review error patterns

## Export Formats

- Dashboard view (Rich console)
- JSON metrics (API export)
- CSV report (Excel analysis)
- Grafana integration
- Slack notifications

## Success Criteria

- [ ] All KPIs calculated accurately
- [ ] Trends visualized clearly
- [ ] Comparisons meaningful
- [ ] Alerts triggered correctly
- [ ] Recommendations actionable
- [ ] Export formats working