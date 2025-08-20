---
allowed-tools: Task, Read, Bash(.claude/scripts/state_manager.py:*), Bash(.claude/scripts/event_stream.py:*), Bash(.claude/scripts/message_bus.py:*), Bash(.claude/scripts/observability.py:*), Bash(echo:*), Write
description: Gracefully stop current sprint with confirmation and summary
argument-hint: [sprint-id] [--force]
model: sonnet
---

# Stop Sprint Orchestration

Gracefully stop the current sprint, save state, and generate summary report.

## Arguments
- Sprint ID: $ARGUMENTS (optional - defaults to active sprint)
- Force flag: --force (skip confirmation)

## Pre-Stop Analysis

### 1. Identify Active Sprint
Find sprint to stop:
- Check for sprint ID in arguments
- Otherwise find active sprint: !`.claude/scripts/state_manager.py get sprints`
- Verify sprint exists and is active

### 2. Current State Assessment
Gather current sprint state:
- Active agents: !`.claude/scripts/state_manager.py get agents.active --format table`
- Task status: !`.claude/scripts/observability.py sprint [sprint-id]`
- Pending communications: !`.claude/scripts/message_bus.py queue_status broadcast`

## Stop Impact Analysis

### Display What Will Be Stopped

```
┌─────────────────────────────────────────────────┐
│           SPRINT STOP CONFIRMATION              │
├─────────────────────────────────────────────────┤
│ Sprint: [sprint-id]                             │
│ Status: Active                                  │
│ Duration: 5 days (35% complete)                 │
│                                                  │
│ This will stop:                                 │
│ • 8 active agents                               │
│ • 3 in-progress tasks                           │
│ • 2 team orchestrators                          │
│                                                  │
│ Current Progress:                               │
│ • Completed: 9 tasks                            │
│ • In Progress: 3 tasks                          │
│ • Queued: 5 tasks                               │
│ • Blocked: 1 task                               │
│                                                  │
│ ⚠️ In-progress work will be saved but halted    │
└─────────────────────────────────────────────────┤
```

### Confirmation Prompt (unless --force)

```
Are you sure you want to stop this sprint?

This action will:
✓ Save all current progress
✓ Generate completion report
✓ Archive sprint data
✗ Stop all active agents
✗ Halt in-progress tasks
✗ Cancel queued tasks

Type 'yes' to confirm or 'no' to cancel:
```

## Graceful Shutdown Process

### 1. Send Stop Signals
Notify all active agents to wrap up:

```python
# Broadcast stop signal to all agents
for agent in active_agents:
    send_message(agent, "STOP_SIGNAL", {
        "action": "graceful_shutdown",
        "save_state": true,
        "timeout": 60
    })
```

Use: !`.claude/scripts/message_bus.py broadcast orchestrator STOP_SIGNAL '{"action": "graceful_shutdown"}' --priority critical`

### 2. Wait for Agent Acknowledgment
Monitor agent responses (with timeout):
- Give agents 60 seconds to save state
- Track acknowledgments
- Force stop any non-responsive agents

### 3. Save Task States
Update all task statuses:
- In-progress → paused
- Queued → backlog
- Active → interrupted

```bash
# Update each in-progress task
for task in in_progress_tasks:
    !`.claude/scripts/state_manager.py update-task [task-id] paused`
```

### 4. Archive Sprint Data
Create sprint archive:

```python
sprint_archive = {
    "sprint_id": sprint_id,
    "stop_time": current_time,
    "stop_reason": "user_requested",
    "final_state": {
        "completed_tasks": completed_list,
        "interrupted_tasks": interrupted_list,
        "cancelled_tasks": cancelled_list,
        "metrics": final_metrics
    },
    "agent_states": agent_final_states,
    "artifacts": generated_artifacts
}
```

Save archive: !`.claude/scripts/state_manager.py set "archive.sprints.[sprint-id]" '[archive-data]'`

### 5. Generate Completion Report

Create comprehensive sprint report:

