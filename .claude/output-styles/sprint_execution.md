# Sprint Execution Output Style

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
  
  layout = """
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
  ├──────────────────────────────────────────────────────────────────────────┤
  │ TEAM VELOCITY      │ BURNDOWN CHART                                      │
  │ Yesterday: {y_vel} │ ▁▂▃▄▅▆▇█▇▆▅▄▃▂▁  {burndown_visual}               │
  │ Today: {t_vel}     │ Ideal: ──── Actual: ████                            │
  │ Average: {avg_vel} │ On Track: {on_track_status}                         │
  ╰──────────────────────────────────────────────────────────────────────────╯
  
  Commands: /move | /assign | /block | /unblock | /estimate | /split | /metrics
  > {command_prompt}
  """
  
  swimlanes = """
  │ [{task_id_1}]      │ [{task_id_4}]       │ [{task_id_7}]            │ [{task_id_10}]         │ [{task_id_13}] │
  │ {task_title_1}     │ {task_title_4}      │ {task_title_7}           │ {task_title_10}        │ {task_title_13}│
  │ @{assignee_1}      │ @{assignee_4}       │ @{assignee_7}            │ @{assignee_10}         │ ✓{points_13}pts│
  │ {points_1}pts      │ {points_4}pts       │ {points_7}pts {progress} │ {points_10}pts         │                │
  │                    │                     │ ⚠️ {blocker_indicator}   │                        │                │
  ├────────────────────┼─────────────────────┼──────────────────────────┼────────────────────────┼───────────────┤
  │ [{task_id_2}]      │ [{task_id_5}]       │ [{task_id_8}]            │ [{task_id_11}]         │ [{task_id_14}] │
  │ {task_title_2}     │ {task_title_5}      │ {task_title_8}           │ {task_title_11}        │ {task_title_14}│
  │ @{assignee_2}      │ @{assignee_5}       │ @{assignee_8}            │ @{assignee_11}         │ ✓{points_14}pts│
  │ {points_2}pts      │ {points_5}pts       │ {points_8}pts            │ {points_11}pts         │                │
  ├────────────────────┼─────────────────────┼──────────────────────────┼────────────────────────┼───────────────┤
  │ [{task_id_3}]      │ [{task_id_6}]       │ [{task_id_9}]            │ [{task_id_12}]         │ [{task_id_15}] │
  │ {task_title_3}     │ {task_title_6}      │ {task_title_9}           │ {task_title_12}        │ {task_title_15}│
  │ Unassigned         │ @{assignee_6}       │ @{assignee_9}            │ @{assignee_12}         │ ✓{points_15}pts│
  │ {points_3}pts      │ {points_6}pts       │ {points_9}pts            │ {points_12}pts         │                │
  """
  
  commands = {
    "/move <task_id> <column>": "Move task to different column",
    "/assign <task_id> @<agent>": "Assign task to agent",
    "/block <task_id> <reason>": "Mark task as blocked",
    "/unblock <task_id>": "Remove blocker from task",
    "/estimate <task_id> <points>": "Set story points for task",
    "/split <task_id>": "Split task into subtasks",
    "/metrics": "Show detailed sprint metrics",
    "/burndown": "Display burndown chart",
    "/velocity": "Show velocity trends",
    "/forecast": "Project sprint completion",
    "/retro": "Open retrospective view",
    "/autoassign": "Auto-assign tasks based on capacity",
    "/wip <column> <limit>": "Set WIP limit for column",
    "/filter <criteria>": "Filter board view",
    "/export": "Export sprint data"
  }
  
  stateIntegration = {
    fetch: "uv run .claude/scripts/state_manager.py get {SESSION_ID} sprint",
    update: "uv run .claude/scripts/state_manager.py set {SESSION_ID} sprint.{path} {value}",
    watch: "uv run .claude/scripts/state_manager.py watch {SESSION_ID} sprint.tasks",
    metrics: "uv run .claude/scripts/state_manager.py get {SESSION_ID} sprint.metrics",
    events: "uv run .claude/scripts/event_stream.py filter sprint {sprint_id}"
  }
  
  processInput(input) {
    // Task movement
    (input starts with "/move ") => {
      [taskId, column] = extractMoveParams(input)
      moveTask(taskId, column)
    }
    
    // Task assignment
    (input starts with "/assign ") => {
      [taskId, agent] = extractAssignParams(input)
      assignTask(taskId, agent)
    }
    
    // Blocker management
    (input starts with "/block ") => {
      [taskId, reason] = extractBlockerParams(input)
      blockTask(taskId, reason)
    }
    (input starts with "/unblock ") => {
      taskId = extractTaskId(input)
      unblockTask(taskId)
    }
    
    // Estimation
    (input starts with "/estimate ") => {
      [taskId, points] = extractEstimateParams(input)
      estimateTask(taskId, points)
    }
    
    // Task splitting
    (input starts with "/split ") => {
      taskId = extractTaskId(input)
      splitTask(taskId)
    }
    
    // Metrics views
    (input == "/metrics") => showDetailedMetrics()
    (input == "/burndown") => showBurndownChart()
    (input == "/velocity") => showVelocityTrends()
    (input == "/forecast") => projectCompletion()
    (input == "/retro") => openRetrospective()
    
    // Automation
    (input == "/autoassign") => autoAssignTasks()
    
    // Configuration
    (input starts with "/wip ") => {
      [column, limit] = extractWipParams(input)
      setWipLimit(column, limit)
    }
    
    // Filtering
    (input starts with "/filter ") => {
      criteria = extractFilterCriteria(input)
      filterBoard(criteria)
    }
    
    // Export
    (input == "/export") => exportSprintData()
    
    default => showSuggestions(input)
  }
  
  moveTask(taskId, targetColumn) {
    // Validate move
    task = `uv run .claude/scripts/state_manager.py get {SESSION_ID} sprint.tasks.{taskId}`
    
    // Check WIP limits
    targetTasks = getColumnTasks(targetColumn)
    wipLimit = getWipLimit(targetColumn)
    
    if (targetTasks.length >= wipLimit && wipLimit != -1) {
      showError(`WIP limit ({wipLimit}) reached for {targetColumn}`)
      return
    }
    
    // Check valid transitions
    if (!isValidTransition(task.status, targetColumn)) {
      showError(`Cannot move from {task.status} to {targetColumn}`)
      return
    }
    
    // Update task status
    newStatus = columnToStatus(targetColumn)
    `uv run .claude/scripts/state_manager.py set {SESSION_ID} sprint.tasks.{taskId}.status {newStatus}`
    
    // Log movement
    event = {
      type: "task_moved",
      taskId: taskId,
      from: task.status,
      to: newStatus,
      timestamp: getCurrentTimestamp(),
      actor: getCurrentUser()
    }
    `uv run .claude/scripts/event_stream.py emit sprint.task_moved {event}`
    
    // Update velocity if moved to done
    if (newStatus == "done") {
      updateVelocity(task.points)
    }
    
    // Refresh board
    refreshBoard()
  }
  
  assignTask(taskId, agent) {
    // Check agent availability
    agentState = `uv run .claude/scripts/state_manager.py get {SESSION_ID} agents.{agent}`
    
    if (agentState.capacity <= 0) {
      showWarning(`{agent} is at full capacity`)
    }
    
    // Update assignment
    `uv run .claude/scripts/state_manager.py set {SESSION_ID} sprint.tasks.{taskId}.assignee {agent}`
    
    // Update agent capacity
    newCapacity = agentState.capacity - 1
    `uv run .claude/scripts/state_manager.py set {SESSION_ID} agents.{agent}.capacity {newCapacity}`
    
    // Notify agent
    `uv run .claude/scripts/shared_state.py notify {agent} task_assigned {taskId}`
    
    // Log assignment
    event = {
      type: "task_assigned",
      taskId: taskId,
      assignee: agent,
      timestamp: getCurrentTimestamp()
    }
    `uv run .claude/scripts/event_stream.py emit sprint.task_assigned {event}`
    
    refreshBoard()
  }
  
  blockTask(taskId, reason) {
    blocker = {
      id: generateId(),
      taskId: taskId,
      reason: reason,
      reportedBy: getCurrentUser(),
      timestamp: getCurrentTimestamp(),
      severity: assessSeverity(reason)
    }
    
    // Add blocker to task
    `uv run .claude/scripts/state_manager.py set {SESSION_ID} sprint.tasks.{taskId}.blocker {blocker}`
    
    // Add to sprint blockers list
    `uv run .claude/scripts/state_manager.py append {SESSION_ID} sprint.blockers {blocker}`
    
    // Notify team
    `uv run .claude/scripts/shared_state.py broadcast sprint.blocker_added {blocker}`
    
    // Update risk assessment
    updateSprintRisk()
    
    refreshBoard()
  }
  
  autoAssignTasks() {
    // Get unassigned tasks
    tasks = `uv run .claude/scripts/state_manager.py get {SESSION_ID} sprint.tasks`
    unassigned = tasks.filter(t => !t.assignee && t.status == "todo")
    
    // Get available agents
    agents = `uv run .claude/scripts/state_manager.py get {SESSION_ID} agents`
    available = agents.filter(a => a.capacity > 0)
    
    // Sort by expertise match and capacity
    assignments = optimizeAssignments(unassigned, available)
    
    // Execute assignments
    for (assignment of assignments) {
      assignTask(assignment.taskId, assignment.agent)
    }
    
    showInfo(`Auto-assigned {assignments.length} tasks`)
  }
  
  showDetailedMetrics() {
    metrics = `uv run .claude/scripts/state_manager.py get {SESSION_ID} sprint.metrics`
    
    display = """
    ╭─── SPRINT METRICS: {sprint_name} ───────────────────────────────────╮
    │ VELOCITY                          │ THROUGHPUT                      │
    │ Current: {metrics.velocity}       │ Daily Avg: {metrics.throughput} │
    │ Target: {metrics.target_velocity} │ Peak: {metrics.peak_throughput} │
    │ Trend: {metrics.velocity_trend}   │ Trend: {metrics.throughput_trend}│
    ├────────────────────────────────────┼─────────────────────────────────┤
    │ CYCLE TIME                        │ LEAD TIME                       │
    │ Average: {metrics.avg_cycle}h     │ Average: {metrics.avg_lead}h    │
    │ Median: {metrics.med_cycle}h      │ Median: {metrics.med_lead}h     │
    │ 95th %: {metrics.p95_cycle}h      │ 95th %: {metrics.p95_lead}h     │
    ├────────────────────────────────────┴─────────────────────────────────┤
    │ FLOW EFFICIENCY: {metrics.flow_efficiency}%                          │
    │ ████████████░░░░░░░ Active vs Waiting Time                          │
    ├───────────────────────────────────────────────────────────────────────┤
    │ WORK DISTRIBUTION                                                     │
    │ Engineering: ████████ {metrics.eng_work}%                           │
    │ QA:         ████░░░░ {metrics.qa_work}%                            │
    │ DevOps:     ██░░░░░░ {metrics.devops_work}%                        │
    │ Product:    █░░░░░░░ {metrics.product_work}%                       │
    ╰───────────────────────────────────────────────────────────────────────╯
    """
    render(display)
  }
  
  showBurndownChart() {
    burndown = `uv run .claude/scripts/state_manager.py get {SESSION_ID} sprint.burndown`
    
    display = """
    ╭─── BURNDOWN CHART: {sprint_name} ───────────────────────────────────╮
    │                                                                      │
    │ 100 ┤ ●                                                            │
    │  90 ┤  ╲                                                           │
    │  80 ┤   ╲___                                                       │
    │  70 ┤       ╲___                     Ideal ─────                  │
    │  60 ┤           ●___                 Actual ●━━━                  │
    │  50 ┤               ╲___                                           │
    │  40 ┤                   ●___                                       │
    │  30 ┤                       ╲___●                                  │
    │  20 ┤                           ╲___                               │
    │  10 ┤                               ╲___●                          │
    │   0 └────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────────    │
    │       Day1  Day2  Day3  Day4  Day5  Day6  Day7  Day8  Day9  Day10   │
    │                                                                      │
    │ Points Remaining: {burndown.remaining}                              │
    │ Burn Rate: {burndown.burn_rate} pts/day                            │
    │ Projected Completion: Day {burndown.projected_completion}           │
    │ Risk Level: {burndown.risk_level}                                   │
    ╰──────────────────────────────────────────────────────────────────────╯
    """
    render(display)
  }
  
  calculateVelocity(sprint) {
    completed = sprint.tasks.filter(t => t.status == "done")
    points = completed.reduce((sum, t) => sum + t.points, 0)
    days = sprint.elapsed_days || 1
    
    return {
      total: points,
      daily: (points / days).toFixed(1),
      projected: (points / days * sprint.total_days).toFixed(0)
    }
  }
  
  updateVelocity(points) {
    // Update today's velocity
    today = getCurrentDate()
    `uv run .claude/scripts/state_manager.py increment {SESSION_ID} sprint.metrics.daily_velocity.{today} {points}`
    
    // Update cumulative velocity
    `uv run .claude/scripts/state_manager.py increment {SESSION_ID} sprint.metrics.total_velocity {points}`
    
    // Recalculate averages
    metrics = `uv run .claude/scripts/state_manager.py get {SESSION_ID} sprint.metrics`
    avgVelocity = calculateAverageVelocity(metrics.daily_velocity)
    `uv run .claude/scripts/state_manager.py set {SESSION_ID} sprint.metrics.avg_velocity {avgVelocity}`
  }
  
  projectCompletion() {
    sprint = `uv run .claude/scripts/state_manager.py get {SESSION_ID} sprint`
    velocity = calculateVelocity(sprint)
    
    remaining = sprint.tasks.filter(t => t.status != "done")
    remainingPoints = remaining.reduce((sum, t) => sum + t.points, 0)
    
    daysNeeded = Math.ceil(remainingPoints / velocity.daily)
    completionDate = addDays(getCurrentDate(), daysNeeded)
    
    onTrack = daysNeeded <= sprint.remaining_days
    
    display = """
    ╭─── SPRINT FORECAST ──────────────────────────────────────────────────╮
    │ Current Velocity: {velocity.daily} pts/day                          │
    │ Remaining Work: {remainingPoints} pts                               │
    │ Days Needed: {daysNeeded}                                           │
    │ Sprint Days Left: {sprint.remaining_days}                           │
    │                                                                      │
    │ Projected Completion: {completionDate}                              │
    │ Status: {onTrack ? "✅ ON TRACK" : "⚠️ AT RISK"}                    │
    │                                                                      │
    │ Recommendations:                                                    │
    {generateRecommendations(onTrack, velocity, remainingPoints)}
    ╰──────────────────────────────────────────────────────────────────────╯
    """
    render(display)
  }
  
  openRetrospective() {
    sprint = `uv run .claude/scripts/state_manager.py get {SESSION_ID} sprint`
    
    display = """
    ╭─── SPRINT RETROSPECTIVE: {sprint.name} ─────────────────────────────╮
    │ METRICS SUMMARY                                                      │
    │ Completed: {sprint.completed_points} pts ({sprint.completion_rate}%) │
    │ Velocity: {sprint.avg_velocity} pts/day                             │
    │ Blockers: {sprint.total_blockers}                                   │
    ├───────────────────────────────────────────────────────────────────────┤
    │ WHAT WENT WELL                    │ WHAT DIDN'T GO WELL            │
    │ • {positive_1}                    │ • {negative_1}                  │
    │ • {positive_2}                    │ • {negative_2}                  │
    │ • {positive_3}                    │ • {negative_3}                  │
    ├────────────────────────────────────┴──────────────────────────────────┤
    │ ACTION ITEMS FOR NEXT SPRINT                                         │
    │ 1. {action_item_1}                                                   │
    │ 2. {action_item_2}                                                   │
    │ 3. {action_item_3}                                                   │
    ╰───────────────────────────────────────────────────────────────────────╯
    
    Commands: /save-retro | /next-sprint | /archive
    """
    render(display)
  }
  
  getTaskCard(task) {
    status_icon = getStatusIcon(task.status)
    blocker_icon = task.blocker ? "🔴" : ""
    
    return """
    [{task.id}] {blocker_icon}
    {task.title.substring(0, 15)}
    @{task.assignee || "unassigned"}
    {task.points}pts {status_icon}
    """
  }
  
  getStatusIcon(status) {
    (status == "backlog") => "📋"
    (status == "todo") => "⏳"
    (status == "in_progress") => "🔄"
    (status == "review") => "👁"
    (status == "done") => "✅"
    default => "❓"
  }
  
  init() {
    // Initialize sprint session
    session = `uv run .claude/scripts/session_manager.py init sprint_execution`
    
    // Load current sprint
    currentSprint = `uv run .claude/scripts/state_manager.py get {session} current_sprint`
    
    if (!currentSprint) {
      // Create new sprint if none exists
      createNewSprint()
    }
    
    // Set WIP limits
    `uv run .claude/scripts/state_manager.py set {session} sprint.wip_limits {
      todo: 10,
      in_progress: 5,
      review: 3
    }`
    
    // Set up watchers
    `uv run .claude/scripts/state_manager.py watch {session} sprint.tasks`
    `uv run .claude/scripts/state_manager.py watch {session} sprint.blockers`
    `uv run .claude/scripts/state_manager.py watch {session} sprint.metrics`
    
    // Calculate initial metrics
    calculateInitialMetrics()
    
    // Refresh display
    refreshBoard()
  }
}
```

## Usage

The Sprint Execution board provides a comprehensive Kanban-style interface for managing sprint tasks.

### Starting Sprint Execution

```bash
# Initialize sprint board
uv run .claude/scripts/session_manager.py init sprint_execution

