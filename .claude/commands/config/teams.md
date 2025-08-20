---
allowed-tools: Read, Edit, Write, Bash(jq:*), Task
description: Show and edit team configurations
argument-hint: [team-name] [action:show|edit|add|remove]
model: sonnet
---

# Team Configuration Management

Manage team configurations in the orchestration system.

## Context
- Teams configuration: @.claude/orchestration/teams.json
- Available agents: !`ls .claude/agents/*.md 2>/dev/null | sed 's|.*/||; s|\.md$||' | head -10`
- Arguments provided: $ARGUMENTS

## Task

Based on the arguments provided, perform the appropriate team configuration action:

### If no arguments or "show":
1. Display all configured teams in a formatted table
2. Show team structure:
   - Team name and description
   - Lead agent
   - Member agents with their roles
   - Team capabilities summary

### If team-name provided with "show":
1. Display detailed information for the specific team
2. Show all team members with their delegations
3. List team workflows if any

### If "add" with team-name:
1. Create a new team configuration
2. Prompt for:
   - Team description
   - Lead agent selection
   - Team member agents
   - Initial capabilities
3. Add to teams.json with proper structure

### If "edit" with team-name:
1. Load current team configuration
2. Allow editing of:
   - Team description
   - Lead agent
   - Add/remove team members
   - Update member delegations
3. Validate changes before saving

### If "remove" with team-name:
1. Confirm removal action
2. Check for dependencies in workflows
3. Remove team from configuration
4. Update related configurations

### For all modifications:
1. Validate JSON syntax before saving
2. Ensure all referenced agents exist
3. Check for circular dependencies
4. Create backup before changes

## Expected Output

Depending on action:
- **Show**: Formatted team information with clear hierarchy
- **Add/Edit**: Confirmation of changes with diff preview
- **Remove**: Confirmation with impact analysis

## Constraints
- Always validate JSON structure
- Preserve existing team configurations
- Ensure agent references are valid
- Maintain backup of original configuration