```markdown
# Sprint [sprint-id] Completion Report

## Summary
- Start Date: [start-date]
- Stop Date: [stop-date]
- Duration: [days] days
- Completion: [percentage]%

## Achievements
### Completed Tasks (9)
1. ✅ task-1: OAuth implementation
2. ✅ task-2: UI components
3. ✅ task-3: Database schema
...

### Partial Progress (3)
1. 🔄 task-4: API endpoints (75% complete)
2. 🔄 task-5: Integration tests (50% complete)
3. 🔄 task-6: Documentation (30% complete)

### Not Started (5)
1. ⏸️ task-7: Performance optimization
2. ⏸️ task-8: Security review
...

## Metrics
- Sprint Velocity: 8 points
- Task Completion Rate: 53%
- Test Coverage: 72%
- Token Usage: 68,420 tokens
- Total Runtime: 4.5 hours

## Team Performance
- Engineering: 67% tasks completed
- QA: 40% tasks completed
- Product: 100% tasks completed

## Artifacts Generated
- Code Files: 23
- Test Files: 15
- Documentation: 8 pages
- API Endpoints: 12

## Blockers Encountered
1. Database migration dependency (resolved)
2. API rate limiting (ongoing)

## Recommendations for Next Sprint
1. Carry over incomplete tasks
2. Address technical debt in auth module
3. Increase QA capacity for better coverage
```

Save report to: `.claude/reports/sprint-[sprint-id]-report.md`

### 6. Update Sprint Status
Mark sprint as stopped:
- !`.claude/scripts/state_manager.py set "sprints.[sprint-id].status" '"stopped"'`
- !`.claude/scripts/state_manager.py set "sprints.[sprint-id].stop_time" '"[timestamp]"'`

### 7. Clear Active Agents
Remove agents from active list:
```bash
# Clear all agents for this sprint
!`.claude/scripts/state_manager.py set agents.active '{}'`
```

### 8. Emit Stop Event
Log sprint stop event:
- !`.claude/scripts/event_stream.py emit sprint_stopped '{"sprint_id": "[id]", "reason": "user_requested", "metrics": {...}}' --source orchestrator`

## Post-Stop Summary

### Display Final Status

```
✅ Sprint [sprint-id] Stopped Successfully

📊 Final Statistics:
• Tasks Completed: 9/17 (53%)
• Sprint Velocity: 8 points
• Total Runtime: 4.5 hours
• Token Usage: 68,420

📁 Archived Data:
• Sprint state saved to: .claude/state/archive/sprint-[id].json
• Report generated at: .claude/reports/sprint-[id]-report.md
• Logs available at: .claude/logs/sprint-[id].log

🔄 Incomplete Tasks (8):
These tasks have been moved to backlog and can be included in the next sprint:
- task-4: API endpoints (75% complete)
- task-5: Integration tests (50% complete)
- task-6: Documentation (30% complete)
- task-7: Performance optimization (not started)
- task-8: Security review (not started)
...

💡 Next Steps:
1. Review sprint report: cat .claude/reports/sprint-[id]-report.md
2. Plan next sprint: /orchestrate sprint plan
3. Address incomplete tasks: /orchestrate backlog review
4. Analyze metrics: /orchestrate metrics analyze
```

## Error Handling

Handle potential issues during shutdown:

### Agent Not Responding
```
⚠️ Warning: Agent [agent-id] not responding
   Waiting 10 more seconds...
   Force stopping agent...
   ✓ Agent terminated
```

### State Save Failure
```
❌ Error: Failed to save state for task-[id]
   Attempting backup save...
   ✓ State backed up to .claude/backup/
```

### Report Generation Failure
```
⚠️ Warning: Could not generate full report
   Partial report saved to: .claude/reports/partial-[id].md
   Raw data saved to: .claude/state/archive/raw-[id].json
```

## Rollback Option

If stop process fails:
```
❌ Sprint stop failed

Would you like to:
1. Retry stop process
2. Force stop (may lose data)
3. Cancel and continue sprint
4. Contact support

Enter choice (1-4):
```

## Cleanup Actions

After successful stop:
1. Clear message queues
2. Release file locks
3. Compact state file
4. Update metrics dashboard
5. Send notifications if configured

## Success Validation

Verify sprint properly stopped:
- [ ] All agents terminated
- [ ] State properly saved
- [ ] Report generated
- [ ] Archive created
- [ ] Metrics updated
- [ ] Events logged
- [ ] No orphaned processes