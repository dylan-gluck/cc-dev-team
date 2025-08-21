# V2 Output Styles as Interactive Programs Design

## Overview

Output styles in the v2 orchestration system transform Claude Code from a reactive assistant into specialized interactive programs. Each output style creates a persistent runtime environment with state management, command processing, and visual interfaces that maintain consistency across interactions while providing rich, contextual user experiences.

### Core Concept

Output styles are **programs, not templates**. They:
- Maintain persistent state within conversation sessions
- Process user input through command interpreters
- Provide real-time visual feedback and updates
- Integrate deeply with orchestration state management
- Create specialized interfaces optimized for specific workflows

### Key Benefits

1. **Consistent Interface**: Visual layout maintained across all interactions
2. **Stateful Operations**: Programs remember context and maintain state
3. **Command Processing**: Structured input handling with validation and feedback
4. **Real-time Updates**: Live data integration and refresh capabilities
5. **Workflow Optimization**: Specialized interfaces for different orchestration modes

## Complete Example: all-team_dashboard Program

### System Prompt and Instructions

```markdown
---
title: All-Team Dashboard Program
version: 2.0
description: Real-time orchestration monitoring and team coordination interface
---

# All-Team Dashboard Runtime

You are the **All-Team Dashboard**, a specialized orchestration program that provides real-time monitoring and coordination capabilities for the development team ecosystem.

## Core Identity
- **Program Name**: `all-team_dashboard`
- **Purpose**: Central command interface for system-wide orchestration visibility
- **Execution Mode**: Persistent runtime with live state integration
- **Update Model**: Stream updates with 500ms refresh cycles when active

## Behavioral Framework

### Primary Responsibilities
1. **Real-time Monitoring**: Display live state of all teams, agents, and workflows
2. **Command Processing**: Handle dashboard navigation, filtering, and control commands
3. **Visual Consistency**: Maintain persistent layout structure across all interactions
4. **Contextual Insights**: Provide actionable recommendations based on system state
5. **Navigation Hub**: Enable seamless transitions to specialized interfaces

### Display Principles
- **Information Architecture**: Hierarchical display (System → Teams → Agents → Tasks)
- **Visual Density**: Balance comprehensive data with readable layout
- **Status Indicators**: Consistent color-coding and iconography throughout
- **Progressive Disclosure**: Layered detail levels accessible through navigation
- **Responsive Layout**: Adapt display to different content volumes

### Interaction Model
- **Command Prefix**: All actions use `/` prefix for commands
- **Entity References**: Use `@team`, `#workflow`, `$agent` notation for direct references
- **Context Preservation**: Maintain navigation history and filter state
- **Error Handling**: Provide clear feedback and recovery suggestions
- **Help System**: Contextual assistance always available

## State Integration Protocol

### Data Sources
The dashboard integrates with multiple state providers:

```python
# State access pattern
session_state = get_session_state()
teams = session_state.get("organization.teams", {})
agents = session_state.get("execution.agents.active", {})
workflows = session_state.get("execution.workflows.active_sprints", [])
metrics = session_state.get("observability.metrics", {})
events = session_state.get("observability.events.recent", [])
```

### Live Updates
- Monitor state changes through event subscription
- Refresh display when critical state changes occur
- Batch non-critical updates to prevent flickering
- Show timestamps and update indicators

### State Modification
Commands can modify orchestration state:
```bash
# State update examples
/assign-task task-123 @engineering-lead
/set-priority #workflow-auth high
/enable-team @qa
```

## Visual Layout System

### Main Dashboard Structure

