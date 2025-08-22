#!/bin/bash
# Session Initializer - Sets up new orchestration sessions
# Called via SessionStart hook

set -euo pipefail

# Create session with v2 orchestration structure
SESSION_ID="session_$(date +%s)_$$"

# Initialize session state with v2 structure
cd "$CLAUDE_PROJECT_DIR/.claude/scripts" && \
uv run session_manager.py create "$SESSION_ID" 2>/dev/null || true

# Set up default state structure
INITIAL_STATE=$(cat <<EOF
{
  "session_id": "$SESSION_ID",
  "created_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "workflow": {
    "type": null,
    "status": "initialized",
    "progress": 0
  },
  "agents": {},
  "metrics": {
    "tokens_used": 0,
    "tasks_completed": 0,
    "tests_written": false,
    "documentation_updated": false
  },
  "shared_context": {},
  "output_style": "default",
  "orchestration_mode": "manual"
}
EOF
)

# Save initial state
cd "$CLAUDE_PROJECT_DIR/.claude/scripts" && \
echo "$INITIAL_STATE" | uv run state_manager.py set "$SESSION_ID" "$" 2>/dev/null || true

# Create session output directory if needed
SESSION_DIR="$CLAUDE_PROJECT_DIR/.claude/state/sessions/$SESSION_ID"
mkdir -p "$SESSION_DIR/outputs" 2>/dev/null || true

# Initialize event stream if available
if [[ -f "$CLAUDE_PROJECT_DIR/.claude/scripts/event_stream.py" ]]; then
    cd "$CLAUDE_PROJECT_DIR/.claude/scripts" && \
    uv run event_stream.py init "$SESSION_ID" 2>/dev/null || true
fi

# Log session creation
if [[ -f "$CLAUDE_PROJECT_DIR/.claude/scripts/observability.py" ]]; then
    cd "$CLAUDE_PROJECT_DIR/.claude/scripts" && \
    uv run observability.py log session_created --session "$SESSION_ID" 2>/dev/null || true
fi

# Export session ID for other hooks
echo "$SESSION_ID" > "$CLAUDE_PROJECT_DIR/.claude/state/current_session" 2>/dev/null || true

# Output session info (will be captured by Claude Code)
echo "Orchestration session initialized: $SESSION_ID"

exit 0