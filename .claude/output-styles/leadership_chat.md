# Leadership Chat Output Style

```sudolang
interface LeadershipChat {
  name = "leadership_chat"
  description = "Multi-agent strategic discussion interface for leadership team coordination and decision making"
  
  constraints {
    Maintain threaded conversation structure
    Track decisions with voting and consensus
    Show participant status and engagement
    Support async and sync discussion modes
    Record all strategic decisions in state
    Enable resource allocation discussions
    Never lose discussion context
    Highlight action items and blockers
  }
  
  layout = """
  ╭─── LEADERSHIP STRATEGIC CHAT ───────────────────────────────────────────╮
  │ Session: {session_id}    Topic: {current_topic}    Mode: {chat_mode}    │
  ├──────────────────────────────────────────────────────────────────────────┤
  │ PARTICIPANTS                      │ AGENDA                              │
  │ ├─ @product-director [active]     │ 1. {agenda_item_1} [{status}]      │
  │ ├─ @engineering-director [active] │ 2. {agenda_item_2} [{status}]      │
  │ ├─ @qa-director [typing...]       │ 3. {agenda_item_3} [{status}]      │
  │ ├─ @devops-manager [active]       │ 4. {agenda_item_4} [{status}]      │
  │ └─ @creative-director [away]      │                                     │
  ├──────────────────────────────────────────────────────────────────────────┤
  │ DISCUSSION THREAD                                                        │
  ├──────────────────────────────────────────────────────────────────────────┤
  {discussion_messages}
  ├──────────────────────────────────────────────────────────────────────────┤
  │ DECISION TRACKING                                                        │
  │ ┌────────────────────────────────────────────────────────────────────┐  │
  │ │ {current_decision}                                                  │  │
  │ │ Votes: ✓ {yes_count} | ✗ {no_count} | ◯ {abstain_count}           │  │
  │ │ Consensus: {consensus_level}% | Status: {decision_status}          │  │
  │ └────────────────────────────────────────────────────────────────────┘  │
  ├──────────────────────────────────────────────────────────────────────────┤
  │ ACTION ITEMS                       │ RESOURCE ALLOCATION                │
  │ • {action_1} (@{owner_1})         │ Budget: ${budget_allocated}        │
  │ • {action_2} (@{owner_2})         │ Team: {team_hours}h                │
  │ • {action_3} (@{owner_3})         │ Timeline: {timeline_days}d         │
  ╰──────────────────────────────────────────────────────────────────────────╯
  
  Commands: /vote | /propose | /assign | /resources | /consensus | /summary
  > {command_prompt}
  """
  
  commands = {
    "/vote <yes|no|abstain>": "Cast vote on current decision",
    "/propose <decision>": "Propose new decision for voting",
    "/assign <@agent> <task>": "Assign action item to agent",
    "/resources": "Open resource allocation discussion",
    "/consensus": "Check consensus on current topic",
    "/summary": "Generate discussion summary",
    "/agenda <add|remove|next>": "Manage meeting agenda",
    "/invite @<agent>": "Invite agent to discussion",
    "/async": "Switch to async discussion mode",
    "/sync": "Switch to sync discussion mode",
    "/history": "View decision history",
    "/export": "Export discussion transcript"
  }
  
  stateIntegration = {
    fetch: "uv run .claude/scripts/state_manager.py get {SESSION_ID} leadership",
    update: "uv run .claude/scripts/state_manager.py set {SESSION_ID} leadership.{path} {value}",
    watch: "uv run .claude/scripts/state_manager.py watch {SESSION_ID} leadership.discussion",
    broadcast: "uv run .claude/scripts/shared_state.py broadcast leadership {message}",
    decisions: "uv run .claude/scripts/state_manager.py get {SESSION_ID} leadership.decisions"
  }
  
  processInput(input) {
    // Voting commands
    (input starts with "/vote ") => {
      vote = extractVote(input)
      castVote(getCurrentUser(), vote)
    }
    
    // Decision management
    (input starts with "/propose ") => {
      decision = extractDecision(input)
      proposeDecision(decision)
    }
    
    // Task assignment
    (input starts with "/assign ") => {
      [agent, task] = extractAssignment(input)
      assignActionItem(agent, task)
    }
    
    // Resource discussions
    (input == "/resources") => openResourceAllocation()
    
    // Consensus checking
    (input == "/consensus") => calculateConsensus()
    
    // Summary generation
    (input == "/summary") => generateSummary()
    
    // Agenda management
    (input starts with "/agenda ") => {
      action = extractAgendaAction(input)
      manageAgenda(action)
    }
    
    // Participant management
    (input starts with "/invite ") => {
      agent = extractAgentName(input)
      inviteParticipant(agent)
    }
    
    // Mode switching
    (input == "/async") => switchToAsync()
    (input == "/sync") => switchToSync()
    
    // History and export
    (input == "/history") => showDecisionHistory()
    (input == "/export") => exportTranscript()
    
    // Regular message
    (input doesn't start with "/") => {
      postMessage(getCurrentUser(), input)
    }
    
    default => showSuggestions(input)
  }
  
  postMessage(sender, message) {
    // Add to discussion thread
    timestamp = getCurrentTimestamp()
    
    discussionEntry = {
      timestamp: timestamp,
      sender: sender,
      message: message,
      type: detectMessageType(message)
    }
    
    // Update state
    `uv run .claude/scripts/state_manager.py append {SESSION_ID} leadership.discussion {discussionEntry}`
    
    // Broadcast to participants
    `uv run .claude/scripts/shared_state.py broadcast leadership.message {discussionEntry}`
    
    // Check for decision triggers
    if (message contains "DECISION:" || message contains "PROPOSAL:") {
      extractAndProposeDecision(message)
    }
    
    // Update display
    refreshDiscussion()
  }
  
  proposeDecision(decision) {
    proposal = {
      id: generateId(),
      text: decision,
      proposer: getCurrentUser(),
      timestamp: getCurrentTimestamp(),
      votes: {},
      status: "voting",
      consensus: 0
    }
    
    // Set as current decision
    `uv run .claude/scripts/state_manager.py set {SESSION_ID} leadership.current_decision {proposal}`
    
    // Notify all participants
    `uv run .claude/scripts/shared_state.py broadcast leadership.decision_proposed {proposal}`
    
    // Start voting timer (5 minutes default)
    startVotingTimer(proposal.id, 300)
  }
  
  castVote(user, vote) {
    // Update vote in current decision
    `uv run .claude/scripts/state_manager.py set {SESSION_ID} leadership.current_decision.votes.{user} {vote}`
    
    // Calculate new consensus
    consensus = calculateConsensus()
    
    // Check if all have voted
    if (allParticipantsVoted()) {
      finalizeDecision()
    }
    
    // Update display
    refreshDecisionTracking()
  }
  
  calculateConsensus() {
    decision = `uv run .claude/scripts/state_manager.py get {SESSION_ID} leadership.current_decision`
    
    votes = decision.votes
    total = Object.keys(votes).length
    yes = Object.values(votes).filter(v => v == "yes").length
    
    consensus = (total > 0) ? ((yes / total) * 100).toFixed(0) : 0
    
    // Update consensus level
    `uv run .claude/scripts/state_manager.py set {SESSION_ID} leadership.current_decision.consensus {consensus}`
    
    return consensus
  }
  
  finalizeDecision() {
    decision = `uv run .claude/scripts/state_manager.py get {SESSION_ID} leadership.current_decision`
    
    consensus = calculateConsensus()
    
    // Determine outcome
    if (consensus >= 75) {
      decision.status = "approved"
    } else if (consensus >= 50) {
      decision.status = "conditional"
    } else {
      decision.status = "rejected"
    }
    
    // Archive decision
    `uv run .claude/scripts/state_manager.py append {SESSION_ID} leadership.decisions {decision}`
    
    // Clear current decision
    `uv run .claude/scripts/state_manager.py set {SESSION_ID} leadership.current_decision null`
    
    // Notify participants
    `uv run .claude/scripts/shared_state.py broadcast leadership.decision_finalized {decision}`
    
    // Create action items if approved
    if (decision.status == "approved") {
      createActionItems(decision)
    }
  }
  
  openResourceAllocation() {
    display = """
    ╭─── RESOURCE ALLOCATION PLANNER ─────────────────────────────────────╮
    │ Available Resources                                                 │
    ├──────────────────────────────────────────────────────────────────────┤
    │ BUDGET                            │ TEAM CAPACITY                   │
    │ Total: ${total_budget}            │ Engineering: {eng_hours}h      │
    │ Allocated: ${allocated}           │ Product: {prod_hours}h         │
    │ Remaining: ${remaining}           │ QA: {qa_hours}h                │
    │                                   │ DevOps: {devops_hours}h        │
    ├──────────────────────────────────────────────────────────────────────┤
    │ PROPOSED ALLOCATION                                                 │
    │ Feature A: ${feature_a_budget} | {feature_a_hours}h                │
    │ Feature B: ${feature_b_budget} | {feature_b_hours}h                │
    │ Infrastructure: ${infra_budget} | {infra_hours}h                   │
    ├──────────────────────────────────────────────────────────────────────┤
    │ Commands: /allocate <item> <budget> <hours> | /optimize | /approve │
    ╰──────────────────────────────────────────────────────────────────────╯
    """
    render(display)
  }
  
  generateSummary() {
    discussion = `uv run .claude/scripts/state_manager.py get {SESSION_ID} leadership.discussion`
    decisions = `uv run .claude/scripts/state_manager.py get {SESSION_ID} leadership.decisions`
    
    summary = """
    ## Leadership Discussion Summary
    
    ### Key Topics Discussed
    {extractTopics(discussion)}
    
    ### Decisions Made
    {decisions.map(d => 
      - {d.text} [{d.status}] (Consensus: {d.consensus}%)
    )}
    
    ### Action Items
    {extractActionItems(discussion)}
    
    ### Resource Allocations
    {extractResourceAllocations(discussion)}
    
    ### Next Steps
    {extractNextSteps(discussion)}
    
    Generated: {getCurrentTimestamp()}
    """
    
    // Save summary
    `uv run .claude/scripts/state_manager.py set {SESSION_ID} leadership.last_summary {summary}`
    
    return summary
  }
  
  switchToAsync() {
    // Enable async discussion mode
    `uv run .claude/scripts/state_manager.py set {SESSION_ID} leadership.mode async`
    
    // Adjust voting timers to 24 hours
    setDefaultVotingTimer(86400)
    
    // Notify participants
    `uv run .claude/scripts/shared_state.py broadcast leadership.mode_change async`
  }
  
  switchToSync() {
    // Enable sync discussion mode
    `uv run .claude/scripts/state_manager.py set {SESSION_ID} leadership.mode sync`
    
    // Adjust voting timers to 5 minutes
    setDefaultVotingTimer(300)
    
    // Notify participants
    `uv run .claude/scripts/shared_state.py broadcast leadership.mode_change sync`
  }
  
  formatMessage(entry) {
    indicator = getParticipantIndicator(entry.sender)
    
    (entry.type == "decision") => """
    │ {indicator} {entry.sender} [{entry.timestamp}]
    │ 📋 DECISION: {entry.message}
    """
    
    (entry.type == "action") => """
    │ {indicator} {entry.sender} [{entry.timestamp}]
    │ ⚡ ACTION: {entry.message}
    """
    
    (entry.type == "resource") => """
    │ {indicator} {entry.sender} [{entry.timestamp}]
    │ 💰 RESOURCE: {entry.message}
    """
    
    default => """
    │ {indicator} {entry.sender} [{entry.timestamp}]
    │ {entry.message}
    """
  }
  
  getParticipantIndicator(participant) {
    status = getParticipantStatus(participant)
    
    (status == "active") => "●"
    (status == "typing") => "◉"
    (status == "away") => "○"
    default => "◌"
  }
  
  init() {
    // Initialize leadership session
    session = `uv run .claude/scripts/session_manager.py init leadership_chat`
    
    // Set default mode
    `uv run .claude/scripts/state_manager.py set {session} leadership.mode sync`
    
    // Initialize participants
    participants = ["product-director", "engineering-director", "qa-director", "devops-manager"]
    `uv run .claude/scripts/state_manager.py set {session} leadership.participants {participants}`
    
    // Set up watchers
    `uv run .claude/scripts/state_manager.py watch {session} leadership.discussion`
    `uv run .claude/scripts/state_manager.py watch {session} leadership.current_decision`
    
    // Initial display
    refreshDisplay()
  }
}
```

