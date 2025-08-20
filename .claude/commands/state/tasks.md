---
allowed-tools: Bash(.claude/scripts/state_manager.py:*), Bash(jq:*)
description: Show all tasks with detailed status, assignments, and dependencies
argument-hint: [--status <status>] [--assigned-to <agent>] [--sprint <sprint-id>]
model: haiku
---

# Task Management Overview

Display comprehensive task information with filtering and analysis capabilities.

## Context

Arguments for filtering: $ARGUMENTS
Current task state: !`.claude/scripts/state_manager.py get tasks --format json`

## Task Analysis

### 1. Parse Filter Arguments

Extract optional filters from arguments:
- `--status`: Filter by status (pending, in_progress, completed, blocked)
- `--assigned-to`: Filter by assigned agent
- `--sprint`: Filter by sprint assignment
- `--unassigned`: Show only unassigned tasks
- `--blocked`: Show only blocked tasks with reasons
- `--age`: Sort by age (oldest first)

### 2. Task Categorization

Group tasks by status:

**📋 Pending Tasks**
- Unassigned tasks requiring attention
- Tasks awaiting dependencies
- Prioritized task queue

**🚀 In Progress**
- Currently active tasks
- Agent assignments
- Time in progress
- Expected completion

**✅ Completed**
- Recently completed (last 24h)
- Completion velocity
- Success metrics

**🚫 Blocked**
- Blocking reasons
- Dependencies required
- Time blocked
- Resolution suggestions

### 3. Task Details Table

Display comprehensive task information:

| ID | Name | Status | Assigned To | Sprint | Created | Updated | Age | Priority |
|----|------|--------|-------------|--------|---------|---------|-----|----------|
| task-1 | Feature A | in_progress | eng-1 | sprint-1 | 2d ago | 1h ago | 2d | High |
| task-2 | Bug Fix | blocked | qa-1 | sprint-1 | 3d ago | 5h ago | 3d | Critical |

### 4. Task Dependencies

Visualize task dependencies:
```
task-1 ──depends-on──> task-3
   └──blocks──> task-5
task-2 ──depends-on──> task-4
```

### 5. Task Metrics

Calculate and display:
- **Total Tasks**: Count by status
- **Completion Rate**: Completed / Total
- **Average Age**: Mean age of incomplete tasks
- **Blocked Percentage**: Blocked / Active
- **Assignment Coverage**: Assigned / Total
- **Sprint Coverage**: In Sprint / Total

### 6. Task Health Indicators

Identify issues:
- 🔴 **Stale Tasks**: No updates > 3 days
- 🟡 **Long Running**: In progress > 5 days
- 🔴 **Unassigned Critical**: High priority without assignment
- 🟡 **Dependency Chains**: > 3 levels deep

### 7. Task Flow Analysis

Show task movement:
```
Last 24 Hours:
pending (5) ──> in_progress (3) ──> completed (2)
                     └──> blocked (1)
```

## Advanced Queries

Support complex task queries:

```bash
# Find stale tasks
/state tasks --age | head -10

# Show blocked tasks with dependencies
/state tasks --blocked --show-dependencies

# Tasks for specific agent
/state tasks --assigned-to engineering-fullstack-1

# Unassigned high-priority tasks
/state tasks --unassigned --priority high
```

## Task Actions

Suggest next actions based on analysis:

1. **Quick Wins**: Tasks that can be completed quickly
2. **Unblock Candidates**: Tasks whose blockers can be resolved
3. **Assignment Suggestions**: Match unassigned tasks to available agents
4. **Priority Rebalancing**: Suggest priority adjustments

## Output Format

Organize output in sections:

```
═══════════════════════════════════════════
              TASK OVERVIEW
═══════════════════════════════════════════

📊 SUMMARY
├─ Total Tasks: 45
├─ Completed Today: 5 (11%)
├─ In Progress: 12 (27%)
├─ Blocked: 3 (7%)
└─ Pending: 25 (55%)

⚡ REQUIRES ACTION (3)
• task-15: Blocked 3 days - needs auth service
• task-8: Unassigned critical bug
• task-22: Stale - no updates for 5 days

📋 TASK BREAKDOWN
[Detailed table here]

🔄 RECENT ACTIVITY
• task-5: pending → in_progress (1h ago)
• task-3: in_progress → completed (2h ago)
• task-7: in_progress → blocked (3h ago)

💡 RECOMMENDATIONS
1. Assign task-8 to available QA agent
2. Resolve task-15 blocker first
3. Check status of task-22 with owner
```

## Interactive Commands

Provide follow-up commands:
- "Update task: `/state set tasks.task-1.status 'completed'`"
- "Assign task: `/state set tasks.task-1.assigned_to 'agent-1'`"
- "View task details: `/state get tasks.task-1`"
- "Update via manager: `!.claude/scripts/state_manager.py update-task task-1 completed`"