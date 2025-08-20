---
allowed-tools: Task, Bash(git:*), Bash(npm version:*), Bash(gh release:*)
argument-hint: [major|minor|patch|prerelease] [--dry-run] [--no-push]
description: Automatically prepare a release with version bump, changelog, and tagging
---

# Git Tag Release

Automatically prepare and publish a new release using the devops-release agent.

## Options: $ARGUMENTS

### Release Automation

This command delegates to the specialized devops-release agent to handle the complete release process:

1. **Version Determination**: Analyze commits to determine appropriate version bump
2. **Changelog Generation**: Create comprehensive changelog from commit history
3. **Release Notes**: Generate detailed release notes for GitHub/GitLab
4. **Version Bumping**: Update version in package.json, pyproject.toml, etc.
5. **Tagging**: Create and push git tag with proper formatting
6. **Release Publishing**: Optionally create GitHub release

### Argument Parsing

```bash
# Parse options from $ARGUMENTS
VERSION_TYPE=""
DRY_RUN=false
NO_PUSH=false

for arg in $ARGUMENTS; do
  case $arg in
    major|minor|patch|prerelease)
      VERSION_TYPE=$arg
      ;;
    --dry-run)
      DRY_RUN=true
      ;;
    --no-push)
      NO_PUSH=true
      ;;
  esac
done
```

### Agent Delegation

Spawn the devops-release agent with comprehensive instructions:

```task
subagent_type: devops-release
description: Prepare and publish release
prompt: |
  Execute a complete release preparation workflow.
  
  Options provided:
  - Version type: ${VERSION_TYPE:-auto-detect}
  - Dry run: $DRY_RUN
  - No push: $NO_PUSH
  
  Your responsibilities:
  
  1. **Analyze Recent Changes**
     - Review commits since last tag: git log $(git describe --tags --abbrev=0)..HEAD
     - Categorize changes (features, fixes, breaking changes)
     - Determine version bump if not specified
  
  2. **Version Determination**
     - If VERSION_TYPE provided, use it
     - Otherwise, analyze commits:
       - Breaking changes → major
       - New features → minor
       - Bug fixes only → patch
     - Check current version from package.json/pyproject.toml
     - Calculate new version number
  
  3. **Update Version Files**
     - package.json (npm/node projects)
     - pyproject.toml (Python projects)
     - version.rb (Ruby projects)
     - Cargo.toml (Rust projects)
     - Any VERSION or version.txt files
  
  4. **Generate Changelog**
     - Create/update CHANGELOG.md
     - Group changes by type:
       - 🚀 Features
       - 🐛 Bug Fixes
       - 💥 Breaking Changes
       - 📚 Documentation
       - 🔧 Maintenance
     - Include contributor acknowledgments
     - Add comparison link to previous version
  
  5. **Create Release Notes**
     - Summary of major changes
     - Migration guide for breaking changes
     - Acknowledgments section
     - Full changelog link
  
  6. **Git Operations**
     - Stage all version and changelog files
     - Create release commit: "chore(release): v{version}"
     - Create annotated tag: "v{version}"
     - Include release notes in tag message
  
  7. **Publish Release** (unless --dry-run or --no-push)
     - Push commit to main/master
     - Push tag to origin
     - Create GitHub release if gh CLI available
     - Attach any build artifacts if present
  
  8. **Post-Release Tasks**
     - Update development version (if using snapshot/dev versions)
     - Create post-release commit if needed
     - Report success with release URL
  
  If --dry-run is set:
  - Show what would be changed
  - Display new version number
  - Preview changelog entries
  - Do not make any actual changes
  
  If --no-push is set:
  - Create all local changes
  - Create tag locally
  - Do not push to remote
  
  Report any errors encountered and provide recovery instructions if needed.
```

### Usage Examples

```bash
# Auto-detect version bump from commits
/git:tag

# Specific version bump
/git:tag minor
/git:tag major
/git:tag patch

# Pre-release version
/git:tag prerelease

# Dry run to preview changes
/git:tag minor --dry-run

# Create tag locally without pushing
/git:tag patch --no-push

# Combine options
/git:tag major --dry-run --no-push
```

### Pre-Release Checklist

The devops-release agent will verify:
- ✅ Working directory is clean
- ✅ On main/master branch (or configured release branch)
- ✅ All tests passing
- ✅ No uncommitted changes
- ✅ Remote is accessible
- ✅ Has permission to push tags

### Version Bump Rules

**Major (x.0.0)**
- Breaking API changes
- Major architectural changes
- Incompatible changes

**Minor (0.x.0)**
- New features
- New functionality
- Backward compatible changes

**Patch (0.0.x)**
- Bug fixes
- Security patches
- Documentation updates
- Small improvements

**Prerelease**
- Alpha/Beta/RC versions
- Testing releases
- Preview features

### Output Format

The agent will provide:
1. Current version → New version
2. List of changes included
3. Generated changelog preview
4. Release notes preview
5. Git operations performed
6. Release URL (if published)

### Error Handling

If the release process fails:
- Rollback any local changes
- Provide clear error message
- Suggest recovery steps
- Preserve work in backup branch if needed

The release process ensures consistent, well-documented releases with proper versioning and comprehensive changelogs.