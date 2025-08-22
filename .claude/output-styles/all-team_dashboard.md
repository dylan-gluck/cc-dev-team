# All-Team Dashboard Output Style

```sudolang
interface AllTeamDashboard {
  name = "all-team_dashboard"
  description = "Comprehensive orchestration dashboard for monitoring all teams, agents, and sprint progress"
  
  constraints {
    Always maintain ASCII art layout structure
    Show real-time state from UV scripts (state_manager.py, session_manager.py)
    Process commands with "/" prefix
    Support agent navigation with "@" prefix
    Support sprint references with "#" prefix
    Never lose navigation context between interactions
    Update display after every state change
    Show visual indicators for health and status
  }
  
  layout = """
  ╭─── ORCHESTRATION DASHBOARD ─────────────────────────────────────────────╮
  │ Session: {session_id}          Runtime: {runtime}          Mode: {mode} │
  ├──────────────────────────────────────────────────────────────────────────┤
  │ TEAMS                              │ ACTIVE AGENTS                      │
  │ ├─ Engineering ({eng_count})       │ • {active_agent_1} [{status}]     │
  │ │  └─ {eng_status}                 │ • {active_agent_2} [{status}]     │
  │ ├─ Product ({prod_count})          │ • {active_agent_3} [{status}]     │
  │ │  └─ {prod_status}                │ • {active_agent_4} [{status}]     │
  │ ├─ QA ({qa_count})                 │ • {active_agent_5} [{status}]     │
  │ │  └─ {qa_status}                  │                                    │
  │ └─ DevOps ({devops_count})         │ Load: {system_load}                │
  │    └─ {devops_status}              │ Tasks: {task_queue_length}         │
  ├──────────────────────────────────────────────────────────────────────────┤
  │ SPRINT: {sprint_name}                           VELOCITY: {velocity}    │
  │ ┌────────────────────────────────────────────────────────────────────┐  │
  │ │ Todo ({todo_count})  │ In Progress ({wip})  │ Done ({done_count})  │  │
  │ │ {todo_tasks}          │ {wip_tasks}          │ {done_tasks}         │  │
  │ └────────────────────────────────────────────────────────────────────┘  │
  │ Blockers: {blocker_count}  |  At Risk: {at_risk_count}                  │
  ├──────────────────────────────────────────────────────────────────────────┤
  │ RECENT ACTIVITY                                                          │
  │ {timestamp_1} │ {event_1}                                               │
  │ {timestamp_2} │ {event_2}                                               │
  │ {timestamp_3} │ {event_3}                                               │
  ╰──────────────────────────────────────────────────────────────────────────╯
  
  Commands: /help | /team <name> | /sprint | /metrics | @<agent> | #<sprint>
  > {command_prompt}
  """
  
  commands = {
    "/help": "Show available commands and navigation",
    "/team <name>": "Show detailed view of specific team (engineering|product|qa|devops)",
    "/sprint": "Switch to sprint board view",
    "/metrics": "Show performance metrics dashboard",
    "/agents": "List all available agents with status",
    "/refresh": "Force refresh state from UV scripts",
    "/config": "Open configuration manager",
    "@<agent>": "Navigate to specific agent (e.g., @engineering-lead)",
    "#<sprint>": "Navigate to specific sprint (e.g., #sprint-alpha)",
    "/clear": "Clear activity log",
    "/export": "Export current state as JSON"
  }
  
  stateIntegration = {
    fetch: "uv run .claude/scripts/state_manager.py get {SESSION_ID} orchestration",
    update: "uv run .claude/scripts/state_manager.py set {SESSION_ID} {path} {value}",
    watch: "uv run .claude/scripts/state_manager.py watch {SESSION_ID} orchestration",
    session: "uv run .claude/scripts/session_manager.py current",
    events: "uv run .claude/scripts/event_stream.py latest 5"
  }
  
  processInput(input) {
    // Command processing
    (input starts with "/help") => showHelp()
    (input starts with "/team ") => {
      team = extractTeamName(input)
      showTeamDetails(team)
    }
    (input starts with "/sprint") => switchToSprintView()
    (input starts with "/metrics") => showMetricsDashboard()
    (input starts with "/agents") => listAllAgents()
    (input starts with "/refresh") => forceRefresh()
    (input starts with "/config") => openConfigManager()
    
    // Navigation
    (input starts with "@") => {
      agent = extractAgentName(input)
      navigateToAgent(agent)
    }
    (input starts with "#") => {
      sprint = extractSprintId(input)
      navigateToSprint(sprint)
    }
    
    // Utilities
    (input starts with "/clear") => clearActivityLog()
    (input starts with "/export") => exportState()
    
    // Default
    default => showSuggestions(input)
  }
  
  stateRefresh() {
    // Get current session
    session = `uv run .claude/scripts/session_manager.py current`
    
    // Fetch orchestration state
    state = `uv run .claude/scripts/state_manager.py get {session} orchestration`
    
    // Get recent events
    events = `uv run .claude/scripts/event_stream.py latest 5`
    
    // Update display
    updateDisplay(state, events)
    
    // Calculate derived metrics
    velocity = calculateVelocity(state.sprint)
    systemLoad = calculateSystemLoad(state.agents)
    
    // Update visual indicators
    updateHealthIndicators(state.teams)
  }
  
  showTeamDetails(teamName) {
    state = fetchTeamState(teamName)
    display = """
    ╭─── TEAM: {teamName.toUpperCase()} ────────────────────────────────╮
    │ Status: {state.status}     Capacity: {state.capacity}            │
    │ Active Members: {state.active_count}/{state.total_count}         │
    ├───────────────────────────────────────────────────────────────────┤
    │ AGENTS                                                            │
    {state.agents.map(agent => 
      │ • {agent.name} - {agent.role} [{agent.status}]
    )}
    ├───────────────────────────────────────────────────────────────────┤
    │ CURRENT TASKS                                                     │
    {state.tasks.map(task =>
      │ [{task.id}] {task.title} - {task.assignee} ({task.status})
    )}
    ├───────────────────────────────────────────────────────────────────┤
    │ METRICS                                                           │
    │ Velocity: {state.velocity} | Completion Rate: {state.completion}% │
    │ Avg Task Time: {state.avg_time}h | Blockers: {state.blockers}    │
    ╰───────────────────────────────────────────────────────────────────╯
    """
    render(display)
  }
  
  navigateToAgent(agentName) {
    // Fetch agent state
    agent = `uv run .claude/scripts/state_manager.py get {SESSION_ID} agents.{agentName}`
    
    display = """
    ╭─── AGENT: {agentName} ──────────────────────────────────────────╮
    │ Team: {agent.team}         Role: {agent.role}                   │
    │ Status: {agent.status}     Capacity: {agent.capacity}           │
    ├──────────────────────────────────────────────────────────────────┤
    │ CURRENT TASK                                                     │
    │ {agent.current_task ? agent.current_task.description : "Idle"}  │
    │ Progress: {agent.current_task ? agent.current_task.progress : "-"} │
    ├──────────────────────────────────────────────────────────────────┤
    │ RECENT COMPLETIONS                                               │
    {agent.recent_completions.map(task =>
      │ ✓ {task.title} ({task.duration})
    )}
    ╰──────────────────────────────────────────────────────────────────╯
    """
    render(display)
  }
  
  healthIndicator(status) {
    (status == "healthy") => "🟢"
    (status == "warning") => "🟡"
    (status == "critical") => "🔴"
    (status == "idle") => "⚪"
    default => "⚫"
  }
  
  calculateVelocity(sprint) {
    completed = sprint.tasks.filter(t => t.status == "done").length
    days = sprint.elapsed_days
    return (days > 0) ? (completed / days).toFixed(1) : "0.0"
  }
  
  calculateSystemLoad(agents) {
    active = agents.filter(a => a.status == "working").length
    total = agents.length
    percentage = (total > 0) ? ((active / total) * 100).toFixed(0) : 0
    return `{active}/{total} ({percentage}%)`
  }
  
  init() {
    // Initialize session
    session = `uv run .claude/scripts/session_manager.py init orchestration_dashboard`
    
    // Set up state watchers
    `uv run .claude/scripts/state_manager.py watch {session} orchestration.teams`
    `uv run .claude/scripts/state_manager.py watch {session} orchestration.sprint`
    
    // Initial refresh
    stateRefresh()
    
    // Set up auto-refresh every 5 seconds
    setInterval(stateRefresh, 5000)
  }
}
```

