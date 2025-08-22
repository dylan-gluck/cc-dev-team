---
name: orchestration-handoff
description: Transfer orchestration session between users with state continuity
config:
  model: sonnet
  temperature: 0.3
---

# Session Handoff

Transfer active orchestration session to another user while preserving state, context, and continuity.

## Context

Handoff request: $ARGUMENTS

## Task

Execute session handoff with comprehensive state transfer:

1. **Validate Handoff Request**
   - Parse source and target session/user from arguments
   - Verify source session exists and is active
   - Check permissions for handoff operation

2. **Prepare Handoff Package**
   - Capture current session state snapshot
   - Document in-progress tasks and blockers
   - Generate handoff summary with context
   - Include recovery procedures if needed

3. **Execute Transfer**
   - Create new session for target if needed
   - Transfer state using session_manager.py handoff
   - Preserve task assignments and progress
   - Maintain audit trail of handoff

4. **Generate Handoff Report**
   - Summary of transferred context
   - Active tasks and their status
   - Critical decisions pending
   - Recommended next actions
   - Recovery procedures if issues arise

5. **Verify Continuity**
   - Confirm state transfer completed
   - Validate target session is operational
   - Provide rollback instructions if needed

## Commands to Execute

```bash
# Get current session state for handoff
uv run /Users/dylan/Workspace/claude/agent-workflows/cc-dev-team/.claude/scripts/session_manager.py info <from-session> --json
uv run /Users/dylan/Workspace/claude/agent-workflows/cc-dev-team/.claude/scripts/state_manager.py get <from-session> "/" --json

# Create target session if needed
uv run /Users/dylan/Workspace/claude/agent-workflows/cc-dev-team/.claude/scripts/session_manager.py create --mode <mode> --parent <from-session> --json

# Execute handoff
uv run /Users/dylan/Workspace/claude/agent-workflows/cc-dev-team/.claude/scripts/session_manager.py handoff <from-session> <to-session> --data '<handoff-context>' --json

# Verify handoff success
uv run /Users/dylan/Workspace/claude/agent-workflows/cc-dev-team/.claude/scripts/session_manager.py info <to-session> --json
```

## Expected Output

```
═══════════════════════════════════════════════════════════════
                    SESSION HANDOFF REPORT
═══════════════════════════════════════════════════════════════

HANDOFF SUMMARY
────────────────
From Session:    dev-session-abc123
To Session:      dev-session-xyz789
Timestamp:       2024-08-21 14:30:00
Status:          ✓ Successfully Transferred

CONTEXT TRANSFER
────────────────
Mode:           development
Project:        my-application
Duration:       3h 45m
State Size:     2.3 MB
Tasks:          15 active, 23 completed

ACTIVE WORK
────────────────
In Progress:
• API endpoint implementation (75% complete)
  - Assignee: engineering-api
  - Next: Complete error handling

• Test suite development (40% complete)
  - Assignee: qa-director
  - Next: Add integration tests

Blocked Tasks:
• Database migration - Waiting for schema approval
  - Action needed: Review with database team

CRITICAL DECISIONS PENDING
────────────────
1. Authentication strategy (OAuth vs JWT)
   - Context: Security review scheduled tomorrow
   - Recommendation: Prepare comparison matrix

2. API versioning approach
   - Context: Breaking changes needed for v2
   - Recommendation: Implement versioning headers

HANDOFF NOTES
────────────────
Current Focus: Completing API implementation for sprint deadline
Key Context: Customer demo scheduled for Friday
Dependencies: Payment gateway integration blocked on credentials
Team Status: Full capacity, no absences planned

RECOMMENDED NEXT ACTIONS
────────────────
1. Review blocked database migration task
2. Continue API endpoint implementation
3. Schedule security review for auth strategy
4. Update sprint board with progress

RECOVERY PROCEDURES
────────────────
If issues arise with new session:
1. Original session backed up at: /tmp/session-backup-abc123.json
2. Restore command: /orchestration/recover abc123
3. Rollback window: 24 hours
4. Contact: Previous owner notified via event stream

NEW SESSION ACCESS
────────────────
Session ID: dev-session-xyz789
Commands:
• /orchestration/dashboard dev-session-xyz789
• /state/get dev-session-xyz789 /
• /orchestration/sprint-board dev-session-xyz789

Handoff completed successfully. New session is active and ready.
```

## Usage Examples

```
/orchestration/handoff from-session to-session
/orchestration/handoff abc123 xyz789 "Shifting to next timezone"
/orchestration/handoff current new-user "End of shift handoff"
/orchestration/handoff --recover abc123
```

## Handoff Data Package

The handoff includes:
- Complete state tree snapshot
- Task assignments and progress
- Configuration and settings
- Team member status
- Active blockers and dependencies
- Session metadata and history
- Audit trail of changes

## Error Handling

- Validate both sessions before transfer
- Create automatic backup before handoff
- Provide rollback mechanism
- Handle partial transfer failures
- Maintain audit log of all handoffs
- Send notifications on handoff events

## Constraints

- Handoffs are atomic operations
- State consistency must be maintained
- Maximum handoff data size: 10MB
- Recovery window: 24 hours
- Audit trail retained for 30 days
- Permissions required for cross-user handoffs