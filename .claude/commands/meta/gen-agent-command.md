---
allowed-tools: Task, Read, TodoWrite
description: Generate a specialized agent and corresponding commands
argument-hint: <agent-name> <command(s)> [description]
---

# Generate Agent + Command

A meta command to generate both a specialized agent and one or more commands that initialize that agent for specific tasks. This command delegates to both meta-agent and command-creator sub-agents, running them in parallel when possible.

## User Input:
$ARGUMENTS

## Context Files:
@.claude/commands/meta/generate-agent.md
@.claude/commands/meta/generate-command.md

## Task Implementation

Parse the user's input to extract:
1. **Agent name** (first parameter)
2. **Command syntax(es)** (second parameter, can be comma-separated)
3. **Description** (optional third parameter or inferred from commands)

### Step 1: Create the Specialized Agent

Use the Task tool to delegate to meta-agent with the following specification:

**Agent Creation Request:**
- Agent name: `{extracted agent-name}`
- Purpose: Extracted from the command description and syntax
- Capabilities: Inferred from the command requirements
- Tools needed: Based on command functionality (file ops, web search, etc.)
- Delegation triggers: Keywords that should invoke this agent

### Step 2: Create Command(s) in Parallel

For each command specified in the command(s) parameter:

Use the Task tool to delegate to command-creator with:

**Command Creation Request:**
- Command syntax: `{each command from comma-separated list}`
- Description: `{provided description or inferred from syntax}`
- Implementation: Configure to use Task tool and delegate to the newly created agent
- Argument handling: Pass through all parameters to the agent

### Step 3: Coordinate Results

After both sub-agents complete:
1. Verify the agent was created successfully
2. Verify all commands were created successfully
3. Provide usage examples showing how the new command(s) work
4. Document the delegation pattern for future orchestration

## Example Processing

**Input:** `doc-fetcher "/agent:doc-fetch <package> [url]" "Fetch and condense technical documentation"`

**Should Create:**
1. **Agent**: `.claude/agents/doc-fetcher.md` 
   - Specializes in fetching and condensing technical documentation
   - Has WebSearch, WebFetch, Read, Write tools
   - Triggered by "documentation", "fetch docs", "technical specs"

2. **Command**: `.claude/commands/agent/doc-fetch.md`
   - Syntax: `/agent:doc-fetch <package> [url]`
   - Delegates to doc-fetcher agent via Task tool
   - Passes package and optional URL parameters

## Implementation Notes

- Run agent creation and command creation in parallel when possible
- Handle multiple commands by creating separate delegation tasks
- Ensure the agent has appropriate tools for the command requirements
- Configure commands to properly delegate to the new agent
- Include comprehensive error handling for parsing failures

## Expected Output

Provide a summary showing:
- Agent created at: `.claude/agents/{agent-name}.md`
- Command(s) created at: appropriate paths based on syntax
- Usage examples for the new command(s)
- Delegation triggers for orchestration integration