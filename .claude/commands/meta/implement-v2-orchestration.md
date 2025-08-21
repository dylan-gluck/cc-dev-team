---
allowed-tools: Task, TodoWrite, Read, LS, Glob
description: Orchestrates complete v2 orchestration system upgrade across all teams
argument-hint: [optional-target-mode]
model: opus
---

# V2 Orchestration System Implementation

This command orchestrates the complete implementation of the v2 orchestration system, coordinating multiple specialized agents to transform the codebase from v1 to v2 architecture.

## Initial Context

- Project root: /Users/dylan/Workspace/claude/agent-workflows/cc-dev-team/
- Implementation docs: @ai_docs/orchestration/v2-implementation-plan.md
- Architecture spec: @ai_docs/orchestration/v2-unified-architecture.md

## Todo Setup

Initialize progress tracking for implementation phases:

<TodoWrite>
# V2 Orchestration Implementation Progress

## Phase 1: Analysis & Preparation
- [ ] Index current v1 implementation state
- [ ] Identify incompatible files for removal
- [ ] Clean up obsolete v1 components

## Phase 2: Core Implementation
- [ ] Implement state_manager.py UV script
- [ ] Implement session_manager.py UV script  
- [ ] Implement shared_state.py UV script
- [ ] Update agents to v2 specifications
- [ ] Create supporting slash commands

## Phase 3: Configuration
- [ ] Update hooks in settings.json
- [ ] Implement SudoLang output styles
- [ ] Configure state persistence paths

## Phase 4: Testing & Documentation
- [ ] Create comprehensive test suite
- [ ] Update all documentation
- [ ] Validate integration points

## Phase 5: Final Review
- [ ] Technical architecture review
- [ ] Business value assessment  
- [ ] Quality assurance review
- [ ] Performance metrics analysis
</TodoWrite>

## Phase 1: Analysis & Preparation

### 1.1 Research Current State

<Task>
You are research-project. Your task is to analyze the current v1 orchestration implementation and identify all components that need updating or removal for v2.

Start by:
cd /Users/dylan/Workspace/claude/agent-workflows/cc-dev-team/

Then analyze these locations:
1. Read all files in .claude/hooks/orchestration/ directory
2. Read .claude/settings.json to understand current hook configurations
3. List all files in .claude/scripts/ to identify existing scripts
4. Read any existing orchestration agents in .claude/agents/meta/
5. Check for any existing output styles in .claude/output-styles/

Create a detailed report with:
- List of v1 files to be removed
- List of hooks that need updating
- Current agent configurations that conflict with v2
- Existing scripts that may interfere

Output format: Structured markdown report saved to ai_docs/orchestration/reports/v1-state-analysis.md

After completion, update the todo item "Index current v1 implementation state" as complete.
</Task>

### 1.2 Clean Up V1 Components

<Task>
You are engineering-cleanup. Your task is to remove all v1 orchestration components that are incompatible with v2.

Start by:
cd /Users/dylan/Workspace/claude/agent-workflows/cc-dev-team/

Read the analysis report: ai_docs/orchestration/reports/v1-state-analysis.md

