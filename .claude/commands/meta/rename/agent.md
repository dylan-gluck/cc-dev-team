---
allowed-tools: Task
description: Rename a Claude Code agent and update all references
argument-hint: <current-agent-name> <new-agent-name>
---

# Rename Agent - Meta Operation

Delegate to the specialized meta-rename agent to rename a Claude Code agent and update all references.

## Task Delegation

Delegating the rename operation to the specialized meta-rename agent.

**Task**: Rename agent from `$ARG1` to `$ARG2`

### Invoking Meta-Rename Agent

```task
subagent_type: meta-rename
description: Rename agent $ARG1 to $ARG2
prompt: |
  Execute a complete rename operation for a Claude Code agent.

  Source agent: $ARG1
  Target agent: $ARG2

  Your responsibilities:
  1. Validate that the source agent exists at ${ARG1}
  2. Ensure the target name is available
  3. Move the agent file
  4. Update agent metadata in the file itself
  5. Search `.claude/` for and update ALL references including:
     - Task tool subagent_type parameters
     - Agent mentions in commands
     - Documentation references
     - Hook configurations
     - Status line references
     - CLAUDE.md agent lists
     - Any other occurrences
  6. Verify the rename was successful
  7. Provide a comprehensive summary of changes

  Pay special attention to:
  - Task tool calls that use subagent_type: "${ARG1}"
  - Agent collaboration references
  - Documentation lists of available agents

  Use parallel sub-agents where appropriate for faster execution.
  Report any errors or issues encountered.
```

The meta-rename agent will handle:
- Agent file movement and validation
- Metadata updates within the agent file
- Comprehensive reference updates across all project files
- Task tool parameter updates
- Complete verification and reporting
