#!/bin/bash
# State Router - Routes state change events to appropriate handlers
# Called via PostToolUse hook with state change detection

set -euo pipefail

# Extract event data from stdin (JSON format from PostToolUse)
EVENT_DATA=$(cat)

# Get the tool name and check if it's a state-changing operation
TOOL_NAME=$(echo "$EVENT_DATA" | jq -r '.tool // empty')
TOOL_INPUT=$(echo "$EVENT_DATA" | jq -r '.input // empty')

# Check if this is a state management operation
if [[ "$TOOL_NAME" == "Bash" ]] && echo "$TOOL_INPUT" | grep -q "state_manager.py"; then
    # Extract session ID from the command
    SESSION_ID=$(echo "$TOOL_INPUT" | grep -oP 'session_[a-z0-9]+' | head -1 || echo "default")
    
    # Get current state
    STATE=$(cd "$CLAUDE_PROJECT_DIR/.claude/scripts" && uv run state_manager.py get "$SESSION_ID" "$" 2>/dev/null || echo "{}")
    
    # Check for state changes that need synchronization
    if echo "$STATE" | jq -e '.workflow.type // empty' > /dev/null; then
        # Sync shared state for active workflows
        cd "$CLAUDE_PROJECT_DIR/.claude/scripts" && \
        uv run shared_state.py sync "$SESSION_ID" 2>/dev/null || true
    fi
    
    # Update observability metrics
    if [[ -f "$CLAUDE_PROJECT_DIR/.claude/scripts/observability.py" ]]; then
        echo "$STATE" | cd "$CLAUDE_PROJECT_DIR/.claude/scripts" && \
        uv run observability.py log state_change --session "$SESSION_ID" 2>/dev/null || true
    fi
fi

# Check for agent spawn events
if [[ "$TOOL_NAME" == "Agent" ]]; then
    AGENT_NAME=$(echo "$TOOL_INPUT" | jq -r '.agent // empty')
    SESSION_ID=$(cd "$CLAUDE_PROJECT_DIR/.claude/scripts" && uv run session_manager.py current 2>/dev/null || echo "default")
    
    # Register agent in session state
    if [[ -n "$AGENT_NAME" ]] && [[ -n "$SESSION_ID" ]]; then
        cd "$CLAUDE_PROJECT_DIR/.claude/scripts" && \
        uv run state_manager.py update "$SESSION_ID" \
            "$.agents.$AGENT_NAME.spawned_at" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" 2>/dev/null || true
    fi
fi

# Always exit 0 to not block operations
exit 0