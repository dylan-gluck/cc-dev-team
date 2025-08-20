---
allowed-tools: Read, Task, Bash(jq:*), Bash(bc:*)
description: Analyze team capacity, utilization, and resource planning
argument-hint: [team-name] [--forecast days]
model: sonnet
---

# Team Capacity Analysis

Perform comprehensive capacity analysis and resource planning for teams.

## Context
- Team configuration: @.claude/orchestration/teams.json
- Current state: @.claude/orchestration/team-state.json
- Analysis parameters: $ARGUMENTS

## Capacity Analysis

### 1. Current Capacity Overview
```
📊 CAPACITY ANALYSIS DASHBOARD
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Team Capacity Utilization:
                    Available  In Use  Reserved  Free
Engineering         ▓▓▓▓▓▓▓▓▓    9       0        0      9
  - Lead           ▓            1       0        0      1
  - Fullstack      ▓▓▓          3       0        0      3
  - UX             ▓▓           2       0        0      2
  - Test           ▓▓           2       0        0      2
  - Docs           ▓            1       0        0      1

Product            ▓▓           2       0        0      2
  - Manager        ▓            1       0        0      1
  - Analyst        ▓            1       0        0      1

QA                 ▓▓▓▓▓        5       0        0      5
  - E2E            ▓▓           2       0        0      2
  - Scripts        ▓▓           2       0        0      2
  - Analyst        ▓            1       0        0      1

DevOps             ▓▓▓          3       0        0      3
  - CI/CD          ▓            1       0        0      1
  - Infrastructure ▓            1       0        0      1
  - Release        ▓            1       0        0      1

TOTAL              ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  19      0        0     19
```

### 2. Utilization Trends (Last 7 Days)
```
Daily Average Utilization:
Day     | Engineering | Product | QA    | DevOps | Overall
--------|-------------|---------|-------|--------|--------
Today   |     0%      |   0%    |  0%   |   0%   |   0%
Day -1  |    45%      |  50%    | 60%   |  33%   |  47%
Day -2  |    55%      |  75%    | 80%   |  66%   |  69%
Day -3  |    33%      |  50%    | 40%   |  33%   |  39%
Day -4  |    66%      | 100%    | 60%   |  66%   |  73%
Day -5  |    44%      |  50%    | 40%   |  33%   |  41%
Day -6  |    22%      |  25%    | 20%   |   0%   |  16%
```

### 3. Peak Utilization Analysis
```
Peak Utilization Times:
Team         | Peak Time      | Peak % | Avg Duration
-------------|----------------|--------|-------------
Engineering  | Weekdays 10-12 |  85%   | 2.5 hours
Product      | Mon/Thu 14-16  |  100%  | 2.0 hours
QA           | Fri 10-14      |  90%   | 4.0 hours
DevOps       | Tue/Thu 16-18  |  100%  | 2.0 hours
```

### 4. Agent-Level Capacity
```
Individual Agent Capacity:
Agent                   | Capacity | Current | Available | Avg Load
------------------------|----------|---------|-----------|----------
engineering-lead        |    1     |    0    |     1     |   65%
engineering-fullstack   |    3     |    0    |     3     |   70%
engineering-ux          |    2     |    0    |     2     |   45%
engineering-test        |    2     |    0    |     2     |   80%
engineering-docs        |    1     |    0    |     1     |   30%
product-manager         |    1     |    0    |     1     |   75%
product-analyst         |    1     |    0    |     1     |   60%
qa-e2e                  |    2     |    0    |     2     |   85%
qa-scripts              |    2     |    0    |     2     |   70%
qa-analyst              |    1     |    0    |     1     |   40%
devops-cicd             |    1     |    0    |     1     |   60%
devops-infrastructure   |    1     |    0    |     1     |   55%
devops-release          |    1     |    0    |     1     |   45%
```

### 5. Resource Bottlenecks
Identify constrained resources:
```
⚠️ Potential Bottlenecks:
1. product-manager: Often at 100% capacity during planning
2. qa-e2e: High demand during release cycles
3. engineering-lead: Review bottleneck when multiple PRs pending
```

### 6. Capacity Forecast
If --forecast parameter provided, show projected capacity:
```
📈 Capacity Forecast (Next X Days):
Day | Engineering | Product | QA | DevOps | Risk Level
----|-------------|---------|----|---------|-----------
+1  |    45%      |  50%    | 60%|   33%   | Low
+2  |    67%      |  75%    | 80%|   66%   | Medium
+3  |    78%      | 100%    | 90%|   66%   | High
+4  |    55%      |  50%    | 70%|   33%   | Medium
+5  |    44%      |  50%    | 60%|   33%   | Low
```

### 7. Optimization Recommendations

Based on analysis, provide recommendations:

**Load Balancing Opportunities:**
- Move documentation tasks from engineering-lead to engineering-docs
- Distribute testing between qa-e2e and qa-scripts
- Consider parallel execution for independent tasks

**Capacity Expansion Needs:**
- Product team at high utilization - consider adding analyst
- QA team peaks during releases - plan buffer capacity

**Efficiency Improvements:**
- Automate recurring DevOps tasks to free capacity
- Implement review batching to reduce engineering-lead bottleneck
- Use parallel agent execution for independent subtasks

### 8. Resource Allocation Matrix
```
Optimal Allocation for Common Tasks:
Task Type           | Primary Team | Support Team | Capacity Needed
--------------------|--------------|--------------|----------------
Feature Development | Engineering  | Product      | 5-7 agents
Bug Fix Sprint      | Engineering  | QA           | 3-4 agents
Release Preparation | DevOps       | QA           | 4-5 agents
Requirements        | Product      | Engineering  | 2-3 agents
Performance Testing | QA           | Engineering  | 3-4 agents
```

### 9. Capacity Planning Actions

Suggest immediate actions:
```
🎯 Recommended Actions:
1. ✅ Immediately Available: Start new feature with engineering team
2. ⚠️ Plan Ahead: Schedule QA testing for tomorrow (better availability)
3. 🔄 Rebalance: Move low-priority docs to next sprint
4. 📅 Schedule: Book product-manager time for requirements review
```

## Interactive Planning

If specific team requested, provide detailed planning:
- Show exact agent availability windows
- Suggest optimal task scheduling
- Identify cross-team dependencies
- Recommend parallel execution opportunities

## Output Format

Present analysis with:
- Visual capacity bars and charts
- Color-coded utilization levels (green < 70%, yellow 70-90%, red > 90%)
- Clear recommendations with priority indicators
- Actionable next steps
- Time-based forecasts when requested