# V2 Orchestration User Guide

A comprehensive guide to using the V2 orchestration system for enterprise-scale AI-powered development teams.

## Table of Contents

- [Getting Started](#getting-started)
- [Step-by-Step Setup](#step-by-step-setup)
- [Common Workflows](#common-workflows)
- [Command Reference](#command-reference)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

## Getting Started

The V2 orchestration system transforms Claude Code into a sophisticated development team coordination platform using UV scripts, session management, and specialized output styles.

### Prerequisites

- **Claude Code** installed and configured
- **UV** (Python package manager) - `curl -LsSf https://astral.sh/uv/install.sh | sh`
- **Git** for version control
- Basic understanding of command-line interfaces

### Architecture Overview

```
V2 Orchestration System
├── Session Management (.claude/scripts/session_manager.py)
├── State Management (.claude/scripts/state_manager.py)  
├── Shared State (.claude/scripts/shared_state.py)
├── Output Styles (.claude/output-styles/*.md)
└── Integration with Claude Code slash commands
```

## Step-by-Step Setup

### 1. Initialize Your First Session

```bash
# Create a development session for your project
uv run .claude/scripts/session_manager.py create \
  --mode development \
  --project myapp \
  --metadata '{"team": "engineering", "priority": "high"}'

# Expected output:
# ✓ Created session: a1b2c3d4-e5f6-7890-abcd-ef1234567890
#   Mode: development
#   Project: myapp
```

### 2. Verify State Management

```bash
# List all sessions to confirm creation
uv run .claude/scripts/session_manager.py list --active

# Check the session state
uv run .claude/scripts/state_manager.py get SESSION_ID "session"
```

### 3. Configure Project Settings

```bash
# Set up project configuration
uv run .claude/scripts/shared_state.py set-config myapp --data '{
  "settings": {
    "default_sprint_length": 14,
    "velocity_target": 20,
    "team_capacity": 5
  },
  "team": {
    "leads": ["engineering-lead", "product-manager"],
    "members": ["engineering-fullstack", "engineering-ux", "qa-analyst"]
  }
}'
```

### 4. Create Your First Epic and Sprint

```bash
# Create an epic
uv run .claude/scripts/shared_state.py update-epic myapp user-auth \
  --title "User Authentication System" \
  --description "Complete OAuth2 authentication with social login" \
  --priority 1

# Create a sprint for the epic
uv run .claude/scripts/shared_state.py create-sprint myapp sprint-1 \
  "Authentication Sprint" \
  --epic-id user-auth \
  --data '{
    "start_date": "2024-01-15",
    "end_date": "2024-01-29",
    "goals": ["OAuth2 integration", "Social login", "User management"]
  }'
```

### 5. Set Up Output Styles

Switch to the appropriate output style based on your workflow:

```bash
# For sprint management
/output-style sprint_execution

# For leadership oversight  
/output-style leadership_chat

# For multi-team coordination
/output-style all-team_dashboard

# For system configuration
/output-style config_manager
```

## Common Workflows

### Development Workflow

#### 1. Daily Development Session

```bash
# Start your development session
SESSION=$(uv run .claude/scripts/session_manager.py create --mode development --project myapp)

# Check current sprint status
uv run .claude/scripts/state_manager.py get $SESSION "sprint.current"

# Switch to sprint execution view
/output-style sprint_execution

# Begin development work
/orchestrate task delegate "Implement OAuth2 provider integration"
```

#### 2. Task Management in Sprint View

Once in `sprint_execution` output style, you can use built-in commands:

```bash
# Move tasks through the pipeline
/move TASK-123 in_progress
/assign TASK-123 @engineering-fullstack

# Handle blockers
/block TASK-456 "Waiting for API documentation from vendor"
/unblock TASK-456

# Update estimates
/estimate TASK-789 8

# Auto-assign based on capacity
/autoassign

# Check metrics
/metrics
/burndown
/forecast
```

#### 3. Code Review Workflow

```bash
# Create review session
uv run .claude/scripts/session_manager.py create --mode development --project myapp

# Hand off context from development session to review session
uv run .claude/scripts/session_manager.py handoff $DEV_SESSION $REVIEW_SESSION \
  --data '{"review_type": "code", "files": ["auth.py", "login.js"]}'

# Switch to appropriate review agents
/orchestrate team activate engineering
```

### Sprint Management Workflow

#### 1. Sprint Planning

```bash
# Create sprint planning session
SESSION=$(uv run .claude/scripts/session_manager.py create --mode sprint --project myapp)

# Switch to leadership view for planning
/output-style leadership_chat

# Create new sprint
uv run .claude/scripts/shared_state.py create-sprint myapp sprint-2 \
  "Feature Development Sprint" \
  --data '{
    "goals": ["Complete user dashboard", "API optimization", "Testing automation"],
    "capacity": 40,
    "velocity_target": 25
  }'

# Plan epic breakdown
/orchestrate epic plan user-dashboard
```

#### 2. Sprint Execution

```bash
# Switch to execution mode
/output-style sprint_execution

# Monitor daily progress
/metrics
/velocity
/burndown

# Handle impediments
/orchestrate team activate devops  # For infrastructure blockers
/orchestrate team activate qa      # For testing issues
```

#### 3. Sprint Review and Retrospective

```bash
# End of sprint analysis
/retro

# Generate completion report
uv run .claude/scripts/state_manager.py get $SESSION "sprint.metrics"

# Create next sprint
uv run .claude/scripts/shared_state.py create-sprint myapp sprint-3 "Deployment Sprint"

# Archive completed sprint
/archive
```

### Team Coordination Workflow

#### 1. Multi-Team Coordination

```bash
# Create leadership session
SESSION=$(uv run .claude/scripts/session_manager.py create --mode leadership --project myapp)

# Switch to team dashboard
/output-style all-team_dashboard

# Activate multiple teams
/orchestrate team activate engineering
/orchestrate team activate product  
/orchestrate team activate qa

# Coordinate cross-team work
/team handoff product engineering "Feature specifications ready for development"
```

#### 2. Resource Management

```bash
# Check team capacity
/team capacity engineering
/team capacity qa

# Balance workload
/team assign engineering-fullstack TASK-123
/team assign qa-analyst TASK-456

# Monitor team metrics
/monitor agents engineering
/monitor metrics performance
```

### Configuration Management Workflow

#### 1. System Configuration

```bash
# Switch to config management mode
/output-style config_manager

# Validate all configurations
/config validate

# Edit team configurations
/config teams engineering edit

# Auto-fix common issues
/config fix --dry-run
/config fix

# Create configuration backup
/config backup create
```

#### 2. Tool Registration

```bash
# Register new tools and agents
uv run .claude/scripts/shared_state.py register-tool \
  --name "security-scanner" \
  --type agent \
  --description "Automated security vulnerability scanning" \
  --dependencies '["bandit", "safety", "semgrep"]' \
  --config '{"scan_level": "strict", "fail_on": "medium"}'

# List all registered tools
uv run .claude/scripts/shared_state.py list-tools --type agent
```

## Command Reference

### Session Management Commands

```bash
# Create sessions
uv run .claude/scripts/session_manager.py create --mode <MODE> --project <PROJECT>
# Modes: development, leadership, sprint, config

# Session lifecycle
uv run .claude/scripts/session_manager.py heartbeat <SESSION_ID>
uv run .claude/scripts/session_manager.py recover <SESSION_ID>
uv run .claude/scripts/session_manager.py handoff <FROM> <TO>

# List and filter
uv run .claude/scripts/session_manager.py list --active --project <PROJECT>
uv run .claude/scripts/session_manager.py info <SESSION_ID>
```

### State Management Commands

```bash
# Read operations
uv run .claude/scripts/state_manager.py get <SESSION_ID> <PATH>
uv run .claude/scripts/state_manager.py list-sessions

# Write operations  
uv run .claude/scripts/state_manager.py set <SESSION_ID> <PATH> <VALUE>
uv run .claude/scripts/state_manager.py merge <SESSION_ID> <PATH> --data <JSON>
uv run .claude/scripts/state_manager.py delete <SESSION_ID> <PATH>

# Maintenance
uv run .claude/scripts/state_manager.py cleanup-expired
```

### Shared State Commands

```bash
# Project configuration
uv run .claude/scripts/shared_state.py get-config <PROJECT_ID>
uv run .claude/scripts/shared_state.py set-config <PROJECT_ID> --data <JSON>

# Epic management
uv run .claude/scripts/shared_state.py update-epic <PROJECT> <EPIC_ID> --status <STATUS>
uv run .claude/scripts/shared_state.py list-epics <PROJECT> --status <STATUS>

# Sprint management
uv run .claude/scripts/shared_state.py create-sprint <PROJECT> <SPRINT_ID> <NAME>
uv run .claude/scripts/shared_state.py list-sprints <PROJECT> --status <STATUS>

# Tool registry
uv run .claude/scripts/shared_state.py register-tool --name <NAME> --type <TYPE>
uv run .claude/scripts/shared_state.py list-tools --type <TYPE>
uv run .claude/scripts/shared_state.py get-tool <NAME>
```

### Claude Code Slash Commands

#### Core Orchestration Commands
```bash
/orchestrate                    # Main orchestration menu
/orchestrate sprint start      # Start sprint with preview
/orchestrate sprint status     # Sprint progress tracking  
/orchestrate task delegate     # Delegate tasks to teams
/orchestrate team activate     # Activate team coordination
/orchestrate epic plan         # Epic planning and breakdown
/orchestrate stop              # Stop all orchestration
```

#### State Management Commands
```bash
/state                         # State overview and menu
/state get <PATH>             # Query state with dot/JSONPath notation
/state set <PATH> <VALUE>     # Update state values
/state summary                # High-level state dashboard
/state tasks --status <STATUS> # Filtered task views
/state reset                  # Safe state reset with backup
```

#### Monitoring Commands
```bash
/monitor                      # Main monitoring dashboard
/monitor live <SECONDS>       # Live monitoring with refresh
/monitor agents <TEAM>        # Team-specific monitoring
/monitor metrics <TYPE>       # Performance KPIs
/monitor events --follow      # Real-time event stream
```

#### Team Management Commands
```bash
/team                         # Team management overview
/team status                  # All teams status
/team capacity <TEAM>         # Capacity analysis
/team assign <AGENT> <TASK>   # Direct agent assignment
/team handoff <FROM> <TO>     # Cross-team handoffs
```

#### Configuration Commands
```bash
/config                       # Configuration overview
/config validate              # Validate all configurations
/config teams <TEAM> edit     # Edit team configurations
/config fix --dry-run        # Preview auto-fixes
/config backup create         # Configuration backups
```

#### Debug Commands
```bash
/debug                        # System health check
/debug state <COMPONENT>      # Debug state management
/debug events --trace         # Event flow analysis
/debug performance --profile  # Performance bottlenecks
/debug integration --test     # Component integration tests
```

### Output Style Commands

Switch between specialized interfaces optimized for different workflows:

```bash
# Sprint management with Kanban board
/output-style sprint_execution

# Executive dashboard with KPIs
/output-style leadership_chat

# Multi-team coordination view
/output-style all-team_dashboard

# System configuration interface
/output-style config_manager
```

## Best Practices

### Session Management Best Practices

1. **Use Appropriate Session Modes**
   - `development` - Daily coding work (24h expiry)
   - `leadership` - Planning and oversight (48h expiry)  
   - `sprint` - Sprint management (1 week expiry)
   - `config` - System configuration (1h expiry)

2. **Send Regular Heartbeats**
   ```bash
   # Keep long-running sessions alive
   uv run .claude/scripts/session_manager.py heartbeat $SESSION_ID
   ```

3. **Use Session Handoffs for Context Transfer**
   ```bash
   # Transfer work between sessions with context
   uv run .claude/scripts/session_manager.py handoff $OLD_SESSION $NEW_SESSION \
     --data '{"work_completed": "Authentication module", "next_steps": "Testing"}'
   ```

### State Management Best Practices

1. **Use JSONPath for Complex Queries**
   ```bash
   # Get all blocked tasks
   uv run .claude/scripts/state_manager.py get $SESSION "$.sprint.tasks[?(@.status=='blocked')]"
   
   # Get tasks by assignee
   uv run .claude/scripts/state_manager.py get $SESSION "$.sprint.tasks[?(@.assignee=='engineering-lead')]"
   ```

2. **Atomic Updates with Merge Operations**
   ```bash
   # Update multiple fields atomically
   uv run .claude/scripts/state_manager.py merge $SESSION "task.TASK-123" --data '{
     "status": "in_progress",
     "assignee": "engineering-fullstack",
     "updated_at": "2024-01-15T10:30:00Z"
   }'
   ```

3. **Regular Cleanup**
   ```bash
   # Clean up expired sessions weekly
   uv run .claude/scripts/state_manager.py cleanup-expired
   ```

### Team Coordination Best Practices

1. **Use Output Styles Appropriately**
   - Use `sprint_execution` for hands-on development work
   - Use `leadership_chat` for strategic planning and oversight
   - Use `all-team_dashboard` for cross-team coordination
   - Use `config_manager` for system administration

2. **Establish Clear Team Hierarchies**
   ```bash
   # Register team structure in shared state
   uv run .claude/scripts/shared_state.py set-config myapp --data '{
     "team": {
       "engineering": {
         "lead": "engineering-lead",
         "members": ["engineering-fullstack", "engineering-ux"],
         "capacity": 3
       }
     }
   }'
   ```

3. **Monitor Team Velocity and Capacity**
   ```bash
   # Regular capacity checks
   /team capacity engineering
   /monitor metrics performance
   ```

### Error Handling Best Practices

1. **Always Check Session Status**
   ```bash
   # Verify session before operations
   if uv run .claude/scripts/session_manager.py info $SESSION_ID >/dev/null 2>&1; then
     echo "Session is active"
   else
     echo "Session not found or expired"
   fi
   ```

2. **Use Dry Run for Safety**
   ```bash
   # Test configuration changes
   /config fix --dry-run
   
   # Preview state cleanup
   uv run .claude/scripts/state_manager.py cleanup-expired --dry-run
   ```

3. **Regular Backups**
   ```bash
   # Backup configurations
   /config backup create
   
   # Export important state
   uv run .claude/scripts/state_manager.py get $SESSION "" --json-output > session-backup.json
   ```

## Troubleshooting

### Common Issues and Solutions

#### Session Issues

**Problem: Session not found**
```bash
# Check if session exists
uv run .claude/scripts/session_manager.py list --json-output | jq '.[] | select(.id=="'$SESSION_ID'")'

# If expired, create new session
SESSION_ID=$(uv run .claude/scripts/session_manager.py create --mode development --project myapp)
```

**Problem: Session expired unexpectedly**
```bash
# Recover session if possible
uv run .claude/scripts/session_manager.py recover $SESSION_ID

# Send heartbeat to prevent future expiry
uv run .claude/scripts/session_manager.py heartbeat $SESSION_ID
```

#### State Management Issues

**Problem: State file corruption**
```bash
# Check state file integrity
uv run .claude/scripts/state_manager.py get $SESSION_ID "session" --json-output | jq .

# Reset to clean state if needed
uv run .claude/scripts/state_manager.py delete $SESSION_ID "corrupted.path"
```

**Problem: JSONPath queries not working**
```bash
# Test JSONPath syntax
echo '{"test": {"nested": "value"}}' | jq '$.test.nested'

# Use dot notation as fallback
uv run .claude/scripts/state_manager.py get $SESSION_ID "test.nested"
```

#### Integration Issues

**Problem: UV scripts failing**
```bash
# Check UV installation
uv --version

# Verify script permissions
ls -la .claude/scripts/

# Test scripts individually
uv run .claude/scripts/state_manager.py --help
```

**Problem: Output styles not working**
```bash
# Check output style files
ls -la .claude/output-styles/

# Verify file format
head .claude/output-styles/sprint_execution.md

# Reset to default output style
/output-style default
```

### Debug Mode

Enable debug mode for detailed troubleshooting:

```bash
# Set debug environment variable
export CLAUDE_ORCHESTRATION_DEBUG=1

# Enable verbose logging
export CLAUDE_LOG_LEVEL=DEBUG

# Run operations with debug output
uv run .claude/scripts/state_manager.py get $SESSION_ID "sprint" 2>&1 | tee debug.log
```

### Performance Issues

**Problem: Slow state operations**
```bash
# Check state file sizes
du -sh ~/.claude/state/sessions/*

# Clean up old sessions
uv run .claude/scripts/state_manager.py cleanup-expired

# Monitor file locks
lsof ~/.claude/state/sessions/*.lock
```

**Problem: Memory usage**
```bash
# Monitor UV process memory
ps aux | grep "uv run"

# Restart session manager
/orchestrate stop
SESSION_ID=$(uv run .claude/scripts/session_manager.py create --mode development --project myapp)
```

### Getting Help

1. **Check Documentation**
   - [API Reference](API_REFERENCE.md)
   - [Migration Guide](MIGRATION_GUIDE.md)
   - [Main README](../README.md)

2. **Use Built-in Help**
   ```bash
   # Script help
   uv run .claude/scripts/session_manager.py --help
   uv run .claude/scripts/state_manager.py --help
   uv run .claude/scripts/shared_state.py --help
   
   # Claude Code help
   /help
   /debug
   ```

3. **Check System Status**
   ```bash
   # Overall system health
   /debug
   /monitor status
   
   # Component-specific checks
   /debug state orchestrator
   /debug integration --test
   ```

4. **Community Resources**
   - [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)
   - [UV Documentation](https://docs.astral.sh/uv/)
   - [Project Issues](https://github.com/dylan-gluck/cc-dev-team/issues)

---

This user guide provides comprehensive coverage of the V2 orchestration system. For additional technical details, see the [API Reference](API_REFERENCE.md) and [Migration Guide](MIGRATION_GUIDE.md).