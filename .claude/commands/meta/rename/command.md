---
allowed-tools: Task, Bash(git:*), Bash(mv:*), Bash(mkdir:*), Read, Write, Edit, MultiEdit, Glob, Grep, LS
description: Rename a Claude Code command and update all references throughout the project
argument-hint: <current-command> <new-command>
---

# Rename Command - Meta Operation

Rename a Claude Code slash command and automatically update all references throughout the project.

**Current Command**: $ARG1
**New Command**: $ARG2

## Step 1: Parse and Validate Commands

### Parse Command Paths
Converting slash-format commands to file paths:
- Current: `$ARG1` 
- New: `$ARG2`

```bash
# Parse current command path
CURRENT_CMD="$ARG1"
NEW_CMD="$ARG2"

# Remove leading slash and replace colons with slashes
CURRENT_PATH="${CURRENT_CMD#/}"
CURRENT_PATH="${CURRENT_PATH//:://}"
CURRENT_FILE=".claude/commands/${CURRENT_PATH}.md"

NEW_PATH="${NEW_CMD#/}"
NEW_PATH="${NEW_PATH//:://}"
NEW_FILE=".claude/commands/${NEW_PATH}.md"

echo "Current file: $CURRENT_FILE"
echo "New file: $NEW_FILE"
```

### Validate Current Command Exists
!`test -f ".claude/commands/${ARG1#/}.md" && echo "✓ Command exists" || echo "✗ Command not found"`

### Check New Command Doesn't Exist
!`test -f ".claude/commands/${ARG2#/}.md" && echo "✗ New command already exists" || echo "✓ New path available"`

## Step 2: Create Target Directory Structure

```bash
# Extract directory path from new command
NEW_DIR=$(dirname ".claude/commands/${ARG2#/}.md")
mkdir -p "$NEW_DIR"
echo "Created directory: $NEW_DIR"
```

## Step 3: Move Command File

```bash
# Use git mv if in a git repository, otherwise use regular mv
if git rev-parse --git-dir > /dev/null 2>&1; then
    git mv ".claude/commands/${ARG1#/}.md" ".claude/commands/${ARG2#/}.md"
    echo "✓ Moved command file using git mv"
else
    mv ".claude/commands/${ARG1#/}.md" ".claude/commands/${ARG2#/}.md"
    echo "✓ Moved command file using mv"
fi
```

## Step 4: Find and Update References (Parallel Tasks)

Deploy parallel agents to search and replace all references:

### Task 1: Update Command References
**Agent**: engineering-cleanup
**Description**: Update references in command files

```
Search for all occurrences of both:
1. Slash format: "$ARG1"
2. Path format: ".claude/commands/${ARG1#/}.md"

Replace with:
1. Slash format: "$ARG2"
2. Path format: ".claude/commands/${ARG2#/}.md"

Target: .claude/commands/**/*.md
```

### Task 2: Update Agent Definitions
**Agent**: engineering-cleanup
**Description**: Update references in agent configurations

```
Search for all occurrences of both:
1. Slash format: "$ARG1"
2. Path format: ".claude/commands/${ARG1#/}.md"

Replace with:
1. Slash format: "$ARG2"
2. Path format: ".claude/commands/${ARG2#/}.md"

Target: .claude/agents/**/*.md
```

### Task 3: Update Documentation
**Agent**: engineering-writer
**Description**: Update references in documentation

```
Search for all occurrences of both:
1. Slash format: "$ARG1"
2. Command mentions in text or code blocks

Replace with:
1. Slash format: "$ARG2"
2. Updated command references

Targets:
- README.md
- CLAUDE.md
- docs/**/*.md
- .claude/README.md
```

### Task 4: Update Hook Configurations
**Agent**: meta-config
**Description**: Update references in hooks and settings

```
Search for command references in:
- .claude/hooks/**/*.md
- .claude/settings.json (if exists)
- Any configuration files that might reference commands

Update all occurrences of "$ARG1" to "$ARG2"
```

## Step 5: Verification and Code Review

### Task 5: Code Review
**Agent**: engineering-lead
**Description**: Verify consistency of changes

```
Review all changes made during the rename operation:

1. Verify the command file was successfully moved
2. Check that all references were updated consistently
3. Ensure no broken links or missing references
4. Validate command still functions correctly
5. Check for any edge cases or missed references

Provide a summary of:
- Total files changed
- References updated
- Any potential issues found
- Confirmation that rename is complete and consistent
```

## Step 6: Final Verification

### List Updated Files
!`git status --short 2>/dev/null | grep -E "(commands|agents|docs|README|CLAUDE)" || echo "Changes outside git"`

### Verify New Command Structure
!`ls -la ".claude/commands/${ARG2#/}.md" 2>/dev/null || echo "Error: New command file not found"`

## Summary

Command rename operation for `$ARG1` → `$ARG2`:

**Completed Actions:**
1. ✓ Validated command existence and availability
2. ✓ Created new directory structure
3. ✓ Moved command file to new location
4. ✓ Updated all references across project
5. ✓ Performed consistency review

**Next Steps:**
- Test the renamed command: `$ARG2`
- Commit changes if satisfied: `git add -A && git commit -m "refactor: rename command $ARG1 to $ARG2"`
- Update any external documentation or references

## Error Handling

If any step fails:
1. Check file permissions in `.claude/` directory
2. Ensure command names use correct format (`/category:subcategory:command`)
3. Verify no naming conflicts with existing commands
4. Review git status for any uncommitted changes that might interfere