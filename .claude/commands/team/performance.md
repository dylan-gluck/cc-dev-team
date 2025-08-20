---
allowed-tools: Read, Task, Bash(jq:*), Bash(date:*), Bash(bc:*)
description: Display team performance metrics, analytics, and trends
argument-hint: [team-name] [--period 7d|30d|all] [--metric velocity|quality|efficiency]
model: sonnet
---

# Team Performance Analytics

Generate comprehensive performance metrics and analytics for teams.

## Context
- Team configuration: @.claude/orchestration/teams.json
- Team state: @.claude/orchestration/team-state.json
- Analysis period: $ARGUMENTS
- Report generated: !`date +"%Y-%m-%d %H:%M:%S"`

## Performance Dashboard

### 1. Executive Summary
```
📊 TEAM PERFORMANCE DASHBOARD
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Period: [Last 7 days/30 days/All time]
Generated: [timestamp]

Overall Performance Score: [85/100] 🟢

Key Metrics:
✅ Tasks Completed: 147
⏱️ Avg Completion Time: 2.3 hours
📈 Velocity Trend: ↗️ +15%
🎯 Success Rate: 96.5%
💡 Efficiency Score: 82%
```

### 2. Team Performance Comparison
```
TEAM PERFORMANCE RANKINGS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Rank | Team        | Score | Tasks | Success | Velocity | Trend
-----|-------------|-------|-------|---------|----------|-------
🥇 1 | Engineering |  92   |  68   |  98.5%  |   High   |  ↗️
🥈 2 | QA          |  88   |  45   |  95.6%  |   High   |  →
🥉 3 | DevOps      |  85   |  24   |  100%   |  Medium  |  ↗️
  4  | Product     |  78   |  10   |  90.0%  |   Low    |  ↘️

Legend: ↗️ Improving | → Stable | ↘️ Declining
```

### 3. Detailed Team Metrics
For each team or specified team:
```
🔧 ENGINEERING TEAM METRICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Performance Overview:
├── Tasks Completed: 68
├── Success Rate: 98.5%
├── Average Time: 2.1 hours
├── Velocity Score: 8.5/10
└── Quality Score: 9.2/10

Task Distribution:
Feature Development  ████████████░░░░ 45% (31 tasks)
Bug Fixes           ████████░░░░░░░░ 30% (20 tasks)
Refactoring         ████░░░░░░░░░░░░ 15% (10 tasks)
Documentation       ██░░░░░░░░░░░░░░ 10% (7 tasks)

Agent Performance:
Agent                 | Tasks | Avg Time | Success | Utilization
----------------------|-------|----------|---------|------------
engineering-lead      |  15   | 1.5 hrs  |  100%   |    65%
engineering-fullstack |  28   | 2.3 hrs  |  96.4%  |    78%
engineering-ux        |  12   | 2.0 hrs  |  100%   |    45%
engineering-test      |  10   | 1.8 hrs  |  100%   |    82%
engineering-docs      |   3   | 1.2 hrs  |  100%   |    25%

Time Analysis:
Fastest Task: 0.3 hours (documentation update)
Slowest Task: 6.2 hours (major refactoring)
Peak Hours: 10:00-14:00 (45% of tasks)
```

### 4. Velocity Trends
```
📈 VELOCITY TRENDS (Tasks/Day)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Engineering:
Day  1  2  3  4  5  6  7  
     █  █  █  █  █  █  █
     8  10 12 9  11 10 8   Avg: 9.7/day ↗️

Product:
Day  1  2  3  4  5  6  7
     █  █  █  █  █  █  █
     2  1  2  1  2  1  1   Avg: 1.4/day →

QA:
Day  1  2  3  4  5  6  7
     █  █  █  █  █  █  █
     6  7  6  8  5  7  6   Avg: 6.4/day →

DevOps:
Day  1  2  3  4  5  6  7
     █  █  █  █  █  █  █
     3  4  3  4  3  4  3   Avg: 3.4/day ↗️
```

### 5. Quality Metrics
```
🎯 QUALITY INDICATORS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

                    Engineering | Product | QA    | DevOps
--------------------|------------|---------|-------|--------
First-Time Success  |    85%     |   75%   |  92%  |   95%
Rework Required     |    15%     |   25%   |   8%  |    5%
Review Pass Rate    |    78%     |   N/A   |  88%  |   90%
Test Coverage       |    82%     |   N/A   |  95%  |   75%
Documentation       |    90%     |  100%   |  85%  |   80%
Code Quality Score  |    8.5     |   N/A   |  9.0  |   8.8

Overall Quality Score: 8.7/10 🟢
```

