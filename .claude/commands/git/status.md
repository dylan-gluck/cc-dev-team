---
allowed-tools: Task
description: Show comprehensive git repository status using the git-commit agent
---

# Git Status

Delegate to the meta-commit agent to analyze and display the current repository state.

## Task for meta-commit Agent

Provide a comprehensive analysis of the current git repository state.

### Your responsibilities:

1. **Gather Repository Information**:
   - Run `git status` to show working directory status
   - Run `git branch --show-current` to identify current branch
   - Run `git diff HEAD` to show all uncommitted changes
   - Run `git log --oneline -10` to show recent commit history
   - Run `git remote -v` to show remote repositories (if any)

2. **Analyze and Summarize**:
   - Current branch and its tracking status
   - Files with staged changes (ready to commit)
   - Files with unstaged changes (modified but not staged)
   - Untracked files (new files not in git)
   - Recent commit history with types and scopes
   - Any merge conflicts or rebase in progress

3. **Provide Actionable Information**:
   - Suggest next steps if changes are staged (ready to commit)
   - Identify files that may need attention
   - Note any unusual repository states

4. **Format Output**:
   - Use clear sections for different aspects of status
   - Highlight important information
   - Keep summary concise but comprehensive

Do not create any commits - this is purely an informational command.
