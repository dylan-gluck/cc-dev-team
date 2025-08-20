---
allowed-tools: Read, Write, Bash(python:*), Bash(jq:*), Task
description: Reload configuration files safely
argument-hint: [--force] [--validate-first]
model: sonnet
---

# Safe Configuration Reload

Reload orchestration configurations while maintaining system integrity.

## Context
- Current orchestration state: @.claude/state/orchestration.json
- Configuration files: !`ls -la .claude/orchestration/*.json 2>/dev/null`
- Arguments: $ARGUMENTS

## Task

Perform safe configuration reload:

1. **Pre-Reload Validation**
   If --validate-first or by default:
   - Run validation on all config files
   - Abort if critical errors found
   - Warn about non-critical issues

2. **State Preservation**
   - Save current orchestration state
   - Record active sessions/workflows
   - Create rollback point

3. **Configuration Loading**
   For each configuration file:
   - Parse and validate JSON structure
   - Check schema compliance
   - Verify inter-file dependencies
   
4. **Incremental Reload Process**
   - Load settings.json first (base configuration)
   - Load teams.json (team definitions)
   - Load workflows.json (workflow rules)
   - Update state/orchestration.json

5. **Compatibility Checks**
   - Ensure new config compatible with active sessions
   - Verify no breaking changes for running workflows
   - Check agent availability

6. **If --force flag provided**
   - Skip compatibility checks
   - Force reload even with warnings
   - Clear active session states if needed

7. **Post-Reload Actions**
   - Verify configuration loaded correctly
   - Test basic orchestration functions
   - Update configuration cache
   - Log reload event with timestamp

8. **Rollback Capability**
   If reload fails:
   - Restore previous configuration
   - Reinstate saved state
   - Report specific failure reason

## Expected Output

Reload status report:
```
Configuration Reload Status
===========================
📥 Loading configurations...

✅ settings.json - Loaded (v1.2.0)
✅ teams.json - Loaded (5 teams)
✅ workflows.json - Loaded (12 workflows)

State Preservation:
- Active sessions: 2 preserved
- Running workflows: 1 migrated

Validation Results:
- No errors found
- 1 warning: Unused agent 'legacy-helper'

🔄 Reload completed successfully!
Configuration version: 1.2.0
Timestamp: 2024-01-20 10:30:45
```

## Constraints
- Never lose active session data
- Maintain backward compatibility
- Always create rollback point
- Validate before committing changes
- Log all reload operations