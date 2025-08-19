# GitHub Commit Message Template

## Format
```
<type>(<scope>): <subject>

<body>

<footer>
```

## Types
- **feat**: New feature or functionality
- **fix**: Bug fix
- **docs**: Documentation changes only
- **style**: Code style changes (formatting, semicolons, etc)
- **refactor**: Code restructuring without changing functionality
- **perf**: Performance improvements
- **test**: Adding or updating tests
- **build**: Build system or dependency changes
- **ci**: CI/CD configuration changes
- **chore**: Maintenance tasks, tool updates
- **revert**: Reverting a previous commit

## Scope (optional)
Brief identifier of the affected component, module, or area:
- `api`, `ui`, `auth`, `db`, `config`, `deps`, etc.

## Subject
- Use imperative mood ("add" not "adds" or "added")
- Don't capitalize first letter
- No period at the end
- Maximum 50 characters

## Body (optional)
- Explain **what** and **why** (not how)
- Wrap at 72 characters
- Use bullet points for multiple changes
- Reference issues and PRs when relevant

## Footer (optional)
- **BREAKING CHANGE**: Description of breaking changes
- **Fixes #123**: Close issues
- **Refs #456**: Reference related issues
- **Co-authored-by**: Credit collaborators

## Examples

### Simple Feature
```
feat(auth): add OAuth2 integration with GitHub

- Implement OAuth2 flow for GitHub authentication
- Add token refresh mechanism
- Store encrypted tokens in database

Fixes #234
```

### Bug Fix
```
fix(api): prevent race condition in payment processing

Multiple concurrent requests could cause duplicate charges.
Added mutex lock to ensure sequential processing of 
payment transactions for the same user.

Fixes #567
```

### Breaking Change
```
feat(api)!: restructure response format for v2

- Changed error response structure
- Renamed 'data' field to 'payload'
- Added mandatory 'version' field

BREAKING CHANGE: API responses now use 'payload' instead
of 'data' field. Clients must update their parsing logic.

Migration guide: docs/migration/v2.md
```

### Multiple Scope Changes
```
refactor: modernize build pipeline

- build: migrate from webpack to vite
- test: update jest to vitest
- ci: optimize GitHub Actions workflow
- deps: upgrade to React 18

Reduces build time by 60% and improves HMR performance.
```

### Revert
```
revert: "feat(ui): add experimental dark mode"

This reverts commit a1b2c3d4e5f6.

Dark mode caused unexpected layout issues on mobile
devices. Reverting until responsive design is fixed.

Refs #789
```

## Best Practices

1. **Atomic Commits**: One logical change per commit
2. **Clear History**: Write messages for future developers
3. **Searchable**: Use consistent types and scopes
4. **Actionable**: Include issue numbers for tracking
5. **Concise**: Keep subject line under 50 chars
6. **Detailed**: Use body for complex changes
7. **Conventional**: Follow team's agreed format

## Quick Reference

```bash
# Interactive commit with template
git commit

# One-line commit (simple changes only)
git commit -m "fix(auth): correct token expiry calculation"

# Multi-line from command line
git commit -m "feat(api): add rate limiting" -m "- Implement token bucket algorithm" -m "- Add Redis for distributed limiting"

# Amend last commit
git commit --amend

# Sign commits
git commit -S -m "feat: add commit signing"
```

## VS Code Integration

Add to `.vscode/settings.json`:
```json
{
  "conventionalCommits.scopes": [
    "api", "ui", "auth", "db", "config", "deps", "docs"
  ]
}
```

## Git Hooks (commitlint)

`.commitlintrc.json`:
```json
{
  "extends": ["@commitlint/config-conventional"],
  "rules": {
    "subject-max-length": [2, "always", 50],
    "body-max-line-length": [2, "always", 72]
  }
}
```