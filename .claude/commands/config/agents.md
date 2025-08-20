---
allowed-tools: Read, LS, Grep, Task, Bash(jq:*)
description: Show and manage agent configurations
argument-hint: [agent-name] [action:list|show|check|stats]
model: sonnet
---

# Agent Configuration Management

View and analyze agent configurations and their usage in the orchestration system.

## Context
- Available agents: !`ls .claude/agents/*.md 2>/dev/null | wc -l | xargs -I {} echo "{} agents available"`
- Teams using agents: @.claude/orchestration/teams.json
- Arguments: $ARGUMENTS

## Task

Based on the arguments, perform agent configuration management:

### If no arguments or "list":
1. Display all available agents in categories:
   - Group by team prefix (engineering-, product-, qa-, etc.)
   - Show agent name, description, and status
   - Indicate which agents are currently assigned to teams
   - Highlight recently added/modified agents

### If agent-name with "show":
1. Display detailed agent information:
   - Read agent file from `.claude/agents/[agent-name].md`
   - Show frontmatter configuration
   - Display delegation description
   - List allowed tools
   - Show which teams use this agent
   - Display recent usage statistics if available

### If "check" (with optional agent-name):
1. Perform agent consistency checks:
   - Verify all agents referenced in teams exist
   - Check for orphaned agents (not used in any team)
   - Validate agent file format and frontmatter
   - Check for duplicate agent definitions
   - Verify tool permissions are valid

### If "stats":
1. Generate agent usage statistics:
   - Total number of agents by category
   - Most/least used agents
   - Agents per team distribution
   - Tool permission analysis
   - Model preference distribution

### Additional Features:
1. **Cross-Reference Analysis**
   - Show which workflows use specific agents
   - Identify agent dependencies
   - Map agent capabilities to team functions

2. **Configuration Insights**
   - Identify agents with similar tools/purposes
   - Suggest potential agent consolidation
   - Highlight agents with excessive permissions

## Expected Output

Formatted agent information:
```
Agent Configuration Overview
============================

📊 Statistics:
- Total Agents: 25
- Teams: 8 teams configured
- Active Agents: 22 (3 orphaned)

🤖 Agents by Team:
Engineering (8):
  ✅ engineering-fullstack - Full-stack development
  ✅ engineering-api - API development specialist
  ⚠️ engineering-legacy - Not assigned to any team

Product (4):
  ✅ product-manager - Product management
  ✅ product-analyst - Analytics and metrics

[Additional teams...]

📈 Usage Insights:
- Most used: engineering-fullstack (15 workflows)
- Least used: qa-performance (1 workflow)
- Suggested review: 3 agents with similar capabilities
```

## Constraints
- Read-only operations (no modifications)
- Handle missing agent files gracefully
- Provide actionable insights
- Group information logically