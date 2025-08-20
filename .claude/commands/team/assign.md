---
allowed-tools: Read, Write, Task, Bash(jq:*), Bash(date:*)
description: Assign specific agent to a task with capacity tracking
argument-hint: <agent-name> <task-description> [--priority high|medium|low] [--duration hours]
model: sonnet
---

# Team Task Assignment

Assign specific agent to a task with automatic capacity tracking and validation.

## Context
- Team configuration: @.claude/orchestration/teams.json
- Current state: @.claude/orchestration/team-state.json
- Assignment request: $ARGUMENTS

## Assignment Process

### 1. Parse Assignment Request
Extract from arguments:
- Agent name (e.g., engineering-fullstack)
- Task description
- Priority level (default: medium)
- Estimated duration (default: 2 hours)

### 2. Validate Agent Availability

Check agent existence and capacity:
```
🔍 Agent Validation:
Agent: [agent-name]
Team: [team-name]
Current Capacity: X/Y
Available: [Yes/No]
Current Tasks: [list of active tasks]
```

If agent not available:
```
⚠️ Agent Unavailable
[agent-name] is currently at full capacity.

Alternative Options:
1. [Similar agent 1] - Available capacity: X
2. [Similar agent 2] - Available capacity: Y
3. Add to queue for [agent-name]

Recommendation: [Suggested action]
```

### 3. Create Task Assignment

Generate task details:
```
📋 Task Assignment Details:
━━━━━━━━━━━━━━━━━━━━━━━━━━━
Task ID: TASK-[timestamp]-[random]
Agent: [agent-name]
Team: [team-name]
Description: [task-description]
Priority: [priority]
Estimated Duration: [duration] hours
Assigned At: [timestamp]
Expected Completion: [calculated time]
Status: Assigned
━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 4. Update Team State

Update the team-state.json file with:
- New assignment in assignments object
- Updated capacity tracking
- Add to active_tasks for the team
- Record event in events array

Example update structure:
```json
{
  "assignments": {
    "[task-id]": {
      "agent": "[agent-name]",
      "team": "[team-name]",
      "description": "[task-description]",
      "priority": "[priority]",
      "duration_hours": [duration],
      "assigned_at": "[timestamp]",
      "expected_completion": "[timestamp]",
      "status": "assigned"
    }
  }
}
```

### 5. Check Dependencies

Identify any dependencies or related tasks:
```
🔗 Dependency Check:
- Related Tasks: [List any related active tasks]
- Prerequisites: [Any tasks that must complete first]
- Downstream Impact: [Teams/agents affected]
```

### 6. Send Notifications

Generate notification messages:
```
📢 Notifications:
→ Agent [agent-name]: New task assigned - [task-description]
→ Team [team-name]: Capacity updated - X/Y utilized
→ Orchestrator: Assignment recorded - Task [task-id]
```

### 7. Skill Matching Analysis

Verify agent skills match task requirements:
```
✅ Skill Match Analysis:
Required Skills: [inferred from task]
Agent Skills: [list from config]
Match Score: X%
Confidence: [High/Medium/Low]
```

### 8. Assignment Confirmation

Display final confirmation:
```
✅ ASSIGNMENT SUCCESSFUL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Agent: [agent-name]
Task: [task-description]
Duration: [duration] hours
Start Time: [timestamp]
Expected End: [timestamp]

Team Impact:
- [team-name] capacity: X/Y → (X+1)/Y
- Available agents in team: Z

Next Steps:
1. Agent will begin task execution
2. Monitor progress via /team status
3. Check completion via /team performance

Track this task: /team track [task-id]
```

### 9. Queue Management

If agent at capacity, offer queuing:
```
📬 Task Queue Options:
1. Add to [agent-name] queue (position #X)
   Estimated start: [time based on current tasks]
   
2. Assign to alternative agent:
   - [agent-1]: Available now
   - [agent-2]: Available in 1 hour
   
3. Split task across multiple agents:
   - Part A → [agent-1]
   - Part B → [agent-2]
   
Select option or modify assignment.
```

### 10. Workload Balancing

Suggest workload optimizations:
```
💡 Workload Optimization:
Current distribution:
- [agent-1]: 80% utilized ⚠️
- [agent-2]: 40% utilized ✅
- [agent-3]: 20% utilized ✅

Recommendation:
Consider assigning to [agent-3] for better balance.
```

## Error Handling

Handle common errors:
- Agent not found: List available agents
- Invalid task format: Show correct format
- Capacity exceeded: Suggest alternatives
- Team offline: Show team activation command

## Integration Points

- Update team-state.json atomically
- Emit assignment event to message bus
- Trigger capacity recalculation
- Update performance metrics
- Log to audit trail

## Output Format

Provide clear, actionable output with:
- Confirmation of successful assignment
- Visual capacity indicators
- Next step recommendations
- Alternative options if needed
- Task tracking information