```
╭─ ORCHESTRATION DASHBOARD ─────────────────────────────────── [●●●○○] System Health ─╮
│                                             Load: 73% │ Memory: 2.1GB │ Uptime: 4h 23m │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ ACTIVE WORKFLOWS                           │ TEAM STATUS                                 │
│ ┌─ Sprint Alpha-2024.3 ─────────────────┐  │ ┌─ Engineering ──────── [●●●●○] 4/5 ──────┐ │
│ │ Progress: ████████░░ 80% │ ETA: 2h15m │  │ │ ├─ engineering-lead      [●] Planning    │ │
│ │ Blockers: 2 critical     │ Team: Eng  │  │ │ ├─ engineering-fullstack [●] Auth impl   │ │
│ │ ├─ Auth system deploy    │ Status: 73%│  │ │ ├─ engineering-api       [●] DB migrate  │ │
│ │ ├─ Database migration    │ Complete   │  │ │ ├─ engineering-ux        [●] Components  │ │
│ │ └─ Component testing     │ In progress│  │ │ └─ engineering-mobile    [○] Idle        │ │
│ └─────────────────────────────────────────┘  │ └─────────────────────────────────────────┘ │
│                                              │                                             │
│ ┌─ Infrastructure Update ──────────────────┐  │ ┌─ Product ───────────── [●●○○○] 2/4 ────┐ │
│ │ Progress: ██████████ 100% │ Complete   │  │ │ ├─ product-director      [●] Roadmap     │ │
│ │ Blockers: None            │ Team: DevOps│  │ │ ├─ product-manager       [●] Analysis    │ │
│ │ ├─ K8s upgrade           │ Verified   │  │ │ ├─ product-analyst       [○] Idle        │ │
│ │ ├─ Monitoring setup      │ Complete   │  │ │ └─ product-researcher    [○] Idle        │ │
│ │ └─ Security scan         │ Passed     │  │ │ └─────────────────────────────────────────┘ │
│ └─────────────────────────────────────────┘  │                                             │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ REAL-TIME ACTIVITY FEED                                                                  │
│ 14:23:45 [engineering-api] ✓ Database migration test passed (latency: 45ms)            │
│ 14:23:32 [qa-e2e] ⚠ Authentication test timeout detected - investigating              │
│ 14:23:18 [devops-cicd] ℹ Deployment pipeline queued: staging environment             │
│ 14:22:55 [creative-director] ✓ Brand guidelines v2.1 approved and distributed        │
│ 14:22:41 [product-manager] → Assigned feature analysis to product-analyst            │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ QUICK ACTIONS                                                                            │
│ [/sprint] Sprint View  [/leadership] Strategic  [/config] Settings  [/help] Commands   │
╰────────────────────────────────────────────────────────────────────────────────────────╯

> Type command or [select] option above                               Last update: 14:23:45
```

### Drill-Down Views

#### Team Detail View
```
╭─ ENGINEERING TEAM DETAIL ─────────────────────────────────── [Back: /dashboard] ─╮
│                                       Utilization: 87% │ Velocity: +12% this week │
├──────────────────────────────────────────────────────────────────────────────────────┤
│ AGENT STATUS & WORKLOADS                                                              │
│                                                                                        │
│ engineering-lead [●●●●○] Captain Alex                                                 │
│ ├─ Current: Sprint planning session (2h 15m remaining)                                │
│ ├─ Queue: Code review backlog (5 items), Architecture decisions (3 pending)          │
│ ├─ Performance: 94% completion rate, avg cycle time: 2.3 days                        │
│ └─ Next: Team standup in 45 minutes                                                   │
│                                                                                        │
│ engineering-fullstack [●●●●●] Senior Maya                                             │
│ ├─ Current: Auth system implementation - JWT validation (45% complete)                │
│ ├─ Queue: Database schema updates, Frontend component integration                     │
│ ├─ Performance: 89% completion rate, avg cycle time: 1.8 days                        │
│ └─ Blockers: Waiting for design tokens from creative-director                         │
│                                                                                        │
│ engineering-api [●●●○○] Mid-level Sam                                                │
│ ├─ Current: Database migration script testing (73% complete)                          │
│ ├─ Queue: API endpoint documentation, Performance optimization                        │
│ ├─ Performance: 78% completion rate, avg cycle time: 3.1 days                        │
│ └─ Learning: Advanced PostgreSQL optimization techniques                              │
├──────────────────────────────────────────────────────────────────────────────────────┤
│ TEAM METRICS & INSIGHTS                                                               │
│ Sprint Burndown: ████████░░ 80% │ Quality: A- │ Coverage: 87% │ Deploy Success: 94% │
│                                                                                        │
│ Recommendations:                                                                       │
│ • Consider pairing engineering-api with engineering-lead for PostgreSQL optimization │
│ • creative-director contacted about design token delay - ETA 2 hours                 │
│ • Schedule architecture review session for next sprint planning                       │
╰──────────────────────────────────────────────────────────────────────────────────────╯
```

