---
allowed-tools: Task, Read, Write, Bash(.claude/scripts/state_manager.py:*), Bash(.claude/scripts/event_stream.py:*), Bash(echo:*), Bash(printf:*)
description: Plan epic breakdown with team assignments and sprint allocation
argument-hint: <epic-description> [--duration weeks] [--teams team1,team2]
model: opus
---

# Epic Planning Orchestration

Break down an epic into sprints, tasks, and team assignments with comprehensive planning.

## Arguments
- Epic description: $ARGUMENTS (required)
- Duration: --duration [weeks] (default: 4)
- Teams: --teams [comma-separated list]

## Epic Analysis

### 1. Parse Epic Requirements
Extract from description:
- Epic title and goals
- Key features/deliverables
- Success criteria
- Technical requirements
- Duration estimate

### 2. Load Planning Context
- Team configurations: @.claude/orchestration/teams.json
- Workflow templates: @.claude/orchestration/workflows.json
- Current capacity: !`.claude/scripts/state_manager.py get agents --format table`
- Active sprints: !`.claude/scripts/state_manager.py get sprints`

## Epic Decomposition

### Feature Breakdown

Analyze epic into features:
```
Epic: [epic-title]
│
├── Feature 1: [name]
│   ├── User Story 1.1
│   ├── User Story 1.2
│   └── User Story 1.3
│
├── Feature 2: [name]
│   ├── User Story 2.1
│   └── User Story 2.2
│
└── Feature 3: [name]
    ├── User Story 3.1
    ├── User Story 3.2
    └── User Story 3.3
```

### Task Generation

Convert features to tasks:
```
Task ID    | Feature      | Description                | Type     | Points
-----------|--------------|----------------------------|----------|--------
epic-1-001 | Auth        | Implement OAuth2 flow      | feature  | 5
epic-1-002 | Auth        | Add 2FA support           | feature  | 3
epic-1-003 | Auth        | Create login UI           | ui       | 3
epic-1-004 | Auth        | Write auth tests          | test     | 2
epic-1-005 | API         | Design REST endpoints     | design   | 2
epic-1-006 | API         | Implement CRUD operations | backend  | 5
...
```

### Dependency Mapping

Identify task dependencies:
```
graph TD
    epic-1-001[OAuth2] --> epic-1-003[Login UI]
    epic-1-001[OAuth2] --> epic-1-002[2FA]
    epic-1-005[API Design] --> epic-1-006[CRUD Ops]
    epic-1-006[CRUD Ops] --> epic-1-007[API Tests]
    epic-1-003[Login UI] --> epic-1-008[E2E Tests]
```

## Sprint Planning

### Sprint Allocation

Distribute tasks across sprints:

```
┌─────────────────────────────────────────────────┐
│              EPIC SPRINT PLANNING               │
├─────────────────────────────────────────────────┤
│ Epic: [epic-title]                              │
│ Duration: [X] weeks ([Y] sprints)               │
│ Total Points: [total]                           │
│ Teams: [team-list]                              │
└─────────────────────────────────────────────────┤

Sprint 1: Foundation (Week 1-2)
├── Goals: Core infrastructure and authentication
├── Points: 18
├── Teams: Engineering, DevOps
└── Tasks:
    • epic-1-001: OAuth2 implementation (5 pts)
    • epic-1-005: API design (2 pts)
    • epic-1-009: Database schema (3 pts)
    • epic-1-010: CI/CD setup (3 pts)
    • epic-1-003: Login UI (3 pts)
    • epic-1-011: Unit test framework (2 pts)

Sprint 2: Core Features (Week 3-4)
├── Goals: Main functionality and integration
├── Points: 21
├── Teams: Engineering, QA
└── Tasks:
    • epic-1-002: 2FA support (3 pts)
    • epic-1-006: CRUD operations (5 pts)
    • epic-1-012: Data models (4 pts)
    • epic-1-004: Auth tests (2 pts)
    • epic-1-007: API tests (3 pts)
    • epic-1-013: Integration tests (4 pts)

Sprint 3: Enhancement (Week 5-6)
├── Goals: Advanced features and optimization
├── Points: 16
├── Teams: Engineering, Product, QA
└── Tasks:
    • epic-1-014: Advanced search (5 pts)
    • epic-1-015: Caching layer (3 pts)
    • epic-1-016: Performance optimization (4 pts)
    • epic-1-017: Security audit (2 pts)
    • epic-1-018: Load testing (2 pts)

Sprint 4: Polish & Release (Week 7-8)
├── Goals: Final testing, documentation, and release
├── Points: 12
├── Teams: All teams
└── Tasks:
    • epic-1-008: E2E tests (3 pts)
    • epic-1-019: Documentation (3 pts)
    • epic-1-020: Bug fixes (3 pts)
    • epic-1-021: Release preparation (3 pts)
```

