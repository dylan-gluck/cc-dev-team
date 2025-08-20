---
allowed-tools: Bash(.claude/scripts/state_manager.py:*), Read
description: State management menu and current orchestration summary
model: haiku
---

# State Management Interface

Display the current orchestration state summary and available state operations.

## Context

Current orchestration state: !`.claude/scripts/state_manager.py summary`

## Task

1. Display a comprehensive summary of the current orchestration state including:
   - Active projects and their status
   - Task distribution (pending, in progress, completed, blocked)
   - Agent assignments and availability
   - Active sprints and progress metrics
   - Recent state change events

2. Present available state management operations:
   - `/state get [path]` - Query specific state values
   - `/state set [path] [value]` - Update state with validation
   - `/state summary` - Detailed orchestration overview
   - `/state tasks` - Task status and assignments
   - `/state agents` - Agent workload and status
   - `/state sprints` - Sprint progress and metrics
   - `/state reset` - Reset orchestration state

3. Provide helpful examples:
   - Query examples: `get tasks.task-1`, `get agents.active`
   - Update examples: `set tasks.task-1.status "completed"`
   - Filter examples: `get "tasks | map(select(.status == \"pending\"))"`

## Output Format

Use Rich formatting to create an organized display with:
- Summary table showing key metrics
- Color-coded status indicators (green=good, yellow=warning, red=blocked)
- Clear section headers for different state categories
- Examples section with common operations

## Constraints

- Read-only operation - do not modify state
- Use jq-style paths for consistency
- Display timestamps in relative format (e.g., "2 hours ago")
- Limit event history to last 10 entries