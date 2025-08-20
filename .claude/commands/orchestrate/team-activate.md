---
allowed-tools: Task, Read, Bash(.claude/scripts/state_manager.py:*), Bash(.claude/scripts/event_stream.py:*), Bash(.claude/scripts/observability.py:*), Bash(echo:*), Write
description: Activate specific team for coordination with orchestrator spawning
argument-hint: <team-name> [--capacity percentage] [--focus area]
model: sonnet
---

# Team Activation

Activate a specific team by spawning its orchestrator and preparing for coordination.

## Arguments
- Team name: $ARGUMENTS (required: engineering|product|qa|devops)
- Capacity: --capacity [1-100] (percentage of team to activate)
- Focus area: --focus [specific area of work]

## Team Validation

### 1. Verify Team Exists
Load team configuration: @.claude/orchestration/teams.json
- Check if team name is valid
- Get team details and settings
- Verify orchestrator is defined

### 2. Check Current State
Assess team's current status:
- Active agents: !`.claude/scripts/state_manager.py get agents.active --format table`
- Current capacity utilization
- Any existing orchestrator

## Team Analysis

### Display Team Information

```
┌─────────────────────────────────────────────────┐
│             TEAM ACTIVATION PREVIEW             │
├─────────────────────────────────────────────────┤
│ Team: [team-name]                               │
│ Description: [team-description]                 │
│                                                  │
│ Team Composition:                               │
│ • Orchestrator: [orchestrator-name]             │
│ • Members: [count] agents available             │
│ • Model preference: [model]                     │
│                                                  │
│ Capabilities:                                   │
│ • [skill-1]                                     │
│ • [skill-2]                                     │
│ • [skill-3]                                     │
│                                                  │
│ Current Status:                                 │
│ • Active agents: [X/Y]                          │
│ • Capacity used: [percentage]%                  │
│ • Current tasks: [count]                        │
│                                                  │
│ Activation Plan:                                │
│ • Spawn orchestrator: [orchestrator-name]       │
│ • Reserve capacity: [percentage]%               │
│ • Focus area: [focus-area or "general"]        │
│ • Estimated tokens: [amount]                    │
└─────────────────────────────────────────────────┤
```

### Team Member Details

Show available team members:

```
Agent Role              | Capacity | Skills                    | Status
------------------------|----------|---------------------------|--------
engineering-lead        | 1        | architecture, review      | available
engineering-fullstack   | 3        | frontend, backend, api    | 2 available
engineering-ux          | 2        | ui, design, responsive    | available
engineering-test        | 2        | testing, automation       | 1 available
```

## Resource Estimation

### Calculate Activation Costs

```
Resource Requirements:
• Orchestrator tokens: ~10,000 (startup + coordination)
• Per-agent tokens: ~5,000 each
• Total estimated: [calculated based on capacity]
• Runtime estimate: [30-60 minutes for orchestrator]
```

### Check Against Limits

```
Resource Check:
                Current | Requested | Limit   | Status
Agents:        3        | +5        | 10      | ✅ OK
Tokens:        25,000   | +35,000   | 100,000 | ✅ OK
Runtime:       15 min   | +45 min   | 60 min  | ⚠️ Warning
```

## Confirmation Flow

### Display Confirmation

```
Activate [team-name] team?

This will:
✓ Spawn [orchestrator-name] orchestrator
✓ Reserve [X]% team capacity
✓ Enable coordination for [focus-area]
✓ Consume approximately [tokens] tokens

⚠️ Note: Orchestrator will coordinate team agents
   but won't auto-spawn without further commands

Proceed? (yes/no):
```

## Team Activation Process

### 1. Update Team State

Create team activation record:
```python
activation_data = {
    "team": team_name,
    "orchestrator": orchestrator_id,
    "activated_at": timestamp,
    "capacity_reserved": capacity_percentage,
    "focus_area": focus_area,
    "status": "activating"
}
```

Save: !`.claude/scripts/state_manager.py set "teams.active.[team-name]" '[activation-data]'`

### 2. Spawn Team Orchestrator

Prepare orchestrator context:

```markdown
# [Team] Orchestrator Activation

You are the [team-name] team orchestrator.

## Team Configuration
- Team: [team-name]
- Capacity: [percentage]% reserved
- Focus: [focus-area or "general coordination"]
- Available members: [member-list]

## Team Capabilities
[List team skills and specializations]

## Current Context
- Active sprint: [sprint-id if any]
- Pending tasks: [count]
- Team utilization: [percentage]%

## Your Responsibilities
1. Coordinate team member activities
2. Manage task assignments within team
3. Monitor team performance and capacity
4. Handle inter-team communications
5. Escalate blockers and issues
6. Ensure quality standards

## Immediate Actions
1. Review team status and capacity
2. Check for pending team tasks
3. Prepare for task delegation
4. Set up team communication channels
5. Initialize team metrics tracking

## Guidelines
- Only spawn agents when explicitly requested
- Always show preview before major actions
- Maintain team capacity within limits
- Coordinate with other team orchestrators
- Report status regularly

## Available Commands
You can coordinate your team using:
- Task tool: Spawn team member agents
- State management: Track team progress
- Message bus: Communicate with other teams
- Observability: Monitor team metrics

Begin by reviewing current team status and preparing for coordination.
```