## Team Assignment Matrix

### Resource Allocation

```
Team         | Sprint 1 | Sprint 2 | Sprint 3 | Sprint 4 | Total
-------------|----------|----------|----------|----------|-------
Engineering  | 70%      | 80%      | 60%      | 40%      | 62.5%
QA           | 10%      | 40%      | 30%      | 50%      | 32.5%
DevOps       | 20%      | 10%      | 10%      | 30%      | 17.5%
Product      | 10%      | 10%      | 30%      | 20%      | 17.5%
```

### Team Responsibilities

```
Engineering Team:
• Lead: Architecture decisions, code reviews
• Fullstack: Feature implementation
• UX: UI/UX implementation
• API: Backend services

QA Team:
• Test planning and strategy
• Automated test development
• E2E testing
• Performance testing

DevOps Team:
• Infrastructure setup
• CI/CD pipeline
• Deployment automation
• Monitoring setup

Product Team:
• Requirements refinement
• Acceptance criteria
• User story validation
• Release coordination
```

## Risk Assessment

### Identify Risks

```
⚠️ Identified Risks:

1. HIGH: Authentication complexity
   - Impact: Could delay Sprint 1
   - Mitigation: Allocate senior engineer
   - Contingency: Extend sprint by 3 days

2. MEDIUM: Third-party API dependencies
   - Impact: Blocking API development
   - Mitigation: Build mock services first
   - Contingency: Implement adapter pattern

3. MEDIUM: Test coverage requirements
   - Impact: May slow down development
   - Mitigation: Parallel test development
   - Contingency: Dedicated test sprint

4. LOW: Documentation lag
   - Impact: Delayed knowledge transfer
   - Mitigation: Document as you code
   - Contingency: Documentation sprint
```

## Resource Projections

### Token & Time Estimates

```
Resource Projections:
                Sprint 1 | Sprint 2 | Sprint 3 | Sprint 4 | Total
Agents:         8        | 10       | 9        | 7        | 34
Tokens:         80,000   | 100,000  | 90,000   | 70,000   | 340,000
Runtime (hrs):  40       | 50       | 45       | 35       | 170
Cost Est:       $80      | $100     | $90      | $70      | $340
```

## Epic Planning Preview

```
┌─────────────────────────────────────────────────┐
│            EPIC PLANNING PREVIEW                │
├─────────────────────────────────────────────────┤
│ Epic: [epic-title]                              │
│                                                  │
│ Breakdown:                                      │
│ • Features: 6                                   │
│ • User Stories: 18                              │
│ • Tasks: 42                                     │
│ • Total Points: 67                              │
│                                                  │
│ Timeline:                                       │
│ • Duration: 8 weeks                             │
│ • Sprints: 4                                    │
│ • Start: [date]                                 │
│ • End: [date]                                   │
│                                                  │
│ Teams Required:                                 │
│ • Engineering (62.5% allocation)                │
│ • QA (32.5% allocation)                         │
│ • DevOps (17.5% allocation)                     │
│ • Product (17.5% allocation)                    │
│                                                  │
│ Resource Estimates:                             │
│ • Total Agents: 34                              │
│ • Total Tokens: ~340,000                        │
│ • Total Runtime: ~170 hours                     │
│                                                  │
│ Key Milestones:                                 │
│ • Week 2: Authentication complete               │
│ • Week 4: Core features done                    │
│ • Week 6: Feature complete                      │
│ • Week 8: Production ready                      │
└─────────────────────────────────────────────────┤
```

