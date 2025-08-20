---
allowed-tools: Read, Write, Task, Bash(jq:*), Bash(date:*)
description: Manage cross-team handoffs with context preservation
argument-hint: <from-team> <to-team> <context/task-description> [--artifacts path]
model: sonnet
---

# Cross-Team Handoff Management

Facilitate smooth handoffs between teams with full context preservation and tracking.

## Context
- Team configuration: @.claude/orchestration/teams.json
- Current state: @.claude/orchestration/team-state.json
- Handoff request: $ARGUMENTS

## Handoff Process

### 1. Parse Handoff Request
Extract parameters:
- Source team (from-team)
- Destination team (to-team)
- Context/task description
- Artifacts path (optional)

### 2. Validate Teams

Verify both teams exist and are available:
```
🔍 Team Validation:
━━━━━━━━━━━━━━━━━━━━━━━━━━━
From Team: [from-team]
  Status: [Active/Idle]
  Current Capacity: X/Y
  Active Tasks: Z

To Team: [to-team]
  Status: [Active/Idle]
  Current Capacity: X/Y
  Available Capacity: W
━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 3. Create Handoff Package

Generate comprehensive handoff documentation:
```
📦 HANDOFF PACKAGE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Handoff ID: HANDOFF-[timestamp]-[random]
From: [from-team]
To: [to-team]
Created: [timestamp]
Priority: [inferred priority]

Context Summary:
[Detailed context description]

Deliverables:
✅ Completed by [from-team]:
- [Item 1]
- [Item 2]
- [Item 3]

📋 Required from [to-team]:
- [Action 1]
- [Action 2]
- [Action 3]

Artifacts:
- Location: [artifacts path]
- Files: [list of relevant files]
- Documentation: [relevant docs]

Dependencies:
- External: [any external dependencies]
- Internal: [internal dependencies]

Success Criteria:
1. [Criterion 1]
2. [Criterion 2]
3. [Criterion 3]

Timeline:
- Handoff Created: [timestamp]
- Expected Start: [timestamp]
- Target Completion: [timestamp]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 4. Workflow Analysis

Determine appropriate workflow for destination team:
```
🔄 Recommended Workflow for [to-team]:
Based on handoff context, suggested approach:

Phase 1: Review & Planning
  → [Specific agent]: Review artifacts
  → [Specific agent]: Create implementation plan

Phase 2: Execution
  → [Specific agent]: [Primary task]
  → [Specific agent]: [Secondary task]

Phase 3: Validation
  → [Specific agent]: Verify completion
  → [Specific agent]: Update documentation
```

### 5. Capacity Impact Assessment

Calculate impact on destination team:
```
📊 Capacity Impact Analysis:
[to-team] Current State:
  Before: X/Y capacity (Z% utilized)
  After:  (X+estimated)/Y capacity (W% utilized)
  
Estimated Resource Needs:
  - [Agent type 1]: N hours
  - [Agent type 2]: M hours
  Total: P hours

Risk Assessment:
  [Green/Yellow/Red] - [Risk description]
```

### 6. Update Team State

Record handoff in team-state.json:
```json
{
  "handoffs": {
    "pending": [
      {
        "id": "[handoff-id]",
        "from_team": "[from-team]",
        "to_team": "[to-team]",
        "context": "[context]",
        "artifacts": "[path]",
        "created_at": "[timestamp]",
        "status": "pending_acceptance"
      }
    ]
  }
}
```

### 7. Generate Acceptance Checklist

Create checklist for receiving team:
```
✅ Handoff Acceptance Checklist:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
For [to-team] to review:

Prerequisites:
□ Review handoff context
□ Verify artifact access
□ Check team capacity
□ Validate dependencies

Deliverables Review:
□ Understand completed work
□ Identify remaining tasks
□ Assess complexity
□ Estimate effort

Team Readiness:
□ Required skills available
□ Capacity confirmed
□ Timeline acceptable
□ Success criteria clear

Accept handoff: /team accept-handoff [handoff-id]
Reject/defer: /team defer-handoff [handoff-id] [reason]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 8. Communication Templates

Generate communication for teams:
```
📨 Team Notifications:

To [from-team]:
"Handoff HANDOFF-XXX initiated to [to-team].
 Status: Pending acceptance
 Context preserved at: [location]"

To [to-team]:
"Incoming handoff from [from-team].
 Review required: [handoff-id]
 Estimated effort: X hours
 Action needed: Review and accept/defer"

To Orchestrators:
"Cross-team handoff initiated.
 From: [from-team]
 To: [to-team]
 Impact: [capacity impact]"
```

### 9. Handoff Tracking

Provide tracking information:
```
📍 Handoff Tracking:
━━━━━━━━━━━━━━━━━━━━━━━━━━━
Handoff ID: [handoff-id]
Status: Pending Acceptance
Track: /team track-handoff [handoff-id]

Status Flow:
pending_acceptance → accepted → in_progress → completed

Estimated Timeline:
- Acceptance: Within 1 hour
- Start: Within 2 hours
- Completion: Within [estimated] hours

Auto-escalation:
If not accepted within 2 hours, escalate to team orchestrators
━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 10. Best Practices Reminder

Include handoff best practices:
```
💡 Handoff Best Practices:
1. Always include context and success criteria
2. Verify artifact accessibility before handoff
3. Check destination team capacity first
4. Use structured templates for consistency
5. Document assumptions and constraints
6. Include rollback plan if applicable
7. Set clear timeline expectations
8. Provide contact for clarifications
```

## Error Handling

Handle edge cases:
- Team not found: List available teams
- Insufficient capacity: Suggest alternatives
- Missing artifacts: Request artifact location
- Circular handoff: Warn about loop
- Stale handoff: Clean up old pending handoffs

## Integration Features

- Atomic state updates
- Event emission for handoff lifecycle
- Audit trail logging
- Performance metric updates
- Notification system integration

## Success Confirmation

Final output:
```
✅ HANDOFF INITIATED SUCCESSFULLY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Handoff ID: [handoff-id]
From: [from-team] → To: [to-team]
Status: Pending Acceptance

Next Steps:
1. [to-team] reviews handoff package
2. Accept/defer decision within 2 hours
3. Work begins upon acceptance
4. Track progress: /team track-handoff [handoff-id]

View all handoffs: /team handoffs
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```