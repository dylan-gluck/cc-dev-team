# Orchestration System V2 Implementation Plan

## Executive Summary

The V2 orchestration system transforms the current file-based, manually-triggered architecture into a **session-aware, program-based orchestration runtime** that leverages Claude Code's native features (output styles, status lines) to create interactive development environments. This evolution reduces complexity from 249 files to approximately 50 core files while maintaining all existing capabilities and adding significant new functionality.

### Key Innovations
- **Session-Based State Management**: Isolated state per Claude Code instance
- **Output Styles as Programs**: Transform main agent into specialized runtimes
- **Intelligent Hook Routing**: Session-aware, conditional orchestration activation
- **Live Status Lines**: Real-time orchestration metrics and state display
- **Simplified Architecture**: 80% reduction in file count, 60% reduction in code complexity

## Architecture Overview

### System Layers

```
┌─────────────────────────────────────────────────┐
│           User Interface Layer                   │
│  (Output Styles, Status Lines, TUI Dashboards)   │
├─────────────────────────────────────────────────┤
│           Orchestration Runtime                  │
│   (Session Manager, State Engine, Event Bus)     │
├─────────────────────────────────────────────────┤
│            Agent Hierarchy                       │
│     (Directors, Specialists, Workers)            │
├─────────────────────────────────────────────────┤
│           Hook System                            │
│    (Lifecycle Events, State Updates)             │
├─────────────────────────────────────────────────┤
│         External Services (MCP)                  │
└─────────────────────────────────────────────────┘
```

### Core Design Principles

1. **Session Isolation**: Each Claude Code instance maintains independent state
2. **Program-Based Interaction**: Output styles define behavior modes
3. **Event-Driven Updates**: All state changes flow through event system
4. **Progressive Enhancement**: Orchestration features activate on-demand
5. **Minimal File I/O**: In-memory state with periodic persistence

## Core Components

### 1. Session Management System

**Location**: `.claude/scripts/session_manager.py`

```python
# Session State Schema
{
    "session_id": "uuid",
    "created_at": "timestamp",
    "orchestration_enabled": bool,
    "mode": "development|leadership|config",
    "active_teams": ["engineering", "qa"],
    "current_epic": "epic_id",
    "current_sprint": "sprint_id",
    "state": {
        "agents": {},
        "tasks": {},
        "messages": {},
        "metrics": {}
    },
    "runtime_config": {
        "output_style": "all-team_dashboard",
        "status_line": "orchestration_metrics"
    }
}
```

**Key Features**:
- In-memory state with Redis-like operations
- File persistence every 30 seconds or on critical changes
- Session expiry after 24 hours of inactivity
- Hot-reload capability for configuration changes

### 2. Output Styles as Programs

**Location**: `.claude/output-styles/`

#### Program Types

1. **all-team_dashboard**: Full orchestration dashboard
   - Visual team status display
   - Task progress tracking
   - Real-time metric updates
   - Interactive command palette

2. **leadership_chat**: Strategic planning interface
   - Multi-agent discussion threads
   - Decision tracking
   - Performance analysis
   - Resource allocation

3. **sprint_execution**: Development workflow runtime
   - Task assignment automation
   - Progress visualization
   - Blocker identification
   - Velocity tracking

4. **config_manager**: System configuration TUI
   - Team configuration
   - Agent management
   - Workflow customization
   - Settings adjustment

#### Implementation Pattern

```markdown
# Output Style: all-team_dashboard

You are running in Orchestration Dashboard mode. Display all responses as a structured dashboard:

## Dashboard Layout
╔════════════════════════════════════════════════╗
║  ORCHESTRATION DASHBOARD - Sprint {{sprint_id}} ║
╠════════════════════════════════════════════════╣
║ Teams     │ Tasks    │ Messages │ Performance  ║
╟───────────┼──────────┼──────────┼──────────────╢
║ {{teams}} │ {{tasks}}│ {{msgs}} │ {{metrics}}  ║
╚════════════════════════════════════════════════╝

## Interaction Commands
- `team <name>`: Activate team
- `task <id>`: View task details
- `assign <task> <agent>`: Delegate work
- `status`: Refresh dashboard
- `help`: Show all commands

## State Integration
Fetch current state using: !bash ~/.claude/scripts/get_session_state.py
Update state using: !bash ~/.claude/scripts/update_state.py --key=value

Maintain visual consistency and update dashboard after each interaction.
```

