# Orchestration Commands Documentation

## Overview

The `/orchestrate` command family provides comprehensive control over multi-agent orchestration, team coordination, and sprint management. These commands integrate with the orchestration infrastructure in `.claude/orchestration/` and `.claude/scripts/`.

## Command Family

### Core Commands

| Command | Description | Confirmation Required |
|---------|-------------|-----------------------|
| `/orchestrate` | Main menu and status overview | No |
| `/orchestrate sprint start [sprint-id]` | Start sprint with team orchestration | Yes |
| `/orchestrate sprint status` | Show current sprint progress | No |
| `/orchestrate sprint stop` | Gracefully stop current sprint | Yes |
| `/orchestrate task delegate <description>` | Delegate task to appropriate team | Yes |
| `/orchestrate team activate <team>` | Activate team for coordination | Yes |
| `/orchestrate epic plan <description>` | Plan epic breakdown | Yes |
| `/orchestrate agents status` | Show all active agents | No |

## Key Features

### 1. Preview and Confirmation System
All commands that spawn agents or consume significant resources show a detailed preview before execution:

```
┌─────────────────────────────────────────────────┐
│          OPERATION PREVIEW                      │
├─────────────────────────────────────────────────┤
│ Agents to spawn: 5                              │
│ Estimated tokens: 50,000                        │
│ Estimated time: 30 minutes                      │
│                                                  │
│ Proceed? (yes/no)                              │
└─────────────────────────────────────────────────┤
```

### 2. Resource Tracking
Every command provides resource estimates:
- Number of agents needed
- Token consumption estimate
- Runtime projection
- Current vs. limit comparison

### 3. State Management Integration
Commands integrate with the state management system:
- Persistent state in `.claude/state/orchestration.json`
- Real-time updates via `state_manager.py`
- Event streaming via `event_stream.py`
- Message passing via `message_bus.py`

## Usage Examples

### Starting a Sprint

```bash
# Start a new sprint with preview
/orchestrate sprint start sprint-3

# Start with specific team
/orchestrate sprint start sprint-3 --team engineering
```

### Checking Status

```bash
# Main orchestration menu
/orchestrate

# Current sprint status
/orchestrate sprint status

# All active agents
/orchestrate agents status

# Specific team agents
/orchestrate agents status --team engineering
```

### Task Delegation

```bash
# Delegate with automatic team selection
/orchestrate task delegate "Implement OAuth2 authentication"

# Delegate to specific team
/orchestrate task delegate "Write E2E tests" --team qa --priority high
```

### Team Coordination

```bash
# Activate engineering team at 80% capacity
/orchestrate team activate engineering --capacity 80

# Activate with focus area
/orchestrate team activate qa --focus "regression testing"
```

### Epic Planning

```bash
# Plan a 4-week epic
/orchestrate epic plan "E-commerce checkout system" --duration 4 --teams engineering,qa,devops
```

## Configuration

### Teams Configuration
Teams are defined in `.claude/orchestration/teams.json`:
- Team composition and roles
- Agent capacities
- Skill mappings
- Model preferences

### Settings
Global settings in `.claude/orchestration/settings.json`:
- Resource limits
- Confirmation thresholds
- Budget management
- Orchestration modes

### Workflows
Sprint and epic templates in `.claude/orchestration/workflows.json`:
- Phase definitions
- Ceremony schedules
- Approval gates

## Safety Features

### User Control
- **No automatic spawning**: All agent creation requires explicit confirmation
- **Preview before execution**: See what will happen before it happens
- **Resource limits**: Configurable limits prevent runaway operations
- **Graceful shutdown**: Stop commands cleanly save state

### Confirmation Thresholds
Operations requiring confirmation when exceeding:
- 3+ agents
- 50,000+ tokens
- 30+ minutes runtime

### State Preservation
- All progress is saved continuously
- Interrupted work can be resumed
- Complete audit trail in event stream

## Integration Points

### State Management
- Read state: `.claude/scripts/state_manager.py get [path]`
- Update state: `.claude/scripts/state_manager.py set [path] [value]`
- Task updates: `.claude/scripts/state_manager.py update-task [id] [status]`

### Observability
- System status: `.claude/scripts/observability.py status`
- Sprint metrics: `.claude/scripts/observability.py sprint [id]`
- Live monitoring: `.claude/scripts/observability.py monitor`

### Communication
- Send messages: `.claude/scripts/message_bus.py send [from] [to] [type] [payload]`
- Check queues: `.claude/scripts/message_bus.py queue_status [agent]`
- Broadcast: `.claude/scripts/message_bus.py broadcast [from] [type] [payload]`

### Event Streaming
- Emit events: `.claude/scripts/event_stream.py emit [type] [data]`
- Stream events: `.claude/scripts/event_stream.py stream --follow`

## Best Practices

### 1. Start Small
Begin with single team activation before full sprint orchestration:
```bash
/orchestrate team activate engineering --capacity 50
```

### 2. Monitor Progress
Use status commands frequently:
```bash
/orchestrate sprint status
/orchestrate agents status
```

### 3. Review Before Confirming
Always review the preview carefully before confirming operations.

### 4. Use Appropriate Models
- `opus` for orchestrators and complex reasoning
- `sonnet` for balanced implementation work
- `haiku` for simple tasks and monitoring

### 5. Set Budgets
Configure token and time budgets in settings to prevent overuse.

## Troubleshooting

### Common Issues

**No teams configured**
- Check `.claude/orchestration/teams.json` exists
- Verify JSON syntax is valid

**State file locked**
- Check for `.claude/state/.orchestration.lock`
- Remove stale lock if needed

**Agent not responding**
- Use `/orchestrate agent restart [agent-id]`
- Check message queue for pending communications

**Token limit exceeded**
- Review usage: `/orchestrate agents status`
- Adjust budgets in settings.json
- Stop unnecessary agents

### Recovery Commands

```bash
# Stop all orchestration
/orchestrate stop

# Clear state (careful!)
rm .claude/state/orchestration.json

# Reload configuration
/orchestrate config reload

# Force stop specific agent
/orchestrate agent stop [agent-id] --force
```

## Advanced Features

### Custom Workflows
Create custom workflow templates in `.claude/orchestration/workflows.json`

### Team Extensions
Add new teams by editing `.claude/orchestration/teams.json`

### Hook Integration
Limited hook support for metrics tracking (not for auto-orchestration)

### Budget Management
Set daily/weekly/monthly token and time budgets

## Security Considerations

- All operations require user confirmation
- Sensitive operations have additional confirmations
- Audit trail maintained in event stream
- State files should be gitignored

## Support

For issues or questions:
1. Check this documentation
2. Review status with `/orchestrate status`
3. Check logs in `.claude/logs/`
4. Review event stream for errors

## Version

Current version: 1.0
Compatible with: Claude Code orchestration framework
Last updated: 2025-01-20