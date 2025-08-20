---
allowed-tools: Task, Read, Bash(.claude/scripts/state_manager.py:*), Bash(.claude/scripts/message_bus.py:*), Bash(.claude/scripts/event_stream.py:*), Bash(echo:*), Write
description: Delegate task to appropriate team with preview and confirmation
argument-hint: <task-description> [--team team-name] [--priority high|medium|low]
model: sonnet
---

# Task Delegation Orchestration

Analyze task requirements and delegate to the appropriate team with confirmation.

## Arguments
- Task description: $ARGUMENTS (required)
- Team override: --team [team-name]
- Priority: --priority [high|medium|low]

## Task Analysis

### 1. Parse Task Description
Extract task details from arguments:
- Task description
- Optional team specification
- Priority level
- Any technical keywords

### 2. Load Team Capabilities
Review team configurations: @.claude/orchestration/teams.json
- Available teams and their skills
- Current capacity
- Agent specializations

### 3. Intelligent Team Assignment

Analyze task to determine best team:

```python
# Task analysis logic
def analyze_task(description):
    keywords = extract_keywords(description)
    
    team_scores = {}
    for team in teams:
        score = calculate_match_score(keywords, team.skills)
        team_scores[team] = score
    
    return sorted(team_scores, key=lambda x: x[1], reverse=True)
```

**Keyword Mapping:**
- UI, frontend, component, design → Engineering (UX specialty)
- API, backend, database, server → Engineering (Backend specialty)
- Test, QA, validation, coverage → QA Team
- Deploy, CI/CD, infrastructure → DevOps Team
- Requirements, user story, criteria → Product Team
- Full feature, end-to-end → Engineering (Fullstack)

## Resource Estimation

### Calculate Requirements

```
Task: [task-description]
Complexity: [simple|medium|complex]
Estimated Points: [1-8]
Estimated Duration: [hours]
Required Agents: [count]
Suggested Team: [team-name]
```

### Check Team Availability

```
Team         | Available Agents | Current Load | Capacity
-------------|------------------|--------------|----------
Engineering  | 3/5             | 60%          | Can accept
QA           | 2/3             | 33%          | Can accept
DevOps       | 1/2             | 50%          | Can accept
Product      | 1/1             | 100%         | At capacity
```

## Delegation Preview

### Display Task Assignment Plan

```
┌─────────────────────────────────────────────────┐
│           TASK DELEGATION PREVIEW               │
├─────────────────────────────────────────────────┤
│ Task: [task-description]                        │
│                                                  │
│ Analysis Results:                               │
│ • Type: [feature|bug|test|infrastructure]       │
│ • Complexity: [simple|medium|complex]           │
│ • Priority: [high|medium|low]                   │
│ • Estimated effort: [X] points                  │
│                                                  │
│ Team Assignment:                                │
│ • Primary: [team-name] (95% match)             │
│ • Alternative: [team-name] (70% match)          │
│                                                  │
│ Execution Plan:                                 │
│ • Agent to spawn: [agent-type]                  │
│ • Estimated tokens: [amount]                    │
│ • Estimated time: [duration]                    │
│                                                  │
│ Dependencies:                                   │
│ • Required before: [task-list]                  │
│ • Blocks: [task-list]                          │
└─────────────────────────────────────────────────┤
```

### Confirmation Prompt

```
Proceed with this task delegation?

✓ Create task: [task-id]
✓ Assign to: [team-name]
✓ Spawn agent: [agent-type]
✓ Priority: [priority]

Confirm? (yes/no/modify):
```

If "modify" selected, allow adjustment of:
- Team assignment
- Priority level
- Task description
- Estimated effort

## Task Creation

### 1. Generate Task ID
Create unique task identifier:
- Format: task-[timestamp]-[hash]
- Example: task-20250120-a3f2

### 2. Create Task Record

```python
task_data = {
    "id": task_id,
    "description": task_description,
    "type": task_type,
    "priority": priority,
    "status": "pending",
    "assigned_team": selected_team,
    "assigned_agent": None,
    "created_at": timestamp,
    "estimated_points": points,
    "dependencies": [],
    "artifacts": [],
    "context": {
        "requirements": extracted_requirements,
        "acceptance_criteria": criteria,
        "technical_notes": notes
    }
}
```

Save task: !`.claude/scripts/state_manager.py set "tasks.[task-id]" '[task-data]'`

### 3. Update Sprint Tasks
If sprint is active, add to sprint:
- !`.claude/scripts/state_manager.py set "sprints.[sprint-id].tasks.queued" '[...existing, task-id]' --merge`

## Agent Spawning

### 1. Select Appropriate Agent

Based on task type and team, choose agent:
```python
agent_selection = {
    "engineering": {
        "ui_task": "engineering-ux",
        "api_task": "engineering-api",
        "feature": "engineering-fullstack",
        "architecture": "engineering-lead"
    },
    "qa": {
        "e2e_test": "qa-e2e",
        "unit_test": "qa-scripts",
        "test_plan": "qa-analyst"
    },
    "devops": {
        "deployment": "devops-release",
        "pipeline": "devops-cicd",
        "infrastructure": "devops-infrastructure"
    }
}
```

