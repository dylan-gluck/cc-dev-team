---
allowed-tools: Bash(.claude/scripts/state_manager.py get:*), Bash(jq:*)
description: Query orchestration state using jq-style paths
argument-hint: <path> [--format json|table]
model: haiku
---

# Query Orchestration State

Retrieve specific values from the orchestration state using jq-style path queries.

## Context

Arguments provided: $ARGUMENTS

## Task

Parse the arguments to extract:
1. The jq-style path query (required)
2. Optional format flag (--format json or --format table)

Execute the state query using the state manager:
1. If no path is provided, show the entire state
2. Use the path to query specific state values
3. Support complex jq expressions for filtering and transformation
4. Format output based on the specified format (default: json)

## Path Examples

Common query patterns:
- **Root sections**: `tasks`, `agents`, `sprints`, `projects`
- **Specific items**: `tasks.task-1`, `agents.active.engineering-fullstack-1`
- **Nested values**: `sprints.sprint-1.metrics.velocity`
- **Array queries**: `communication.questions[0]`
- **Filters**: `tasks | map(select(.status == "in_progress"))`
- **Transformations**: `agents.active | keys`
- **Counts**: `tasks | map(select(.status == "completed")) | length`

## Advanced Queries

Support complex jq expressions:
- **Multiple conditions**: `tasks | map(select(.status == "pending" and .priority == "high"))`
- **Projections**: `tasks | map({id, status, assigned_to})`
- **Aggregations**: `sprints | map(.metrics.velocity) | add`
- **Path existence**: `tasks | map(select(has("assigned_to")))`

## Output Formatting

Based on the format flag:
- **json** (default): Pretty-printed JSON with syntax highlighting
- **table**: Structured table for dict/list data with headers

For table format with nested data:
- Flatten one level for readability
- Show JSON for deeply nested structures
- Use color coding for different data types

## Error Handling

- If path doesn't exist: Show available paths at parent level
- If jq expression is invalid: Display jq error with correction suggestions
- If result is empty: Indicate no matching data found
- Suggest similar paths if typo is suspected

## Examples

```bash
# Get all tasks
/state get tasks

# Get specific task with table format
/state get tasks.task-1 --format table

# Get pending tasks
/state get "tasks | map(select(.status == \"pending\"))"

# Get agent assignments
/state get "agents.active | map({(.id): .current_task})"

# Count completed tasks
/state get "tasks | map(select(.status == \"completed\")) | length"
```