### 3. Intelligent Hook System

**Location**: `.claude/hooks/orchestration/`

#### Hook Router Implementation

```python
#!/usr/bin/env uv
# /// script
# requires-python = ">=3.12"
# dependencies = ["pydantic", "typing-extensions"]
# ///

import json
import sys
from pathlib import Path
from typing import Any, Dict

def route_hook_event(data: Dict[str, Any]) -> Dict[str, Any]:
    """Route hook events based on session state"""
    
    session_id = data.get("session_id")
    hook_event = data.get("hook_event_name")
    
    # Load session state
    session_state = load_session_state(session_id)
    
    # Check if orchestration is enabled
    if not session_state.get("orchestration_enabled"):
        return {}  # Pass through without orchestration
    
    # Route based on hook type and state
    if hook_event == "UserPromptSubmit":
        return handle_user_prompt(data, session_state)
    elif hook_event == "SubagentStop":
        return handle_subagent_complete(data, session_state)
    elif hook_event == "PreToolUse":
        return handle_tool_permission(data, session_state)
    
    return {}
```

#### Hook Categories

1. **Session Hooks**
   - SessionStart: Initialize orchestration state
   - SessionEnd: Persist state and cleanup
   - Stop: Checkpoint current progress

2. **Agent Hooks**
   - SubagentStart: Track agent activation
   - SubagentStop: Capture results and metrics
   - AgentCapacity: Monitor resource usage

3. **Tool Hooks**
   - PreToolUse: Validate permissions
   - PostToolUse: Capture side effects
   - ToolError: Handle failures

4. **State Hooks**
   - StateChange: Emit events
   - TaskUpdate: Track progress
   - MessageReceived: Route communications

### 4. Slash Command System

**Location**: `.claude/commands/orchestration/`

#### Command Categories

1. **Workflow Commands**
   ```
   /start-sprint --teams="engineering,qa" --epic="user-auth"
   /delegate-tasks --strategy="parallel" --priority="high"
   /review-progress --format="dashboard"
   ```

2. **Team Commands**
   ```
   /activate-team engineering
   /team-standup --async
   /assign-lead @engineering-lead
   ```

3. **State Commands**
   ```
   /enable-orchestration
   /set-mode leadership
   /checkpoint-state
   ```

#### Command Template

```markdown
---
name: start-sprint
description: Initialize a new development sprint
model: opus
---

# Start Sprint Command

!bash ~/.claude/scripts/orchestration.py enable-session {{SESSION_ID}}
!bash ~/.claude/scripts/orchestration.py set-mode "sprint_execution"
!bash ~/.claude/scripts/orchestration.py activate-teams {{teams}}

## Sprint Initialization

You are now starting a new sprint with the following configuration:
- Teams: {{teams}}
- Epic: {{epic}}
- Duration: {{duration}}

Begin by:
1. Loading the epic requirements
2. Breaking down into sprint tasks
3. Assigning tasks to teams
4. Setting up monitoring

Use the Task tool to delegate initial planning to team directors.
```

### 5. Status Line Implementation

**Location**: `.claude/scripts/status_line.py`

