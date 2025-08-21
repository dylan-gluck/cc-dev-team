# V2 State Management: Active vs Planned Work Clarification

## Executive Summary

This document clarifies the critical distinction between **Planned Work** (shared configuration state) and **Active Work** (session-specific runtime state) in the v2 orchestration system. This separation ensures that multiple Claude Code sessions can operate independently while sharing common project definitions and plans.

## Core Concepts

### Planned Work (Shared Configuration State)

**Definition**: Planned work represents the project's roadmap, team structure, and work definitions that exist independently of any specific Claude Code session. This is the "what could be done" layer.

**Characteristics**:
- Persists across sessions
- Read-mostly data (infrequently updated)
- Shared reference point for all sessions
- Defines the universe of possible work
- Version controlled and auditable

**Storage Location**: `/shared/` namespace in state

### Active Work (Session Runtime State)

**Definition**: Active work represents the actual execution state within a specific Claude Code session. This is the "what is being done right now" layer.

**Characteristics**:
- Session-specific and isolated
- Frequently updated during execution
- Contains runtime data and progress
- Destroyed when session ends
- Tracks actual vs planned progress

**Storage Location**: `/sessions/{session-id}/` namespace in state

## Active vs Planned Work Separation

### Data Model Architecture

```json
{
  "shared": {
    "project_definitions": {
      "epics": {
        "epic-auth-system": {
          "id": "epic-auth-system",
          "title": "Authentication System Overhaul",
          "description": "Complete redesign of authentication",
          "status": "approved",
          "features": [
            "feature-oauth2",
            "feature-mfa",
            "feature-session-mgmt"
          ],
          "requirements": {
            "functional": [...],
            "non_functional": [...]
          },
          "estimated_sprints": 3,
          "success_criteria": [...]
        }
      },
      "sprints": {
        "sprint-2024-w45": {
          "id": "sprint-2024-w45",
          "epic_id": "epic-auth-system",
          "name": "Sprint 45: OAuth Implementation",
          "planned_tasks": {
            "task-oauth-provider": {
              "id": "task-oauth-provider",
              "title": "Implement OAuth2 Provider Interface",
              "type": "feature",
              "estimated_effort": 8,
              "requirements": [...],
              "acceptance_criteria": [...],
              "assigned_team": "engineering"
            },
            "task-oauth-tests": {
              "id": "task-oauth-tests",
              "title": "OAuth2 Integration Tests",
              "type": "testing",
              "estimated_effort": 5,
              "dependencies": ["task-oauth-provider"]
            }
          },
          "team_allocations": {
            "engineering": {
              "capacity": 40,
              "members": ["engineering-lead", "engineering-fullstack"]
            }
          },
          "goals": [
            "Complete OAuth2 provider implementation",
            "Achieve 90% test coverage",
            "Documentation complete"
          ]
        }
      },
      "team_configurations": {
        "engineering": {
          "name": "Engineering Team",
          "orchestrator": "engineering-director",
          "available_agents": [
            {
              "agent_id": "engineering-lead",
              "role": "Technical Lead",
              "skills": ["architecture", "code-review", "mentoring"],
              "default_capacity": 1
            },
            {
              "agent_id": "engineering-fullstack",
              "role": "Full Stack Developer",
              "skills": ["frontend", "backend", "database"],
              "default_capacity": 3
            }
          ],
          "policies": {
            "max_parallel_agents": 5,
            "require_approval": true,
            "auto_scaling": false
          }
        }
      }
    },
    "metadata": {
      "version": "2.0.0",
      "last_updated": "2024-11-15T10:00:00Z",
      "update_frequency": "weekly",
      "governance": {
        "approval_required": true,
        "approvers": ["product-director", "engineering-director"]
      }
    }
  },
  "sessions": {
    "session-abc123": {
      "session_info": {
        "id": "session-abc123",
        "created_at": "2024-11-15T14:30:00Z",
        "mode": "development",
        "user": "developer@example.com"
      },
      "active_work": {
        "current_epic": "epic-auth-system",
        "current_sprint": "sprint-2024-w45",
        "execution_state": {
          "tasks": {
            "task-oauth-provider": {
              "status": "in_progress",
              "assignee": "engineering-fullstack-1",
              "started_at": "2024-11-15T14:35:00Z",
              "actual_effort": 3,
              "progress_percentage": 40,
              "blockers": [],
              "artifacts": [
                "src/auth/oauth_provider.py",
                "tests/auth/test_oauth_provider.py"
              ],
              "last_update": "2024-11-15T15:45:00Z"
            },
            "task-oauth-tests": {
              "status": "pending",
              "assignee": null,
              "dependencies_met": false
            }
          },
          "agents": {
            "engineering-fullstack-1": {
              "instance_id": "ef-1-abc123",
              "agent_type": "engineering-fullstack",
              "status": "busy",
              "current_task": "task-oauth-provider",
              "spawned_at": "2024-11-15T14:34:00Z",
              "resource_usage": {
                "tokens": 15420,
                "memory_mb": 256
              }
            }
          },
          "sprint_metrics": {
            "tasks_completed": 0,
            "tasks_in_progress": 1,
            "tasks_pending": 1,
            "velocity": 0,
            "time_elapsed_hours": 1.25,
            "estimated_completion": "2024-11-17T18:00:00Z"
          }
        },
        "communication": {
          "messages": [...],
          "handoffs": [...],
          "events": [...]
        }
      }
    },
    "session-def456": {
      "session_info": {
        "id": "session-def456",
        "created_at": "2024-11-15T09:00:00Z",
        "mode": "development",
        "user": "other-dev@example.com"
      },
      "active_work": {
        "current_epic": "epic-performance-opt",
        "current_sprint": "sprint-2024-w44",
        "execution_state": {
          "// Different sprint, different work": "..."
        }
      }
    }
  }
}
```

