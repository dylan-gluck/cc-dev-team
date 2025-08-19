---
allowed-tools: Bash(git:*), Read, LS
description: Create a git commit with staged changes
---

# Git Commit

Analyze the current repository state and create a meaningful commit.

## Context

- Current Status: !`git status`
- Staged changes: !`git diff --cached`
- Current branch: !`git branch --show-current`
- Recent commits: !`git log --oneline -5`

## Task

Based on the staged changes above:
1. Analyze what has been changed
2. Create an appropriate semantic commit message (`feat:`, `fix:`, `docs:`, etc.)
3. Commit the staged changes

Scope: $ARGUMENTS

## Commit Guidelines

- Use semantic commit prefixes: `feat:`, `fix:`, `docs:`, `chore:`, `refactor:`, `test:`
- Keep commit messages concise and descriptive
- Focus on what changed and why, not how
- Do not use emojis
- Do not credit Claude
