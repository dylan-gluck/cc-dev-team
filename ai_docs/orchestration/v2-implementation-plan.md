# V2 Orchestration Implementation Plan

## Executive Summary

The V2 orchestration system transforms Claude Code into a sophisticated development team coordinator through a radically simplified architecture based on **JSON state files**, **UV scripts**, and **SudoLang programs**. This approach eliminates all external dependencies while providing powerful multi-session coordination capabilities.

### Key Deliverables

1. **Three UV Scripts**: Core state management operations with inline dependencies
2. **Four SudoLang Programs**: Interactive output styles for different workflows
3. **JSON State Structure**: Clear separation of shared vs session state
4. **Zero Infrastructure**: No servers, databases, or external services required

### Timeline: 10 Days Total

- **Days 1-2**: UV scripts implementation
- **Days 3-5**: SudoLang output styles
- **Days 6-7**: Hook integration
- **Days 8-10**: Testing and documentation

## Architecture Summary

```
User Interaction
       ↓
SudoLang Programs (Output Styles)
       ↓
UV Scripts (State Operations)
       ↓
JSON Files (State Persistence)
```

### Core Principles

1. **Simplicity First**: JSON + UV scripts = complete solution
2. **No Dependencies**: Works on any system with Python
3. **Human-Readable**: All state in inspectable JSON
4. **Natural Language**: SudoLang programs for UI behavior
5. **Progressive Enhancement**: Add complexity only when needed

## Phase 1: UV Scripts (Days 1-2)

### Day 1: Core State Manager

**File**: `ai_docs/orchestration/scripts/state_manager.py`

**Features to Implement**:
```python
# Core operations
- get(session_id, path) → JSONPath query
- set(session_id, path, value) → Atomic update
- merge(session_id, path, data) → Deep merge
- delete(session_id, path) → Remove key
- list-sessions() → Show all sessions
- cleanup-expired() → Remove old sessions
```

**State Structure**:
```json
{
  "session": {
    "id": "uuid",
    "mode": "development|leadership|sprint|config",
    "created_at": "ISO-8601",
    "lifecycle": {
      "status": "active|paused|completed",
      "last_activity": "ISO-8601",
      "expiry": "ISO-8601"
    }
  },
  "execution": {
    "agents": {},
    "tasks": {},
    "workflows": {}
  },
  "observability": {
    "metrics": {},
    "events": []
  }
}
```

### Day 2: Session & Shared State Scripts

**File**: `ai_docs/orchestration/scripts/session_manager.py`

**Features**:
```bash
# Session lifecycle
uv run session_manager.py create --mode development --project myapp
uv run session_manager.py heartbeat SESSION_ID
uv run session_manager.py handoff FROM_SESSION TO_SESSION
uv run session_manager.py list --active --project myapp
```

**File**: `ai_docs/orchestration/scripts/shared_state.py`

**Features**:
```bash
# Shared configuration
uv run shared_state.py get-config PROJECT_ID
uv run shared_state.py update-epic PROJECT_ID EPIC_ID --status completed
uv run shared_state.py list-sprints PROJECT_ID --status active
uv run shared_state.py list-tools
```

## Phase 2: SudoLang Programs (Days 3-5)

### Day 3: Dashboard Program

**File**: `ai_docs/orchestration/v2-output-style-dashboard.md`

**SudoLang Implementation**:
```sudolang
interface DashboardProgram {
  name = "all-team_dashboard"
  
  constraints {
    Always maintain ASCII art layout structure
    Show real-time state from UV scripts
    Process commands with "/" prefix
    Never lose navigation context
  }
  
  layout = """
  ╭─ ORCHESTRATION DASHBOARD ───────────────────╮
  │ Teams: {team_status}  Tasks: {task_summary} │
  │ Sprint: {sprint_progress}  Velocity: {vel}  │
  ├──────────────────────────────────────────────┤
  │ {main_content_area}                         │
  ├──────────────────────────────────────────────┤
  │ Activity: {recent_events}                   │
  ╰──────────────────────────────────────────────╯
  > {command_prompt}
  """
  
  commands = {
    "/team <name>": "Show team details",
    "/sprint": "Sprint board view",
    "/metrics": "Performance dashboard",
    "@<agent>": "Navigate to agent"
  }
  
  stateRefresh() {
    state = `uv run state_manager.py get {SESSION_ID} $`
    updateDisplay(state)
  }
}
```

