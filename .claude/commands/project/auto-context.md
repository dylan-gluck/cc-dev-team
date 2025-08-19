---
allowed-tools: Read, Glob, Grep, LS, Bash(git:*), Bash(ls:*), Bash(find:*), Bash(fd:*), Bash(rg:*)
description: Automatically analyze project structure and load relevant context
argument-hint: [specific requirements]
---

# Auto-Context Project Analysis

Perform comprehensive project analysis to understand the codebase structure, identify key files, and load relevant context for the current task.

## User Requirements
$ARGUMENTS

## Project Discovery

### Repository Status
!`git status --short || echo "Not a git repository"`
!`git branch --show-current 2>/dev/null || echo "No git branch"`

### Configuration Files
@package.json (if exists)
@pyproject.toml (if exists)
@Cargo.toml (if exists)
@go.mod (if exists)
@pom.xml (if exists)
@build.gradle (if exists)
@Gemfile (if exists)
@composer.json (if exists)

### Documentation
@README.md (if exists)
@CLAUDE.md (if exists)
@.claude/CLAUDE.md (if exists)
@docs/README.md (if exists)

### Key Directories
!`fd -t d -d 2 . 2>/dev/null || find . -type d -maxdepth 2 2>/dev/null | head -30`

## Analysis Tasks

1. **Identify Project Type**: Determine the primary programming language(s) and framework(s)
2. **Map Structure**: Understand the directory layout and organization patterns
3. **Find Entry Points**: Locate main files, index files, or application entry points
4. **Detect Dependencies**: Review package files for key dependencies
5. **Understand Architecture**: Identify patterns (MVC, microservices, monorepo, etc.)
6. **Locate Tests**: Find test directories and testing frameworks
7. **Review Documentation**: Check for README, docs, or inline documentation

## Context Summary

After analysis, provide:
- **Project Type**: Language, framework, and tooling
- **Architecture**: High-level structure and patterns
- **Key Files**: Most important files to understand the project
- **Dependencies**: Major libraries and frameworks
- **Development Setup**: How to build, test, and run the project
- **Notable Features**: Any special configurations or unique aspects

## Next Steps

Based on the analysis, suggest:
1. Which files to examine for deeper understanding
2. Any missing documentation or setup steps
3. Potential areas needing attention
4. Recommended development workflow for this project type