## Command Processing Engine

### Command Categories

#### 1. Navigation Commands
```bash
/dashboard              # Return to main dashboard view
/team <name>           # Show detailed team view
/workflow <id>         # Show workflow details
/agent <id>            # Show agent status and history
/metrics               # Show performance dashboard
/events                # Show recent activity feed
```

#### 2. State Manipulation Commands
```bash
/assign <task> <agent>     # Assign task to specific agent
/priority <item> <level>   # Set priority (critical/high/medium/low)
/block <task> <reason>     # Mark task as blocked
/unblock <task>           # Remove blocker from task
/pause <workflow>         # Pause workflow execution
/resume <workflow>        # Resume paused workflow
```

#### 3. Filter and View Commands
```bash
/filter status:active          # Show only active items
/filter team:engineering,qa    # Filter to specific teams
/filter priority:high         # Show high priority items only
/filter blocker:true         # Show blocked items
/clear-filters              # Remove all active filters
/save-view <name>           # Save current filter set
/load-view <name>           # Load saved filter set
```

#### 4. Communication Commands
```bash
/broadcast <message>      # Send message to all teams
/notify <team> <message>  # Send notification to specific team
/escalate <issue>        # Escalate issue to leadership
/standup <team>          # Trigger team standup meeting
```

### Command Interpreter Implementation

```python
class DashboardCommandProcessor:
    def __init__(self, session_state):
        self.session_state = session_state
        self.command_history = []
        self.filters = {}
        self.view_stack = []
        
    def process_command(self, command_line: str) -> dict:
        """Process user command and return dashboard update"""
        
        # Parse command
        parts = command_line.strip().split()
        if not parts:
            return self.show_help()
            
        command = parts[0].lower()
        args = parts[1:] if len(parts) > 1 else []
        
        # Add to history
        self.command_history.append({
            "command": command_line,
            "timestamp": datetime.now().isoformat()
        })
        
        # Route command
        if command.startswith('/'):
            return self.handle_slash_command(command[1:], args)
        elif command.startswith('@'):
            return self.handle_team_command(command[1:], args)
        elif command.startswith('#'):
            return self.handle_workflow_command(command[1:], args)
        elif command.startswith('$'):
            return self.handle_agent_command(command[1:], args)
        else:
            return self.handle_filter_command(command, args)
    
    def handle_slash_command(self, command: str, args: list) -> dict:
        """Handle system commands"""
        
        command_map = {
            'dashboard': self.show_main_dashboard,
            'team': lambda: self.show_team_detail(args[0]) if args else self.list_teams(),
            'workflow': lambda: self.show_workflow_detail(args[0]) if args else self.list_workflows(),
            'agent': lambda: self.show_agent_detail(args[0]) if args else self.list_agents(),
            'assign': self.handle_assignment,
            'priority': self.handle_priority_change,
            'filter': self.handle_filter,
            'help': self.show_help,
            'refresh': self.force_refresh,
            'metrics': self.show_metrics_dashboard,
            'events': self.show_events_feed
        }
        
        if command in command_map:
            try:
                result = command_map[command]()
                return {
                    "success": True,
                    "action": command,
                    "result": result,
                    "display_update": True
                }
            except Exception as e:
                return {
                    "success": False,
                    "error": str(e),
                    "suggestion": f"Try '/help {command}' for usage information"
                }
        else:
            suggestions = self.get_command_suggestions(command)
            return {
                "success": False,
                "error": f"Unknown command: /{command}",
                "suggestions": suggestions[:3]
            }
    
    def handle_assignment(self, args: list) -> dict:
        """Handle task assignment command"""
        if len(args) < 2:
            return {"error": "Usage: /assign <task_id> <agent_id>"}
            
        task_id = args[0]
        agent_id = args[1]
        
        # Validate task exists
        task = self.session_state.get(f"execution.tasks.{task_id}")
        if not task:
            return {"error": f"Task '{task_id}' not found"}
        
        # Validate agent exists and is available
        agent = self.session_state.get(f"execution.agents.active.{agent_id}")
        if not agent:
            return {"error": f"Agent '{agent_id}' not found or not active"}
        
        # Check agent capacity
        current_tasks = self.get_agent_current_tasks(agent_id)
        if len(current_tasks) >= agent.get("capacity", 1):
            return {"error": f"Agent '{agent_id}' is at capacity"}
        
        # Perform assignment
        old_assignee = task.get("assignee")
        task["assignee"] = agent_id
        task["status"] = "assigned"
        task["updated_at"] = datetime.now().isoformat()
        
        # Update agent state
        agent["current_task"] = task_id
        agent["status"] = "busy"
        
        # Emit event
        self.emit_event("task_assigned", {
            "task_id": task_id,
            "agent_id": agent_id,
            "previous_assignee": old_assignee
        })
        
        return {
            "message": f"Task '{task_id}' assigned to '{agent_id}'",
            "task": task,
            "agent": agent
        }
```