```python
#!/usr/bin/env uv
# /// script
# requires-python = ">=3.12"
# dependencies = ["rich", "arrow"]
# ///

import json
import sys
from pathlib import Path

def generate_status_line(data: dict) -> str:
    """Generate context-aware status line"""
    
    session_id = data.get("session_id")
    session_state = load_session_state(session_id)
    
    if not session_state.get("orchestration_enabled"):
        # Default status line
        return f"[{data['model']['display_name']}] 📁 {Path.cwd().name}"
    
    # Orchestration status line
    mode = session_state.get("mode", "idle")
    active_agents = len(session_state.get("state", {}).get("agents", {}))
    pending_tasks = count_pending_tasks(session_state)
    
    icons = {
        "development": "⚡",
        "leadership": "👥",
        "config": "⚙️",
        "idle": "💤"
    }
    
    return (
        f"{icons.get(mode, '📊')} {mode.upper()} | "
        f"👥 {active_agents} agents | "
        f"📝 {pending_tasks} tasks | "
        f"🏃 Sprint Day {get_sprint_day(session_state)}"
    )

if __name__ == "__main__":
    data = json.load(sys.stdin)
    print(generate_status_line(data))
```

## Implementation Phases

### Phase 1: Foundation (Week 1-2)
**Goal**: Establish core session management and state system

1. **Session Manager Implementation**
   - [ ] Create session state schema
   - [ ] Implement state persistence layer
   - [ ] Build session isolation mechanism
   - [ ] Add state query API

2. **Hook Router Development**
   - [ ] Create universal hook handler
   - [ ] Implement session state loading
   - [ ] Add conditional routing logic
   - [ ] Build response formatting

3. **Basic Status Line**
   - [ ] Create status line script
   - [ ] Add session state integration
   - [ ] Implement mode detection
   - [ ] Test with multiple sessions

### Phase 2: Output Styles (Week 3-4)
**Goal**: Create interactive program runtimes

1. **Dashboard Program**
   - [ ] Design TUI layout system
   - [ ] Implement state visualization
   - [ ] Add command interpreter
   - [ ] Create refresh mechanism

2. **Leadership Program**
   - [ ] Build discussion thread UI
   - [ ] Add multi-agent coordination
   - [ ] Implement decision tracking
   - [ ] Create metrics display

3. **Sprint Execution Program**
   - [ ] Design task board layout
   - [ ] Add progress tracking
   - [ ] Implement auto-assignment
   - [ ] Build velocity calculator

### Phase 3: Command Integration (Week 5-6)
**Goal**: Streamline workflow automation

1. **Core Commands**
   - [ ] Convert existing commands to new format
   - [ ] Add session state integration
   - [ ] Implement bash execution patterns
   - [ ] Create command discovery

2. **Workflow Commands**
   - [ ] Build sprint management commands
   - [ ] Add team coordination commands
   - [ ] Create review commands
   - [ ] Implement state commands

3. **Debug Commands**
   - [ ] Add state inspection commands
   - [ ] Create event replay commands
   - [ ] Build performance profiling
   - [ ] Implement rollback commands

### Phase 4: Agent Optimization (Week 7-8)
**Goal**: Enhance agent coordination

1. **Agent Simplification**
   - [ ] Consolidate duplicate agents
   - [ ] Streamline system prompts
   - [ ] Optimize tool permissions
   - [ ] Improve delegation rules

2. **Communication Enhancement**
   - [ ] Upgrade message bus to session-aware
   - [ ] Add priority routing
   - [ ] Implement broadcast optimization
   - [ ] Create agent discovery

3. **Performance Tuning**
   - [ ] Add capacity management
   - [ ] Implement load balancing
   - [ ] Create fallback mechanisms
   - [ ] Build error recovery

## Migration Strategy

### 1. Parallel Operation
- Run V2 alongside V1 for 2 weeks
- Use feature flags to enable V2 per session
- Maintain backward compatibility

### 2. Data Migration
```python
# Migration script
def migrate_v1_to_v2():
    v1_state = load_v1_orchestration_state()
    v2_sessions = {}
    
    for project in v1_state.get("projects", {}).values():
        session = create_v2_session()
        session["state"]["tasks"] = project.get("tasks", {})
        session["state"]["agents"] = v1_state.get("agents", {})
        v2_sessions[session["session_id"]] = session
    
    save_v2_sessions(v2_sessions)
```

### 3. Feature Parity Checklist
- [ ] All V1 commands work in V2
- [ ] Agent coordination maintained
- [ ] State queries produce same results
- [ ] Performance metrics comparable
- [ ] Error handling improved

