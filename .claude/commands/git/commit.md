---
allowed-tools: Bash(git status:*), Bash(git diff:*), Bash(git log:*), Bash(git add:*), Bash(git commit:*), Bash(git push:*), Bash(git branch:*), Bash(git remote:*), Read
description: Create a git commit with staged changes and optionally push to remote
argument-hint: [message] [--push] [--push-force] [--set-upstream] [--no-verify]
model: sonnet
---

# Git Commit

Create a conventional commit with staged changes and optionally push to remote repository.

## Arguments

Parse the following arguments from: $ARGUMENTS

- **Commit message**: Any text not starting with `--` becomes part of the commit message
- **--push**: Automatically push to remote after successful commit
- **--push-force**: Force push with lease after commit (implies --push)
- **--set-upstream**: Set upstream branch and push (implies --push)
- **--no-verify**: Skip pre-commit hooks during commit

## Workflow

### 1. Parse Arguments
Extract flags and message from $ARGUMENTS:
- Identify push-related flags
- Collect non-flag arguments as commit message hint
- Set appropriate flags for later processing

### 2. Analyze Repository State
Run the following commands to understand current state:
- !`git status` - Check for staged/unstaged changes
- !`git diff --cached` - Review staged changes in detail
- !`git log --oneline -5` - Recent commit history for context
- !`git branch --show-current` - Current branch name

### 3. Determine Commit Type
Based on the changes, determine:
- Commit type: feat, fix, docs, style, refactor, test, chore, perf, ci, build
- Scope (if applicable): component, module, or feature area
- Breaking changes: Look for API changes, removals, or incompatible updates

### 4. Create Commit Message
Follow conventional commit format:
```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

Reference template: @.claude/templates/commit-message.md

### 5. Execute Commit
Build the git commit command:
- If --no-verify flag is present: !`git commit --no-verify -m "<message>"`
- Otherwise: !`git commit -m "<message>"`

Handle any pre-commit hook modifications:
- If hooks modify files, stage changes and retry once
- Report any persistent failures

### 6. Push to Remote (if requested)
If any push flag was provided:

1. **Check remote connectivity**: !`git remote -v`
2. **Get current branch**: !`git branch --show-current`
3. **Check if branch exists on remote**: !`git ls-remote --heads origin <branch>`

4. **Execute appropriate push command**:
   - If --set-upstream: !`git push --set-upstream origin <branch>`
   - If --push-force: !`git push --force-with-lease origin <branch>`
   - If --push only: !`git push origin <branch>`

5. **Handle push results**:
   - Report success with remote URL
   - Handle authentication errors
   - Explain any rejection reasons
   - Suggest solutions for common issues

### 7. Confirm Results
Show final status:
- Commit hash and message
- Push status (if attempted)
- Remote branch URL (if pushed)
- Any warnings or next steps

## Error Handling

- **No staged changes**: Inform user and suggest `git add`
- **Pre-commit failures**: Show hook output and suggestions
- **Push rejected**: Explain reason (behind remote, protected branch, etc.)
- **Network issues**: Suggest checking connectivity and credentials
- **Force push safety**: Warn about implications before executing

## Examples

```bash
# Basic commit
/git:commit

# Commit with message hint
/git:commit fix authentication bug

# Commit and push
/git:commit --push

# Commit with message and push
/git:commit "feat: add user dashboard" --push

# Force push after commit
/git:commit --push-force

# Create new remote branch
/git:commit --set-upstream

# Skip hooks and push
/git:commit --no-verify --push
```

## Safety Notes

- Force push uses `--force-with-lease` for safety
- Always shows diff before committing
- Warns before destructive operations
- Validates remote access before pushing
- Preserves all existing staged changes