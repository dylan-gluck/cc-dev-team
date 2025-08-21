# V2 Orchestration: JSON-Based State Management API (Revised)

## Overview

This document presents a simplified inter-session communication architecture using JSON files for state persistence and UV scripts for state operations. This approach eliminates the need for WebSocket servers, Redis, or other external dependencies while maintaining robust state management capabilities.

## 1. Architecture Overview

### 1.1 Core Principles

**Simplicity First**
- JSON files for all state persistence
- UV scripts with parameters for state operations
- File-based message passing when coordination is needed
- No external dependencies (no Redis, no WebSocket server)

**State Boundaries**
```
┌─────────────────────────────────────────────────────────┐
│                    SHARED STATE                          │
│  (Cross-session: configurations, tools, epics, sprints)  │
├─────────────────────────────────────────────────────────┤
│  ~/.claude/orchestration/                                │
│  ├── config.json          # Global configuration         │
│  ├── tools.json           # Shared tool registry         │
│  ├── projects/                                           │
│  │   └── {project_id}/                                   │
│  │       ├── epics.json   # Project epics                │
│  │       ├── sprints.json # Sprint planning              │
│  │       └── team.json    # Team configuration           │
│  └── locks/              # File-based locking            │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                   SESSION STATE                          │
│    (Isolated: messages, events, hooks, active tasks)     │
├─────────────────────────────────────────────────────────┤
│  ~/.claude/sessions/{session_id}/                        │
│  ├── state.json          # Session runtime state         │
│  ├── messages.json       # Message history               │
│  ├── events.json         # Event log                     │
│  ├── hooks.json          # Active hooks                  │
│  └── tasks.json          # Active task queue             │
└─────────────────────────────────────────────────────────┘
```

### 1.2 State Categories

**Shared State (Cross-Session)**
- Global configurations
- Tool registrations
- Project epics and sprints
- Team structure
- Shared resources

**Session State (Isolated)**
- Runtime messages
- Event streams
- Active hooks
- Task execution state
- Session-specific context

### 1.3 Communication Patterns

```
Session A                     Shared State                    Session B
    │                              │                              │
    ├──── Read Config ────────────▶│                              │
    │                              │◀───── Read Config ───────────┤
    │                              │                              │
    ├──── Update Epic ────────────▶│                              │
    │                              │──── File Watch Trigger ─────▶│
    │                              │                              │
    └──── Write Message ──────────▶│──── Poll Messages ──────────▶│
                                   │                              │
```

## 2. JSON State Schemas

### 2.1 Shared Configuration State

**`~/.claude/orchestration/config.json`**
```json
{
  "version": "2.0.0",
  "updated_at": "2025-01-21T10:00:00Z",
  "global": {
    "default_project": "myapp",
    "max_parallel_agents": 5,
    "session_timeout": 3600,
    "state_sync_interval": 5000
  },
  "features": {
    "enable_orchestration": true,
    "enable_state_sharing": true,
    "enable_message_passing": false,
    "enable_auto_recovery": true
  },
  "paths": {
    "shared_state": "~/.claude/orchestration",
    "session_state": "~/.claude/sessions",
    "scripts": "~/.claude/scripts",
    "locks": "~/.claude/orchestration/locks"
  }
}
```

**`~/.claude/orchestration/tools.json`**
```json
{
  "version": "1.0.0",
  "tools": {
    "engineering-fullstack": {
      "id": "engineering-fullstack",
      "name": "Full Stack Developer",
      "capabilities": ["frontend", "backend", "database"],
      "max_instances": 2,
      "priority": "high",
      "config": {
        "languages": ["javascript", "typescript", "python"],
        "frameworks": ["react", "nextjs", "fastapi"]
      }
    },
    "qa-e2e": {
      "id": "qa-e2e",
      "name": "E2E Test Engineer",
      "capabilities": ["testing", "automation"],
      "max_instances": 1,
      "priority": "normal"
    }
  }
}
```

### 2.2 Project Planning State