## Key Design Patterns

### 1. Reference Pattern

Active work references planned work by ID, never duplicates it:

```python
# Session state references shared configuration
def start_sprint(session_id: str, sprint_id: str):
    # Get sprint definition from shared state
    sprint_def = state.get(f"shared.project_definitions.sprints.{sprint_id}")
    
    if not sprint_def:
        raise ValueError(f"Sprint {sprint_id} not found in planned work")
    
    # Set active sprint reference in session
    state.set(f"sessions.{session_id}.active_work.current_sprint", sprint_id)
    
    # Initialize execution state for tasks
    for task_id, task_def in sprint_def["planned_tasks"].items():
        state.set(f"sessions.{session_id}.active_work.execution_state.tasks.{task_id}", {
            "status": "pending",
            "assignee": None,
            "started_at": None,
            "actual_effort": 0,
            "progress_percentage": 0
        })
```

### 2. Progress Tracking Pattern

Progress is tracked in session state, separate from plans:

```python
def update_task_progress(session_id: str, task_id: str, progress: dict):
    # Update session-specific progress
    task_path = f"sessions.{session_id}.active_work.execution_state.tasks.{task_id}"
    
    current_state = state.get(task_path)
    current_state.update(progress)
    current_state["last_update"] = datetime.now().isoformat()
    
    state.set(task_path, current_state)
    
    # Planned work remains unchanged
    # Only execution state is modified
```

### 3. Multi-Session Coordination Pattern

Multiple sessions can work on different sprints simultaneously:

```python
def get_active_sessions_summary():
    sessions = state.get("sessions", {})
    summary = []
    
    for session_id, session_data in sessions.items():
        active_work = session_data.get("active_work", {})
        summary.append({
            "session_id": session_id,
            "current_epic": active_work.get("current_epic"),
            "current_sprint": active_work.get("current_sprint"),
            "active_tasks": len([
                t for t in active_work.get("execution_state", {}).get("tasks", {}).values()
                if t["status"] == "in_progress"
            ]),
            "session_status": session_data["session_info"].get("status", "unknown")
        })
    
    return summary
```

## State Lifecycle Examples

### Example 1: Starting a New Sprint

```python
# Leadership mode creates the sprint plan
def plan_sprint(sprint_definition):
    # This updates SHARED state
    sprint_id = sprint_definition["id"]
    state.set(f"shared.project_definitions.sprints.{sprint_id}", sprint_definition)
    emit_event("sprint_planned", {"sprint_id": sprint_id})

# Development mode activates the sprint in a session
def activate_sprint_in_session(session_id, sprint_id):
    # This updates SESSION state only
    state.set(f"sessions.{session_id}.active_work.current_sprint", sprint_id)
    
    # Copy task structure (not data) for tracking
    sprint_def = state.get(f"shared.project_definitions.sprints.{sprint_id}")
    for task_id in sprint_def["planned_tasks"]:
        initialize_task_tracking(session_id, task_id)
```

