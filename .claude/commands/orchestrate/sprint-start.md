---
allowed-tools: Task, Read, Write, Bash(git:*), Bash(.claude/scripts/state_manager.py:*), Bash(.claude/scripts/orchestrate.py:*), Bash(.claude/scripts/event_stream.py:*), Bash(echo:*), Bash(printf:*)
description: Start sprint with preview, confirmation, and team orchestration
argument-hint: [sprint-id] [--team engineering|product|qa|devops]
model: sonnet
---

# Start Sprint Orchestration

Initialize a new sprint with full team orchestration, including preview and confirmation.

## Arguments
- Sprint ID: $ARGUMENTS (or prompt if not provided)
- Team selection can be specified with --team flag

## Pre-Flight Checks

1. **Validate Configuration**
   - Check teams configuration: @.claude/orchestration/teams.json
   - Check settings: @.claude/orchestration/settings.json
   - Verify state directory exists: !`test -d .claude/state && echo "✅ State directory ready" || echo "❌ State directory missing"`

2. **Check Current State**
   - Active sprints: !`.claude/scripts/state_manager.py get sprints --format table`
   - Active agents: !`.claude/scripts/state_manager.py get agents.active --format table`
   - Resource usage: !`.claude/scripts/observability.py metrics`

## Sprint Analysis

Parse sprint requirements from arguments or prompt user:
1. Sprint ID (e.g., "sprint-3", "sprint-auth-2")
2. Epic association (if applicable)
3. Primary team(s) to activate
4. Sprint goals and deliverables
5. Task list or backlog items

## Resource Estimation

Calculate required resources based on sprint scope:

### Agent Requirements
- Analyze tasks to determine agent types needed
- Calculate capacity based on team configuration
- Estimate parallelization opportunities

### Resource Projections
```
Agents to spawn: [calculated number]
Estimated tokens: [token estimate]
Estimated runtime: [time in minutes]
Peak concurrency: [max parallel agents]
```

## Preview Generation

### 📋 Sprint Overview
```
Sprint: [sprint-id]
Epic: [epic-id if applicable]
Duration: [days]
Start Date: [today]
End Date: [calculated]
```

### 👥 Team Allocation
Display table of teams and agents to be activated:
```
Team         | Orchestrator          | Agents | Model  | Capacity
-------------|--------------------- |--------|--------|----------
Engineering  | engineering-director  | 5      | opus   | 100%
QA           | qa-director          | 3      | opus   | 75%
```

### 📝 Task Breakdown
Show initial task distribution:
```
Priority | Task ID | Description           | Assigned Team | Estimate
---------|---------|----------------------|---------------|----------
High     | task-1  | OAuth implementation | Engineering   | 5 points
High     | task-2  | UI components        | Engineering   | 3 points
Medium   | task-3  | Test automation      | QA            | 3 points
```

### 💰 Resource Estimates
```
Resource         | Estimate    | Limit      | Usage %
-----------------|-------------|------------|----------
Agents           | 8           | 10         | 80%
Tokens           | 75,000      | 100,000    | 75%
Runtime          | 45 min      | 60 min     | 75%
```

### ⚠️ Warnings and Notices
- Check if estimates exceed warning thresholds
- Note any resource constraints
- Highlight dependencies or blockers

## Confirmation Flow

### Display Confirmation Prompt
```
┌─────────────────────────────────────────────────┐
│          SPRINT ORCHESTRATION PREVIEW           │
├─────────────────────────────────────────────────┤
│ This operation will:                            │
│ • Spawn 8 agents across 2 teams                 │
│ • Consume approximately 75,000 tokens           │
│ • Run for approximately 45 minutes              │
│ • Execute 12 tasks in parallel batches          │
│                                                  │
│ Teams to activate:                              │
│ • Engineering (5 agents)                        │
│ • QA (3 agents)                                 │
│                                                  │
│ ⚠️ This action cannot be undone without         │
│    stopping all orchestration activities.       │
└─────────────────────────────────────────────────┘

Proceed with sprint orchestration? (yes/no):
```

## Orchestration Execution

If confirmed, execute the following steps:

### 1. Initialize Sprint State
```python
# Update state with sprint initialization
sprint_data = {
    "id": sprint_id,
    "status": "initializing",
    "start_date": today,
    "end_date": calculated_end,
    "teams": selected_teams,
    "tasks": task_breakdown,
    "metrics": initial_metrics
}
```
- Update via: !`.claude/scripts/state_manager.py set sprints.[sprint-id] '[sprint-data]'`

### 2. Emit Start Event
- Log sprint start: !`.claude/scripts/event_stream.py emit sprint_started '{"sprint_id": "[id]", "teams": [...]}' --source orchestrator`

### 3. Spawn Team Orchestrators

Use Task tool to spawn orchestrators in parallel:

**Engineering Team Orchestrator:**
```
You are the Engineering Team orchestrator for [sprint-id].

Sprint Context:
- Sprint goals: [goals]
- Tasks assigned: [task-list]
- Team capacity: [capacity]

Your responsibilities:
1. Coordinate engineering team agents
2. Manage task dependencies
3. Track progress and blockers
4. Ensure code quality standards

Begin by:
1. Analyzing the task list
2. Creating execution plan
3. Spawning specialized agents for parallel work
4. Monitoring progress
```

**QA Team Orchestrator:**
```
You are the QA Team orchestrator for [sprint-id].

Sprint Context:
- Sprint goals: [goals]
- Testing requirements: [requirements]
- Team capacity: [capacity]

Your responsibilities:
1. Coordinate QA team agents
2. Ensure test coverage
3. Track quality metrics
4. Validate implementations

Begin by:
1. Creating test plan
2. Assigning test tasks
3. Setting up automation
4. Monitoring quality
```

### 4. Update Sprint Status
- Mark sprint as active: !`.claude/scripts/state_manager.py update-task [sprint-id] active`

### 5. Monitor Initial Progress
- Check agent spawning: !`.claude/scripts/state_manager.py get agents.active --format table`
- Display initial status: !`.claude/scripts/observability.py sprint [sprint-id]`

## Post-Start Actions

### Display Status Dashboard
Show real-time sprint status:
```
Sprint [sprint-id] Started Successfully!

📊 Initial Status:
• Teams activated: 2
• Orchestrators running: 2
• Agents spawning: 6
• Tasks queued: 12

📍 Next Steps:
• Monitor progress: /orchestrate sprint status
• View agents: /orchestrate agents status
• Check metrics: /orchestrate metrics

💡 Tips:
• Use /orchestrate sprint status for real-time updates
• Check /orchestrate stop if you need to halt operations
• View detailed logs in .claude/state/events.jsonl
```

## Error Handling

Handle potential issues:
- Configuration missing or invalid
- State file locked or corrupted
- Resource limits already exceeded
- Previous sprint still active
- Network or API issues

Provide clear error messages and remediation steps:
```
❌ Error: Another sprint is currently active
   
   Active Sprint: sprint-2
   Status: in_progress
   
   Options:
   1. Complete current sprint: /orchestrate sprint stop
   2. View current status: /orchestrate sprint status
   3. Force stop (not recommended): /orchestrate stop --force
```

## Rollback Procedure

If issues occur during initialization:
1. Stop spawned agents
2. Revert state changes
3. Emit failure event
4. Display error summary
5. Suggest corrective actions

## Success Criteria

Sprint start is successful when:
- [ ] Sprint state initialized
- [ ] Team orchestrators spawned
- [ ] Initial tasks assigned
- [ ] Metrics collection started
- [ ] Event stream updated
- [ ] Status dashboard displayed