# V2 Orchestration Hooks

This directory contains the hook handlers for the V2 orchestration system. These hooks integrate with Claude Code's event system to provide automatic state management, task tracking, and session orchestration.

## Hook Integration Points

### SessionStart Hook
- **Handler**: `orchestration_session_init.py`
- **Purpose**: Initializes new orchestration sessions
- **Triggers**: When a new Claude Code session starts
- **Actions**:
  - Creates session with unique ID
  - Initializes state structure
  - Sets up session directories
  - Configures event stream
  - Logs session creation

### PostToolUse Hook
- **Handler**: `orchestration_handler.py`
- **Purpose**: Tracks state changes and task completions
- **Triggers**: After any tool execution
- **Actions**:
  - Monitors TodoWrite for task tracking
  - Tracks Agent spawning
  - Syncs state changes
  - Updates metrics and progress

## Shell Scripts (Legacy/Backup)

The `.sh` scripts provide bash-based alternatives:
- `state-router.sh` - Routes state change events
- `task-handler.sh` - Processes task completions
- `session-init.sh` - Initializes sessions

## Integration with UV Scripts

The hooks integrate with the core UV scripts in `.claude/scripts/`:
- `state_manager.py` - State persistence
- `session_manager.py` - Session lifecycle
- `shared_state.py` - Cross-agent state sync
- `observability.py` - Metrics and logging
- `event_stream.py` - Event broadcasting

## Hook Configuration

The hooks are configured in `.claude/settings.json`:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "",
        "hooks": [{
          "type": "command",
          "command": "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/orchestration_session_init.py",
          "timeout": 5
        }]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "",
        "hooks": [{
          "type": "command",
          "command": "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/orchestration_handler.py",
          "timeout": 3
        }]
      }
    ]
  }
}
```

## Hook Behavior

### Non-Blocking Design
- All hooks exit with code 0 to avoid blocking operations
- Errors are logged but don't interrupt workflow
- Timeouts ensure hooks don't delay tool execution

### State Synchronization
- Automatic state sync on agent spawns
- Progress tracking for sprint workflows
- Metrics collection for all operations

### Task Tracking
- Monitors TodoWrite tool for task updates
- Calculates completion percentages
- Updates sprint progress automatically

## Data Flow

```
Claude Code Event
    ↓
Hook Triggered
    ↓
Handler Script
    ↓
UV Script Call
    ↓
State Update
    ↓
Observability Log
```

## Testing Hooks

Test session initialization:
```bash
echo '{}' | uv run orchestration_session_init.py
```

Test task handling:
```bash
echo '{"tool": "TodoWrite", "input": {"todos": [{"content": "Test", "status": "completed"}]}}' | \
  uv run orchestration_handler.py
```

## Debugging

Check hook execution logs:
```bash
# View state for current session
uv run state_manager.py get $(uv run session_manager.py current) '$'

# Check observability logs
ls .claude/state/observability/

# View current session
cat .claude/state/current_session
```

## Security Notes

- Hooks run with project directory permissions only
- No external network calls
- State files are local to project
- Timeouts prevent infinite loops
- All operations are read/write to `.claude/` directory only