### 4. Deprecation Timeline
- Week 1-2: V2 development
- Week 3-4: Internal testing
- Week 5-6: Beta release
- Week 7-8: Production release
- Week 9-10: V1 deprecation
- Week 11-12: V1 removal

## Technical Specifications

### File Structure (Simplified)
```
.claude/
├── output-styles/
│   ├── all-team_dashboard.md
│   ├── leadership_chat.md
│   ├── sprint_execution.md
│   └── config_manager.md
├── commands/
│   └── orchestration/
│       ├── start-sprint.md
│       ├── delegate-tasks.md
│       └── review-progress.md
├── hooks/
│   └── orchestration/
│       ├── router.py
│       └── handlers.py
├── scripts/
│   ├── session_manager.py
│   ├── status_line.py
│   ├── state_engine.py
│   └── event_bus.py
├── agents/
│   └── [consolidated to ~30 core agents]
└── state/
    └── sessions/
        └── [session_id].json
```

### Performance Targets
- Session initialization: < 100ms
- State query: < 50ms
- Hook processing: < 200ms
- Dashboard refresh: < 500ms
- Agent spawn: < 1s

### Resource Limits
- Max concurrent sessions: 10
- Max agents per session: 20
- State file size: < 1MB
- Event buffer: 1000 events
- Message queue: 100 messages

## Risk Mitigation

### Technical Risks

1. **State Corruption**
   - Mitigation: Implement write-ahead logging
   - Backup: Automatic state snapshots every hour
   - Recovery: State reconstruction from event log

2. **Performance Degradation**
   - Mitigation: In-memory caching
   - Monitoring: Performance metrics in status line
   - Optimization: Lazy loading of state sections

3. **Session Conflicts**
   - Mitigation: Strong session isolation
   - Detection: Conflict detection in hooks
   - Resolution: Session merge capabilities

### Operational Risks

1. **Migration Failures**
   - Mitigation: Comprehensive migration testing
   - Rollback: One-command V1 restoration
   - Support: Migration troubleshooting guide

2. **User Adoption**
   - Mitigation: Extensive documentation
   - Training: Video tutorials
   - Support: Discord community channel

## Success Metrics

### Quantitative Metrics
- **Complexity Reduction**: 80% fewer files (249 → 50)
- **Performance Improvement**: 3x faster state operations
- **Automation Increase**: 60% reduction in manual commands
- **Error Reduction**: 50% fewer state-related errors
- **Response Time**: 40% faster orchestration operations

### Qualitative Metrics
- **Developer Experience**: Simplified mental model
- **Debugging**: Clear event traces
- **Extensibility**: Easy to add new programs
- **Maintainability**: Reduced code duplication
- **Documentation**: Self-documenting architecture

## Implementation Timeline

### Month 1: Foundation
- Week 1-2: Core session management
- Week 3-4: Output styles development

### Month 2: Integration
- Week 5-6: Command system upgrade
- Week 7-8: Agent optimization

### Month 3: Deployment
- Week 9-10: Migration and testing
- Week 11-12: Production rollout

## Conclusion

The V2 orchestration system represents a fundamental shift from file-based coordination to session-based, program-driven orchestration. By leveraging Claude Code's native features and simplifying the architecture, we achieve:

1. **Better User Experience**: Interactive dashboards and real-time feedback
2. **Improved Performance**: In-memory state and optimized operations
3. **Reduced Complexity**: 80% fewer files with clearer organization
4. **Enhanced Automation**: Intelligent routing and auto-delegation
5. **Future-Proof Design**: Extensible architecture for new features

This implementation plan provides a clear path from the current V1 system to a more sophisticated, efficient, and maintainable V2 orchestration platform that will significantly enhance the development workflow capabilities of Claude Code.

## Next Steps

1. Review and approve implementation plan
2. Set up V2 development branch
3. Begin Phase 1 implementation
4. Create migration test suite
5. Document V2 architecture for team

---

*Document Version: 1.0*  
*Last Updated: 2025-01-21*  
*Status: Ready for Implementation*