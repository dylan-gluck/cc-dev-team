---
allowed-tools: Bash(.claude/scripts/state_manager.py set:*), Bash(.claude/scripts/state_manager.py get:*), Bash(.claude/scripts/event_stream.py emit:*)
description: Update orchestration state with validation and event emission
argument-hint: <path> <value> [--merge]
model: sonnet
---

# Update Orchestration State

Modify state values with validation, rollback capability, and automatic event emission.

## Context

Arguments to parse: $ARGUMENTS
Current state value at path: !`.claude/scripts/state_manager.py get $ARGUMENTS.path --format json`

## Task

Parse arguments to extract:
1. **Path**: jq-style path to the value to update
2. **Value**: New value (JSON or string)
3. **Options**: --merge flag for object merging vs replacement

## Validation Steps

Before applying changes:

1. **Path Validation**:
   - Verify path exists or can be created
   - Check parent path exists for new values
   - Validate path syntax for jq compatibility

2. **Value Validation**:
   - Parse JSON values for validity
   - Type-check against existing value
   - Validate against schema if applicable:
     - Task status: Must be 'pending', 'in_progress', 'completed', or 'blocked'
     - Agent status: Must be 'idle', 'busy', or 'blocked'
     - Timestamps: Must be ISO format
     - IDs: Must follow naming conventions

3. **Relationship Validation**:
   - If updating task assignment, verify agent exists
   - If updating sprint tasks, verify task exists
   - Check for circular dependencies
   - Validate parent-child relationships

## Update Process

1. **Backup Current State**:
   - Store current value for potential rollback
   - Log the change attempt

2. **Apply Update**:
   - Use --merge for partial object updates
   - Use --replace (default) for complete replacement
   - Handle array operations (append, remove, insert)

3. **Emit Events**:
   - Emit 'state_updated' event with change details
   - Include old and new values in event data
   - Add timestamp and user context

4. **Verify Update**:
   - Re-read the value to confirm change
   - Compare with expected result
   - Report any discrepancies

## Special Handlers

For common state updates, provide enhanced handling:

### Task Updates
```bash
# Update task status with automatic sprint list management
/state set tasks.task-1.status "completed"

# Assign task to agent with bidirectional update
/state set tasks.task-1.assigned_to "engineering-fullstack-1"
```

### Agent Updates
```bash
# Update agent status with task validation
/state set agents.active.agent-1.status "busy"

# Clear agent assignment
/state set agents.active.agent-1.current_task null
```

### Sprint Updates
```bash
# Update sprint metrics with merge
/state set sprints.sprint-1.metrics '{"velocity": 8, "burndown": 15}' --merge
```

## Bulk Operations

Support multiple updates in a single command:
```bash
# Update multiple task statuses
/state set "tasks | map(select(.sprint_id == \"sprint-1\")) | .status" "in_progress"
```

## Rollback Capability

If update fails or needs reversal:
1. Store previous state before modification
2. Provide rollback command in output
3. Log all changes for audit trail

## Output Format

After successful update:
1. Show before/after comparison
2. Display affected related entities
3. List emitted events
4. Provide verification command
5. Suggest next logical operations

## Error Recovery

On failure:
- Display clear error message
- Show current state of target path
- Provide corrected command syntax
- Suggest alternative approaches
- Offer rollback if partial update occurred

## Examples

```bash
# Simple value update
/state set projects.project-1.status "active"

# Object merge
/state set agents.active.agent-1 '{"status": "busy", "last_checkin": "2024-08-20T10:30:00Z"}' --merge

# Complex path update
/state set "sprints.sprint-1.tasks.completed[0]" "task-5"

# Null value (deletion)
/state set tasks.task-1.assigned_to null
```