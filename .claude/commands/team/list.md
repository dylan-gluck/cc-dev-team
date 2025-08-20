---
allowed-tools: Read, Glob, Bash(jq:*), LS
description: List all available teams and their agents with detailed information
argument-hint: [--format tree|table|json] [--team team-name]
model: haiku
---

# List Teams and Agents

Display comprehensive listing of all available teams, their agents, and capabilities.

## Context
- Team configuration: @.claude/orchestration/teams.json
- Agent directory: !`fd -t f . .claude/agents/ -e md | wc -l` total agents
- Display format: $ARGUMENTS

## Team Listing

### 1. Organization Tree View (Default)
```
🏢 ORGANIZATION STRUCTURE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📁 Teams (4 teams, 19 total capacity)
│
├── 🔧 Engineering Team [opus] (9 capacity)
│   ├── 👤 engineering-lead [opus] - Technical Leadership (1)
│   │   └── Skills: architecture, code_review, technical_spec
│   ├── 👤 engineering-fullstack [sonnet] - Full Stack Development (3)
│   │   └── Skills: frontend, backend, api, database
│   ├── 👤 engineering-ux [sonnet] - UX Engineering (2)
│   │   └── Skills: ui_components, responsive_design, accessibility
│   ├── 👤 engineering-test [haiku] - Quality Assurance (2)
│   │   └── Skills: unit_testing, integration_testing, e2e_testing
│   └── 👤 engineering-docs [haiku] - Documentation (1)
│       └── Skills: technical_writing, api_documentation
│
├── 📊 Product Team [opus] (2 capacity)
│   ├── 👤 product-manager [opus] - Product Management (1)
│   │   └── Skills: requirements, user_stories, prioritization
│   └── 👤 product-analyst [sonnet] - Business Analysis (1)
│       └── Skills: requirements_analysis, process_mapping
│
├── ✅ QA Team [opus] (5 capacity)
│   ├── 👤 qa-e2e [sonnet] - End-to-End Testing (2)
│   │   └── Skills: e2e_testing, user_journey_validation
│   ├── 👤 qa-scripts [haiku] - Test Automation (2)
│   │   └── Skills: test_scripting, automation_frameworks
│   └── 👤 qa-analyst [haiku] - Quality Analysis (1)
│       └── Skills: test_reporting, metrics_analysis
│
└── 🚀 DevOps Team [opus] (3 capacity)
    ├── 👤 devops-cicd [sonnet] - CI/CD Pipeline Management (1)
    │   └── Skills: github_actions, build_automation
    ├── 👤 devops-infrastructure [sonnet] - Infrastructure (1)
    │   └── Skills: docker, kubernetes, terraform
    └── 👤 devops-release [haiku] - Release Coordination (1)
        └── Skills: version_management, changelog_generation
```

### 2. Table Format View
If --format table specified:
```
TEAMS AND AGENTS ROSTER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Team         | Agent                    | Role                  | Cap | Model  | Status
-------------|--------------------------|----------------------|-----|--------|--------
Engineering  | engineering-lead         | Technical Leadership |  1  | opus   | Ready
             | engineering-fullstack    | Full Stack Dev       |  3  | sonnet | Ready
             | engineering-ux           | UX Engineering       |  2  | sonnet | Ready
             | engineering-test         | Quality Assurance    |  2  | haiku  | Ready
             | engineering-docs         | Documentation        |  1  | haiku  | Ready
-------------|--------------------------|----------------------|-----|--------|--------
Product      | product-manager          | Product Management   |  1  | opus   | Ready
             | product-analyst          | Business Analysis    |  1  | sonnet | Ready
-------------|--------------------------|----------------------|-----|--------|--------
QA           | qa-e2e                   | E2E Testing          |  2  | sonnet | Ready
             | qa-scripts               | Test Automation      |  2  | haiku  | Ready
             | qa-analyst               | Quality Analysis     |  1  | haiku  | Ready
-------------|--------------------------|----------------------|-----|--------|--------
DevOps       | devops-cicd              | CI/CD Pipeline       |  1  | sonnet | Ready
             | devops-infrastructure    | Infrastructure       |  1  | sonnet | Ready
             | devops-release           | Release Coord        |  1  | haiku  | Ready
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total: 4 teams | 13 unique agents | 19 total capacity
```