**`~/.claude/orchestration/projects/{project_id}/epics.json`**
```json
{
  "version": "1.0.0",
  "project_id": "myapp",
  "updated_at": "2025-01-21T10:00:00Z",
  "updated_by": "session-abc123",
  "epics": [
    {
      "id": "epic-001",
      "title": "User Authentication System",
      "status": "in_progress",
      "priority": "high",
      "created_at": "2025-01-20T10:00:00Z",
      "stories": [
        {
          "id": "story-001",
          "title": "Implement JWT authentication",
          "status": "completed",
          "assigned_to": "engineering-api",
          "points": 5
        },
        {
          "id": "story-002",
          "title": "Add OAuth2 providers",
          "status": "pending",
          "assigned_to": null,
          "points": 8
        }
      ]
    }
  ]
}
```

**`~/.claude/orchestration/projects/{project_id}/sprints.json`**
```json
{
  "version": "1.0.0",
  "project_id": "myapp",
  "current_sprint": "sprint-003",
  "sprints": [
    {
      "id": "sprint-003",
      "name": "Sprint 3 - Authentication",
      "status": "active",
      "start_date": "2025-01-15",
      "end_date": "2025-01-29",
      "velocity": 21,
      "stories": ["story-001", "story-002", "story-003"],
      "completed_points": 5,
      "total_points": 21
    }
  ]
}
```

### 2.3 Session Runtime State

**`~/.claude/sessions/{session_id}/state.json`**
```json
{
  "session_id": "session-abc123",
  "project_id": "myapp",
  "created_at": "2025-01-21T10:00:00Z",
  "last_heartbeat": "2025-01-21T10:05:00Z",
  "status": "active",
  "user": {
    "id": "user-001",
    "name": "Developer"
  },
  "context": {
    "working_directory": "/projects/myapp",
    "current_branch": "feature/auth",
    "active_epic": "epic-001",
    "active_story": "story-002"
  },
  "agents": [
    {
      "id": "agent-001",
      "type": "engineering-fullstack",
      "status": "idle",
      "started_at": "2025-01-21T10:00:00Z"
    }
  ]
}
```

**`~/.claude/sessions/{session_id}/tasks.json`**
```json
{
  "tasks": [
    {
      "id": "task-001",
      "type": "code_review",
      "status": "pending",
      "priority": "high",
      "created_at": "2025-01-21T10:00:00Z",
      "assigned_to": "engineering-lead",
      "payload": {
        "files": ["src/auth/jwt.ts", "src/auth/oauth.ts"],
        "pr_number": 42
      }
    }
  ]
}
```

## 3. UV Script API

### 3.1 State Query Operations

**`scripts/state-query.py`**
```python
#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.11"
# dependencies = ["typer", "rich", "pydantic"]
# ///

import typer
import json
from pathlib import Path
from typing import Optional, List, Dict, Any
from enum import Enum

app = typer.Typer()

class StateType(str, Enum):
    CONFIG = "config"
    TOOLS = "tools"
    EPICS = "epics"
    SPRINTS = "sprints"
    SESSION = "session"
    TASKS = "tasks"

@app.command()
def get(
    state_type: StateType,
    project_id: Optional[str] = None,
    session_id: Optional[str] = None,
    field: Optional[str] = None,
    format: str = "json"
):
    """Query state with optional field filtering"""
    state_path = resolve_state_path(state_type, project_id, session_id)
    
    if not state_path.exists():
        typer.echo(f"State not found: {state_path}", err=True)
        raise typer.Exit(1)
    
    with open(state_path) as f:
        data = json.load(f)
    
    # Apply field filter if specified
    if field:
        data = extract_field(data, field)
    
    # Output in requested format
    if format == "json":
        typer.echo(json.dumps(data, indent=2))
    elif format == "value":
        typer.echo(str(data))

@app.command()
def list(
    state_type: StateType,
    project_id: Optional[str] = None,
    filter_status: Optional[str] = None
):
    """List items from state with optional filtering"""
    state_path = resolve_state_path(state_type, project_id)
    
    with open(state_path) as f:
        data = json.load(f)
    
    # Apply status filter
    items = extract_list_items(data, state_type)
    if filter_status:
        items = [i for i in items if i.get("status") == filter_status]
    
    typer.echo(json.dumps(items, indent=2))

@app.command()
def watch(
    state_type: StateType,
    project_id: Optional[str] = None,
    interval: int = 5
):
    """Watch state file for changes"""
    import time
    state_path = resolve_state_path(state_type, project_id)
    last_mtime = 0
    
    while True:
        current_mtime = state_path.stat().st_mtime
        if current_mtime > last_mtime:
            with open(state_path) as f:
                data = json.load(f)
            typer.echo(f"State updated at {current_mtime}")
            typer.echo(json.dumps(data, indent=2))
            last_mtime = current_mtime
        time.sleep(interval)
```

