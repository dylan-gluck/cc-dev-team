# Multi-Team Orchestration

This purpose of this repo is to build a multi-team orchestration and observibility framework on top of claude-code.

## Hooks

Hook are single-file uv scripts that are run during lifecycle events. Currently we are only logging events in the `.claude/logs/` dir. The goal is to update the existing scripts to provide a visibility and orchestration layer across multiple subagents within a session.

Existing scripts: `.claude/hooks/*.py`
Logs for data reference: `.claude/logs/*.json`

We need to refactor the existing scripts to support the updated functionality:
- Initialize session directory & state data on SessionStart
- Parse hook data (PreToolUse & PostToolUse most notably) & update state object during runtime
  - Add agent-name to agents array on PreToolUse "Task"
  - Remove agent-name from agents array on PostToolUse "Task"
  - Add file-path to file.new array on PostToolUse "Write"
  - Add file-path to file.edited array on PostToolUse "Edit|MultiEdit"

### SessionStart `.claude/hooks/session_start.py`

1. Create a new directory for session state `.claude/sessions/{session_id}/`

2. Initialize session state `.claude/sessions/{session_id}/state.json`
```json
{
  "session_id": "{session_id}",
  "created_at": "{created_at}",
  "updated_at": "{updated_at}",
  "orchestration": false,
  "workflow": "",
  "agents": [],
  "files": {
    "new": [],
    "edited": []
  },
}
```

3. Initialize session messages `.claude/sessions/{session_id}/messages.json`
```json
{
  "messages": []
}
```
