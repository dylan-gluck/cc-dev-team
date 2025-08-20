---
allowed-tools: Task, Bash(git:*), Bash(mv:*), Bash(mkdir:*), Read, Write, Edit, MultiEdit, Glob, Grep, LS
description: Rename a Claude Code agent and update all references throughout the project
argument-hint: <current-agent-name> <new-agent-name>
---

# Rename Agent - Meta Operation

Rename a Claude Code agent and automatically update all references throughout the project.

**Current Agent**: $ARG1
**New Agent**: $ARG2

## Step 1: Parse and Validate Agent Names

### Parse Agent File Paths
Converting agent names to file paths:
- Current: `$ARG1` 
- New: `$ARG2`

```bash
# Parse agent names
CURRENT_AGENT="$ARG1"
NEW_AGENT="$ARG2"

# Create file paths
CURRENT_FILE=".claude/agents/${CURRENT_AGENT}.md"
NEW_FILE=".claude/agents/${NEW_AGENT}.md"

echo "Current file: $CURRENT_FILE"
echo "New file: $NEW_FILE"
```

### Validate Current Agent Exists
!`test -f ".claude/agents/${ARG1}.md" && echo "✓ Agent exists" || echo "✗ Agent not found"`

### Check New Agent Doesn't Exist
!`test -f ".claude/agents/${ARG2}.md" && echo "✗ New agent already exists" || echo "✓ New name available"`

## Step 2: Move Agent File

```bash
# Use git mv if in a git repository, otherwise use regular mv
if git rev-parse --git-dir > /dev/null 2>&1; then
    git mv ".claude/agents/${ARG1}.md" ".claude/agents/${ARG2}.md"
    echo "✓ Moved agent file using git mv"
else
    mv ".claude/agents/${ARG1}.md" ".claude/agents/${ARG2}.md"
    echo "✓ Moved agent file using mv"
fi
```

## Step 3: Update Agent Metadata

### Update Agent Name in File
**Agent**: engineering-cleanup
**Description**: Update agent name in metadata

```
Read the moved agent file at .claude/agents/${ARG2}.md
Update the following:
1. Agent name in the YAML frontmatter (if present)
2. Any self-references to the agent name in the description
3. Update the delegation description to reflect the new name

Ensure the agent's internal name matches its filename.
```

## Step 4: Find and Update References (Parallel Tasks)

Deploy parallel agents to search and replace all references:

### Task 1: Update Command References
**Agent**: engineering-cleanup
**Description**: Update agent references in command files

```
Search for all occurrences of:
1. Agent name in Task tool calls: subagent_type: "${ARG1}"
2. Agent mentions in descriptions or documentation
3. File path references: .claude/agents/${ARG1}.md

Replace with:
1. subagent_type: "${ARG2}"
2. Updated agent name in text
3. .claude/agents/${ARG2}.md

Target: .claude/commands/**/*.md
```

### Task 2: Update Other Agent References
**Agent**: engineering-cleanup
**Description**: Update references in other agent configurations

```
Search for all occurrences of:
1. References to the agent in Task tool calls
2. Mentions in agent collaboration descriptions
3. Path references to the agent file

Replace all occurrences of "${ARG1}" with "${ARG2}"

Target: .claude/agents/**/*.md
```

### Task 3: Update Documentation
**Agent**: engineering-writer
**Description**: Update references in documentation

```
Search for all occurrences of:
1. Agent name: "${ARG1}"
2. Agent descriptions and usage examples
3. Lists of available agents

Replace with:
1. Agent name: "${ARG2}"
2. Updated references maintaining context

Targets:
- README.md
- CLAUDE.md
- docs/**/*.md
- .claude/README.md
- .claude/TODO.md
```

### Task 4: Update Hook Configurations
**Agent**: meta-config
**Description**: Update references in hooks and settings

```
Search for agent references in:
- .claude/hooks/**/*.py
- .claude/hooks/**/*.md
- .claude/settings.json (if exists)
- Any configuration files that might reference agents

Update all occurrences of "${ARG1}" to "${ARG2}"
```

### Task 5: Update Status Lines
**Agent**: engineering-cleanup
**Description**: Update agent references in status line configurations

```
Search for agent references in:
- .claude/status_lines/**/*.py
- Any status line configuration that might list or reference agents

Update all occurrences of "${ARG1}" to "${ARG2}"
```

## Step 5: Verification and Code Review

### Task 6: Code Review
**Agent**: engineering-lead
**Description**: Verify consistency of changes

```
Review all changes made during the rename operation:

1. Verify the agent file was successfully moved
2. Check that all references were updated consistently
3. Ensure no broken Task tool calls
4. Validate agent still functions correctly with new name
5. Check for any edge cases or missed references
6. Verify CLAUDE.md agent lists are updated

Provide a summary of:
- Total files changed
- References updated
- Any potential issues found
- Confirmation that rename is complete and consistent
```

## Step 6: Final Verification

### List Updated Files
!`git status --short 2>/dev/null | grep -E "(agents|commands|docs|README|CLAUDE|hooks|status)" || echo "Changes outside git"`

### Verify New Agent File
!`ls -la ".claude/agents/${ARG2}.md" 2>/dev/null || echo "Error: New agent file not found"`

### Test Agent Invocation
Test that the renamed agent can still be invoked:

```bash
# This is a validation message, not an actual invocation
echo "Ready to test agent '${ARG2}' via Task tool"
echo "Suggested test: Use Task tool with subagent_type: '${ARG2}'"
```

## Summary

Agent rename operation for `$ARG1` → `$ARG2`:

**Completed Actions:**
1. ✓ Validated agent existence and availability
2. ✓ Moved agent file to new name
3. ✓ Updated agent metadata and self-references
4. ✓ Updated all references across project
5. ✓ Performed consistency review

**Next Steps:**
- Test the renamed agent: Use Task tool with `subagent_type: "${ARG2}"`
- Commit changes if satisfied: `git add -A && git commit -m "refactor: rename agent ${ARG1} to ${ARG2}"`
- Update any external documentation or references
- Notify team members of the agent name change

## Error Handling

If any step fails:
1. Check file permissions in `.claude/agents/` directory
2. Ensure agent names follow naming conventions (e.g., `team-role` format)
3. Verify no naming conflicts with existing agents
4. Review git status for any uncommitted changes that might interfere
5. Check that all Task tool references are updated correctly