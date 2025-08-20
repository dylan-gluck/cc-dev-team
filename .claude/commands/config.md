---
allowed-tools: Read, LS, Task
description: Configuration management overview and help
model: haiku
---

# Configuration Management Overview

Display configuration management options and current status for the orchestration system.

## Context
- Configuration directory: !`ls -la .claude/orchestration/ 2>/dev/null || echo "No orchestration config found"`
- Validation script: !`test -f .claude/scripts/validate_orchestration.py && echo "Available" || echo "Not found"`
- Current agents: !`ls .claude/agents/*.md 2>/dev/null | wc -l | xargs -I {} echo "{} agents configured"`

## Task

Provide a comprehensive overview of the configuration management system:

1. **Current Configuration Status**
   - List all configuration files in `.claude/orchestration/`
   - Show last modified dates for each config
   - Display validation status summary

2. **Available Commands**
   Display the following configuration commands with descriptions:
   - `/config teams` - View and edit team configurations
   - `/config validate` - Run full configuration validation
   - `/config reload` - Safely reload configuration files
   - `/config agents` - Manage agent configurations
   - `/config workflows` - Edit workflow configurations
   - `/config fix` - Auto-fix common configuration issues
   - `/config backup` - Backup and restore configurations

3. **Quick Health Check**
   - Check if all required config files exist
   - Verify basic JSON syntax validity
   - Count configured teams, agents, and workflows

4. **Recent Changes**
   - Show last 5 configuration changes (if git available)
   - Highlight any uncommitted config changes

## Expected Output

A formatted overview showing:
- Configuration health status (✅ Good / ⚠️ Warning / ❌ Error)
- Table of configuration files with status
- List of available commands with usage hints
- Any immediate action items or warnings

## Constraints
- Use clear status indicators (emojis or symbols)
- Keep overview concise but informative
- Highlight any critical issues prominently