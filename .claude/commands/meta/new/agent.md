---
allowed-tools: Task
description: Generate a new specialized sub-agent using the meta-agent
argument-hint: <agent-name> [purpose & capabilities]
---

# Generate Agent
Use the meta-agent to create new specialized sub-agents with proper naming and configuration.

## User Input:
$ARGUMENTS

## Task for meta-agent

You are tasked with creating a new specialized sub-agent. Parse the user's input to extract the agent name and specification.

### Agent Naming Convention (STRICT):
- ALL agents must follow `<team>-<agent>` format
- Valid teams: engineering, product, qa, devops, creative, research, marketing, data, meta
- Use `meta-` prefix for Claude Code configuration agents
- Examples:
  - "TechLead" → "engineering-lead"
  - "UXEngineer" → "engineering-ux"
  - "documentation expert" → "engineering-docs"
  - "aiResearch" → "research-ai"
  - "seo specialist" → "marketing-seo"
  - "test automation" → "qa-automation"
- If user provides name without team prefix, infer the most logical team

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
   - Place file at: `.claude/agents/{team}-{agent-name}.md`
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

### Example Input Processing:
- Input: "Create a TechLead agent for code review"
  → Agent name: "engineering-lead" (tech leadership → engineering team)
- Input: "documentation_expert for API docs"
  → Agent name: "engineering-docs" (documentation → engineering team)
- Input: "ai-research agent for staying current"
  → Agent name: "research-ai" (research → research team)
- Input: "seo analysis"
  → Agent name: "marketing-seo" (seo → marketing team)

### Tool Selection Guidelines:
- File operations: Read, Write, Edit, MultiEdit
- Search: Grep, Glob, LS
- Execution: Bash with specific command permissions
- Web: WebSearch, WebFetch, mcp__freecrawl__*
- Task management: TodoWrite, Task
- Browser automation: mcp__playwright__*
- Audio: mcp__ElevenLabs__*

Create the agent configuration file with all necessary details, ensuring the agent name follows the strict `<team>-<agent>` naming convention above.
