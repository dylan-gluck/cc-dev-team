# Orchestration System Quick Start Guide

A hands-on guide to getting the Claude Code orchestration system running immediately. This system enables multi-team software development with specialized AI agents working in parallel.

## Prerequisites

Before starting, ensure you have these tools installed:

### Required Dependencies
```bash
# 1. Python 3.11+ with uv (Python package management)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. jq (JSON processing - used extensively by orchestration scripts)
# macOS:
brew install jq
# Ubuntu/Debian:
sudo apt install jq
# Or download from: https://jqlang.github.io/jq/

# 3. Basic development tools
git --version  # Should be available
```

### Verification
```bash
# Test that prerequisites work
uv --version      # Should show uv version
jq --version      # Should show jq version
python3 --version # Should show Python 3.11+
```

## Initial Setup

### 1. Install the Orchestration System

For a new project:
```bash
# Clone or copy the cc-dev-team scaffolding
git clone <this-repo> cc-dev-team
cd cc-dev-team

# Install to your project
uv run scripts/install.py /path/to/your/project

# Or install globally for all Claude Code projects
uv run scripts/install.py --global
```

### 2. Create Orchestration Directory Structure

The installer creates this structure:
```
your-project/
├── .claude/
│   ├── orchestration/          # Configuration (version controlled)
│   │   ├── teams.json         # Team definitions
│   │   ├── workflows.json     # Sprint/epic workflows
│   │   └── settings.json      # Global settings
│   ├── state/                 # Runtime state (gitignored)
│   │   └── orchestration.json # Current state
│   ├── agents/                # AI agent definitions
│   ├── commands/              # Slash commands
│   └── scripts/               # Orchestration scripts
└── .gitignore                 # Excludes state files
```

### 3. Make Scripts Executable

```bash
# Ensure orchestration scripts are executable
chmod +x .claude/scripts/state_manager.py
chmod +x .claude/scripts/message_bus.py
chmod +x .claude/scripts/event_stream.py
chmod +x .claude/scripts/observability.py

# Verify scripts work
.claude/scripts/state_manager.py --help
.claude/scripts/observability.py --help
```

### 4. Validate Configuration

```bash
# Check that JSON configuration is valid
jq . .claude/orchestration/*.json

# Initialize state management
.claude/scripts/state_manager.py get
```

## Basic Usage Examples

### State Management Operations

```bash
# Initialize and view current state
.claude/scripts/state_manager.py get --format=table

# Get specific state information
.claude/scripts/state_manager.py get "agents.active"
.claude/scripts/state_manager.py get "sprints"

# Set state values
.claude/scripts/state_manager.py set "organization.name" '"My Company"'
.claude/scripts/state_manager.py set "projects.current.name" '"E-Commerce Platform"'

# Update task status
.claude/scripts/state_manager.py update-task task-123 in_progress

# Update agent status
.claude/scripts/state_manager.py update-agent engineering-fullstack-1 --status=busy
```

### Message Bus Communication

```bash
# Send a message between agents
.claude/scripts/message_bus.py send \
  engineering-ux \
  engineering-fullstack \
  ARTIFACT_READY \
  '{"component": "LoginForm.tsx", "location": "src/components/"}'

# Send high-priority message
.claude/scripts/message_bus.py send \
  engineering-fullstack \
  engineering-lead \
  REVIEW_REQUEST \
  '{"task": "oauth-implementation", "files": ["src/auth/*.ts"]}' \
  --priority=high

# Check messages for an agent
.claude/scripts/message_bus.py receive engineering-lead --format=table

# Broadcast to all active agents
.claude/scripts/message_bus.py broadcast \
  system \
  SPRINT_STARTED \
  '{"sprint_id": "sprint-3", "start_date": "2025-01-20"}'

# Check queue status
.claude/scripts/message_bus.py queue-status engineering-fullstack
```

### Event Streaming and Monitoring

```bash
# Emit events to the stream
.claude/scripts/event_stream.py emit task_completed \
  '{"task_id": "task-123", "agent": "engineering-ux", "duration": "45min"}'

.claude/scripts/event_stream.py emit sprint_milestone \
  '{"sprint": "sprint-3", "milestone": "ui_components_complete"}'

# Watch event stream live
.claude/scripts/event_stream.py stream --follow

# View recent events
.claude/scripts/event_stream.py stream --tail=20
```

### Observability Dashboard

```bash
# Quick system status
.claude/scripts/observability.py status --format=summary

# Detailed status tables
.claude/scripts/observability.py status

# Sprint-specific view
.claude/scripts/observability.py sprint sprint-3

# Live monitoring dashboard (updates every 30 seconds)
.claude/scripts/observability.py monitor --interval=30

# Calculate and display metrics
.claude/scripts/observability.py metrics --days=7
```

## Common Workflows

### Starting a Sprint

1. **Configure Your Team** (edit `.claude/orchestration/teams.json`):
```json
{
  "teams": {
    "engineering": {
      "orchestrator": "engineering-director",
      "members": [
        {
          "agent": "engineering-fullstack",
          "capacity": 2,
          "skills": ["frontend", "backend"]
        },
        {
          "agent": "engineering-ux",
          "capacity": 1,
          "skills": ["ui", "components"]
        }
      ]
    }
  }
}
```