### 3. Detailed Team Information
If --team specified, show detailed info:
```
🔧 ENGINEERING TEAM DETAILS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Overview:
- Name: Engineering Team
- Description: Core development team for implementation tasks
- Orchestrator: engineering-director
- Model Preference: opus
- Total Capacity: 9

Settings:
- Max Parallel Agents: 5
- Code Review Required: Yes
- Test Coverage Threshold: 80%
- Auto Documentation: Enabled
- Branch Strategy: feature/{epic}/{task}

Team Members:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. engineering-lead
   Role: Technical Leadership
   Capacity: 1
   Model: opus
   Skills:
   - architecture
   - code_review
   - technical_spec
   - data_model_design
   Responsibilities:
   - Write technical specifications
   - Review all code changes
   - Design system architecture
   - Make technical decisions

2. engineering-fullstack
   Role: Full Stack Development
   Capacity: 3
   Model: sonnet
   Skills:
   - frontend
   - backend
   - api
   - database
   - integration
   Responsibilities:
   - Implement features end-to-end
   - Write unit and integration tests
   - Create API endpoints
   - Build UI components

[Additional agents...]

Workflows:
- Task Flow: specification → implementation → testing → review → documentation
- Review Requirements:
  - Code: engineering-lead
  - Design: engineering-ux, engineering-lead
  - Tests: engineering-test
```

### 4. Skills Matrix
Show skills across all teams:
```
📊 ORGANIZATION SKILLS MATRIX
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Skill                    | Teams Available | Agents with Skill
-------------------------|-----------------|-------------------
Frontend Development     | Engineering     | engineering-fullstack, engineering-ux
Backend Development      | Engineering     | engineering-fullstack
API Development          | Engineering     | engineering-fullstack
Database                 | Engineering     | engineering-fullstack
UI Components            | Engineering     | engineering-ux
Testing                  | Engineering, QA | engineering-test, qa-e2e, qa-scripts
Documentation            | Engineering     | engineering-docs
Requirements Analysis    | Product         | product-manager, product-analyst
CI/CD                    | DevOps          | devops-cicd
Infrastructure           | DevOps          | devops-infrastructure
Architecture             | Engineering     | engineering-lead
Code Review              | Engineering     | engineering-lead
Process Mapping          | Product         | product-analyst
Test Automation          | QA              | qa-scripts
Performance Analysis     | QA              | qa-analyst
```

### 5. Agent Availability Summary
Quick availability check:
```
⚡ QUICK AVAILABILITY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Immediately Available (100% free):
✅ engineering-lead (1 capacity)
✅ engineering-fullstack (3 capacity)
✅ engineering-ux (2 capacity)
✅ product-manager (1 capacity)
✅ qa-e2e (2 capacity)
✅ devops-cicd (1 capacity)

Partially Available (50-99% free):
⚠️ None currently

Busy (< 50% free):
❌ None currently

Total Available Capacity: 19/19 (100%)
```

### 6. Team Comparison
Compare team capabilities:
```
📈 TEAM COMPARISON
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Metric              | Engineering | Product | QA  | DevOps
--------------------|-------------|---------|-----|--------
Total Capacity      |      9      |    2    |  5  |   3
Max Parallel        |      5      |    3    |  4  |   3
Unique Agents       |      5      |    2    |  3  |   3
Model (Primary)     |    opus     |  opus   | opus|  opus
Avg Model Cost      |   Medium    |  High   | Low | Medium
Specializations     |      5      |    2    |  3  |   3
```

### 7. JSON Format
If --format json specified, output raw JSON from teams.json

### 8. Additional Agents
List agents not assigned to teams:
```
📦 UNASSIGNED AGENTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Specialist Agents (not in teams):
- research-ai: AI/ML research specialist
- meta-agent: Agent creation specialist
- meta-summary: Audio summary generator
- [other unassigned agents...]

Total: X unassigned specialist agents
```

## Statistics Summary

End with overall statistics:
```
📊 ORGANIZATION STATISTICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Teams:                  4
Total Team Agents:      13 unique (19 capacity)
Specialist Agents:      X
Total Agents:           Y
Total Capacity:         19

Model Distribution:
- Opus:    X agents (Y%)
- Sonnet:  X agents (Y%)
- Haiku:   X agents (Y%)

Capability Coverage:
- Development:    ████████░░ 80%
- Testing:        ████████░░ 80%
- Documentation:  ██████░░░░ 60%
- DevOps:         ███████░░░ 70%
- Product:        ██████░░░░ 60%
```

## Output Format

Adapt output based on format parameter:
- Default/tree: Hierarchical tree view
- table: Structured table format
- json: Raw JSON output
- Specific team: Detailed team information

Always include:
- Clear visual organization
- Capacity indicators
- Skill listings
- Status information