### 3.2 State Update Operations

**`scripts/state-update.py`**
```python
#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.11"
# dependencies = ["typer", "filelock", "pydantic"]
# ///

import typer
import json
from pathlib import Path
from filelock import FileLock
from typing import Optional, Dict, Any
from datetime import datetime

app = typer.Typer()

@app.command()
def set(
    state_type: str,
    field: str,
    value: str,
    project_id: Optional[str] = None,
    session_id: Optional[str] = None
):
    """Set a field value in state with atomic locking"""
    state_path = resolve_state_path(state_type, project_id, session_id)
    lock_path = get_lock_path(state_path)
    
    with FileLock(lock_path, timeout=10):
        # Read current state
        with open(state_path) as f:
            data = json.load(f)
        
        # Update field
        set_nested_field(data, field, json.loads(value))
        data["updated_at"] = datetime.utcnow().isoformat()
        if session_id:
            data["updated_by"] = session_id
        
        # Write atomically
        write_atomic(state_path, data)
    
    typer.echo(f"Updated {field} in {state_type}")

@app.command()
def append(
    state_type: str,
    list_field: str,
    item: str,
    project_id: Optional[str] = None
):
    """Append item to a list field"""
    state_path = resolve_state_path(state_type, project_id)
    lock_path = get_lock_path(state_path)
    
    with FileLock(lock_path, timeout=10):
        with open(state_path) as f:
            data = json.load(f)
        
        # Get list and append
        target_list = get_nested_field(data, list_field)
        if not isinstance(target_list, list):
            typer.echo(f"Field {list_field} is not a list", err=True)
            raise typer.Exit(1)
        
        target_list.append(json.loads(item))
        data["updated_at"] = datetime.utcnow().isoformat()
        
        write_atomic(state_path, data)
    
    typer.echo(f"Appended to {list_field}")

@app.command()
def update_task(
    task_id: str,
    status: Optional[str] = None,
    assigned_to: Optional[str] = None,
    session_id: Optional[str] = None
):
    """Update task status with proper locking"""
    tasks_path = Path(f"~/.claude/sessions/{session_id}/tasks.json").expanduser()
    lock_path = get_lock_path(tasks_path)
    
    with FileLock(lock_path, timeout=10):
        with open(tasks_path) as f:
            data = json.load(f)
        
        # Find and update task
        for task in data["tasks"]:
            if task["id"] == task_id:
                if status:
                    task["status"] = status
                    task["updated_at"] = datetime.utcnow().isoformat()
                if assigned_to:
                    task["assigned_to"] = assigned_to
                break
        else:
            typer.echo(f"Task {task_id} not found", err=True)
            raise typer.Exit(1)
        
        write_atomic(tasks_path, data)
    
    typer.echo(f"Updated task {task_id}")

def write_atomic(path: Path, data: Dict[Any, Any]):
    """Write file atomically using temp file + rename"""
    import tempfile
    import os
    
    # Write to temp file in same directory
    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=path.stem,
        suffix=".tmp"
    )
    
    try:
        with os.fdopen(temp_fd, 'w') as f:
            json.dump(data, f, indent=2)
        
        # Atomic rename
        Path(temp_path).replace(path)
    except:
        Path(temp_path).unlink(missing_ok=True)
        raise

def get_lock_path(state_path: Path) -> Path:
    """Get lock file path for a state file"""
    locks_dir = Path("~/.claude/orchestration/locks").expanduser()
    locks_dir.mkdir(parents=True, exist_ok=True)
    
    # Use state file name as lock name
    lock_name = f"{state_path.stem}.lock"
    return locks_dir / lock_name
```

