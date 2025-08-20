---
allowed-tools: Read, Bash(echo:*), Bash(cat:*), Bash(.claude/scripts/state_manager.py:*), Bash(.claude/scripts/orchestrate.py:*), Bash(.claude/scripts/observability.py:*)
description: Main orchestration menu and system status overview
model: haiku
---

# Orchestration Control Center

Display the main orchestration menu and current system status.

## Context Gathering

Check current orchestration state:
- Active teams: !`.claude/scripts/state_manager.py get agents.active --format table`
- Current sprints: !`.claude/scripts/state_manager.py get sprints --format table`
- System metrics: !`.claude/scripts/observability.py status --format summary`

## Main Menu

Display interactive orchestration menu with the following options:

### 🚀 Sprint Management
- **Start Sprint** - Initialize a new sprint with team orchestration
- **Sprint Status** - View current sprint progress and metrics
- **Sprint Stop** - Gracefully stop active sprint

### 👥 Team Coordination
- **Activate Team** - Activate a specific team for coordination
- **Task Delegate** - Delegate tasks to appropriate teams
- **Team Status** - View team capacity and assignments

### 📋 Epic Planning
- **Plan Epic** - Break down epic into sprints with team assignments
- **Epic Status** - View epic progress across sprints

### 📊 System Overview
- **Agents Status** - Show all active agents and their tasks
- **Metrics Dashboard** - Display system performance metrics
- **Event Stream** - View recent orchestration events

### ⚙️ Configuration
- **Show Config** - Display current orchestration settings
- **Reload Config** - Reload configuration from files
- **Mode Settings** - View/change orchestration mode

### 🛑 Control
- **Stop All** - Gracefully stop all orchestration activities
- **Clear State** - Reset orchestration state (requires confirmation)

## Status Summary

Provide a comprehensive status overview including:

1. **Active Operations**
   - Running sprints with progress
   - Active teams and their orchestrators
   - Agents currently executing tasks

2. **Resource Usage**
   - Total active agents vs. limits
   - Token usage vs. budget
   - Runtime vs. limits

3. **Task Pipeline**
   - Queued tasks
   - In-progress tasks
   - Completed tasks
   - Blocked tasks

4. **Health Indicators**
   - Test coverage status
   - Build success rate
   - Agent utilization
   - Error rate

## Quick Actions

Suggest relevant quick actions based on current state:
- If no sprint active: "Start a new sprint"
- If tasks blocked: "Review blocked tasks"
- If agents idle: "Delegate pending tasks"
- If sprint complete: "Start sprint review"

## Command Help

Provide usage examples:
```
/orchestrate                     # Show this menu
/orchestrate sprint start        # Start new sprint
/orchestrate sprint status       # Check sprint progress
/orchestrate task delegate       # Delegate a task
/orchestrate team activate       # Activate a team
/orchestrate epic plan          # Plan an epic
/orchestrate agents status      # Show all agents
/orchestrate stop               # Stop everything
```

## Interactive Selection

If user input is empty ($ARGUMENTS), present numbered menu for selection:
1. Start Sprint
2. Check Sprint Status
3. Delegate Task
4. Activate Team
5. Plan Epic
6. View Agents
7. Show Metrics
8. Stop Orchestration
9. Exit

Wait for user selection and provide guidance on next steps.

## Display Format

Use rich formatting with:
- ✅ Green for active/healthy items
- ⚠️ Yellow for warnings or pending items
- ❌ Red for errors or blocked items
- 📊 Charts/tables for metrics
- 🎯 Clear action items
- 💡 Helpful tips and suggestions

## Error Handling

Check for common issues:
- No configuration files found
- State file corrupted
- No teams configured
- Resource limits exceeded

Provide clear remediation steps for any issues found.