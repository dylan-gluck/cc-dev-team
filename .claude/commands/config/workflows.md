---
allowed-tools: Read, Edit, Write, Bash(jq:*), Task
description: Show and edit workflow configurations
argument-hint: [workflow-name] [action:list|show|edit|add|remove|test]
model: sonnet
---

# Workflow Configuration Management

Manage workflow configurations for the orchestration system.

## Context
- Workflows configuration: @.claude/orchestration/workflows.json
- Available teams: !`jq -r '.teams | keys[]' .claude/orchestration/teams.json 2>/dev/null | head -5`
- Arguments: $ARGUMENTS

## Task

Manage workflow configurations based on provided arguments:

### If no arguments or "list":
1. Display all configured workflows:
   - Workflow name and description
   - Trigger patterns
   - Assigned team/agent
   - Priority level
   - Enable/disable status
   - Last triggered (if tracked)

### If workflow-name with "show":
1. Display detailed workflow information:
   - Full workflow configuration
   - Trigger conditions and patterns
   - Team/agent assignment logic
   - Delegation instructions
   - Context requirements
   - Success criteria

### If "add" with workflow-name:
1. Create new workflow configuration:
   - Prompt for workflow description
   - Define trigger patterns (keywords, patterns)
   - Select team or specific agent
   - Set priority (high/medium/low)
   - Define delegation template
   - Add context requirements

### If "edit" with workflow-name:
1. Modify existing workflow:
   - Load current configuration
   - Allow editing of all fields
   - Validate trigger patterns
   - Ensure team/agent exists
   - Preview changes before saving

### If "remove" with workflow-name:
1. Remove workflow:
   - Confirm deletion
   - Check for dependencies
   - Archive configuration
   - Update workflows.json

### If "test" with workflow-name:
1. Test workflow configuration:
   - Validate trigger patterns with examples
   - Check team/agent availability
   - Simulate delegation process
   - Report potential issues

### Advanced Features:
1. **Workflow Analysis**
   - Identify overlapping triggers
   - Find unused workflows
   - Suggest optimizations
   - Check for conflicts

2. **Bulk Operations**
   - Enable/disable multiple workflows
   - Export/import workflow sets
   - Clone workflow with modifications

## Expected Output

Formatted workflow information:
```
Workflow Configuration
======================

📋 Active Workflows (8):

High Priority:
  🔴 code-review
     Triggers: "review", "pr review", "check code"
     Team: qa-team
     Status: ✅ Enabled

  🔴 bug-fix
     Triggers: "bug", "fix", "error", "issue"
     Agent: engineering-fullstack
     Status: ✅ Enabled

Medium Priority:
  🟡 documentation
     Triggers: "document", "docs", "readme"
     Team: documentation-team
     Status: ⚠️ No team configured

[Additional workflows...]

📊 Summary:
- Total: 8 workflows
- Enabled: 6
- Disabled: 2
- Issues: 1 workflow needs attention
```

For modifications:
```
Workflow Updated: code-review
=============================
Changes:
  - Added trigger: "code check"
  - Updated team: qa-team → engineering-team
  - Priority: medium → high

✅ Configuration saved and validated
```

## Constraints
- Validate JSON structure before saving
- Ensure no trigger conflicts
- Verify team/agent references
- Maintain workflow priority order
- Create backups before modifications