### 3.3 Session Coordination Scripts

**`scripts/session-coordinate.py`**
```python
#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.11"
# dependencies = ["typer", "rich"]
# ///

import typer
import json
from pathlib import Path
from typing import Optional, List
from datetime import datetime, timedelta

app = typer.Typer()

@app.command()
def heartbeat(session_id: str):
    """Update session heartbeat"""
    session_path = Path(f"~/.claude/sessions/{session_id}/state.json").expanduser()
    
    with open(session_path) as f:
        data = json.load(f)
    
    data["last_heartbeat"] = datetime.utcnow().isoformat()
    
    with open(session_path, 'w') as f:
        json.dump(data, f, indent=2)
    
    typer.echo(f"Heartbeat updated for {session_id}")

@app.command()
def list_active(project_id: Optional[str] = None, timeout_minutes: int = 5):
    """List active sessions"""
    sessions_dir = Path("~/.claude/sessions").expanduser()
    active_sessions = []
    
    timeout = datetime.utcnow() - timedelta(minutes=timeout_minutes)
    
    for session_dir in sessions_dir.iterdir():
        if not session_dir.is_dir():
            continue
            
        state_file = session_dir / "state.json"
        if not state_file.exists():
            continue
        
        with open(state_file) as f:
            state = json.load(f)
        
        # Check if session is active
        last_heartbeat = datetime.fromisoformat(state["last_heartbeat"])
        if last_heartbeat > timeout:
            if not project_id or state.get("project_id") == project_id:
                active_sessions.append({
                    "session_id": state["session_id"],
                    "project_id": state.get("project_id"),
                    "status": state["status"],
                    "last_heartbeat": state["last_heartbeat"]
                })
    
    typer.echo(json.dumps(active_sessions, indent=2))

@app.command()
def send_message(
    from_session: str,
    to_session: str,
    message_type: str,
    payload: str
):
    """Send message between sessions via file"""
    messages_dir = Path("~/.claude/orchestration/messages").expanduser()
    messages_dir.mkdir(parents=True, exist_ok=True)
    
    message = {
        "id": f"msg-{datetime.utcnow().timestamp()}",
        "from": from_session,
        "to": to_session,
        "type": message_type,
        "payload": json.loads(payload),
        "timestamp": datetime.utcnow().isoformat(),
        "read": False
    }
    
    # Write to recipient's inbox
    inbox_dir = messages_dir / to_session / "inbox"
    inbox_dir.mkdir(parents=True, exist_ok=True)
    
    msg_file = inbox_dir / f"{message['id']}.json"
    with open(msg_file, 'w') as f:
        json.dump(message, f, indent=2)
    
    typer.echo(f"Message sent to {to_session}")

@app.command()
def poll_messages(session_id: str, mark_read: bool = True):
    """Poll messages for a session"""
    inbox_dir = Path(f"~/.claude/orchestration/messages/{session_id}/inbox").expanduser()
    
    if not inbox_dir.exists():
        typer.echo("[]")
        return
    
    messages = []
    for msg_file in inbox_dir.glob("*.json"):
        with open(msg_file) as f:
            message = json.load(f)
        
        if not message["read"]:
            messages.append(message)
            
            if mark_read:
                message["read"] = True
                with open(msg_file, 'w') as f:
                    json.dump(message, f, indent=2)
    
    typer.echo(json.dumps(messages, indent=2))
```

## 4. API Usage Patterns

### 4.1 Reading Shared State

```bash
# Get global configuration
uv run scripts/state-query.py get config

# Get specific field from config
uv run scripts/state-query.py get config --field "features.enable_orchestration"

# List all tools
uv run scripts/state-query.py get tools

# Get project epics
uv run scripts/state-query.py get epics --project-id myapp

# List active sprints
uv run scripts/state-query.py list sprints --project-id myapp --filter-status active

# Watch for epic changes
uv run scripts/state-query.py watch epics --project-id myapp --interval 5
```