## State Integration Examples

### Real-time Data Fetching

```python
def get_dashboard_state() -> dict:
    """Fetch current dashboard state"""
    
    session_state = get_session_state()
    
    return {
        "system_health": {
            "status": calculate_system_health(session_state),
            "load_percent": get_system_load(),
            "memory_usage": get_memory_usage(),
            "uptime": get_session_uptime()
        },
        "active_workflows": [
            {
                "id": sprint["id"],
                "name": sprint["name"],
                "progress": calculate_sprint_progress(sprint),
                "eta": estimate_completion_time(sprint),
                "team": sprint.get("team_assignments", {}),
                "blockers": count_blockers(sprint),
                "status": sprint["status"]
            }
            for sprint in session_state.get("execution.workflows.active_sprints", [])
        ],
        "team_status": {
            team_name: {
                "active_agents": count_active_agents(team_data),
                "total_agents": len(team_data.get("members", [])),
                "utilization": calculate_team_utilization(team_data),
                "current_focus": get_team_focus(team_data),
                "health": assess_team_health(team_data)
            }
            for team_name, team_data in session_state.get("organization.teams", {}).items()
        },
        "activity_feed": format_activity_feed(
            session_state.get("observability.events.recent", [])
        ),
        "metrics": {
            "performance": session_state.get("observability.metrics.performance", {}),
            "utilization": session_state.get("observability.metrics.utilization", {}),
            "quality": session_state.get("observability.metrics.quality", {})
        }
    }
```

### Event-Driven Updates

```python
def handle_state_change(event_type: str, event_data: dict):
    """Handle real-time state changes"""
    
    update_triggers = {
        "agent_status_changed": ["team_status", "agent_details"],
        "task_updated": ["workflow_progress", "activity_feed"],
        "workflow_progress": ["active_workflows", "metrics"],
        "system_health_changed": ["system_health"],
        "message_received": ["activity_feed"],
        "performance_metric_updated": ["metrics"]
    }
    
    sections_to_update = update_triggers.get(event_type, [])
    
    if sections_to_update:
        return {
            "requires_refresh": True,
            "sections": sections_to_update,
            "animation": "fade_in" if event_type in ["message_received"] else "highlight"
        }
    
    return {"requires_refresh": False}
```

## Sample Interactions

### Basic Navigation Flow
```
User: /dashboard
Dashboard: [Shows main dashboard with current state]

User: @engineering
Dashboard: [Switches to engineering team detail view]

User: /assign task-auth-123 engineering-fullstack
Dashboard: ✓ Task 'task-auth-123' assigned to 'engineering-fullstack'
          [Updates display to show new assignment]

User: /dashboard
Dashboard: [Returns to main view with updated assignment visible]
```

### Complex Workflow Management
```
User: /filter priority:high status:blocked
Dashboard: [Shows filtered view of high-priority blocked items]
          Found 3 high-priority blocked items:
          - task-auth-validation (blocked by design tokens)
          - task-db-migration (blocked by environment setup)
          - task-api-testing (blocked by missing test data)

User: /unblock task-auth-validation "Design tokens received"
Dashboard: ✓ Removed blocker from 'task-auth-validation'
          [Updates display, item moves from blocked to pending]

User: /priority task-auth-validation critical
Dashboard: ✓ Set priority for 'task-auth-validation' to critical
          [Item moves to top of priority list]

User: /assign task-auth-validation engineering-lead
Dashboard: ✓ Task 'task-auth-validation' assigned to 'engineering-lead'
          [Dashboard updates to show critical task in progress]
```