### Day 4: Leadership & Sprint Programs

**Leadership Chat** (`v2-output-style-leadership.md`):
- Multi-agent discussion threads
- Decision tracking with voting
- Resource allocation interface
- Strategic planning tools

**Sprint Execution** (`v2-output-style-sprint.md`):
- Kanban board visualization
- Task assignment automation
- Velocity tracking
- Blocker management

### Day 5: Config Manager Program

**Config Manager** (`v2-output-style-config.md`):
- Team configuration UI
- Agent pool management
- Settings with validation
- Rollback capabilities

## Phase 3: Hook Integration (Days 6-7)

### Day 6: State-Triggered Hooks

**Hook Router Script**:
```bash
#!/bin/bash
# .claude/hooks/orchestration/router.sh

EVENT_TYPE=$1
SESSION_ID=$2
PAYLOAD=$3

# Get current session state
STATE=$(uv run state_manager.py get "$SESSION_ID" "$")

# Route based on event and state
case "$EVENT_TYPE" in
  "task_completed")
    update_sprint_progress "$SESSION_ID" "$PAYLOAD"
    ;;
  "agent_spawned")
    register_agent "$SESSION_ID" "$PAYLOAD"
    ;;
  "epic_updated")
    sync_shared_state "$SESSION_ID" "$PAYLOAD"
    ;;
esac
```

### Day 7: Cross-Session Coordination

**Message Passing** (Optional):
```python
# Simple file-based messaging
def send_message(from_session, to_session, message):
    msg_file = f"~/.claude/messages/{to_session}/inbox/{uuid4()}.json"
    with open(msg_file, 'w') as f:
        json.dump({
            "from": from_session,
            "to": to_session,
            "timestamp": datetime.now().isoformat(),
            "message": message
        }, f)

def poll_messages(session_id):
    inbox = f"~/.claude/messages/{session_id}/inbox"
    messages = []
    for msg_file in Path(inbox).glob("*.json"):
        with open(msg_file) as f:
            messages.append(json.load(f))
        msg_file.unlink()  # Mark as read
    return messages
```

## Phase 4: Testing & Polish (Days 8-10)

### Day 8: Integration Testing

**Test Scenarios**:

1. **Multi-Session Coordination**:
```bash
# Session A starts sprint
SESSION_A=$(uv run session_manager.py create --mode development)
uv run shared_state.py activate-sprint myapp sprint-001 --session $SESSION_A

# Session B joins sprint
SESSION_B=$(uv run session_manager.py create --mode development)
uv run state_manager.py set $SESSION_B "active_work.sprint" "sprint-001"

# Verify both see same sprint
uv run shared_state.py get-sprint myapp sprint-001
```

2. **State Recovery**:
```bash
# Simulate crash
kill -9 $CLAUDE_PID

# Recover state
uv run session_manager.py recover $SESSION_ID

# Verify state integrity
uv run state_manager.py get $SESSION_ID "$.execution.tasks"
```

### Day 9: Performance Optimization

**Optimization Areas**:

1. **Query Caching**:
```python
class CachedStateManager:
    def __init__(self):
        self.cache = {}
        self.cache_ttl = 5  # seconds
    
    def get(self, session_id, path):
        cache_key = f"{session_id}:{path}"
        if cache_key in self.cache:
            entry = self.cache[cache_key]
            if time.time() - entry['time'] < self.cache_ttl:
                return entry['value']
        
        value = self._fetch_from_disk(session_id, path)
        self.cache[cache_key] = {'value': value, 'time': time.time()}
        return value
```

2. **Batch Operations**:
```python
def batch_update(session_id, updates):
    with FileLock(get_lock_path(session_id)):
        state = load_state(session_id)
        for path, value in updates.items():
            set_nested(state, path, value)
        save_state(session_id, state)
```

### Day 10: Documentation & Examples

