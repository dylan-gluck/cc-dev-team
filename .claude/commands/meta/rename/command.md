---
allowed-tools: Task
description: Rename a Claude Code command and update all references throughout the project
argument-hint: <current-command> <new-command>
---

# Rename Command - Meta Operation

Delegate to the specialized meta-rename agent to rename a Claude Code slash command and update all references.

## Task Delegation

Delegating the rename operation to the specialized meta-rename agent.

**Task**: Rename command from `$ARG1` to `$ARG2`

### Invoking Meta-Rename Agent

```task
subagent_type: meta-rename
description: Rename command $ARG1 to $ARG2
prompt: |
  Execute a complete rename operation for a Claude Code command.
  
  Source command: $ARG1
  Target command: $ARG2
  
  Your responsibilities:
  1. Validate that the source command exists
  2. Ensure the target path is available
  3. Create any necessary directory structure
  4. Move the command file using git mv
  5. Search for and update ALL references including:
     - Command references in other commands
     - References in agent definitions
     - Documentation mentions
     - Hook configurations
     - Any other occurrences
  6. Verify the rename was successful
  7. Provide a comprehensive summary of changes
  
  Use parallel sub-agents where appropriate for faster execution.
  Report any errors or issues encountered.
```

The meta-rename agent will handle:
- File validation and movement
- Comprehensive reference updates
- Parallel execution for efficiency
- Complete verification and reporting