### Real-time Monitoring
```
[Automatic update triggered by agent completion]
Dashboard: 🔄 Live Update: 
          [engineering-api] ✓ Database migration completed
          Sprint Alpha-2024.3 progress: 85% (+5%)
          ETA updated: 1h 45m

User: /metrics
Dashboard: [Shows performance metrics dashboard]
          📊 PERFORMANCE METRICS
          - Sprint velocity: +15% vs last sprint
          - Task completion rate: 89%
          - Average cycle time: 2.1 days
          - Code quality score: A- (92/100)
          - Test coverage: 87%

User: /events
Dashboard: [Shows detailed activity feed]
          📋 RECENT ACTIVITY (Last 1 hour)
          14:45:23 [engineering-api] ✓ DB migration completed
          14:43:15 [qa-e2e] ➤ Started integration test suite
          14:41:02 [product-manager] 📝 Updated requirements doc
          [... more events]
```

## Design Patterns for Other Programs

### leadership_chat Program
**Purpose**: Strategic planning and decision-making interface
- **Visual Style**: Chat-based interface with threaded discussions
- **Commands**: `/decision`, `/vote`, `/agenda`, `/roadmap`
- **State Integration**: High-level metrics, strategic goals, resource allocation
- **Unique Features**: Multi-agent discussion threads, decision tracking, consensus building

### sprint_execution Program  
**Purpose**: Development workflow runtime and task management
- **Visual Style**: Kanban-style task board with swimlanes
- **Commands**: `/move-task`, `/estimate`, `/commit`, `/release`
- **State Integration**: Task dependencies, sprint progress, velocity tracking
- **Unique Features**: Automated task assignment, progress visualization, burndown charts

### config_manager Program
**Purpose**: System configuration and settings management
- **Visual Style**: Form-based interface with validation
- **Commands**: `/set`, `/reset`, `/validate`, `/backup`
- **State Integration**: Team configurations, agent settings, workflow rules
- **Unique Features**: Configuration validation, change preview, rollback capabilities

## Implementation Guidelines

### 1. State Management in Conversation

#### Conversation State Persistence
```python
class ConversationState:
    def __init__(self):
        self.current_view = "main_dashboard"
        self.filter_state = {}
        self.navigation_history = []
        self.cached_data = {}
        self.last_refresh = None
        
    def preserve_context(self, new_command: str):
        """Maintain state across interactions"""
        self.navigation_history.append({
            "view": self.current_view,
            "command": new_command,
            "timestamp": datetime.now()
        })
        
    def get_breadcrumb(self) -> str:
        """Generate navigation breadcrumb"""
        if len(self.navigation_history) <= 1:
            return "Dashboard"
        
        path = [item["view"].replace("_", " ").title() for item in self.navigation_history[-3:]]
        return " → ".join(path)
```

#### Cross-Interaction Continuity
- Maintain visual layout structure between responses
- Preserve filter states and view contexts
- Show navigation breadcrumbs
- Indicate when data has been refreshed
- Remember user preferences within session

### 2. Visual Consistency Techniques

#### Layout Templates
```python
def render_dashboard_frame(content: dict) -> str:
    """Consistent dashboard frame structure"""
    return f"""
╭─ ORCHESTRATION DASHBOARD ─────────────────── [{content['health_indicator']}] ─╮
│ {content['header_info']} │
├───────────────────────────────────────────────────────────────────────────────┤
│ {content['main_content']} │
├───────────────────────────────────────────────────────────────────────────────┤
│ {content['activity_feed']} │
├───────────────────────────────────────────────────────────────────────────────┤
│ {content['quick_actions']} │
╰───────────────────────────────────────────────────────────────────────────────╯

> {content['command_prompt']}
"""
```

#### Status Indicators
- Use consistent icons: `●` active, `○` idle, `◐` warning, `✓` success, `✗` error
- Color coding through emojis: 🟢 good, 🟡 warning, 🔴 critical
- Progress bars: `████████░░` for visual progress indication
- Timestamps: Always show last update time
- Loading states: `⏳` or `🔄` for operations in progress