**Documentation Structure**:

1. **Quick Start Guide**:
```markdown
# V2 Orchestration Quick Start

## Installation (30 seconds)
1. Copy UV scripts to `.claude/scripts/`
2. Copy SudoLang programs to `.claude/output-styles/`
3. Run: `uv run session_manager.py create --mode development`

## Basic Usage
- Start dashboard: Type "dashboard mode"
- View state: `uv run state_manager.py get SESSION_ID $`
- Update task: `uv run state_manager.py set SESSION_ID "tasks.task-001.status" "done"`
```

2. **Example Workflows**:
- Sprint planning session
- Multi-agent code review
- Emergency incident response
- Team handoff procedures

## File Structure

```
.claude/
├── scripts/                      # UV Scripts (3 files)
│   ├── state_manager.py         # Core state operations
│   ├── session_manager.py       # Session lifecycle
│   └── shared_state.py          # Cross-session config
├── output-styles/                # SudoLang Programs (4 files)
│   ├── all-team_dashboard.md    # Main dashboard
│   ├── leadership_chat.md       # Strategic planning
│   ├── sprint_execution.md      # Development workflow
│   └── config_manager.md        # Settings management
├── hooks/                        # Hook Scripts
│   └── orchestration/
│       ├── router.sh            # Event router
│       └── handlers/            # Event handlers
└── state/                        # Runtime State (auto-created)
    ├── sessions/                 # Session states
    └── shared/                   # Shared configs
```

## Implementation Checklist

### Core Scripts
- [ ] `state_manager.py` - JSONPath queries, atomic updates
- [ ] `session_manager.py` - Session lifecycle management
- [ ] `shared_state.py` - Project configuration management

### SudoLang Programs
- [ ] Dashboard - Real-time monitoring interface
- [ ] Leadership - Strategic planning chat
- [ ] Sprint - Kanban task board
- [ ] Config - Settings management UI

### Integration
- [ ] Hook router - Event-based triggers
- [ ] State triggers - Automated responses
- [ ] Message passing - Cross-session coordination

### Testing
- [ ] Multi-session scenarios
- [ ] State recovery testing
- [ ] Performance benchmarks
- [ ] Error handling validation

### Documentation
- [ ] Quick start guide
- [ ] API reference
- [ ] Example workflows
- [ ] Troubleshooting guide

## Success Criteria

### Functional Requirements
- ✅ Zero external dependencies
- ✅ Multi-session support
- ✅ State persistence and recovery
- ✅ Interactive dashboards
- ✅ Command processing

### Performance Targets
- State query: < 50ms
- State update: < 100ms
- Dashboard refresh: < 500ms
- Session creation: < 200ms
- File operations: < 10ms

### Quality Metrics
- Code coverage: > 80%
- Documentation: Complete
- Examples: 5+ workflows
- Error handling: Comprehensive

## Risk Mitigation

### Technical Risks

1. **File Lock Contention**
   - Mitigation: Timeout handling, retry logic
   - Fallback: Read-only mode

2. **State File Corruption**
   - Mitigation: Atomic writes, backup copies
   - Recovery: From event log or backup

3. **Performance Degradation**
   - Mitigation: Caching, query optimization
   - Monitoring: Performance metrics

### Operational Risks

1. **User Adoption**
   - Mitigation: Simple commands, clear docs
   - Support: Examples and tutorials

2. **Migration Complexity**
   - Mitigation: Compatibility layer
   - Rollback: Keep v1 as fallback

## Conclusion

The V2 implementation delivers powerful orchestration capabilities through radical simplification:

- **3 UV Scripts** handle all state operations
- **4 SudoLang Programs** provide interactive interfaces
- **JSON Files** store all state transparently
- **Zero Dependencies** ensure universal compatibility
- **10-Day Timeline** enables rapid deployment

This approach proves that sophisticated coordination doesn't require complex infrastructure. The combination of UV scripts and SudoLang programs creates a system that is immediately useful, easily maintainable, and progressively enhanceable.

---

*Document Version: 2.0 (Simplified)*  
*Last Updated: 2025-01-21*  
*Status: Ready for Implementation*