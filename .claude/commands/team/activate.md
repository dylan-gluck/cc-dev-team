---
allowed-tools: Read, Write, Task, Bash(jq:*)
description: Activate a team for coordinated task execution
argument-hint: <team-name> [--mode parallel|sequential] [--agents specific,agents]
model: opus
---

# Team Activation

Activate a team for coordinated task execution with orchestration setup.

## Context
- Team configuration: @.claude/orchestration/teams.json
- Current state: @.claude/orchestration/team-state.json
- Activation request: $ARGUMENTS

## Activation Process

### 1. Parse Activation Parameters
Extract from arguments:
- Team name to activate
- Execution mode (parallel/sequential, default: parallel)
- Specific agents (optional, default: all team agents)

### 2. Team Readiness Check

Verify team status and availability:
```
🚀 TEAM ACTIVATION PREFLIGHT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Team: [team-name]
Orchestrator: [orchestrator-agent]
Model Preference: [model]

Team Composition:
Total Agents: X
Available: Y
Busy: Z

Agents Status:
✅ [agent-1]: Ready (100% capacity available)
✅ [agent-2]: Ready (100% capacity available)
⚠️ [agent-3]: Partial (50% capacity available)
❌ [agent-4]: Busy (0% capacity available)

Settings:
- Max Parallel Agents: [number]
- Code Review Required: [yes/no]
- Test Coverage Threshold: [percentage]
- Auto Documentation: [enabled/disabled]

Readiness Score: [X/100]
Status: [Ready/Partially Ready/Not Ready]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 3. Create Activation Plan

Generate execution strategy:
```
📋 ACTIVATION PLAN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Execution Mode: [Parallel/Sequential]
Orchestrator: [orchestrator-agent]

Agent Activation Sequence:
Phase 1 (Immediate):
  → [agent-1]: [Typical responsibility]
  → [agent-2]: [Typical responsibility]
  
Phase 2 (After Phase 1):
  → [agent-3]: [Typical responsibility]
  
Phase 3 (Final):
  → [agent-4]: [Typical responsibility]

Workflow Pipeline:
[specification] → [implementation] → [testing] → [review] → [documentation]

Resource Allocation:
- Tokens Reserved: [estimated]
- Execution Time: [estimated]
- Parallel Streams: [number]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 4. Initialize Team Workspace

Set up team coordination structure:
```
🏗️ Workspace Initialization:

Communication Channels:
- Message Bus: /team/[team-name]/messages
- Event Stream: /team/[team-name]/events
- Artifact Store: /team/[team-name]/artifacts

Shared Context:
- Team Goal: [To be defined]
- Success Criteria: [To be defined]
- Constraints: [From team settings]
- Timeline: [To be set]

Coordination Points:
- Sync Checkpoints: Every [X] minutes
- Review Gates: [List of review points]
- Handoff Points: [Inter-agent handoffs]
```

### 5. Update Team State

Mark team as active in team-state.json:
```json
{
  "active_teams": ["[team-name]"],
  "capacity_tracking": {
    "[team-name]": {
      "status": "active",
      "activated_at": "[timestamp]",
      "mode": "[parallel/sequential]",
      "active_agents": ["agent-1", "agent-2"],
      "orchestrator": "[orchestrator-agent]"
    }
  }
}
```

### 6. Generate Team Brief

Create team briefing document:
```
📄 TEAM BRIEFING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Team: [team-name]
Mission: [Awaiting definition]
Activated: [timestamp]

Team Members & Roles:
[agent-1] - [Role]: [Responsibilities]
[agent-2] - [Role]: [Responsibilities]
[agent-3] - [Role]: [Responsibilities]

Operating Procedures:
1. All work must meet team quality standards
2. Code review required for all changes
3. Test coverage must exceed [X]%
4. Documentation updates mandatory
5. Regular sync at coordination points

Communication Protocol:
- Use message bus for inter-agent communication
- Emit events for major milestones
- Store artifacts in team workspace
- Report blockers immediately

Success Metrics:
- Quality: [Metric]
- Speed: [Metric]
- Coverage: [Metric]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 7. Activation Commands

Provide team control commands:
```
🎮 TEAM CONTROL PANEL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Team: [team-name] [ACTIVE]

Available Commands:
/team assign [team-name].[agent] [task]  - Assign task to team agent
/team status [team-name]                 - Check team status
/team pause [team-name]                  - Pause team execution
/team resume [team-name]                 - Resume team execution
/team deactivate [team-name]            - Deactivate team

Quick Actions:
📝 Define goal: /team goal [team-name] "goal description"
⏰ Set deadline: /team deadline [team-name] [time]
🎯 Set criteria: /team criteria [team-name] "success criteria"
📊 View metrics: /team metrics [team-name]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 8. Team Capabilities

List what the activated team can do:
```
💪 TEAM CAPABILITIES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[team-name] Specializations:

Core Competencies:
• [Competency 1]: [Description]
• [Competency 2]: [Description]
• [Competency 3]: [Description]

Typical Workflows:
1. [Workflow 1]: [Description]
2. [Workflow 2]: [Description]
3. [Workflow 3]: [Description]

Best Suited For:
- [Task type 1]
- [Task type 2]
- [Task type 3]

Not Recommended For:
- [Task type that doesn't fit team]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 9. Integration Hooks

Set up team integration points:
```
🔌 Integration Active:

Event Subscriptions:
- Task assignments → Team message bus
- Status updates → Team dashboard
- Completion events → Performance metrics
- Error events → Alert system

Automation Triggers:
- On task complete → Next phase activation
- On review pass → Documentation generation
- On test pass → Deployment preparation
- On error → Rollback procedures
```

### 10. Activation Confirmation

Final activation summary:
```
✅ TEAM ACTIVATED SUCCESSFULLY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Team: [team-name]
Status: ACTIVE ⚡
Mode: [Parallel/Sequential]
Agents: [X] ready
Orchestrator: [orchestrator-agent] online

Ready for tasking!

Next Steps:
1. Define team goal: /team goal [team-name] "..."
2. Assign first task: /team assign [team-name].[agent] "..."
3. Monitor progress: /team status [team-name]

The team is now ready to receive coordinated tasks.
Use team-prefixed commands for team-specific operations.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Error Handling

Handle activation issues:
- Team not found: List available teams
- Insufficient capacity: Show capacity report
- Orchestrator unavailable: Suggest alternative
- Conflicting activation: Warn about active teams

## Performance Optimization

For parallel mode:
- Set up work queues for each agent
- Enable concurrent task execution
- Configure result aggregation
- Monitor resource consumption

For sequential mode:
- Define clear handoff points
- Set up pipeline stages
- Configure stage gates
- Monitor bottlenecks