### Example 2: Task Assignment and Execution

```python
def assign_task(session_id: str, task_id: str, agent_id: str):
    # Check task exists in planned work
    sprint_id = state.get(f"sessions.{session_id}.active_work.current_sprint")
    task_def = state.get(f"shared.project_definitions.sprints.{sprint_id}.planned_tasks.{task_id}")
    
    if not task_def:
        raise ValueError(f"Task {task_id} not in sprint plan")
    
    # Update session execution state
    state.set(f"sessions.{session_id}.active_work.execution_state.tasks.{task_id}", {
        "status": "assigned",
        "assignee": agent_id,
        "started_at": datetime.now().isoformat(),
        "planned_effort": task_def["estimated_effort"],
        "actual_effort": 0
    })
    
    # Spawn agent in session context
    spawn_agent_for_task(session_id, agent_id, task_id)
```

### Example 3: Session Handoff

```python
def prepare_session_handoff(from_session_id: str, to_session_id: str):
    """
    Prepare handoff from one session to another
    """
    from_state = state.get(f"sessions.{from_session_id}.active_work")
    
    handoff_package = {
        "from_session": from_session_id,
        "to_session": to_session_id,
        "timestamp": datetime.now().isoformat(),
        "current_epic": from_state["current_epic"],
        "current_sprint": from_state["current_sprint"],
        "work_completed": [],
        "work_in_progress": [],
        "work_pending": [],
        "recommendations": []
    }
    
    # Categorize tasks by status
    for task_id, task_state in from_state["execution_state"]["tasks"].items():
        task_summary = {
            "task_id": task_id,
            "status": task_state["status"],
            "progress": task_state.get("progress_percentage", 0),
            "artifacts": task_state.get("artifacts", [])
        }
        
        if task_state["status"] == "completed":
            handoff_package["work_completed"].append(task_summary)
        elif task_state["status"] in ["in_progress", "assigned"]:
            handoff_package["work_in_progress"].append(task_summary)
        else:
            handoff_package["work_pending"].append(task_summary)
    
    # Store handoff for new session
    state.set(f"sessions.{to_session_id}.handoff_received", handoff_package)
    
    return handoff_package
```

## Query Patterns

### Finding Available Work

```python
# Query planned work that hasn't been started in any session
def find_available_sprints():
    all_sprints = state.get("shared.project_definitions.sprints", {})
    active_sprints = set()
    
    # Check all sessions for active sprints
    for session_id in state.get("sessions", {}).keys():
        current_sprint = state.get(f"sessions.{session_id}.active_work.current_sprint")
        if current_sprint:
            active_sprints.add(current_sprint)
    
    # Return sprints not currently active
    available = {
        sprint_id: sprint_def 
        for sprint_id, sprint_def in all_sprints.items()
        if sprint_id not in active_sprints
    }
    
    return available
```

### Aggregating Progress Across Sessions

```python
def get_epic_progress(epic_id: str):
    """
    Aggregate progress on an epic across all sessions
    """
    epic_def = state.get(f"shared.project_definitions.epics.{epic_id}")
    if not epic_def:
        return None
    
    progress = {
        "epic_id": epic_id,
        "total_sprints": len(epic_def.get("sprints", [])),
        "sprints_completed": 0,
        "sprints_in_progress": 0,
        "overall_progress": 0,
        "sessions_working": []
    }
    
    # Check progress in each session
    for session_id, session_data in state.get("sessions", {}).items():
        active_work = session_data.get("active_work", {})
        
        if active_work.get("current_epic") == epic_id:
            progress["sessions_working"].append({
                "session_id": session_id,
                "current_sprint": active_work.get("current_sprint"),
                "tasks_completed": len([
                    t for t in active_work.get("execution_state", {}).get("tasks", {}).values()
                    if t["status"] == "completed"
                ])
            })
    
    return progress
```

## Migration Path

### From V1 (Mixed State) to V2 (Separated State)

