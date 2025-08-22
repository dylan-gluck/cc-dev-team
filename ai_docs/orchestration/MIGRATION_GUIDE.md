# V1 to V2 Orchestration Migration Guide

Complete guide for migrating from V1 to V2 orchestration system with compatibility notes, automated migration tools, and rollback procedures.

## Table of Contents

- [Migration Overview](#migration-overview)
- [Pre-Migration Assessment](#pre-migration-assessment)
- [Automated Migration Steps](#automated-migration-steps)
- [Manual Migration Steps](#manual-migration-steps)
- [Compatibility Notes](#compatibility-notes)
- [Rollback Procedures](#rollback-procedures)
- [Testing and Validation](#testing-and-validation)
- [FAQ](#faq)

## Migration Overview

### What's New in V2

**Core Improvements:**
- **UV Script Architecture**: Replacing ad-hoc scripting with standardized UV single-file scripts
- **Session Management**: Formal session lifecycle with modes, heartbeats, and handoffs
- **State Management**: Atomic operations with JSONPath queries and file locking
- **Shared State**: Project-level configuration separate from session state
- **Output Styles**: Specialized SudoLang interfaces for different workflows
- **Enhanced Observability**: Structured metrics and event tracking

**Breaking Changes:**
- State file format changed from flat JSON to hierarchical structure
- Hook interfaces updated with new JSON schema
- Command-line interfaces standardized across all scripts
- Session persistence moved from `.claude/data/sessions/` to `~/.claude/state/sessions/`

### Migration Timeline

**Recommended migration approach:**
1. **Assessment Phase** (1-2 days): Analyze current setup and plan migration
2. **Backup Phase** (1 hour): Create complete backup of existing configuration
3. **Migration Phase** (2-4 hours): Run automated migration and manual updates
4. **Testing Phase** (1-2 days): Validate functionality and performance
5. **Rollback Window** (1 week): Keep V1 backup available for emergency rollback

## Pre-Migration Assessment

### 1. Inventory Current Configuration

Run the assessment script to analyze your current setup:

```bash
# Create assessment of current configuration
uv run .claude/scripts/migration/assess_v1.py --project-path . --output assessment.json
```

**Expected output:**
```json
{
  "compatibility": {
    "agents": {"compatible": 15, "needs_update": 3, "incompatible": 0},
    "hooks": {"compatible": 8, "needs_update": 0, "incompatible": 0},
    "commands": {"compatible": 12, "needs_update": 2, "incompatible": 1},
    "session_data": {"sessions": 23, "total_size_mb": 45.2}
  },
  "migration_complexity": "medium",
  "estimated_time": "2-3 hours",
  "recommended_approach": "automated_with_manual_review"
}
```

### 2. Check Prerequisites

Verify your environment is ready for V2:

```bash
# Check UV installation
uv --version
# Required: uv 0.1.0 or higher

# Check Python version
python --version  
# Required: Python 3.11 or higher

# Check available disk space
df -h ~/.claude/
# Required: At least 100MB free space

# Check file permissions
ls -la .claude/
# Verify read/write access to .claude directory
```

### 3. Backup Current Configuration

Create a complete backup before migration:

```bash
# Run comprehensive backup
uv run .claude/scripts/migration/backup_v1.py --project-path . --backup-path ./v1-backup-$(date +%Y%m%d)

# Verify backup integrity
uv run .claude/scripts/migration/verify_backup.py --backup-path ./v1-backup-$(date +%Y%m%d)
```

**Backup includes:**
- All `.claude/` configuration files
- Session data from `.claude/data/sessions/`
- Hook configurations and custom scripts
- Agent definitions and commands
- Project-specific settings

## Automated Migration Steps

### 1. Run Migration Script

The automated migration handles most of the conversion:

```bash
# Run automated migration with dry-run first
uv run .claude/scripts/migration/migrate_to_v2.py --project-path . --dry-run

# Review planned changes, then run actual migration
uv run .claude/scripts/migration/migrate_to_v2.py --project-path . --backup-v1
```

**Migration script handles:**
- Converting session data format
- Updating hook configurations  
- Migrating agent definitions
- Creating shared state structure
- Installing new UV scripts
- Updating command interfaces

### 2. Initialize V2 State Management

Set up the new state management system:

```bash
# Initialize state directories
mkdir -p ~/.claude/state/{sessions,shared/projects}

# Migrate existing session data
for session_file in .claude/data/sessions/*.json; do
  SESSION_ID=$(basename "$session_file" .json)
  uv run .claude/scripts/migration/convert_session.py --input "$session_file" --session-id "$SESSION_ID"
done

# Verify migration
uv run .claude/scripts/session_manager.py list
```

### 3. Create Shared State Configuration

Convert project-level configuration to shared state:

```bash
# Extract project configuration from V1 settings
PROJECT_ID=$(basename $(pwd))
uv run .claude/scripts/migration/extract_project_config.py --project-path . --project-id "$PROJECT_ID"

# Verify shared state setup
uv run .claude/scripts/shared_state.py get-config "$PROJECT_ID"
```

## Manual Migration Steps

### 1. Update Agent Definitions

V2 requires minor updates to agent definitions for enhanced delegation:

**V1 Format:**
```yaml
---
name: engineering-fullstack
description: "Handles end-to-end application development"
tools: Read, Write, Edit, Bash
---
```

**V2 Format:**
```yaml
---
name: engineering-fullstack
description: "Use proactively for end-to-end application development and integration tasks"
tools: Read, Write, Edit, Bash
model: sonnet
color: blue
delegation_triggers:
  - "fullstack development"
  - "end-to-end implementation"
  - "application integration"
---
```

**Migration script:**
```bash
# Update all agent files
for agent_file in .claude/agents/*.md; do
  uv run .claude/scripts/migration/update_agent_format.py --input "$agent_file"
done
```

### 2. Migrate Custom Hooks

Update hook interfaces for V2 JSON schema:

**V1 Hook Example:**
```python
#!/usr/bin/env python3
import sys
import json

# Simple text output
print("Hook executed successfully")
sys.exit(0)
```

**V2 Hook Example:**
```python
#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.11"
# dependencies = ["rich>=13.0"]
# ///

import sys
import json
from rich.console import Console

console = Console()

# Read hook input
hook_input = json.loads(sys.stdin.read())
session_id = hook_input.get('sessionId')

# Process with new state management
result = {
    "continue": True,
    "suppressOutput": False
}

# Use UV scripts for state operations
if session_id:
    subprocess.run([
        'uv', 'run', '.claude/scripts/session_manager.py', 
        'heartbeat', session_id
    ])

print(json.dumps(result))
sys.exit(0)
```

**Migration helper:**
```bash
# Update all custom hooks
for hook_file in .claude/hooks/*.py; do
  uv run .claude/scripts/migration/update_hook_format.py --input "$hook_file"
done
```

### 3. Update Command Interfaces

Convert custom commands to use V2 APIs:

**V1 Command Example:**
```markdown
# /build-feature

Builds a complete feature with the engineering team.

Instructions: Delegate to engineering-fullstack agent to implement the requested feature.
```

**V2 Command Example:**
```markdown
# /build-feature

Builds a complete feature with the engineering team using V2 orchestration.

## Usage
`/build-feature <feature-name> [--epic EPIC_ID] [--sprint SPRINT_ID]`

## Implementation
```sudolang
process_command(input) {
  // Extract parameters
  [feature_name, epic_id, sprint_id] = parse_parameters(input)
  
  // Create task in state management
  task_data = {
    id: generate_task_id(),
    title: feature_name,
    epic_id: epic_id,
    sprint_id: sprint_id,
    status: "todo",
    created_at: getCurrentTimestamp()
  }
  
  // Add to state
  `uv run .claude/scripts/state_manager.py merge $SESSION_ID "sprint.tasks.{task_data.id}" {task_data}`
  
  // Delegate to engineering team
  /orchestrate task delegate feature_name
}
```

Instructions: Creates a structured task in the sprint board and delegates to the engineering team with proper state tracking.
```

### 4. Configure Output Styles

Set up specialized output styles for different workflows:

```bash
# Test each output style
/output-style sprint_execution
# Verify Kanban board displays correctly

/output-style leadership_chat  
# Verify executive dashboard shows KPIs

/output-style all-team_dashboard
# Verify multi-team coordination view

/output-style config_manager
# Verify configuration management interface
```

## Compatibility Notes

### Backward Compatibility

**What Still Works:**
- ✅ Existing agent definitions (with minor format updates)
- ✅ Basic hook functionality (with interface updates)
- ✅ Custom slash commands (with API updates)
- ✅ Session data (after format conversion)
- ✅ Project file structure

**What Requires Updates:**
- ⚠️ Hook exit code handling (enhanced in V2)
- ⚠️ State persistence paths (moved to ~/.claude/state/)
- ⚠️ Command interfaces (standardized CLI)
- ⚠️ Event logging format (structured JSON)

**What's Deprecated:**
- ❌ Direct file manipulation of session data
- ❌ Ad-hoc hook scripts without UV dependencies
- ❌ Flat JSON configuration format
- ❌ Manual session management

### API Compatibility Matrix

| Component | V1 API | V2 API | Migration Required |
|-----------|--------|--------|--------------------|
| Session Management | File-based | UV script CLI | Yes - automated |
| State Operations | Direct JSON | JSONPath + CLI | Yes - automated |
| Hook Interface | Basic | Enhanced JSON | Yes - semi-automated |
| Agent Delegation | Simple | Structured | No - compatible |
| Command Format | Basic | SudoLang enhanced | Optional |
| Output Styles | None | SudoLang interfaces | New feature |

### Data Format Changes

**Session Data Format:**

V1 Format:
```json
{
  "session_id": "uuid",
  "agent_name": "string", 
  "prompts": ["array"],
  "extras": {"key": "value"}
}
```

V2 Format:
```json
{
  "session": {
    "id": "uuid",
    "mode": "development",
    "lifecycle": {"status": "active", "expiry": "ISO8601"}
  },
  "execution": {"agents": {}, "tasks": {}, "workflows": {}},
  "observability": {"metrics": {}, "events": []}
}
```

**Migration handled by:**
```bash
uv run .claude/scripts/migration/convert_session_format.py --input v1-session.json --output v2-session.json
```

## Rollback Procedures

### Emergency Rollback

If critical issues occur, you can quickly rollback to V1:

```bash
# Stop all V2 processes
pkill -f "uv run .claude/scripts"

# Restore V1 configuration
cp -r ./v1-backup-$(date +%Y%m%d)/.claude/ .claude/

# Restore V1 session data
cp -r ./v1-backup-$(date +%Y%m%d)/.claude/data/sessions/ .claude/data/sessions/

# Verify V1 functionality
claude-code --version
```

### Planned Rollback

For planned rollback after testing:

```bash
# Export any V2 data you want to keep
uv run .claude/scripts/state_manager.py list-sessions --json-output > v2-sessions-export.json
uv run .claude/scripts/shared_state.py get-config PROJECT_ID --json-output > v2-config-export.json

# Clean V2 state
rm -rf ~/.claude/state/

# Restore V1 backup
uv run .claude/scripts/migration/rollback_to_v1.py --backup-path ./v1-backup-$(date +%Y%m%d)

# Verify rollback
ls -la .claude/
```

### Partial Rollback

Rollback specific components while keeping others:

```bash
# Rollback hooks only
cp ./v1-backup-$(date +%Y%m%d)/.claude/hooks/* .claude/hooks/

# Rollback agents only  
cp ./v1-backup-$(date +%Y%m%d)/.claude/agents/* .claude/agents/

# Rollback session data only
rm -rf ~/.claude/state/sessions/
cp -r ./v1-backup-$(date +%Y%m%d)/.claude/data/sessions/ .claude/data/sessions/
```

### Rollback Validation

After rollback, verify everything works:

```bash
# Test basic functionality
claude-code --help

# Test agent delegation
echo "Test delegation to research-ai agent" | claude-code

# Test hooks
echo '{}' | .claude/hooks/session_start.py

# Test commands
# Use any custom slash command you had working in V1
```

## Testing and Validation

### 1. Functional Testing

Verify all major workflows work correctly:

```bash
# Test session management
SESSION_ID=$(uv run .claude/scripts/session_manager.py create --mode development --project test)
uv run .claude/scripts/session_manager.py heartbeat $SESSION_ID
uv run .claude/scripts/session_manager.py info $SESSION_ID

# Test state management
uv run .claude/scripts/state_manager.py set $SESSION_ID "test.value" "hello"
uv run .claude/scripts/state_manager.py get $SESSION_ID "test.value"
uv run .claude/scripts/state_manager.py delete $SESSION_ID "test.value"

# Test shared state
uv run .claude/scripts/shared_state.py set-config test --data '{"setting": "value"}'
uv run .claude/scripts/shared_state.py get-config test
```

### 2. Performance Testing

Compare performance between V1 and V2:

```bash
# Benchmark session operations
time uv run .claude/scripts/session_manager.py create --mode development --project benchmark
time uv run .claude/scripts/session_manager.py list

# Benchmark state operations
time uv run .claude/scripts/state_manager.py set $SESSION_ID "benchmark.test" "value"
time uv run .claude/scripts/state_manager.py get $SESSION_ID "benchmark.test"

# Test concurrent access
for i in {1..10}; do
  uv run .claude/scripts/state_manager.py set $SESSION_ID "concurrent.$i" "value$i" &
done
wait
```

### 3. Integration Testing

Test integration with Claude Code:

```bash
# Test output styles
/output-style sprint_execution
/move TASK-123 in_progress

/output-style leadership_chat  
/kpis

# Test slash commands
/orchestrate sprint start
/state summary
/monitor status

# Test agent delegation
"Create a test feature using the engineering team"
```

### 4. Data Integrity Testing

Verify data migration was successful:

```bash
# Compare session counts
V1_SESSIONS=$(ls -1 ./v1-backup-$(date +%Y%m%d)/.claude/data/sessions/ | wc -l)
V2_SESSIONS=$(uv run .claude/scripts/session_manager.py list --json-output | jq '. | length')
echo "V1 had $V1_SESSIONS sessions, V2 has $V2_SESSIONS sessions"

# Verify agent migration
V1_AGENTS=$(ls -1 ./v1-backup-$(date +%Y%m%d)/.claude/agents/ | wc -l)
V2_AGENTS=$(ls -1 .claude/agents/ | wc -l)
echo "V1 had $V1_AGENTS agents, V2 has $V2_AGENTS agents"

# Check for data loss
uv run .claude/scripts/migration/validate_migration.py --v1-backup ./v1-backup-$(date +%Y%m%d) --v2-current .
```

## FAQ

### General Migration Questions

**Q: How long does migration typically take?**
A: 2-4 hours for automated migration, plus 1-2 days for testing and validation. Complex configurations may require additional time.

**Q: Can I migrate gradually or must it be all-at-once?**
A: V2 is a significant architectural change requiring complete migration. However, you can test V2 in a separate directory first.

**Q: What happens to my existing session data?**
A: Session data is converted to the new format and moved to `~/.claude/state/sessions/`. All historical data is preserved.

**Q: Do I need to retrain my agents?**
A: No, agent behavior remains the same. Only the definition format is updated slightly for enhanced delegation.

### Technical Questions

**Q: Why did session storage move to `~/.claude/state/`?**
A: V2 separates project-specific configuration from system-wide session state, enabling better cross-project coordination and state management.

**Q: Can I continue using my custom hooks?**
A: Yes, but they need minor updates for the new JSON interface and UV script format. The migration script handles most updates automatically.

**Q: What if I have very large session files?**
A: V2's file locking and atomic operations handle large files better than V1. Performance should improve for large datasets.

**Q: How do I access V1 session data after migration?**
A: Use the V2 state manager: `uv run .claude/scripts/state_manager.py get SESSION_ID ""` returns the complete session data.

### Troubleshooting Questions

**Q: Migration failed halfway through, what do I do?**
A: Use the rollback procedure to restore V1, fix the issue, then retry migration. Check `migration.log` for specific error details.

**Q: Some agents aren't working after migration?**
A: Run `uv run .claude/scripts/migration/validate_agents.py` to identify issues. Most problems are minor format updates.

**Q: Performance seems slower than V1?**
A: Initial V2 setup has some overhead. Performance should improve after the first few sessions. Check for large state files that may need cleanup.

**Q: Output styles aren't displaying correctly?**
A: Verify `.claude/output-styles/` directory exists and contains the SudoLang files. Re-run migration if files are missing.

### Post-Migration Questions

**Q: How do I monitor system health in V2?**
A: Use `/monitor status` and `/debug` commands, plus UV script monitoring: `uv run .claude/scripts/session_manager.py list --active`

**Q: Can I customize the new output styles?**
A: Yes, output styles are SudoLang files you can modify. See the [API Reference](API_REFERENCE.md) for customization details.

**Q: How do I backup V2 configurations?**
A: Use `/config backup create` or manually backup `~/.claude/state/` and `.claude/` directories.

**Q: What's the recommended maintenance schedule for V2?**
A: Weekly: `uv run .claude/scripts/state_manager.py cleanup-expired`
Monthly: `/config backup create` and system health review

### Getting Additional Help

**If you encounter issues not covered in this guide:**

1. **Check Migration Logs**: `tail -f migration.log` for detailed error information
2. **Run Diagnostics**: `uv run .claude/scripts/migration/diagnose.py` for automated problem detection
3. **Community Support**: [GitHub Issues](https://github.com/dylan-gluck/cc-dev-team/issues) for migration-specific questions
4. **Documentation**: [User Guide](USER_GUIDE.md) and [API Reference](API_REFERENCE.md) for detailed V2 usage

**Emergency Support:**
If you need immediate assistance during migration, create a detailed issue with:
- Migration log output
- System configuration (`uv --version`, `python --version`)
- Specific error messages
- Steps taken before the issue occurred

---

This migration guide provides comprehensive coverage for transitioning from V1 to V2 orchestration. The migration is designed to be safe and reversible, with multiple validation points to ensure data integrity and system functionality.