# The board will:
# - Load current sprint or create new one
# - Set up task columns with WIP limits
# - Calculate initial velocity
# - Display interactive Kanban board
```

### Task Management

- **Move Tasks**: `/move TASK-123 in_progress`
- **Assign Work**: `/assign TASK-123 @engineering-fullstack`
- **Block Tasks**: `/block TASK-123 "Waiting for API specs"`
- **Unblock**: `/unblock TASK-123`
- **Estimate**: `/estimate TASK-123 5`

### Automation Features

- **Auto-assign**: `/autoassign` - Optimally distributes tasks based on capacity
- **WIP Limits**: `/wip in_progress 5` - Enforce work-in-progress limits
- **Filtering**: `/filter team:engineering` - Focus on specific work

### Metrics & Forecasting

- **Velocity**: Track points completed per day
- **Burndown**: Visualize progress against ideal
- **Forecast**: Project sprint completion based on current velocity
- **Metrics**: Deep dive into cycle time, lead time, flow efficiency

### Visual Indicators

- 🔴 **Blocked**: Task has a blocker
- 🟡 **At Risk**: Task may not complete in sprint
- 🔄 **In Progress**: Active work
- ✅ **Done**: Completed and verified
- ⚠️ **WIP Limit**: Column at capacity

### Sprint Retrospective

Use `/retro` at sprint end to:
- Review metrics and achievements
- Identify what went well/poorly
- Create action items for improvement
- Archive sprint data

### Integration Points

- `state_manager.py` - Task state persistence
- `event_stream.py` - Activity tracking
- `shared_state.py` - Real-time updates
- `session_manager.py` - Sprint sessions