## Usage

The Leadership Chat interface enables strategic discussions and decision-making among team leaders.

### Starting a Leadership Session

```bash
# Initialize leadership chat
uv run .claude/scripts/session_manager.py init leadership_chat

# The chat will automatically:
# - Create a leadership session
# - Invite default participants
# - Set up discussion thread
# - Enable decision tracking
```

### Discussion Modes

- **Sync Mode**: Real-time discussion with 5-minute voting windows
- **Async Mode**: Extended discussion with 24-hour voting windows

### Decision Process

1. **Propose**: `/propose We should adopt TypeScript for the frontend`
2. **Discuss**: Team members discuss pros and cons
3. **Vote**: `/vote yes` or `/vote no` or `/vote abstain`
4. **Consensus**: Automatic calculation when all vote or timer expires
5. **Action**: Approved decisions create action items

### Resource Allocation

Use `/resources` to open the allocation planner for:
- Budget distribution
- Team capacity planning
- Timeline management
- Priority adjustments

### Consensus Levels

- **75%+**: Full approval, proceed with implementation
- **50-74%**: Conditional approval, may need refinement
- **<50%**: Rejected, requires rework or abandonment

### Integration Points

- `state_manager.py` - Decision persistence
- `shared_state.py` - Real-time participant sync
- `event_stream.py` - Discussion history
- `session_manager.py` - Session management