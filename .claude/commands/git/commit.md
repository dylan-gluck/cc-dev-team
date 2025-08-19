---
allowed-tools: Task
description: Create a git commit with staged changes using the git-commit agent
argument-hint: [optional scope or message]
---

# Git Commit

Delegate to the specialized git-commit agent to analyze repository state and create a conventional commit.

## Task for git-commit Agent

Analyze the current repository state and create a meaningful conventional commit message.

Additional context: $ARGUMENTS

### Your responsibilities:
1. Run git commands to understand the current state:
   - `git status` to see staged/unstaged files
   - `git diff --cached` to examine staged changes
   - `git log --oneline -5` for recent commit context
   - `git branch --show-current` for branch information

2. Analyze the changes and determine:
   - Appropriate commit type (feat, fix, docs, refactor, etc.)
   - Scope if applicable (api, ui, auth, etc.)
   - Whether changes constitute breaking changes

3. Create and execute a conventional commit:
   - Format: `<type>(<scope>): <subject>`
   - Include detailed body if changes are complex
   - Reference issues if mentioned in arguments
   - Follow all conventional commit best practices

4. Confirm successful commit with the commit hash.

Reference the commit message template at: @.claude/templates/commit-message.md
