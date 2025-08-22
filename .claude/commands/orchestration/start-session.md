---
name: orchestration-start-session
description: Initialize a new orchestration session with mode and tracking
config:
  model: haiku
  temperature: 0.2
---

# Initialize Orchestration Session

Start a new orchestration session to coordinate team activities with proper state tracking and mode configuration.

## Context

Session initialization request: $ARGUMENTS

## Task

Initialize a new orchestration session with the following steps:

1. **Parse Session Parameters**
   - Extract mode from arguments (development/leadership/sprint/config)
   - Identify project context if provided
   - Determine parent session if this is a sub-session

2. **Create Session**
   - Use UV to run session_manager.py create command
   - Set appropriate mode based on arguments
   - Configure session metadata

3. **Initialize State**
   - Set up initial state structure for the session
   - Configure team member availability
   - Set default configurations based on mode

4. **Return Session Details**
   - Provide session ID for tracking
   - Display session configuration
   - Show available commands for the mode

## Commands to Execute

```bash
# Create new session based on arguments
uv run /Users/dylan/Workspace/claude/agent-workflows/cc-dev-team/.claude/scripts/session_manager.py create \
  --mode <extracted-mode> \
  --project <project-name-if-provided> \
  --json
```

## Expected Output

```
Session Created Successfully
==========================
Session ID: <generated-id>
Mode: <mode>
Status: active
Project: <project-name>

Available Commands:
- /orchestration/dashboard - View session status
- /orchestration/sprint-board - Manage sprint tasks (if sprint mode)
- /orchestration/handoff - Transfer session ownership
- /state/get - Query session state
- /state/set - Update session state

Use session ID in subsequent commands for context.
```

## Usage Examples

```
/orchestration/start-session development my-project
/orchestration/start-session sprint sprint-2024-w42
/orchestration/start-session leadership quarterly-planning
/orchestration/start-session config system-setup
```

## Error Handling

- Validate mode is one of: development, leadership, sprint, config
- Check for existing active sessions in same project
- Ensure proper UV environment is available
- Handle session creation failures gracefully

## Constraints

- Session IDs must be unique and trackable
- Mode determines available features and workflows
- Sessions expire after 24 hours of inactivity
- Parent sessions can spawn child sessions for delegation