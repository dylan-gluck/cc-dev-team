---
name: orchestration-dashboard
description: Launch interactive dashboard to view session state and team status
config:
  model: haiku
  temperature: 0.1
---

# Orchestration Dashboard

Display real-time orchestration state with team status, active tasks, and session metrics.

## Context

Dashboard request: $ARGUMENTS

## Task

Launch and display the orchestration dashboard with these components:

1. **Session Overview**
   - Get current session ID from arguments or find active session
   - Query session info using session_manager.py
   - Display session mode, status, and metadata

2. **Team Status Panel**
   - Show active team members from state
   - Display agent availability and current assignments
   - List recent agent interactions

3. **Task Tracking**
   - Query current tasks from state_manager.py
   - Show task status (pending/in-progress/completed/blocked)
   - Display task assignments and dependencies

4. **Metrics Dashboard**
   - Calculate completion rate
   - Show session duration and activity
   - Display resource utilization

5. **State Visualization**
   - Query full state tree
   - Format as hierarchical display
   - Highlight recent changes

## Commands to Execute

```bash
# Get session info
uv run /Users/dylan/Workspace/claude/agent-workflows/cc-dev-team/.claude/scripts/session_manager.py info <session-id> --json

# Get session state
uv run /Users/dylan/Workspace/claude/agent-workflows/cc-dev-team/.claude/scripts/state_manager.py get <session-id> "/" --json

# List active sessions if no ID provided
uv run /Users/dylan/Workspace/claude/agent-workflows/cc-dev-team/.claude/scripts/session_manager.py list --active --json
```

## Expected Output

```
═══════════════════════════════════════════════════════════════
                    ORCHESTRATION DASHBOARD
═══════════════════════════════════════════════════════════════

SESSION INFO
────────────
ID:         <session-id>
Mode:       <mode>
Status:     <status>
Started:    <timestamp>
Duration:   <time-elapsed>

TEAM STATUS                          ACTIVE TASKS
────────────                         ────────────
engineering-lead    [Active]         ✓ API design review
engineering-api     [Busy]           ⧗ Implement endpoints
qa-director        [Available]       ⧗ Test suite setup
devops-manager     [Active]          ○ CI/CD pipeline
                                    ✗ Database migration (blocked)

METRICS                              RECENT ACTIVITY
────────────                         ────────────
Tasks Complete:  12/20 (60%)         19:45 - Task assigned to api team
Velocity:        3.2 tasks/hour      19:42 - Sprint goal updated
Blockers:        2                   19:38 - Config validated
Team Utilization: 75%                19:35 - Session started

STATE TREE
────────────
/
├── config/
│   ├── mode: "development"
│   └── project: "my-app"
├── team/
│   ├── engineering/
│   │   ├── lead: {status: "active", task: "review"}
│   │   └── api: {status: "busy", task: "implement"}
│   └── qa/
│       └── director: {status: "available"}
└── tasks/
    ├── current: ["api-design", "endpoints", "tests"]
    └── completed: ["setup", "planning", ...]

Commands:
• /state/set <path> <value> - Update state
• /orchestration/handoff - Transfer session
• /orchestration/sprint-board - Sprint view
```

## Usage Examples

```
/orchestration/dashboard
/orchestration/dashboard session-abc123
/orchestration/dashboard --project my-app
```

## Error Handling

- Handle missing session ID by finding active session
- Display helpful message if no sessions exist
- Format JSON responses into readable tables
- Handle state query failures gracefully

## Constraints

- Dashboard is read-only view of state
- Refreshes on each invocation (not real-time)
- Limited to current session context
- Performance optimized for large state trees