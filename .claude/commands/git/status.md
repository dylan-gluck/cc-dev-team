---
allowed-tools: Bash(git:*)
description: Show comprehensive git repository status
---

# Git Status

Display the current state of the git repository.

## Repository Information

- Working directory status: !`git status`
- Current branch: !`git branch --show-current`
- Uncommitted changes: !`git diff HEAD`
- Recent commits: !`git log --oneline -10`

## Task

Provide a clear summary of:
1. Current branch and its status
2. Any uncommitted changes (staged and unstaged)
3. Recent commit history
4. Any files that need attention