### 4.2 Updating Shared State

```bash
# Update epic status
uv run scripts/state-update.py set epics "epics[0].status" '"completed"' --project-id myapp

# Add new story to epic
uv run scripts/state-update.py append epics "epics[0].stories" \
  '{"id": "story-003", "title": "Add password reset", "status": "pending", "points": 3}' \
  --project-id myapp

# Update sprint velocity
uv run scripts/state-update.py set sprints "sprints[0].velocity" "25" --project-id myapp
```

### 4.3 Session Operations

```bash
# Update session heartbeat
uv run scripts/session-coordinate.py heartbeat session-abc123

# List active sessions for project
uv run scripts/session-coordinate.py list-active --project-id myapp

# Update task status
uv run scripts/state-update.py update-task task-001 --status completed --session-id session-abc123

# Send coordination message
uv run scripts/session-coordinate.py send-message session-abc123 session-xyz789 \
  "handoff_request" '{"task_id": "task-001", "context": "Completed auth implementation"}'

# Poll for messages
uv run scripts/session-coordinate.py poll-messages session-xyz789
```

### 4.4 Hook Integration

**`.claude/hooks/on-epic-update.sh`**
```bash
#!/bin/bash
# Hook triggered when epics are updated

PROJECT_ID="${1:-myapp}"
SESSION_ID="${2:-$CLAUDE_SESSION_ID}"

# Check if any stories are ready for development
PENDING_STORIES=$(uv run scripts/state-query.py list epics \
  --project-id "$PROJECT_ID" \
  --filter-status pending \
  --format json | jq -r '.[] | select(.assigned_to == null)')

if [ -n "$PENDING_STORIES" ]; then
  echo "Found unassigned stories. Creating tasks..."
  
  # Create tasks for pending stories
  echo "$PENDING_STORIES" | jq -c '.' | while read -r story; do
    STORY_ID=$(echo "$story" | jq -r '.id')
    TITLE=$(echo "$story" | jq -r '.title')
    
    # Create task in session
    uv run scripts/state-update.py append tasks "tasks" \
      "{\"id\": \"task-$STORY_ID\", \"type\": \"implement_story\", \"story_id\": \"$STORY_ID\", \"title\": \"$TITLE\", \"status\": \"pending\"}" \
      --session-id "$SESSION_ID"
  done
fi
```

## 5. Locking and Safety

### 5.1 File-based Locking

All state updates use `filelock` for safe concurrent access:

```python
from filelock import FileLock

def safe_update_state(state_path: Path, updates: dict):
    lock_path = state_path.with_suffix('.lock')
    
    # Acquire lock with timeout
    with FileLock(lock_path, timeout=10):
        # Read current state
        with open(state_path) as f:
            data = json.load(f)
        
        # Apply updates
        data.update(updates)
        data["updated_at"] = datetime.utcnow().isoformat()
        
        # Write atomically
        temp_path = state_path.with_suffix('.tmp')
        with open(temp_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        # Atomic rename
        temp_path.replace(state_path)
```

### 5.2 Atomic Operations

All writes use temp file + atomic rename pattern:

```python
def write_atomic(path: Path, data: dict):
    """Write file atomically to prevent partial writes"""
    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=path.stem,
        suffix='.tmp'
    )
    
    try:
        # Write to temp file
        with os.fdopen(temp_fd, 'w') as f:
            json.dump(data, f, indent=2)
        
        # Atomic rename (POSIX compliant)
        Path(temp_path).replace(path)
    except:
        # Clean up on error
        Path(temp_path).unlink(missing_ok=True)
        raise
```

### 5.3 Version Control

States include version numbers for conflict detection:

```python
def update_with_version_check(state_path: Path, updates: dict, expected_version: int):
    with FileLock(get_lock_path(state_path)):
        with open(state_path) as f:
            data = json.load(f)
        
        # Check version
        if data.get("version") != expected_version:
            raise VersionConflictError(
                f"Expected version {expected_version}, found {data.get('version')}"
            )
        
        # Apply updates and increment version
        data.update(updates)
        data["version"] = expected_version + 1
        data["updated_at"] = datetime.utcnow().isoformat()
        
        write_atomic(state_path, data)
```

