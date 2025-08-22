# V2 Orchestration API Reference

Complete technical reference for the V2 orchestration system UV scripts, SudoLang output styles, and state management APIs.

## Table of Contents

- [UV Script APIs](#uv-script-apis)
- [SudoLang Output Style Reference](#sudolang-output-style-reference) 
- [Hook Specifications](#hook-specifications)
- [State Schema Documentation](#state-schema-documentation)
- [Integration APIs](#integration-apis)

## UV Script APIs

### state_manager.py

**Purpose**: Atomic state operations with JSONPath query support and file locking for concurrent access to session state files.

**Dependencies**: `jsonpath-ng>=1.6`, `filelock>=3.12`, `click>=8.1`, `rich>=13.0`

#### CLI Commands

##### get
```bash
uv run .claude/scripts/state_manager.py get SESSION_ID PATH [--json-output]
```

**Parameters:**
- `SESSION_ID`: Unique session identifier
- `PATH`: JSONPath (starts with `$`) or dot notation path
- `--json-output`: Output as JSON instead of formatted

**Examples:**
```bash
# Get session info
uv run .claude/scripts/state_manager.py get session-123 "session.mode"

# JSONPath query for blocked tasks
uv run .claude/scripts/state_manager.py get session-123 "$.sprint.tasks[?(@.status=='blocked')]"

# Get all agent assignments
uv run .claude/scripts/state_manager.py get session-123 "execution.agents"
```

**Return Values:**
- Single value for unique paths
- Array for multiple matches
- `null` for non-existent paths

##### set
```bash
uv run .claude/scripts/state_manager.py set SESSION_ID PATH VALUE [--json-value]
```

**Parameters:**
- `SESSION_ID`: Unique session identifier  
- `PATH`: Dot notation path (creates nested structure as needed)
- `VALUE`: String value to set
- `--json-value`: Parse VALUE as JSON

**Examples:**
```bash
# Set task status
uv run .claude/scripts/state_manager.py set session-123 "sprint.tasks.TASK-456.status" "in_progress"

# Set complex JSON value
uv run .claude/scripts/state_manager.py set session-123 "sprint.config" \
  '{"velocity_target": 25, "capacity": 40}' --json-value
```

##### merge
```bash
uv run .claude/scripts/state_manager.py merge SESSION_ID PATH --data JSON_DATA
```

**Parameters:**
- `SESSION_ID`: Unique session identifier
- `PATH`: Target path for merge operation
- `--data`: JSON object to deep merge

**Examples:**
```bash
# Merge task updates
uv run .claude/scripts/state_manager.py merge session-123 "sprint.tasks.TASK-123" \
  --data '{"assignee": "engineering-lead", "points": 8, "updated_at": "2024-01-15T10:30:00Z"}'

# Merge sprint metrics
uv run .claude/scripts/state_manager.py merge session-123 "sprint.metrics" \
  --data '{"velocity": 23, "burndown": {"remaining": 67}}'
```

##### delete
```bash
uv run .claude/scripts/state_manager.py delete SESSION_ID PATH
```

**Parameters:**
- `SESSION_ID`: Unique session identifier
- `PATH`: Dot notation path to delete

**Examples:**
```bash
# Remove blocker from task
uv run .claude/scripts/state_manager.py delete session-123 "sprint.tasks.TASK-456.blocker"

# Clear expired data
uv run .claude/scripts/state_manager.py delete session-123 "observability.events"
```

##### list-sessions
```bash
uv run .claude/scripts/state_manager.py list-sessions [--json-output]
```

**Returns:** Array of session metadata
```json
[
  {
    "id": "session-123",
    "mode": "development", 
    "status": "active",
    "created_at": "2024-01-15T08:00:00Z",
    "last_activity": "2024-01-15T10:30:00Z",
    "expiry": "2024-01-16T08:00:00Z"
  }
]
```

##### cleanup-expired
```bash
uv run .claude/scripts/state_manager.py cleanup-expired [--dry-run]
```

**Parameters:**
- `--dry-run`: Show what would be removed without removing

**Returns:** List of removed session IDs

#### Python API

```python
from state_manager import StateManager

manager = StateManager()

# CRUD operations
value = manager.get(session_id, "sprint.tasks") 
success = manager.set(session_id, "task.status", "done")
success = manager.merge(session_id, "sprint", {"velocity": 25})
success = manager.delete(session_id, "task.blocker")

# Session management
sessions = manager.list_sessions()
removed = manager.cleanup_expired()
```

### session_manager.py

**Purpose**: Manages session lifecycle including creation, heartbeat, handoff, and recovery with different session modes.

**Dependencies**: `click>=8.1`, `rich>=13.0`, `filelock>=3.12`

#### Session Modes

```python
class SessionMode(str, Enum):
    DEVELOPMENT = "development"  # 24h expiry, daily coding work
    LEADERSHIP = "leadership"    # 48h expiry, planning and oversight
    SPRINT = "sprint"           # 168h expiry, sprint management
    CONFIG = "config"           # 1h expiry, system configuration
```

#### Session Status

```python
class SessionStatus(str, Enum):
    ACTIVE = "active"      # Session is running normally
    PAUSED = "paused"      # Session is paused but recoverable  
    COMPLETED = "completed" # Session finished successfully
    FAILED = "failed"      # Session terminated with error
```

#### CLI Commands

##### create
```bash
uv run .claude/scripts/session_manager.py create \
  [--mode MODE] [--project PROJECT] [--parent-session PARENT] \
  [--metadata JSON] [--json-output]
```

**Parameters:**
- `--mode`: Session mode (development|leadership|sprint|config)
- `--project`: Project identifier for grouping
- `--parent-session`: Parent session ID for inheritance
- `--metadata`: Additional metadata as JSON
- `--json-output`: Return session ID as JSON

**Examples:**
```bash
# Create development session
uv run .claude/scripts/session_manager.py create --mode development --project myapp

# Create sprint session with metadata
uv run .claude/scripts/session_manager.py create --mode sprint --project myapp \
  --metadata '{"sprint_id": "sprint-1", "team": "engineering"}'

# Create child session
uv run .claude/scripts/session_manager.py create --mode development \
  --parent-session parent-session-id --project myapp
```

**Return Value:**
```json
{
  "session_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
}
```

##### heartbeat
```bash
uv run .claude/scripts/session_manager.py heartbeat SESSION_ID [--json-output]
```

**Purpose**: Extends session expiry and updates last activity timestamp

**Examples:**
```bash
# Send heartbeat
uv run .claude/scripts/session_manager.py heartbeat session-123

# Automated heartbeat in scripts
SESSION_ID="session-123"
while true; do
  sleep 300  # 5 minutes
  uv run .claude/scripts/session_manager.py heartbeat $SESSION_ID
done
```

##### handoff
```bash
uv run .claude/scripts/session_manager.py handoff FROM_SESSION TO_SESSION \
  [--data JSON] [--json-output]
```

**Purpose**: Transfer context and mark completion of source session

**Parameters:**
- `FROM_SESSION`: Source session ID
- `TO_SESSION`: Target session ID (created if doesn't exist)
- `--data`: Handoff data as JSON

**Examples:**
```bash
# Hand off development work to testing
uv run .claude/scripts/session_manager.py handoff dev-session-123 test-session-456 \
  --data '{"completed_features": ["auth", "dashboard"], "pending": ["tests"]}'

# Hand off sprint planning to execution
uv run .claude/scripts/session_manager.py handoff planning-session execution-session \
  --data '{"sprint_goals": ["feature-a", "feature-b"], "capacity": 40}'
```

##### list
```bash
uv run .claude/scripts/session_manager.py list \
  [--active] [--project PROJECT] [--mode MODE] [--json-output]
```

**Filters:**
- `--active`: Show only active sessions
- `--project`: Filter by project name
- `--mode`: Filter by session mode

**Examples:**
```bash
# List all active sessions
uv run .claude/scripts/session_manager.py list --active

# List development sessions for project
uv run .claude/scripts/session_manager.py list --project myapp --mode development

# Get session data for processing
SESSIONS=$(uv run .claude/scripts/session_manager.py list --json-output)
echo $SESSIONS | jq '.[] | select(.project=="myapp")'
```

##### recover
```bash
uv run .claude/scripts/session_manager.py recover SESSION_ID [--json-output]
```

**Purpose**: Recover failed or paused session

**Examples:**
```bash
# Recover failed session
uv run .claude/scripts/session_manager.py recover session-123

# Batch recovery
uv run .claude/scripts/session_manager.py list --json-output | \
  jq -r '.[] | select(.status=="failed") | .id' | \
  xargs -I {} uv run .claude/scripts/session_manager.py recover {}
```

##### info
```bash
uv run .claude/scripts/session_manager.py info SESSION_ID [--json-output]
```

**Returns:** Detailed session information
```json
{
  "session": {
    "id": "session-123",
    "mode": "development",
    "project": "myapp",
    "status": "active",
    "created_at": "2024-01-15T08:00:00Z",
    "expiry": "2024-01-16T08:00:00Z"
  },
  "execution_summary": {
    "agent_count": 3,
    "task_count": 12,
    "workflow_count": 2
  },
  "metrics": {
    "start_time": "2024-01-15T08:00:00Z",
    "heartbeat_count": 5,
    "task_count": 12,
    "agent_count": 3
  },
  "recent_events": [
    {
      "timestamp": "2024-01-15T10:30:00Z",
      "type": "task_completed",
      "data": {"task_id": "TASK-123"}
    }
  ]
}
```

#### Python API

```python
from session_manager import SessionManager, SessionMode

manager = SessionManager()

# Create session
session_id = manager.create(
    mode=SessionMode.DEVELOPMENT,
    project="myapp",
    metadata={"team": "engineering"}
)

# Lifecycle management
success = manager.heartbeat(session_id)
success = manager.handoff(from_session, to_session, handoff_data)
success = manager.recover(session_id)

# Query sessions
sessions = manager.list(active_only=True, project="myapp")
info = manager.get_info(session_id)
```

### shared_state.py

**Purpose**: Manages project-level configuration, epics, sprints, and tool registry shared across multiple sessions.

**Dependencies**: `click>=8.1`, `rich>=13.0`, `filelock>=3.12`, `pydantic>=2.0`

#### Data Models

##### Epic Model
```python
class Epic(BaseModel):
    id: str
    title: str
    description: str = ""
    status: EpicStatus = EpicStatus.PLANNED  # planned, in_progress, completed, blocked, cancelled
    priority: int = Field(ge=1, le=5, default=3)
    created_at: str
    updated_at: str
    completed_at: Optional[str] = None
    tags: List[str] = []
    metadata: Dict[str, Any] = {}
```

##### Sprint Model
```python
class Sprint(BaseModel):
    id: str
    name: str
    epic_id: Optional[str] = None
    status: SprintStatus = SprintStatus.PLANNED  # planned, active, completed, cancelled
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    goals: List[str] = []
    tasks: List[str] = []
    created_at: str
    updated_at: str
    metadata: Dict[str, Any] = {}
```

##### Tool Model  
```python
class Tool(BaseModel):
    name: str
    type: ToolType  # agent, command, hook, workflow, library
    version: str = "1.0.0"
    description: str = ""
    path: Optional[str] = None
    dependencies: List[str] = []
    config: Dict[str, Any] = {}
    registered_at: str
    updated_at: str
```

#### CLI Commands

##### get-config / set-config
```bash
# Get project configuration
uv run .claude/scripts/shared_state.py get-config PROJECT_ID [--json-output]

# Set project configuration
uv run .claude/scripts/shared_state.py set-config PROJECT_ID --data JSON_DATA
```

**Configuration Schema:**
```json
{
  "project_id": "myapp",
  "created_at": "2024-01-15T08:00:00Z",
  "settings": {
    "default_sprint_length": 14,
    "velocity_target": 20,
    "team_capacity": 5
  },
  "team": {
    "leads": ["engineering-lead", "product-manager"],
    "members": ["engineering-fullstack", "engineering-ux", "qa-analyst"]
  },
  "environments": {
    "development": {"url": "dev.myapp.com"},
    "staging": {"url": "staging.myapp.com"},
    "production": {"url": "myapp.com"}
  },
  "metadata": {
    "repository": "github.com/myorg/myapp",
    "tech_stack": ["python", "react", "postgresql"]
  }
}
```

##### Epic Management
```bash
# Update epic
uv run .claude/scripts/shared_state.py update-epic PROJECT_ID EPIC_ID \
  [--status STATUS] [--title TITLE] [--description DESC] [--priority INT] [--data JSON]

# List epics
uv run .claude/scripts/shared_state.py list-epics PROJECT_ID \
  [--status STATUS] [--json-output]
```

**Examples:**
```bash
# Create new epic
uv run .claude/scripts/shared_state.py update-epic myapp user-auth \
  --title "User Authentication System" \
  --description "Complete OAuth2 authentication with social login" \
  --priority 1

# Update epic status
uv run .claude/scripts/shared_state.py update-epic myapp user-auth --status in_progress

# List active epics
uv run .claude/scripts/shared_state.py list-epics myapp --status in_progress
```

##### Sprint Management
```bash
# Create sprint
uv run .claude/scripts/shared_state.py create-sprint PROJECT_ID SPRINT_ID NAME \
  [--epic-id EPIC_ID] [--data JSON]

# List sprints
uv run .claude/scripts/shared_state.py list-sprints PROJECT_ID \
  [--status STATUS] [--epic-id EPIC_ID] [--json-output]
```

**Examples:**
```bash
# Create sprint for epic
uv run .claude/scripts/shared_state.py create-sprint myapp sprint-1 \
  "Authentication Sprint" --epic-id user-auth \
  --data '{
    "start_date": "2024-01-15",
    "end_date": "2024-01-29", 
    "goals": ["OAuth2 integration", "Social login", "User management"]
  }'

# List active sprints
uv run .claude/scripts/shared_state.py list-sprints myapp --status active
```

##### Tool Registry
```bash
# Register tool
uv run .claude/scripts/shared_state.py register-tool \
  --name NAME --type TYPE [--version VERSION] [--description DESC] \
  [--path PATH] [--dependencies JSON_ARRAY] [--config JSON]

# List tools
uv run .claude/scripts/shared_state.py list-tools [--type TYPE] [--json-output]

# Get tool info
uv run .claude/scripts/shared_state.py get-tool NAME [--json-output]
```

**Examples:**
```bash
# Register agent tool
uv run .claude/scripts/shared_state.py register-tool \
  --name "qa-automation" --type agent \
  --description "Automated testing and quality assurance" \
  --dependencies '["pytest", "selenium", "allure"]' \
  --config '{"test_timeout": 300, "parallel_tests": 4}'

# Register workflow
uv run .claude/scripts/shared_state.py register-tool \
  --name "ci-pipeline" --type workflow \
  --path ".github/workflows/ci.yml" \
  --description "Continuous integration pipeline"

# List all agent tools
uv run .claude/scripts/shared_state.py list-tools --type agent
```

#### Python API

```python
from shared_state import SharedStateManager, EpicStatus, SprintStatus, ToolType

manager = SharedStateManager()

# Configuration
config = manager.get_config("myapp")
success = manager.set_config("myapp", {"settings": {"velocity": 25}})

# Epic management
success = manager.update_epic("myapp", "epic-1", EpicStatus.IN_PROGRESS)
epics = manager.list_epics("myapp", status=EpicStatus.ACTIVE)

# Sprint management
success = manager.create_sprint("myapp", "sprint-1", "Sprint Name")
sprints = manager.list_sprints("myapp", status=SprintStatus.ACTIVE)

# Tool registry
success = manager.register_tool("tool-name", ToolType.AGENT)
tools = manager.list_tools()
tool = manager.get_tool("tool-name")
```

## SudoLang Output Style Reference

### Output Style Interface

All output styles implement this base interface:

```sudolang
interface OutputStyle {
  name: string
  description: string
  constraints: object
  layout: string
  commands: object
  stateIntegration: object
  processInput(input: string): void
  init(): void
}
```

### sprint_execution.md

**Purpose**: Kanban-style sprint board with task automation, velocity tracking, and blocker management

#### Interface Definition
```sudolang
interface SprintExecution {
  name = "sprint_execution"
  description = "Kanban-style sprint board with task automation, velocity tracking, and blocker management"
  
  constraints {
    Maintain Kanban board layout with swim lanes
    Auto-calculate velocity and burndown metrics
    Highlight blockers and at-risk items visually
    Support drag-drop simulation via commands
    Track WIP limits per column
    Show agent assignments clearly
    Update in real-time from state changes
    Preserve sprint history for retrospectives
  }
}
```

#### State Integration
```sudolang
stateIntegration = {
  fetch: "uv run .claude/scripts/state_manager.py get {SESSION_ID} sprint",
  update: "uv run .claude/scripts/state_manager.py set {SESSION_ID} sprint.{path} {value}",
  watch: "uv run .claude/scripts/state_manager.py watch {SESSION_ID} sprint.tasks",
  metrics: "uv run .claude/scripts/state_manager.py get {SESSION_ID} sprint.metrics",
  events: "uv run .claude/scripts/event_stream.py filter sprint {sprint_id}"
}
```

#### Commands
- `/move <task_id> <column>` - Move task between columns
- `/assign <task_id> @<agent>` - Assign task to agent  
- `/block <task_id> <reason>` - Mark task as blocked
- `/unblock <task_id>` - Remove blocker
- `/estimate <task_id> <points>` - Set story points
- `/autoassign` - Auto-assign tasks based on capacity
- `/metrics` - Show detailed sprint metrics
- `/burndown` - Display burndown chart
- `/forecast` - Project sprint completion
- `/retro` - Open retrospective view

#### Visual Layout
```
╭─── SPRINT BOARD: {sprint_name} ─────────────────────────────────────────╮
│ Day {current_day}/{total_days}  Velocity: {velocity}  Burndown: {trend} │
├──────────────────────────────────────────────────────────────────────────┤
│ BACKLOG (∞)        │ TODO ({todo_limit})  │ IN PROGRESS ({wip_limit}) │ REVIEW ({review_limit}) │ DONE (∞)      │
├────────────────────┼─────────────────────┼──────────────────────────┼────────────────────────┼───────────────┤
{swimlanes}
├──────────────────────────────────────────────────────────────────────────┤
│ BLOCKERS & RISKS                                                         │
│ 🔴 {blocker_1} - {blocker_description_1} (@{blocker_owner_1})          │
│ 🟡 {risk_1} - {risk_description_1} (@{risk_owner_1})                   │
╰──────────────────────────────────────────────────────────────────────────╯
```

### leadership_chat.md

**Purpose**: Executive dashboard with KPIs and strategic overview

#### Key Features
- High-level KPI tracking
- Strategic goal monitoring  
- Resource allocation overview
- Risk assessment dashboard
- Team performance metrics
- Budget and timeline tracking

#### Commands
- `/kpis` - Show key performance indicators
- `/goals` - Strategic goal tracking
- `/risks` - Risk assessment and mitigation
- `/resources` - Resource allocation overview
- `/budget` - Budget and cost tracking
- `/timeline` - Project timeline and milestones

### all-team_dashboard.md

**Purpose**: Multi-team coordination with resource allocation

#### Key Features
- Cross-team workload visualization
- Capacity planning and allocation
- Dependency tracking
- Communication channels
- Handoff management
- Performance comparison

#### Commands
- `/teams` - Team overview and status
- `/capacity` - Capacity planning
- `/dependencies` - Cross-team dependencies  
- `/handoffs` - Team handoff management
- `/performance` - Team performance comparison
- `/allocation` - Resource allocation optimization

### config_manager.md

**Purpose**: System configuration and settings management

#### Key Features
- Configuration validation
- Settings management
- Tool registry
- System health monitoring
- Backup and restore
- Environment management

#### Commands
- `/validate` - Validate configurations
- `/backup` - Create configuration backup
- `/restore` - Restore from backup
- `/tools` - Tool registry management
- `/health` - System health check
- `/environments` - Environment management

## Hook Specifications

### Hook Interface

All hooks receive JSON input via stdin and communicate via exit codes and stdout/stderr:

```typescript
interface HookInput {
  hookType: string
  sessionId: string
  timestamp: string
  data: {
    // Hook-specific data
    toolName?: string
    toolInput?: any
    toolOutput?: any
    userPrompt?: string
    notification?: string
  }
}

interface HookOutput {
  continue?: boolean           // Whether to continue execution
  stopReason?: string         // Reason when continue=false
  suppressOutput?: boolean    // Hide stdout from transcript
  decision?: "approve" | "block" | undefined  // Hook-specific decision
  reason?: string            // Explanation for decision
}
```

### Exit Code Behavior

| Exit Code | Behavior | Description |
|-----------|----------|-------------|
| 0 | Success | Hook executed successfully |
| 2 | Blocking Error | Critical error that blocks execution |
| Other | Non-blocking Error | Error shown to user, execution continues |

### Hook-Specific Integrations

#### UserPromptSubmit Hook
```python
# Integration with session management
session_id = get_current_session()
uv run .claude/scripts/session_manager.py heartbeat {session_id}

# State tracking
uv run .claude/scripts/state_manager.py set {session_id} "last_prompt" "{prompt}"
```

#### PostToolUse Hook  
```python
# Log tool usage
event = {
    "type": "tool_used",
    "tool": tool_name,
    "timestamp": timestamp,
    "success": success
}
uv run .claude/scripts/event_stream.py emit tool.usage {event}

# Update metrics
uv run .claude/scripts/state_manager.py increment {session_id} "metrics.tool_usage.{tool_name}" 1
```

#### Stop Hook
```python
# Generate completion summary
summary = generate_completion_summary()
uv run .claude/scripts/state_manager.py set {session_id} "completion_summary" "{summary}"

# Trigger TTS if enabled
uv run .claude/hooks/utils/tts/elevenlabs_tts.py "{completion_message}"
```

## State Schema Documentation

### Session State Schema

```json
{
  "session": {
    "id": "string",
    "mode": "development|leadership|sprint|config", 
    "project": "string|null",
    "parent_session": "string|null",
    "created_at": "ISO8601",
    "created_by": "string",
    "metadata": {},
    "lifecycle": {
      "status": "active|paused|completed|failed",
      "last_activity": "ISO8601",
      "heartbeat": "ISO8601", 
      "expiry": "ISO8601"
    }
  },
  "execution": {
    "agents": {
      "agent_id": {
        "name": "string",
        "type": "string", 
        "capacity": "number",
        "current_tasks": ["string"],
        "status": "active|busy|idle",
        "last_active": "ISO8601"
      }
    },
    "tasks": {
      "task_id": {
        "id": "string",
        "title": "string",
        "description": "string",
        "status": "backlog|todo|in_progress|review|done|blocked",
        "assignee": "string|null",
        "points": "number",
        "priority": "number",
        "created_at": "ISO8601",
        "updated_at": "ISO8601",
        "blocker": {
          "id": "string",
          "reason": "string", 
          "reported_by": "string",
          "timestamp": "ISO8601",
          "severity": "low|medium|high|critical"
        }
      }
    },
    "workflows": {
      "workflow_id": {
        "name": "string",
        "type": "string",
        "status": "pending|running|completed|failed",
        "steps": [],
        "current_step": "number",
        "created_at": "ISO8601"
      }
    },
    "context": {
      "project": "string",
      "parent_session": "string|null",
      "inherited_context": {}
    }
  },
  "observability": {
    "metrics": {
      "start_time": "ISO8601",
      "heartbeat_count": "number",
      "task_count": "number", 
      "agent_count": "number",
      "velocity": "number",
      "throughput": "number",
      "cycle_time": "number",
      "lead_time": "number"
    },
    "events": [
      {
        "timestamp": "ISO8601",
        "type": "string",
        "data": {}
      }
    ]
  }
}
```

### Shared State Schema

#### Project Configuration
```json
{
  "project_id": "string",
  "created_at": "ISO8601",
  "updated_at": "ISO8601",
  "settings": {
    "default_sprint_length": "number",
    "velocity_target": "number", 
    "team_capacity": "number",
    "wip_limits": {
      "todo": "number",
      "in_progress": "number",
      "review": "number"
    }
  },
  "team": {
    "leads": ["string"],
    "members": ["string"],
    "capacity_by_role": {}
  },
  "environments": {
    "development": {"url": "string"},
    "staging": {"url": "string"},
    "production": {"url": "string"}
  },
  "metadata": {}
}
```

#### Epic Schema
```json
{
  "id": "string",
  "title": "string", 
  "description": "string",
  "status": "planned|in_progress|completed|blocked|cancelled",
  "priority": "number (1-5)",
  "created_at": "ISO8601",
  "updated_at": "ISO8601", 
  "completed_at": "ISO8601|null",
  "tags": ["string"],
  "metadata": {}
}
```

#### Sprint Schema
```json
{
  "id": "string",
  "name": "string",
  "epic_id": "string|null",
  "status": "planned|active|completed|cancelled",
  "start_date": "ISO8601|null",
  "end_date": "ISO8601|null", 
  "goals": ["string"],
  "tasks": ["string"],
  "created_at": "ISO8601",
  "updated_at": "ISO8601",
  "metadata": {
    "velocity_target": "number",
    "capacity": "number", 
    "team_assignments": {}
  }
}
```

#### Tool Registry Schema
```json
{
  "name": "string",
  "type": "agent|command|hook|workflow|library",
  "version": "string",
  "description": "string",
  "path": "string|null",
  "dependencies": ["string"],
  "config": {},
  "registered_at": "ISO8601",
  "updated_at": "ISO8601"
}
```

### JSONPath Query Examples

```bash
# Get all active tasks
$.execution.tasks[?(@.status in ['todo', 'in_progress', 'review'])]

# Get blocked tasks with high severity
$.execution.tasks[?(@.blocker && @.blocker.severity == 'high')]

# Get tasks assigned to specific agent
$.execution.tasks[?(@.assignee == 'engineering-fullstack')]

# Get overdue tasks (would need date comparison)
$.execution.tasks[?(@.due_date < '2024-01-15')]

# Get high priority tasks
$.execution.tasks[?(@.priority >= 4)]

# Get tasks by points range
$.execution.tasks[?(@.points >= 5 && @.points <= 10)]

# Get agents by capacity
$.execution.agents[?(@.capacity > 0)]

# Get recent events
$.observability.events[-5:]

# Get metrics for specific period
$.observability.metrics[?(@.timestamp >= '2024-01-15')]
```

## Integration APIs

### Claude Code Integration

#### Slash Command Integration
```bash
# State management commands
/state get <path>              # Maps to: uv run .claude/scripts/state_manager.py get $SESSION_ID <path>
/state set <path> <value>      # Maps to: uv run .claude/scripts/state_manager.py set $SESSION_ID <path> <value>
/state summary                 # Maps to: uv run .claude/scripts/state_manager.py list-sessions

# Session management commands  
/session create <mode>         # Maps to: uv run .claude/scripts/session_manager.py create --mode <mode>
/session heartbeat            # Maps to: uv run .claude/scripts/session_manager.py heartbeat $SESSION_ID
/session handoff <to>         # Maps to: uv run .claude/scripts/session_manager.py handoff $SESSION_ID <to>

# Shared state commands
/config get <project>         # Maps to: uv run .claude/scripts/shared_state.py get-config <project>
/epic list <project>          # Maps to: uv run .claude/scripts/shared_state.py list-epics <project>
/sprint create <args>         # Maps to: uv run .claude/scripts/shared_state.py create-sprint <args>
```

#### Environment Variable Integration
```bash
# Set in hooks and commands
export CLAUDE_SESSION_ID="current-session-id"
export CLAUDE_PROJECT_ID="current-project" 
export CLAUDE_MODE="development|leadership|sprint|config"

# Used by UV scripts
uv run .claude/scripts/state_manager.py get $CLAUDE_SESSION_ID "sprint.tasks"
```

### Hook Integration Points

#### Session Start Hook
```python
# Initialize session state
session_id = os.environ.get('CLAUDE_SESSION_ID')
if not session_id:
    session_id = subprocess.check_output([
        'uv', 'run', '.claude/scripts/session_manager.py', 'create',
        '--mode', 'development', '--project', project_name
    ]).decode().strip()
    
# Load development context
subprocess.run([
    'uv', 'run', '.claude/scripts/state_manager.py', 'merge', session_id,
    'execution.context', '--data', json.dumps(context_data)
])
```

#### User Prompt Submit Hook
```python
# Track prompt activity
subprocess.run([
    'uv', 'run', '.claude/scripts/state_manager.py', 'set', session_id,
    'session.lifecycle.last_activity', datetime.now().isoformat()
])

# Send heartbeat
subprocess.run([
    'uv', 'run', '.claude/scripts/session_manager.py', 'heartbeat', session_id
])
```

#### Post Tool Use Hook
```python
# Log tool usage
event_data = {
    'type': 'tool_used',
    'tool': tool_name,
    'success': tool_success,
    'timestamp': datetime.now().isoformat()
}

subprocess.run([
    'uv', 'run', '.claude/scripts/state_manager.py', 'merge', session_id,
    'observability.events', '--data', json.dumps([event_data])
])
```

### External System Integration

#### Git Integration
```bash
# Track git state in session
GIT_BRANCH=$(git branch --show-current)
GIT_STATUS=$(git status --porcelain)

uv run .claude/scripts/state_manager.py set $SESSION_ID "execution.context.git" "{
  \"branch\": \"$GIT_BRANCH\",
  \"status\": \"$GIT_STATUS\",
  \"last_commit\": \"$(git rev-parse HEAD)\"
}"
```

#### CI/CD Integration
```bash
# Update deployment status
uv run .claude/scripts/shared_state.py set-config $PROJECT_ID --data "{
  \"environments\": {
    \"staging\": {
      \"last_deploy\": \"$(date -Iseconds)\",
      \"commit\": \"$(git rev-parse HEAD)\",
      \"status\": \"deployed\"
    }
  }
}"
```

#### Monitoring Integration
```bash
# Export metrics for external monitoring
uv run .claude/scripts/state_manager.py get $SESSION_ID "observability.metrics" --json-output | \
  curl -X POST -H "Content-Type: application/json" -d @- \
  https://monitoring.example.com/api/metrics
```

This API reference provides complete technical documentation for the V2 orchestration system. For usage examples and workflows, see the [User Guide](USER_GUIDE.md).