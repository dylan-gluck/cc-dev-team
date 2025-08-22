---
name: orchestration-sprint-board
description: Display kanban task board with sprint progress and velocity metrics
config:
  model: haiku
  temperature: 0.1
---

# Sprint Board

Interactive kanban board for sprint task management with velocity tracking and blocker visibility.

## Context

Sprint board request: $ARGUMENTS

## Task

Display and manage sprint tasks in kanban format:

1. **Load Sprint Data**
   - Get session ID from arguments or find active sprint session
   - Query sprint state from state_manager.py
   - Load task assignments and status

2. **Render Kanban Board**
   - Organize tasks by status columns (TODO/IN PROGRESS/REVIEW/DONE)
   - Show task details (ID, title, assignee, points)
   - Highlight blockers with visual indicators

3. **Calculate Metrics**
   - Sprint velocity (points completed / time)
   - Burndown progress
   - Team capacity utilization
   - Blocker impact analysis

4. **Update Capabilities**
   - Parse task updates from arguments
   - Move tasks between columns
   - Update task assignments
   - Mark/unmark blockers

5. **Sprint Summary**
   - Days remaining in sprint
   - Completion percentage
   - Risk assessment
   - Suggested focus areas

## Commands to Execute

```bash
# Get sprint session state
uv run /Users/dylan/Workspace/claude/agent-workflows/cc-dev-team/.claude/scripts/state_manager.py get <session-id> "/sprint" --json

# List sprints if needed
uv run /Users/dylan/Workspace/claude/agent-workflows/cc-dev-team/.claude/scripts/shared_state.py list-sprints <project-id> --json

# Update task status if arguments provided
uv run /Users/dylan/Workspace/claude/agent-workflows/cc-dev-team/.claude/scripts/state_manager.py set <session-id> "/sprint/tasks/<task-id>/status" "<new-status>"
```

## Expected Output

```
═══════════════════════════════════════════════════════════════
                        SPRINT BOARD
                   Sprint 2024-W42 (Day 3/5)
═══════════════════════════════════════════════════════════════

┌─────────────────┬─────────────────┬─────────────────┬─────────────────┐
│      TODO       │   IN PROGRESS   │     REVIEW      │      DONE       │
├─────────────────┼─────────────────┼─────────────────┼─────────────────┤
│ [API-123] 3pts  │ [API-125] 5pts  │ [API-121] 2pts  │ [API-120] 3pts  │
│ User auth flow  │ Payment gateway │ Email service   │ Database schema │
│ @engineering    │ @api-team       │ @qa-director    │ ✓ Complete      │
│                 │ ⚠️ Blocked       │                 │                 │
│─────────────────│─────────────────│─────────────────│─────────────────│
│ [API-124] 2pts  │ [API-126] 3pts  │                 │ [API-119] 5pts  │
│ Rate limiting   │ Webhook handler │                 │ API scaffolding │
│ Unassigned      │ @engineering    │                 │ ✓ Complete      │
│                 │                 │                 │                 │
│─────────────────│                 │                 │─────────────────│
│ [API-127] 5pts  │                 │                 │ [API-118] 2pts  │
│ Documentation   │                 │                 │ Project setup   │
│ @tech-writer    │                 │                 │ ✓ Complete      │
└─────────────────┴─────────────────┴─────────────────┴─────────────────┘

VELOCITY METRICS                    SPRINT PROGRESS
────────────────                    ────────────────
Current Velocity: 2.3 pts/day       ████████░░░░░░░░ 50% (10/20 pts)
Projected:       11.5 pts           Days Remaining: 2
Team Capacity:   85%                At Risk: 2 tasks

BLOCKERS                            TEAM LOAD
────────────                       ────────────
⚠️ Payment gateway - Waiting for    engineering: ████████░░ 80%
   3rd party API credentials        api-team:    ██████████ 100%
                                   qa:          ████░░░░░░ 40%
                                   devops:      ██████░░░░ 60%

ACTIONS
────────
• Move task: /orchestration/sprint-board move API-123 in-progress
• Assign task: /orchestration/sprint-board assign API-124 @engineering
• Mark blocker: /orchestration/sprint-board block API-125 "reason"
• Update points: /orchestration/sprint-board points API-126 5
```

## Usage Examples

```
/orchestration/sprint-board
/orchestration/sprint-board session-sprint-123
/orchestration/sprint-board move API-123 review
/orchestration/sprint-board assign API-124 engineering-api
/orchestration/sprint-board block API-125 "Waiting for external API"
/orchestration/sprint-board unblock API-125
```

## Task Update Syntax

- `move <task-id> <column>` - Move task to new status
- `assign <task-id> <agent>` - Assign task to team member
- `block <task-id> <reason>` - Mark task as blocked
- `unblock <task-id>` - Remove blocker
- `points <task-id> <number>` - Update story points

## Error Handling

- Validate task IDs exist before updates
- Check valid status transitions
- Ensure assignees are valid team members
- Handle sprint not found scenarios
- Prevent moving completed tasks backward

## Constraints

- Only active sprints can be modified
- Task status must follow workflow rules
- Blocked tasks show in current column with indicator
- Velocity calculated from current sprint only
- Maximum 100 tasks displayed per board