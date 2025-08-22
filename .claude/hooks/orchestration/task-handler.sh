#!/bin/bash
# Task Handler - Processes task completion events
# Called via PostToolUse hook when tasks are marked complete

set -euo pipefail

# Extract event data from stdin
EVENT_DATA=$(cat)

# Get tool information
TOOL_NAME=$(echo "$EVENT_DATA" | jq -r '.tool // empty')
TOOL_OUTPUT=$(echo "$EVENT_DATA" | jq -r '.output // empty')

# Check for TodoWrite operations (task completions)
if [[ "$TOOL_NAME" == "TodoWrite" ]]; then
    # Extract todos from the tool input
    TODOS=$(echo "$EVENT_DATA" | jq -r '.input.todos // empty')
    
    if [[ -n "$TODOS" ]] && [[ "$TODOS" != "empty" ]]; then
        # Get current session
        SESSION_ID=$(cd "$CLAUDE_PROJECT_DIR/.claude/scripts" && uv run session_manager.py current 2>/dev/null || echo "default")
        
        # Count completed tasks
        COMPLETED_COUNT=$(echo "$TODOS" | jq '[.[] | select(.status == "completed")] | length')
        IN_PROGRESS_COUNT=$(echo "$TODOS" | jq '[.[] | select(.status == "in_progress")] | length')
        PENDING_COUNT=$(echo "$TODOS" | jq '[.[] | select(.status == "pending")] | length')
        
        # Update session metrics
        if [[ "$COMPLETED_COUNT" -gt 0 ]]; then
            cd "$CLAUDE_PROJECT_DIR/.claude/scripts" && \
            uv run state_manager.py update "$SESSION_ID" \
                "$.metrics.tasks_completed" "$COMPLETED_COUNT" 2>/dev/null || true
            
            # Update sprint progress if in sprint workflow
            STATE=$(cd "$CLAUDE_PROJECT_DIR/.claude/scripts" && uv run state_manager.py get "$SESSION_ID" "$" 2>/dev/null || echo "{}")
            WORKFLOW_TYPE=$(echo "$STATE" | jq -r '.workflow.type // empty')
            
            if [[ "$WORKFLOW_TYPE" == "sprint" ]]; then
                # Calculate sprint progress
                TOTAL_TASKS=$((COMPLETED_COUNT + IN_PROGRESS_COUNT + PENDING_COUNT))
                if [[ "$TOTAL_TASKS" -gt 0 ]]; then
                    PROGRESS=$((COMPLETED_COUNT * 100 / TOTAL_TASKS))
                    
                    cd "$CLAUDE_PROJECT_DIR/.claude/scripts" && \
                    uv run state_manager.py update "$SESSION_ID" \
                        "$.workflow.progress" "$PROGRESS" 2>/dev/null || true
                fi
            fi
        fi
        
        # Log task metrics
        if [[ -f "$CLAUDE_PROJECT_DIR/.claude/scripts/observability.py" ]]; then
            cd "$CLAUDE_PROJECT_DIR/.claude/scripts" && \
            uv run observability.py log task_update \
                --session "$SESSION_ID" \
                --completed "$COMPLETED_COUNT" \
                --in_progress "$IN_PROGRESS_COUNT" \
                --pending "$PENDING_COUNT" 2>/dev/null || true
        fi
    fi
fi

# Check for explicit task completion markers in Write/Edit operations
if [[ "$TOOL_NAME" == "Write" ]] || [[ "$TOOL_NAME" == "Edit" ]]; then
    # Check if file path indicates test completion
    FILE_PATH=$(echo "$EVENT_DATA" | jq -r '.input.file_path // empty')
    
    if echo "$FILE_PATH" | grep -qE '(test|spec)\.(py|js|ts)$'; then
        SESSION_ID=$(cd "$CLAUDE_PROJECT_DIR/.claude/scripts" && uv run session_manager.py current 2>/dev/null || echo "default")
        
        # Mark test writing as completed
        cd "$CLAUDE_PROJECT_DIR/.claude/scripts" && \
        uv run state_manager.py update "$SESSION_ID" \
            "$.metrics.tests_written" "true" 2>/dev/null || true
    fi
fi

# Always exit 0 to not block operations
exit 0