### 2. Prepare Agent Context

Create comprehensive context for agent:

```markdown
# Task Assignment

You have been assigned task: [task-id]

## Task Details
Description: [task-description]
Priority: [priority]
Estimated Effort: [points] points
Type: [task-type]

## Requirements
[detailed requirements]

## Acceptance Criteria
[acceptance criteria list]

## Context
- Current sprint: [sprint-id]
- Related tasks: [related-task-ids]
- Dependencies: [dependency-list]

## Your Responsibilities
1. Analyze requirements thoroughly
2. Implement solution following team standards
3. Write/update tests as needed
4. Document your work
5. Update task status when complete

## Available Resources
- Team lead: [lead-agent] (for questions)
- Related code: [file-paths]
- Documentation: [doc-links]

Begin by:
1. Reading any related code/documentation
2. Planning your approach
3. Implementing the solution
4. Testing thoroughly
5. Updating task status
```

### 3. Spawn Agent with Task

Use Task tool to spawn agent:
```
Task: [agent-type]
Context: [prepared-context]
```

### 4. Update Task Assignment

After spawning:
- !`.claude/scripts/state_manager.py update-task [task-id] assigned`
- !`.claude/scripts/state_manager.py set "tasks.[task-id].assigned_agent" '"[agent-id]"'`

## Communication Setup

### 1. Notify Team Orchestrator

Send message to team orchestrator:
- !`.claude/scripts/message_bus.py send delegator [team]-orchestrator TASK_ASSIGNED '{"task_id": "[id]", "agent": "[agent-id]"}' --priority high`

### 2. Set Up Monitoring

Create monitoring entry:
```python
monitoring_data = {
    "task_id": task_id,
    "agent_id": agent_id,
    "start_time": timestamp,
    "expected_duration": estimated_time,
    "check_interval": 300  # 5 minutes
}
```

### 3. Emit Delegation Event

Log event:
- !`.claude/scripts/event_stream.py emit task_delegated '{"task_id": "[id]", "team": "[team]", "agent": "[agent]"}' --source orchestrator`

## Post-Delegation Status

### Display Confirmation

```
✅ Task Successfully Delegated

📋 Task Details:
• ID: [task-id]
• Description: [description]
• Team: [team-name]
• Agent: [agent-id]
• Priority: [priority]
• Status: Assigned

⏱️ Execution:
• Started: [timestamp]
• Expected duration: [duration]
• Token budget: [tokens]

📊 Monitoring:
• Track progress: /orchestrate task status [task-id]
• View agent: /orchestrate agents status [agent-id]
• Check messages: /orchestrate communication status

💡 Tips:
• Agent will update status as work progresses
• You'll be notified when task completes
• Use /orchestrate task status for real-time updates
```

## Smart Suggestions

Based on task type, suggest related actions:

```
🎯 Related Actions:

Since you delegated a [task-type] task, you might want to:

1. Create test task: /orchestrate task delegate "Write tests for [feature]"
2. Add documentation: /orchestrate task delegate "Document [feature]"
3. Schedule review: /orchestrate task delegate "Review [feature] implementation"
4. Check dependencies: /orchestrate dependencies check [task-id]
```

## Error Handling

### Team at Capacity
```
⚠️ Warning: [team-name] is at capacity

Current load: 100%
Active agents: 5/5

Options:
1. Wait for capacity (queue task)
2. Select alternative team: [alt-team]
3. Override and spawn anyway (not recommended)
4. Cancel delegation

Choice (1-4):
```

### No Suitable Team
```
❌ Error: No team matches task requirements

Task: [description]
Analyzed keywords: [keywords]

Please specify team manually:
1. Engineering
2. QA
3. DevOps
4. Product

Select team (1-4):
```

### Agent Spawn Failure
```
❌ Error: Failed to spawn agent

Reason: [error-message]

Troubleshooting:
1. Check resource limits: /orchestrate status
2. Verify team configuration: /orchestrate config show
3. Try alternative agent: [suggestion]
4. Contact support

Retry? (yes/no):
```

## Delegation Patterns

### Batch Delegation
If multiple tasks provided:
```
🔄 Batch Delegation Mode

Found 3 tasks to delegate:
1. [task-1] → Engineering
2. [task-2] → QA
3. [task-3] → DevOps

Proceed with batch delegation? (yes/no/review):
```

### Sequential Dependencies
Handle dependent tasks:
```
📦 Dependency Chain Detected

Task order:
1. [task-1] - Backend API (must complete first)
2. [task-2] - Frontend integration (depends on task-1)
3. [task-3] - E2E tests (depends on task-2)

Delegate entire chain? (yes/no):
```

## Success Criteria

Task delegation successful when:
- [ ] Task created with unique ID
- [ ] Team correctly identified
- [ ] Agent successfully spawned
- [ ] Task status updated
- [ ] Orchestrator notified
- [ ] Monitoring established
- [ ] Event logged