Spawn orchestrator using Task tool with above context.

### 3. Initialize Team Workspace

Set up team-specific resources:

```python
# Create team workspace
workspace_data = {
    "tasks": {"pending": [], "active": [], "completed": []},
    "agents": {"available": member_list, "busy": []},
    "metrics": {
        "tasks_completed": 0,
        "average_duration": 0,
        "velocity": 0
    },
    "communications": {"inbox": [], "outbox": []}
}
```

### 4. Establish Communication Channels

Set up team message queue:
- !`.claude/scripts/message_bus.py send system [orchestrator-id] TEAM_ACTIVATED '{"team": "[team-name]", "capacity": [percentage]}' --priority high`

### 5. Emit Activation Event

Log team activation:
- !`.claude/scripts/event_stream.py emit team_activated '{"team": "[team-name]", "orchestrator": "[orchestrator-id]", "capacity": [percentage]}' --source orchestrator`

## Post-Activation Dashboard

### Display Team Status

```
✅ [Team-name] Team Activated Successfully

👤 Orchestrator Details:
• ID: [orchestrator-id]
• Status: Active
• Model: [model]
• Focus: [focus-area]

📊 Team Capacity:
• Total members: [count]
• Reserved: [percentage]%
• Available agents: [count]
• Current load: [percentage]%

🎯 Ready for:
• Task delegation
• Sprint participation
• Cross-team coordination
• Specialized [focus-area] work

📋 Next Steps:
1. Delegate tasks: /orchestrate task delegate "[task]" --team [team-name]
2. Check status: /orchestrate team status [team-name]
3. Assign work: /orchestrate team assign [team-name] [work-package]
4. View metrics: /orchestrate team metrics [team-name]

💡 Tips:
• Orchestrator is now monitoring for team tasks
• Use task delegation to assign work
• Team will coordinate internally
• Monitor progress with status commands
```

## Team Coordination Features

### Work Assignment

After activation, enable work assignment:
```
📦 Work Packages Available:
1. Sprint tasks for [team-name]
2. Backlog items matching team skills
3. Cross-team dependencies
4. Technical debt items

Assign work package? (1-4/none):
```

### Capacity Management

Show capacity allocation:
```
Team Capacity Allocation:
████████████████░░░░ 80% reserved
                     20% available

By Role:
Lead:       ████████████████████ 100% (1/1)
Fullstack:  ████████░░░░░░░░░░░░ 40% (1.2/3)
UX:         ██████████░░░░░░░░░░ 50% (1/2)
Test:       ░░░░░░░░░░░░░░░░░░░░ 0% (0/2)
```

### Focus Area Configuration

If focus area specified:
```
🎯 Focus Area: [focus-area]

Optimizing team for:
• Prioritizing [focus-area] tasks
• Allocating senior members to [focus-area]
• Loading relevant context and documentation
• Setting up specialized tools

Configuration complete ✓
```

## Inter-Team Coordination

### Enable Cross-Team Communication

```
🔗 Inter-Team Coordination Enabled

Connected Teams:
• [team-1] ←→ [team-2]
• Shared communication channel established
• Dependency tracking enabled
• Handoff protocols activated
```

### Orchestrator Network

Show orchestrator connections:
```
Active Orchestrators:
┌──────────────┐     ┌──────────────┐
│ Engineering  │────│   Product     │
│ Orchestrator │     │ Orchestrator  │
└──────────────┘     └──────────────┘
        │                    │
        └────────┬───────────┘
                 │
         ┌──────────────┐
         │      QA      │
         │ Orchestrator │
         └──────────────┘
```

## Error Handling

### Team Already Active
```
⚠️ Team [team-name] is already active

Current orchestrator: [orchestrator-id]
Active since: [timestamp]
Current capacity: [percentage]%

Options:
1. Increase capacity reservation
2. Change focus area
3. Restart orchestrator
4. Cancel

Choice (1-4):
```

### Insufficient Capacity
```
❌ Error: Insufficient capacity for team activation

Requested: [percentage]% ([X] agents)
Available: [percentage]% ([Y] agents)

Options:
1. Reduce capacity request
2. Stop other teams to free capacity
3. Wait for agents to become available
4. Override limits (requires confirmation)

Choice (1-4):
```

### Orchestrator Spawn Failure
```
❌ Error: Failed to spawn orchestrator

Reason: [error-message]

Attempting fallback...
✓ Spawning with reduced model: sonnet
✓ Orchestrator started with limitations

Note: Some coordination features may be limited
```

## Deactivation Option

Provide deactivation command:
```
To deactivate this team later:
/orchestrate team deactivate [team-name]

This will:
• Stop the orchestrator
• Complete current tasks
• Free reserved capacity
• Archive team state
```

## Success Criteria

Team activation successful when:
- [ ] Team configuration validated
- [ ] Orchestrator successfully spawned
- [ ] Team state initialized
- [ ] Communication channels established
- [ ] Capacity properly reserved
- [ ] Activation event logged
- [ ] Status dashboard displayed