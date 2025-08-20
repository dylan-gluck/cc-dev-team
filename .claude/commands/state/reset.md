---
allowed-tools: Bash(.claude/scripts/state_manager.py:*), Bash(cp:*), Bash(mv:*), Write, Read
description: Reset orchestration state with backup and confirmation
argument-hint: [--force] [--backup] [--partial <section>]
model: sonnet
---

# Reset Orchestration State

Safely reset the orchestration state with backup creation and selective reset options.

## Context

Current state overview: !`.claude/scripts/state_manager.py summary`
Reset arguments: $ARGUMENTS

## Reset Process

### 1. Parse Reset Options

Extract reset parameters from arguments:
- `--force`: Skip confirmation prompt (dangerous!)
- `--backup`: Create backup before reset (default: true)
- `--partial <section>`: Reset only specific section (tasks, agents, sprints, etc.)
- `--preserve <section>`: Keep specific sections during full reset
- `--dry-run`: Show what would be reset without making changes

### 2. Pre-Reset Validation

Before any reset operation:

**State Assessment**:
```
Current State Summary:
├─ Active Tasks: X (Y in progress)
├─ Active Agents: X (Y busy)
├─ Active Sprints: X
├─ Pending Communications: X
└─ Recent Events: X

⚠️ WARNING: This will affect:
• X active task assignments
• Y agent workloads
• Z sprint progress tracking
```

**Confirmation Required** (unless --force):
```
This action will reset orchestration state.
Active work will be lost if not backed up.

Type 'RESET' to confirm: _
```

### 3. Backup Creation

Create timestamped backup:

```bash
# Backup location
.claude/state/backups/orchestration_YYYYMMDD_HHMMSS.json

# Backup contents
- Full state snapshot
- Reset metadata (who, when, why)
- Active task list for recovery
```

### 4. Reset Strategies

#### Full Reset (Default)
Reset to clean initial state:
```json
{
  "organization": {},
  "projects": {},
  "epics": {},
  "sprints": {},
  "tasks": {},
  "agents": {"active": {}},
  "communication": {"questions": [], "handoffs": []},
  "observability": {"metrics": {}, "events": []}
}
```

#### Partial Reset
Reset only specified sections:
```bash
# Reset only tasks
/state reset --partial tasks

# Reset tasks and agents
/state reset --partial tasks,agents

# Reset all except projects
/state reset --preserve projects
```

#### Smart Reset
Preserve structure, clear data:
```bash
# Keep project/sprint structure, clear tasks
/state reset --smart

# Maintains:
- Project definitions
- Sprint timelines
- Agent definitions

# Clears:
- Task assignments
- Agent status
- Communication queue
- Events/metrics
```

### 5. Reset Execution

Perform the reset operation:

1. **Create Backup**:
   ```bash
   cp .claude/state/orchestration.json \
      .claude/state/backups/orchestration_$(date +%Y%m%d_%H%M%S).json
   ```

2. **Generate Reset State**:
   - Build new state structure
   - Preserve sections if specified
   - Validate structure integrity

3. **Apply Reset**:
   - Write new state to file
   - Emit reset event
   - Log reset operation

4. **Verify Reset**:
   - Read back new state
   - Confirm expected structure
   - Report success/failure

### 6. Post-Reset Actions

After successful reset:

**Recovery Information**:
```
✅ State Reset Complete

Backup created: .claude/state/backups/orchestration_20240820_143022.json

To restore from backup:
cp .claude/state/backups/orchestration_20240820_143022.json \
   .claude/state/orchestration.json

Quick recovery commands:
• View backup: /state get --file backups/orchestration_20240820_143022.json
• Restore tasks: /state restore tasks --from-backup 20240820_143022
• Restore all: /state restore --from-backup 20240820_143022
```

### 7. Reset History

Maintain reset audit log:

```
Reset History (.claude/state/reset.log):
├─ 2024-08-20 14:30:22 - Full reset by user
├─ 2024-08-19 09:15:10 - Partial reset (tasks)
└─ 2024-08-18 16:45:33 - Smart reset
```

## Safety Features

### Validation Checks

1. **Active Work Detection**:
   - Warn if tasks in progress
   - Alert on busy agents
   - Flag active sprints

2. **Backup Verification**:
   - Ensure backup completes successfully
   - Verify backup file is valid JSON
   - Check backup file size is reasonable

3. **Rollback Capability**:
   - Keep last 3 backups minimum
   - Provide immediate rollback command
   - Test restore process

### Recovery Options

If reset causes issues:

```bash
# Immediate rollback
mv .claude/state/backups/orchestration_LATEST.json \
   .claude/state/orchestration.json

# Selective restore
/state restore tasks --from-backup TIMESTAMP
/state restore agents --from-backup TIMESTAMP

# Manual recovery
/state set tasks "$(cat backup.json | jq .tasks)"
```

## Output Format

```
═══════════════════════════════════════════
         STATE RESET OPERATION
═══════════════════════════════════════════

⚠️  RESET CONFIRMATION REQUIRED

Current State:
├─ 15 active tasks (5 in progress)
├─ 8 active agents (3 busy)
├─ 1 active sprint (45% complete)
└─ 3 pending communications

Reset Type: [Full/Partial/Smart]
Sections: [All/Specified]
Backup: [Created/Skipped]

This operation will:
✓ Create backup at backups/orchestration_20240820_143022.json
✓ Reset specified sections to initial state
✓ Preserve: [none/sections]
✗ Clear all active assignments
✗ Remove task history
✗ Reset agent status

[Type 'RESET' to confirm or Ctrl+C to cancel]

... (after confirmation) ...

📦 Creating backup... Done
🔄 Resetting state... Done
✅ Verification... Passed

RESET COMPLETE

Backup: backups/orchestration_20240820_143022.json
Affected: 15 tasks, 8 agents, 1 sprint

Recovery: /state restore --from-backup 20240820_143022
```

## Error Handling

Handle reset failures gracefully:

1. **Backup Failure**: Abort reset, provide manual backup command
2. **Write Failure**: Restore from backup automatically
3. **Validation Failure**: Show specific errors, suggest fixes
4. **Partial Failure**: Rollback entire operation

## Interactive Follow-ups

Post-reset commands:
- "View new state: `/state summary`"
- "Restore from backup: `/state restore --from-backup TIMESTAMP`"
- "Re-initialize project: `/state set projects.project-1 '{...}'`"
- "Import tasks: `/state import tasks.json`"