## 6. Message Passing (Optional)

For cases requiring inter-session coordination:

### 6.1 File-based Message Queue

```
~/.claude/orchestration/messages/
├── {session_id}/
│   ├── inbox/
│   │   ├── msg-12345.json
│   │   └── msg-12346.json
│   ├── outbox/
│   └── processed/
```

### 6.2 Message Format

```json
{
  "id": "msg-12345",
  "from": "session-abc123",
  "to": "session-xyz789",
  "type": "task_handoff",
  "priority": "normal",
  "payload": {
    "task_id": "task-001",
    "context": "Authentication implementation complete"
  },
  "timestamp": "2025-01-21T10:00:00Z",
  "ttl": 3600,
  "read": false,
  "processed": false
}
```

### 6.3 Polling Pattern

Sessions can poll for messages when needed:

```bash
# Poll messages every 5 seconds
while true; do
  MESSAGES=$(uv run scripts/session-coordinate.py poll-messages "$SESSION_ID")
  
  if [ -n "$MESSAGES" ]; then
    echo "$MESSAGES" | jq -c '.[]' | while read -r msg; do
      MESSAGE_TYPE=$(echo "$msg" | jq -r '.type')
      
      case "$MESSAGE_TYPE" in
        "task_handoff")
          handle_task_handoff "$msg"
          ;;
        "emergency_stop")
          handle_emergency_stop "$msg"
          ;;
      esac
    done
  fi
  
  sleep 5
done
```

## 7. Implementation Benefits

### 7.1 Simplicity
- No external dependencies to install or manage
- Pure JSON files are human-readable and debuggable
- UV scripts are self-contained with inline dependencies
- File-based approach works on all platforms

### 7.2 Reliability
- Atomic file operations prevent corruption
- File locks ensure safe concurrent access
- Version tracking enables conflict detection
- Persistent state survives session crashes

### 7.3 Performance
- Local file access is fast for reasonable data sizes
- No network overhead or latency
- Efficient JSON parsing with modern libraries
- Optional caching in scripts for repeated reads

### 7.4 Flexibility
- Easy to extend with new state types
- Scripts can be customized per project
- Hook integration for event-driven updates
- Optional message passing when needed

## 8. Migration Path

### 8.1 From WebSocket to File-based

1. **Phase 1: Parallel Operation**
   - Run file-based system alongside WebSocket
   - Mirror state updates to both systems
   - Validate consistency

2. **Phase 2: Primary Switch**
   - Make file-based system primary
   - WebSocket becomes read-only backup
   - Monitor for issues

3. **Phase 3: Full Migration**
   - Remove WebSocket dependencies
   - Clean up legacy code
   - Document new patterns

### 8.2 Backwards Compatibility

Scripts can provide compatibility layer:

```python
@app.command()
def legacy_websocket_bridge():
    """Bridge legacy WebSocket calls to file-based system"""
    # Monitor WebSocket-style calls
    # Translate to file operations
    # Maintain compatibility during transition
```

## 9. Security Considerations

### 9.1 File Permissions
- Shared state: Read-only for most operations
- Session state: User-owned, restricted access
- Lock files: Temporary, auto-cleaned
- Message files: Restricted to sender/receiver

### 9.2 Data Validation
- JSON schema validation on all inputs
- Type checking in UV scripts
- Sanitization of user-provided values
- Audit logging of state changes

### 9.3 Session Isolation
- Each session has isolated runtime state
- No direct session-to-session file access
- Messages go through controlled channels
- Shared state requires explicit coordination

## 10. Summary

This revised architecture provides a robust, simple, and dependency-free approach to inter-session state management:

- **JSON files** for all persistence (no databases)
- **UV scripts** for state operations (no servers)
- **File locks** for safety (no complex coordination)
- **Clear boundaries** between shared and session state
- **Optional messaging** when coordination is needed

The system maintains the collaboration benefits of the original design while dramatically reducing complexity and external dependencies. This makes it easier to deploy, debug, and maintain across different development environments.