```python
def migrate_v1_to_v2(v1_state: dict) -> dict:
    """
    Migrate from v1 mixed state to v2 separated state
    """
    v2_state = {
        "shared": {
            "project_definitions": {
                "epics": {},
                "sprints": {},
                "team_configurations": {}
            }
        },
        "sessions": {}
    }
    
    # Extract planned work to shared state
    if "execution" in v1_state and "workflows" in v1_state["execution"]:
        # Move epic definitions
        for epic_id, epic_data in v1_state["execution"]["workflows"].get("epics", {}).items():
            # Separate definition from execution state
            epic_def = {
                "id": epic_id,
                "title": epic_data.get("title"),
                "description": epic_data.get("description"),
                "features": epic_data.get("features", []),
                "requirements": epic_data.get("requirements", {}),
                "success_criteria": epic_data.get("success_criteria", [])
            }
            v2_state["shared"]["project_definitions"]["epics"][epic_id] = epic_def
    
    # Extract team configurations
    if "organization" in v1_state and "teams" in v1_state["organization"]:
        v2_state["shared"]["project_definitions"]["team_configurations"] = v1_state["organization"]["teams"]
    
    # Create session for current execution state
    session_id = v1_state.get("session", {}).get("id", str(uuid.uuid4()))
    v2_state["sessions"][session_id] = {
        "session_info": v1_state.get("session", {}),
        "active_work": {
            "execution_state": {
                "tasks": v1_state.get("execution", {}).get("tasks", {}),
                "agents": v1_state.get("execution", {}).get("agents", {})
            }
        }
    }
    
    return v2_state
```

## Benefits of Separation

### 1. Session Independence
- Multiple developers can work on different sprints
- No conflicts between concurrent sessions
- Clean isolation of runtime state

### 2. Shared Planning
- Single source of truth for project plans
- Consistent reference across all sessions
- Version-controlled project definitions

### 3. Clear Responsibilities
- Leadership mode manages shared plans
- Development mode executes against plans
- Configuration mode updates team structures

### 4. Improved Recovery
- Session crashes don't affect plans
- Easy to restart work from shared definitions
- Clear handoff points between sessions

### 5. Better Observability
- Track planned vs actual across sessions
- Aggregate metrics from multiple executions
- Clear audit trail of who did what when

## Implementation Guidelines

### State Access Patterns

```python
class StateAccessor:
    """
    Helper class to enforce correct state access patterns
    """
    def __init__(self, session_id: str):
        self.session_id = session_id
    
    def get_plan(self, path: str) -> Any:
        """Read from shared planned work"""
        return state.get(f"shared.project_definitions.{path}")
    
    def get_active(self, path: str) -> Any:
        """Read from session active work"""
        return state.get(f"sessions.{self.session_id}.active_work.{path}")
    
    def set_active(self, path: str, value: Any) -> None:
        """Update session active work only"""
        state.set(f"sessions.{self.session_id}.active_work.{path}", value)
    
    def update_plan(self, path: str, value: Any) -> None:
        """Update shared plans (requires permission)"""
        if not self.has_planning_permission():
            raise PermissionError("Cannot update shared plans from this session")
        state.set(f"shared.project_definitions.{path}", value)
```

### Event Patterns

```python
# Events should clearly indicate scope
def emit_work_event(event_type: str, data: dict, scope: str = "session"):
    event = {
        "type": event_type,
        "scope": scope,  # "shared" or "session"
        "session_id": current_session_id if scope == "session" else None,
        "timestamp": datetime.now().isoformat(),
        "data": data
    }
    
    if scope == "shared":
        # Shared events affect all sessions
        broadcast_to_all_sessions(event)
    else:
        # Session events are local
        emit_to_session(event)
```

## Conclusion

The separation of Planned Work (shared configuration) and Active Work (session runtime) is fundamental to the v2 orchestration system. This architecture enables:

1. **Multiple concurrent sessions** working on different parts of the project
2. **Clean separation** between planning and execution
3. **Independent failure domains** where session crashes don't affect plans
4. **Clear handoff mechanisms** between sessions
5. **Comprehensive audit trails** of actual work performed

This design ensures that the orchestration system can scale to support complex, multi-session development workflows while maintaining consistency and reliability.