2. **Create Sprint Definition**:
```bash
# Set up sprint in state
.claude/scripts/state_manager.py set "sprints.sprint-3" '{
  "id": "sprint-3",
  "status": "planning",
  "start_date": "2025-01-20",
  "end_date": "2025-02-03",
  "tasks": {
    "queued": ["task-oauth", "task-ui-login"],
    "active": [],
    "completed": []
  }
}'
```

3. **Use Orchestration Commands** (in Claude Code):
```
/orchestrate sprint start sprint-3
```

This shows a preview, asks for confirmation, then spawns agents.

### Delegating Tasks

1. **Manual Task Delegation**:
```
/orchestrate task delegate "Implement OAuth2 login flow with React components"
```

2. **Monitor Task Progress**:
```bash
# Check task status
.claude/scripts/state_manager.py get "tasks"

# Watch for task updates
.claude/scripts/event_stream.py stream --follow | grep task
```

3. **Handle Task Completion**:
```bash
# Mark task complete
.claude/scripts/state_manager.py update-task task-oauth completed

# This automatically triggers notifications to other agents
```

### Monitoring Progress

```bash
# Real-time system overview
.claude/scripts/observability.py status

# Sprint burndown
.claude/scripts/observability.py sprint

# Agent activity
.claude/scripts/state_manager.py get "agents.active" --format=table

# Recent communications
.claude/scripts/message_bus.py receive orchestrator
```

### Handling Handoffs Between Agents

1. **Agent A completes work and signals handoff**:
```bash
.claude/scripts/message_bus.py send \
  engineering-ux \
  engineering-fullstack \
  ARTIFACT_READY \
  '{"artifact": "components/LoginForm.tsx", "task": "task-oauth", "status": "ready_for_integration"}'
```

2. **Agent B receives notification**:
```bash
.claude/scripts/message_bus.py receive engineering-fullstack
```

3. **Agent B acknowledges and begins work**:
```bash
.claude/scripts/message_bus.py send \
  engineering-fullstack \
  engineering-ux \
  ARTIFACT_RECEIVED \
  '{"artifact": "components/LoginForm.tsx", "status": "integrating"}'

# Update state
.claude/scripts/state_manager.py update-agent engineering-fullstack --status=busy
```

## Troubleshooting

### Common Issues and Solutions

#### 1. "jq: command not found"
```bash
# Install jq
brew install jq  # macOS
sudo apt install jq  # Ubuntu
```

#### 2. "Permission denied" on scripts
```bash
# Make scripts executable
chmod +x .claude/scripts/*.py
```

#### 3. "State file not found"
```bash
# Initialize state
.claude/scripts/state_manager.py get
# This creates the state file if it doesn't exist
```

#### 4. "Invalid JSON" errors
```bash
# Validate configuration files
jq . .claude/orchestration/teams.json
jq . .claude/orchestration/workflows.json
jq . .claude/orchestration/settings.json

# Fix JSON syntax errors and try again
```

#### 5. Messages not reaching agents
```bash
# Check message queue
.claude/scripts/message_bus.py queue-status agent-name

# Check if agent is registered as active
.claude/scripts/state_manager.py get "agents.active"
```

#### 6. Orchestration commands not working
```bash
# Check if you're in a project with .claude/ directory
ls .claude/

# Verify configuration is valid
jq . .claude/orchestration/*.json

# Try manual state operations first
.claude/scripts/state_manager.py get
```

### Debug Mode

Enable verbose logging:
```bash
# Set debug environment variable
export CLAUDE_ORCHESTRATION_DEBUG=1

# Run any orchestration command to see detailed logs
.claude/scripts/state_manager.py get --format=table
```

### Reset State

If you need to start fresh:
```bash
# Backup current state
cp .claude/state/orchestration.json .claude/state/orchestration.backup.json

# Reset to empty state
rm .claude/state/orchestration.json
.claude/scripts/state_manager.py get
```

## Quick Reference

### Essential Commands
```bash
# State management
.claude/scripts/state_manager.py get [path]
.claude/scripts/state_manager.py set path value
.claude/scripts/state_manager.py update-task task-id status

# Communication
.claude/scripts/message_bus.py send from to type payload
.claude/scripts/message_bus.py receive agent-id

# Monitoring
.claude/scripts/observability.py status
.claude/scripts/observability.py monitor

# Events
.claude/scripts/event_stream.py emit type data
.claude/scripts/event_stream.py stream --follow
```

### Key File Locations
- **Configuration**: `.claude/orchestration/*.json` (edit these)
- **State**: `.claude/state/orchestration.json` (auto-managed)
- **Scripts**: `.claude/scripts/*.py` (orchestration tools)
- **Agents**: `.claude/agents/*.md` (AI agent definitions)

### Next Steps

1. **Start Small**: Begin with single-agent tasks before full orchestration
2. **Customize Teams**: Edit `.claude/orchestration/teams.json` for your project
3. **Monitor Everything**: Use the observability dashboard to understand system behavior
4. **Iterate**: Gradually increase automation as you become comfortable

For detailed technical specifications, see `ai_docs/ORCHESTRATION_SPEC.md`.