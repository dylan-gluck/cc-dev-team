---
allowed-tools: Write, Read, Edit, LS, WebFetch, WebSearch
description: Generate a new specialized sub-agent configuration file from a description
argument-hint: <agent-purpose> [specific requirements]
---

# Generate Agent
Create a new specialized sub-agent by delegating to the meta-agent with a clear description of the agent's purpose and capabilities.

## User Prompt:
$ARGUMENTS

## Instructions

### 1. Parse Agent Requirements
Extract from the user's description:
- Agent's core purpose and specialization
- Primary tasks and responsibilities
- Domain expertise required
- Specific tools needed for the agent's tasks
- When the agent should be proactively invoked
- Expected output format or deliverables

### 2. Prepare Meta-Agent Delegation
Use the Task tool to invoke the meta-agent specialist with:
- `subagent_type`: "meta-agent"
- `description`: Brief summary of the agent being created
- `prompt`: Comprehensive agent specification including all details below

### 3. Provide Complete Agent Specification
Include these essential details in your prompt to meta-agent:

#### Core Configuration:
- **Name**: Suggest a kebab-case name (e.g., code-reviewer, test-runner)
- **Description**: Action-oriented description for automatic delegation
  - Use phrases like "Use proactively when...", "Specialist for..."
  - Clearly state trigger conditions
- **Model**: Specify if needed (haiku for speed, sonnet for balance, opus for complexity)
- **Color**: Visual identifier (red, blue, green, yellow, purple, orange, pink, cyan)

#### Tool Requirements:
- Specify exact tools needed based on the agent's tasks
- Reference available tool categories:
  - File Operations: Read, Write, Edit, MultiEdit, NotebookEdit
  - Search: Grep, Glob, LS
  - Execution: Bash(command:*) with specific permissions
  - Web: WebSearch, WebFetch
  - Task Management: TodoWrite, Task
  - MCP Tools: mcp__* prefixed tools if needed
  - Browser: mcp__playwright__* for automation
  - Audio: mcp__ElevenLabs__* for TTS/STT

#### System Prompt Elements:
- Clear role definition and expertise area
- Step-by-step workflow when invoked
- Best practices for the domain
- Output format and structure
- Quality checks and validation steps
- Error handling approach

### 4. Example Delegation Format
```
Create a new sub-agent with the following specification:

Purpose: [Detailed purpose]
Trigger: [When to use proactively]
Tasks: [List of primary responsibilities]
Tools Needed: [Specific tools required]
Output: [Expected deliverables]
Domain: [Area of expertise]
Special Requirements: [Any unique needs]
```

### 5. Quality Validation
Ensure the specification includes:
- [ ] Clear, single-responsibility purpose
- [ ] Proactive trigger conditions
- [ ] Minimal but sufficient tool set
- [ ] Structured workflow steps
- [ ] Domain-specific best practices
- [ ] Well-defined output format

## Workflow
1. Parse the user's agent description thoroughly
2. Identify all required capabilities and tools
3. Delegate to meta-agent with subagent_type "meta-agent"
4. Provide comprehensive specification with all details
5. Meta-agent will create the complete `.claude/agents/{agent-name}.md` file
6. Confirm successful agent creation

## Files:
@.claude/agents/meta-agent.md
@ai_docs/cc/anthropic_docs_subagents.md
