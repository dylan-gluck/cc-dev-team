---
allowed-tools: Task
description: Generate a new specialized sub-agent using the meta-agent
argument-hint: "[name] [purpose & capabilities]"
---

# Generate Agent
Use the meta-agent to create new specialized sub-agents with proper naming and configuration.

## User Input:
$ARGUMENTS

## Task for meta-agent

You are tasked with creating a new specialized sub-agent. Parse the user's input to extract the agent name and specification.

### Agent Naming Convention (STRICT):
- ALL agents must follow camel-case format
- Use `meta-` prefix for Claude Code configuration agents

### Required Specification:

Create a new sub-agent with the following details:

1. **Parse the user's input** to identify:
   - Agent name (apply naming convention above)
   - Core purpose and specialization
   - Primary tasks and responsibilities
   - Domain expertise required
   - Tools needed for the agent's tasks
   - When to invoke proactively
   - Expected output format

2. **Generate Complete Agent Configuration**:
   - Place file at: `.claude/agents/{agent-name}.md`
   - Include comprehensive system prompt
   - Specify minimal but sufficient tool set
   - Define clear delegation triggers
   - Set appropriate model (haiku for speed, sonnet for balance, opus for complexity)
   - Choose identifying color

3. **Agent Structure Requirements**:
   - Single responsibility principle
   - Clear proactive invocation conditions
   - Domain-specific best practices
   - Structured workflow steps
   - Well-defined output format
   - Error handling approach

### Tool Selection Guidelines:
- Subagent delegation: Task
- Multi-step operations: TodoWrite
- Read local files: Read
- Search & list files: Grep, Glob, LS
- Edit existing files: Edit, MultiEdit
- Create new files: Write
- Execution: Bash (with specific command permissions)
- Web: WebSearch, WebFetch, mcp__freecrawl__*
- Browser automation: mcp__playwright__*
- Audio: mcp__ElevenLabs__*

#### Remember:
**ALWAYS** enable TodoWrite tool for all agents
**ALWAYS** enable Task when subagent functionality is expected

Create the agent configuration file with all necessary details, ensuring the agent name follows the strict camel-case naming convention.