### 6. Efficiency Analysis
```
⚡ EFFICIENCY METRICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Team Efficiency Scores:
Engineering  ████████░░  82% (Good)
Product      ███████░░░  75% (Good)
QA           █████████░  90% (Excellent)
DevOps       ████████░░  85% (Good)

Bottleneck Analysis:
1. Code Review (Engineering): 35% of time
2. Requirements Clarification (Product): 40% of time
3. Test Execution (QA): 25% of time
4. Deployment Pipeline (DevOps): 30% of time

Optimization Opportunities:
• Parallelize code reviews to reduce wait time
• Implement requirement templates for clarity
• Automate repetitive test scenarios
• Optimize CI/CD pipeline stages
```

### 7. Cross-Team Collaboration
```
🤝 COLLABORATION METRICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Handoff Success Rate:
Engineering → QA:        95% successful
Product → Engineering:   88% successful
QA → DevOps:            92% successful
DevOps → Engineering:    90% successful

Average Handoff Time:
Engineering → QA:        0.5 hours
Product → Engineering:   1.2 hours
QA → DevOps:            0.3 hours
DevOps → Engineering:    0.8 hours

Collaboration Score: 91% 🟢
```

### 8. Performance Trends
```
📊 30-DAY PERFORMANCE TRENDS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

         Week 1 | Week 2 | Week 3 | Week 4 | Trend
---------|-------|--------|--------|--------|-------
Tasks    |  142  |  156   |  168   |  147   |  ↗️
Success  | 94.3% | 95.5%  | 96.4%  | 96.5%  |  ↗️
Velocity |  20.3 |  22.3  |  24.0  |  21.0  |  ↗️
Quality  |  8.2  |  8.4   |  8.6   |  8.7   |  ↗️
Efficiency| 78%  |  80%   |  81%   |  82%   |  ↗️
```

### 9. Individual Agent Leaderboard
```
🏆 TOP PERFORMING AGENTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Rank | Agent                  | Tasks | Success | Avg Time | Score
-----|------------------------|-------|---------|----------|-------
🥇 1 | qa-e2e                 |  28   |  100%   | 1.2 hrs  |  95
🥈 2 | engineering-fullstack  |  28   |  96.4%  | 2.3 hrs  |  92
🥉 3 | devops-cicd            |  12   |  100%   | 1.5 hrs  |  90
  4  | engineering-lead       |  15   |  100%   | 1.5 hrs  |  88
  5  | qa-scripts             |  17   |  94.1%  | 1.8 hrs  |  85
```

### 10. Recommendations
```
💡 PERFORMANCE RECOMMENDATIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Immediate Actions:
1. 🔴 Address Product team velocity decline
   - Consider adding product-analyst capacity
   - Review and optimize requirement processes

2. 🟡 Optimize Engineering code review process
   - Implement parallel reviews for large PRs
   - Consider automated review tools

3. 🟢 Scale successful QA automation
   - Expand qa-scripts capacity
   - Share automation patterns with other teams

Strategic Improvements:
• Implement cross-team pairing for knowledge transfer
• Establish performance baselines for new projects
• Create team playbooks for common scenarios
• Invest in tooling for bottleneck areas

Training Opportunities:
• Engineering: Advanced testing techniques
• Product: Agile requirement writing
• QA: Performance testing tools
• DevOps: Infrastructure as code
```

### 11. Performance Score Calculation
```
📐 PERFORMANCE SCORE BREAKDOWN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Overall Score: 85/100

Components:
Velocity      (25%): 21/25 - High task throughput
Quality       (25%): 22/25 - Excellent success rates
Efficiency    (20%): 16/20 - Good resource utilization
Collaboration (15%): 14/15 - Strong team coordination
Innovation    (10%):  8/10 - Process improvements
Reliability   (5%):   4/5  - Consistent delivery

Grade: B+ (Very Good)
```

## Custom Metrics

If specific metric requested (--metric flag):
- velocity: Focus on task completion rates
- quality: Emphasize success rates and rework
- efficiency: Highlight resource utilization

## Export Options

Provide export suggestions:
```
📤 Export Options:
- Full report: /team performance --export pdf
- CSV data: /team performance --export csv
- Dashboard link: /team performance --dashboard
- Email summary: /team performance --email team-leads
```

## Output Format

Present metrics with:
- Visual charts and progress bars
- Color-coded performance indicators
- Trend arrows for quick scanning
- Actionable recommendations
- Historical comparisons
- Clear score calculations