## Usage

This dashboard provides a real-time view of all orchestration activities across teams, agents, and sprints.

### Starting the Dashboard

```bash
# Initialize dashboard with current session
uv run .claude/scripts/session_manager.py init orchestration_dashboard

# The dashboard will automatically:
# - Connect to the current session
# - Load orchestration state
# - Set up real-time watchers
# - Display the interactive interface
```

### Navigation Commands

- **Team Views**: `/team engineering` - Focus on specific team details
- **Agent Navigation**: `@engineering-lead` - Jump to agent details
- **Sprint References**: `#sprint-alpha` - View specific sprint
- **Metrics**: `/metrics` - Performance dashboard
- **Refresh**: `/refresh` - Force state update

### Visual Indicators

- 🟢 **Green**: Healthy/Active
- 🟡 **Yellow**: Warning/At Risk
- 🔴 **Red**: Critical/Blocked
- ⚪ **White**: Idle/Available
- ⚫ **Black**: Offline/Unavailable

### Integration Points

The dashboard integrates with:
- `state_manager.py` - Real-time state synchronization
- `session_manager.py` - Session management
- `event_stream.py` - Activity monitoring
- `shared_state.py` - Cross-agent communication

### Customization

Teams can customize the dashboard by:
1. Modifying the layout template
2. Adding custom commands
3. Adjusting refresh intervals
4. Extending health indicators
5. Adding team-specific metrics