## Confirmation Flow

```
Proceed with epic planning?

This will:
✓ Create epic: [epic-id]
✓ Generate 4 sprints
✓ Create 42 tasks
✓ Set up team assignments
✓ Initialize tracking

Note: This creates the plan but does NOT start execution.
You'll need to explicitly start each sprint.

Confirm? (yes/no/modify):
```

## Epic Creation

If confirmed:

### 1. Create Epic Record

```python
epic_data = {
    "id": epic_id,
    "title": epic_title,
    "description": epic_description,
    "status": "planned",
    "created_at": timestamp,
    "features": features_list,
    "sprints": sprint_ids,
    "total_points": total_points,
    "teams_assigned": teams_list,
    "milestones": milestones,
    "risks": risks_list,
    "success_criteria": criteria_list
}
```

Save: !`.claude/scripts/state_manager.py set "epics.[epic-id]" '[epic-data]'`

### 2. Create Sprint Records

For each sprint:
```python
sprint_data = {
    "id": sprint_id,
    "epic_id": epic_id,
    "name": sprint_name,
    "goals": sprint_goals,
    "status": "planned",
    "start_date": calculated_start,
    "end_date": calculated_end,
    "tasks": task_list,
    "teams": team_assignments,
    "points": sprint_points
}
```

### 3. Create Task Records

For each task:
```python
task_data = {
    "id": task_id,
    "epic_id": epic_id,
    "sprint_id": assigned_sprint,
    "description": task_description,
    "type": task_type,
    "points": story_points,
    "dependencies": dependency_list,
    "assigned_team": team,
    "status": "backlog"
}
```

### 4. Generate Planning Artifacts

Create planning documents:

**Epic Charter** (`.claude/epics/[epic-id]/charter.md`):
- Vision and goals
- Success metrics
- Stakeholders
- Constraints
- Assumptions

**Sprint Plans** (`.claude/epics/[epic-id]/sprint-[n].md`):
- Sprint goals
- Task breakdown
- Team assignments
- Acceptance criteria

**Dependency Graph** (`.claude/epics/[epic-id]/dependencies.md`):
- Visual dependency map
- Critical path
- Risk areas

## Post-Planning Dashboard

```
✅ Epic Planning Complete!

📋 Epic: [epic-title]
ID: [epic-id]
Status: Planned and ready for execution

📊 Planning Summary:
• Features: 6 defined
• Sprints: 4 planned
• Tasks: 42 created
• Teams: 4 assigned
• Duration: 8 weeks

📁 Planning Artifacts:
• Epic charter: .claude/epics/[epic-id]/charter.md
• Sprint plans: .claude/epics/[epic-id]/sprint-*.md
• Task backlog: .claude/epics/[epic-id]/backlog.json
• Risk register: .claude/epics/[epic-id]/risks.md

🚀 Next Steps:
1. Review plan with stakeholders
2. Start first sprint: /orchestrate sprint start [sprint-1-id]
3. Activate teams: /orchestrate team activate [team]
4. Set up monitoring: /orchestrate epic monitor [epic-id]

📅 Suggested Timeline:
• Week 1-2: Sprint 1 - Foundation
• Week 3-4: Sprint 2 - Core Features
• Week 5-6: Sprint 3 - Enhancement
• Week 7-8: Sprint 4 - Polish & Release

💡 Tips:
• Review dependencies before starting
• Consider running sprints with 1-day overlap
• Set up daily standups for coordination
• Monitor velocity to adjust plans
```

## Alternative Planning Modes

Offer different planning approaches:

```
Planning Modes Available:

1. Waterfall: Sequential phases, fixed scope
2. Agile: Iterative sprints, flexible scope
3. Kanban: Continuous flow, WIP limits
4. Hybrid: Mixed approach

Current: Agile (default)
Change mode? (1-4/no):
```

## Success Criteria

Epic planning successful when:
- [ ] Epic record created
- [ ] Features decomposed
- [ ] Tasks generated with estimates
- [ ] Dependencies mapped
- [ ] Sprints planned
- [ ] Teams assigned
- [ ] Risks identified
- [ ] Artifacts generated
- [ ] Plan reviewed and confirmed