Then remove these v1 components:
1. Delete any WebSocket-based scripts in .claude/scripts/
2. Remove v1 orchestration hooks from .claude/hooks/orchestration/
3. Clean up any Redis or external service configurations
4. Archive (don't delete) any v1 agent definitions to ai_docs/orchestration/archived/

Important: DO NOT remove:
- User-created agents unrelated to orchestration
- Project-specific configurations
- Non-orchestration hooks

Create a cleanup report listing all removed files at: ai_docs/orchestration/reports/v1-cleanup-complete.md

After completion, update the todo items "Identify incompatible files for removal" and "Clean up obsolete v1 components" as complete.
</Task>

## Phase 2: Core Implementation (Parallel Execution)

### 2.1 UV Scripts Implementation

<Task>
You are meta-script-uv. Your task is to implement the three core UV scripts for state management.

Start by:
cd /Users/dylan/Workspace/claude/agent-workflows/cc-dev-team/

Read the specifications from:
- ai_docs/orchestration/v2-implementation-plan.md (lines 45-105 for state_manager.py spec)
- ai_docs/orchestration/v2-implementation-plan.md (lines 86-105 for session_manager.py spec)  
- ai_docs/orchestration/v2-unified-architecture.md (lines 146-192 for API examples)

Create these three UV scripts in .claude/scripts/:

1. **state_manager.py**
   - Implement get, set, merge, delete operations
   - Add JSONPath query support
   - Include file locking for concurrent access
   - Add list-sessions and cleanup-expired functions

2. **session_manager.py**
   - Implement create, heartbeat, handoff, list functions
   - Support different modes (development, leadership, sprint, config)
   - Include session lifecycle management
   - Add recovery mechanisms

3. **shared_state.py**
   - Implement get-config, update-epic, list-sprints functions
   - Support project-level configuration
   - Include tool registry management
   - Add team configuration support

Each script must:
- Use inline UV script dependencies (no requirements.txt)
- Include comprehensive error handling
- Support --help documentation
- Use atomic file operations
- Return JSON output for programmatic use

After creating all three scripts, update the todo items for UV script implementation as complete.
</Task>

### 2.2 Agent Updates

<Task>
You are meta-agent. Your task is to update and consolidate agents according to v2 specifications.

Start by:
cd /Users/dylan/Workspace/claude/agent-workflows/cc-dev-team/

Read the v2 agent specifications from:
- ai_docs/orchestration/v2-unified-architecture.md (agent hierarchy section)
- Current agent definitions in .claude/agents/

Update these critical agents to support v2 orchestration:

1. **meta/orchestrator.md** - Main orchestration coordinator
   - Add UV script invocation capabilities
   - Include state management patterns
   - Support session awareness

2. **engineering/engineering-lead.md** - Technical coordination
   - Add sprint execution support
   - Include task assignment patterns
   - Support state queries

3. **product/product-director.md** - Strategic planning
   - Add epic management
   - Include roadmap coordination
   - Support shared state updates

For each agent:
- Preserve existing capabilities
- Add v2 state management patterns
- Include session context awareness
- Update tool permissions for UV scripts

After updating agents, update the todo item "Update agents to v2 specifications" as complete.
</Task>

### 2.3 Slash Commands Creation

<Task>
You are meta-command. Your task is to create supporting slash commands for v2 orchestration.

Start by:
cd /Users/dylan/Workspace/claude/agent-workflows/cc-dev-team/

Create these essential commands in .claude/commands/:

1. **/orchestration/start-session**
   - Location: .claude/commands/orchestration/start-session.md
   - Initialize new orchestration session
   - Set mode (development/leadership/sprint/config)
   - Return session ID for tracking

2. **/orchestration/dashboard**
   - Location: .claude/commands/orchestration/dashboard.md
   - Launch interactive dashboard
   - Connect to current session
   - Display real-time state

3. **/orchestration/sprint-board**
   - Location: .claude/commands/orchestration/sprint-board.md
   - Show kanban task board
   - Support task updates
   - Calculate velocity metrics

4. **/orchestration/handoff**
   - Location: .claude/commands/orchestration/handoff.md
   - Transfer session between users
   - Preserve state continuity
   - Document handoff notes

Each command must:
- Include proper YAML frontmatter
- Reference UV scripts for state operations
- Support $ARGUMENTS for dynamic input
- Include usage examples

After creating commands, update the todo item "Create supporting slash commands" as complete.
</Task>

## Phase 3: Configuration

### 3.1 Hook Configuration

<Task>
You are meta-config. Your task is to update the hook system for v2 orchestration.

Start by:
cd /Users/dylan/Workspace/claude/agent-workflows/cc-dev-team/

Read current configuration:
- .claude/settings.json
- ai_docs/orchestration/v2-implementation-plan.md (hook integration section)

Update .claude/settings.json to include v2 hooks:

1. **orchestration:state-changed** hook
   - Trigger on state updates
   - Call state synchronization scripts
   - Update dashboards

2. **orchestration:task-completed** hook
   - Trigger on task status changes
   - Update sprint metrics
   - Notify relevant agents

3. **orchestration:session-created** hook
   - Initialize session state
   - Set up monitoring
   - Configure output styles

Also create hook handler scripts in .claude/hooks/orchestration/:
- state-router.sh - Route state events
- task-handler.sh - Process task updates
- session-init.sh - Initialize new sessions

After updating hooks, update the todo item "Update hooks in settings.json" as complete.
</Task>

### 3.2 Output Styles Implementation

<Task>
You are engineering-lead. Your task is to implement SudoLang output styles for v2 orchestration.

Start by:
cd /Users/dylan/Workspace/claude/agent-workflows/cc-dev-team/

Read the SudoLang specifications from:
- ai_docs/orchestration/v2-implementation-plan.md (lines 109-176 for SudoLang patterns)
- ai_docs/orchestration/v2-unified-architecture.md (lines 94-140 for program structure)

Create these SudoLang output style programs in .claude/output-styles/:

1. **all-team_dashboard.md**
   - Interactive monitoring dashboard
   - Command processing (/team, @agent, #sprint)
   - Real-time state display
   - ASCII art layout

2. **leadership_chat.md**
   - Multi-agent discussion interface
   - Decision tracking
   - Strategic planning tools
   - Consensus building

3. **sprint_execution.md**
   - Kanban board visualization
   - Task assignment automation
   - Velocity calculations
   - Blocker management

4. **config_manager.md**
   - Settings management UI
   - Team configuration
   - Agent pool management
   - Validation and rollback

Each output style must:
- Use SudoLang constraint-based patterns
- Include state integration via UV scripts
- Support interactive commands
- Maintain visual consistency

After creating output styles, update the todo items "Implement SudoLang output styles" and "Configure state persistence paths" as complete.
</Task>

## Phase 4: Testing & Documentation

### 4.1 Test Suite Creation

<Task>
You are qa-scripts. Your task is to create a comprehensive test suite for v2 orchestration.

Start by:
cd /Users/dylan/Workspace/claude/agent-workflows/cc-dev-team/

Create test scripts in .claude/tests/orchestration/:

1. **test_state_manager.py**
   - Test all CRUD operations
   - Verify JSONPath queries
   - Test concurrent access
   - Validate error handling

2. **test_session_manager.py**
   - Test session lifecycle
   - Verify handoff procedures
   - Test recovery mechanisms
   - Validate heartbeat functionality

3. **test_shared_state.py**
   - Test project configuration
   - Verify epic/sprint management
   - Test tool registry
   - Validate team updates

4. **integration_test.sh**
   - Multi-session coordination test
   - State synchronization verification
   - Hook trigger validation
   - Performance benchmarks

Include test scenarios for:
- Session creation and handoff
- Concurrent state updates
- Error recovery
- Performance under load

Create test report at: ai_docs/orchestration/reports/v2-test-results.md

After creating tests, update the todo item "Create comprehensive test suite" as complete.
</Task>

### 4.2 Documentation Update

<Task>
You are engineering-writer. Your task is to update all documentation for v2 orchestration.

Start by:
cd /Users/dylan/Workspace/claude/agent-workflows/cc-dev-team/

Update or create these documentation files:

1. **README.md** (update orchestration section)
   - Add v2 quick start guide
   - Include UV script examples
   - Document output styles
   - Add troubleshooting section

2. **ai_docs/orchestration/USER_GUIDE.md** (create)
   - Step-by-step setup instructions
   - Common workflow examples
   - Command reference
   - Best practices

3. **ai_docs/orchestration/API_REFERENCE.md** (create)
   - UV script API documentation
   - SudoLang program reference
   - Hook specifications
   - State schema documentation

4. **ai_docs/orchestration/MIGRATION_GUIDE.md** (create)
   - V1 to V2 migration steps
   - Compatibility notes
   - Rollback procedures
   - FAQ section

Ensure documentation includes:
- Clear examples with expected outputs
- Troubleshooting common issues
- Performance optimization tips
- Architecture diagrams

After updating documentation, update the todo item "Update all documentation" as complete.
</Task>

## Phase 5: Final Review (Parallel Execution)

### 5.1 Technical Review

<Task>
You are engineering-lead. Conduct a comprehensive technical review of the v2 implementation.

Start by:
cd /Users/dylan/Workspace/claude/agent-workflows/cc-dev-team/

Review these components:
1. All UV scripts in .claude/scripts/
2. SudoLang programs in .claude/output-styles/
3. Hook configurations in .claude/settings.json
4. Test results in ai_docs/orchestration/reports/

Validate:
- Code quality and patterns
- Error handling completeness
- Performance characteristics
- Security considerations
- Integration points

Create technical review report at: ai_docs/orchestration/reports/v2-technical-review.md

Include:
- Architecture assessment
- Code quality metrics
- Performance benchmarks
- Security analysis
- Recommendations for optimization

After review, update the todo item "Technical architecture review" as complete.
</Task>

### 5.2 Business Value Assessment

<Task>
You are product-analyst. Assess the business value and impact of the v2 orchestration system.

Start by:
cd /Users/dylan/Workspace/claude/agent-workflows/cc-dev-team/

Analyze:
1. Implementation complexity reduction (v1 vs v2)
2. Developer productivity improvements
3. Maintenance cost reduction
4. Scalability improvements
5. User experience enhancements

Read:
- ai_docs/orchestration/v2-unified-architecture.md (business impact section)
- ai_docs/orchestration/reports/v2-technical-review.md
- Test results and performance metrics

Create business assessment at: ai_docs/orchestration/reports/v2-business-value.md

Include:
- ROI analysis
- Productivity metrics
- Cost-benefit comparison
- Risk mitigation assessment
- Adoption readiness score

After assessment, update the todo item "Business value assessment" as complete.
</Task>

### 5.3 Quality Assurance Review

<Task>
You are qa-analyst. Perform final quality assurance review of the v2 implementation.

Start by:
cd /Users/dylan/Workspace/claude/agent-workflows/cc-dev-team/

Review:
1. Test coverage reports
2. Error handling scenarios
3. Edge case handling
4. Recovery procedures
5. Documentation completeness

Validate:
- All tests passing
- Code coverage > 80%
- Documentation accuracy
- Error messages clarity
- User experience consistency

Create QA report at: ai_docs/orchestration/reports/v2-qa-final.md

Include:
- Test coverage analysis
- Bug risk assessment
- Documentation gaps
- Usability findings
- Release readiness score

After review, update the todo item "Quality assurance review" as complete.
</Task>

### 5.4 Performance Analysis

<Task>
You are data-analytics. Analyze performance metrics of the v2 orchestration system.

Start by:
cd /Users/dylan/Workspace/claude/agent-workflows/cc-dev-team/

Measure and analyze:
1. State query performance (<50ms target)
2. State update latency (<100ms target)
3. Dashboard refresh time (<500ms target)
4. Session creation time (<200ms target)
5. Concurrent operation handling

Read test results from:
- ai_docs/orchestration/reports/v2-test-results.md
- Integration test outputs

Create performance report at: ai_docs/orchestration/reports/v2-performance-metrics.md

Include:
- Performance benchmarks vs targets
- Bottleneck identification
- Optimization recommendations
- Scalability projections
- Resource utilization analysis

After analysis, update the todo item "Performance metrics analysis" as complete.
</Task>

## Success Criteria

The v2 orchestration implementation is complete when:

1. ✅ All UV scripts functioning correctly
2. ✅ SudoLang output styles implemented
3. ✅ Hooks configured and tested
4. ✅ All tests passing with >80% coverage
5. ✅ Documentation complete and accurate
6. ✅ Performance targets met
7. ✅ All review reports positive

## Error Handling

If any phase fails:
1. Check error logs in ai_docs/orchestration/reports/
2. Review specific agent outputs for detailed errors
3. Rollback changes if critical failure occurs
4. Escalate blockers to user for resolution

## Completion

Upon successful completion:
1. All todos marked complete
2. V2 system fully operational
3. Documentation updated
4. Teams ready for v2 workflows

The system will provide a final summary report consolidating all phase outcomes.