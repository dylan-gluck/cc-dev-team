---
allowed-tools: Bash(git:*), Read, LS
description: Understand the current state of the git repository
---

# Git Status

Check git status, diff and logs to get a clear understanding of the current state of the git repository. Craft a clear commit message that summarizes the changes.

Scope: $ARGUMENTS

## Universal Rules

- Semantic commits: `feat:`, `fix:`, `docs:`
- Format code before every commit
- Do not use emojis
- Do not credit claude

## Command Examples

- Current Status: !`git status`
- Add all: !`git add .`
- Current diff: !`git diff HEAD origin/main`
- Current branch: !`git branch --show-current`
- Log: !`git log`
- Git commit: !`git commit -m "$MESSAGE"`

## Files
@README.md