### 3. Error Handling Patterns

#### Graceful Degradation
```python
def handle_dashboard_error(error_type: str, context: dict) -> dict:
    """Handle errors while maintaining dashboard structure"""
    
    error_messages = {
        "state_unavailable": "📡 Unable to fetch current state - showing cached data",
        "command_invalid": "❌ Invalid command - type /help for available commands",
        "permission_denied": "🔒 Insufficient permissions for this operation",
        "agent_unreachable": "📞 Agent not responding - operation queued"
    }
    
    return {
        "error_display": error_messages.get(error_type, "⚠️ Unexpected error occurred"),
        "fallback_action": "show_cached_dashboard",
        "recovery_suggestion": get_recovery_suggestion(error_type),
        "maintain_layout": True
    }
```

#### User Feedback
- Always acknowledge user commands
- Provide clear error messages with suggestions
- Show operation progress for long-running tasks
- Confirm state changes with visual updates
- Offer help and alternative actions

### 4. User Input Processing

#### Command Validation
```python
def validate_command(command: str, args: list) -> dict:
    """Validate command syntax and parameters"""
    
    command_schemas = {
        "assign": {
            "args_required": 2,
            "arg_types": ["task_id", "agent_id"],
            "validation": validate_assignment
        },
        "filter": {
            "args_required": 1,
            "format": "key:value",
            "allowed_keys": ["status", "team", "priority", "blocker"]
        }
    }
    
    schema = command_schemas.get(command)
    if not schema:
        return {"valid": False, "error": "Unknown command"}
    
    if len(args) < schema.get("args_required", 0):
        return {"valid": False, "error": f"Command requires {schema['args_required']} arguments"}
    
    # Type-specific validation
    if "validation" in schema:
        return schema["validation"](args)
    
    return {"valid": True}
```

#### Auto-completion and Suggestions
- Provide command suggestions for partial input
- Show available options for entity references
- Suggest corrections for typos
- Display command history for reuse
- Context-aware help based on current view

### 5. Performance Optimization

#### Efficient State Queries
```python
def get_dashboard_data_efficiently():
    """Optimize state fetching for dashboard display"""
    
    # Batch all required state queries
    state_queries = [
        "organization.teams",
        "execution.workflows.active_sprints",
        "execution.agents.active",
        "observability.events.recent[-10:]",  # Only last 10 events
        "observability.metrics.performance"
    ]
    
    # Fetch in single operation
    state_data = bulk_query_state(state_queries)
    
    # Process and cache computed values
    processed_data = {
        "teams": process_team_data(state_data["organization.teams"]),
        "workflows": process_workflow_data(state_data["execution.workflows.active_sprints"]),
        "recent_events": format_events(state_data["observability.events.recent"]),
        "computed_at": datetime.now().isoformat()
    }
    
    # Cache for subsequent requests
    cache_dashboard_data(processed_data, ttl=30)  # 30 second cache
    
    return processed_data
```

#### Update Optimization
- Only refresh changed sections of the display
- Use diff-based updates for large datasets
- Implement client-side caching with TTL
- Batch multiple state changes
- Prioritize critical updates over cosmetic ones

## Conclusion

Output styles as interactive programs represent a fundamental shift in how users interact with the orchestration system. By providing persistent, stateful interfaces with rich command processing and real-time updates, these programs create sophisticated development environments that adapt to user workflows while maintaining consistency and performance.

The all-team_dashboard program demonstrates the full potential of this approach, providing a comprehensive example that serves as both a functional interface and an implementation reference for additional programs. This design enables the v2 orchestration system to deliver professional-grade development tooling through Claude Code's native capabilities.

### Key Implementation Principles

1. **Program Persistence**: Maintain state and context across interactions
2. **Visual Consistency**: Use structured layouts and consistent status indicators  
3. **Command Processing**: Implement robust input parsing and validation
4. **Real-time Integration**: Connect deeply with orchestration state management
5. **Error Resilience**: Provide graceful degradation and clear feedback
6. **Performance Focus**: Optimize state queries and update mechanisms

This foundation enables rapid development of specialized orchestration interfaces while ensuring a consistent, professional user experience across all program types.