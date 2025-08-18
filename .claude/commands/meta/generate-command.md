---
allowed-tools: Bash, Write, Read, Glob, Grep, Edit, LS, WebFetch, WebSearch
description: Generate a new Claude Code command file from a description
---

# Generate Command
Create a new command file following the standard command template format.

## User Prompt:
$ARGUMENTS

## Instructions

### 1. Parse Command Requirements
Extract from the user's description:
- Command name (will become the filename without .md extension)
- Primary purpose and intended use cases
- Required tools and capabilities
- Whether it needs file access, bash execution, or other special features
- Expected arguments (if any)

### 2. Configure Frontmatter
Every command MUST include frontmatter with these fields:

#### Required Fields:
- `allowed-tools`: Specify exact tools needed. Available tools include:
  - **File Operations**: `Read`, `Write`, `Edit`, `MultiEdit`, `NotebookEdit`
  - **Search Tools**: `Glob`, `Grep`, `LS`
  - **Execution**: `Bash(command:*)` - specify exact commands or patterns
  - **Web Tools**: `WebFetch`, `WebSearch`
  - **Specialized**: `Task`, `TodoWrite`, `ExitPlanMode`
  - **MCP Tools**: Any `mcp__*` prefixed tools if MCP servers are connected
  - **Browser Tools**: `mcp__playwright__*` for browser automation
  - **Audio Tools**: `mcp__ElevenLabs__*` for text-to-speech
- `description`: Brief one-line description (shows in /help)

#### Optional Fields:
- `argument-hint`: Format hint for arguments (e.g., `[file-path] [options]`)
- `model`: Specific model to use (e.g., `claude-3-5-haiku-20241022` for fast tasks)

### 3. Tool Selection Guidelines

Choose tools based on the command's purpose:

**For Code Analysis Commands:**
```yaml
allowed-tools: Read, Grep, Glob, LS
```

**For Code Modification Commands:**
```yaml
allowed-tools: Read, Edit, MultiEdit, Write, Bash(npm test:*), Bash(npm run:*)
```

**For Git Operations:**
```yaml
allowed-tools: Bash(git:*), Read, Write
```

**For Research Commands:**
```yaml
allowed-tools: WebSearch, WebFetch, Task, Write
```

**For Build/Deploy Commands:**
```yaml
allowed-tools: Bash(npm:*), Bash(docker:*), Bash(kubectl:*), Read
```

### 4. Command Body Structure

The command body should follow this template:

```markdown
---
allowed-tools: [specific tools needed]
argument-hint: [optional argument format]
description: [brief description]
model: [optional model preference]
---

# [Command Title]

[Brief introduction of what this command does]

## Context
[Include any necessary context gathering, such as:]
- Current status: !`bash command` (requires Bash tool)
- File contents: @path/to/file (automatic file inclusion)
- User input: $ARGUMENTS (if arguments are expected)

## Task
[Clear, specific instructions for Claude Code]

## Expected Output
[Describe what the command should produce]

## Constraints
[Any limitations or requirements]
```

### 5. Special Features

#### Bash Command Execution
To include command output in context, use `!` prefix:
```markdown
- Current branch: !`git branch --show-current`
- Test results: !`npm test`
```
**IMPORTANT**: Must include specific Bash permissions in allowed-tools

#### File References
Include file contents with `@` prefix:
```markdown
Review the code in @src/main.js
Compare @old-version.js with @new-version.js
```

#### Arguments
Use `$ARGUMENTS` placeholder for dynamic values:
```markdown
Fix issue #$ARGUMENTS following our coding standards
```

#### Extended Thinking
Trigger deep analysis by including keywords:
- "think step by step"
- "reason through this"
- "analyze carefully"

### 6. Directory Structure

Place commands in appropriate subdirectories:
- `.claude/commands/` - Base directory for all project commands
- `.claude/commands/dev/` - Development tasks (build, test, debug)
- `.claude/commands/git/` - Git operations
- `.claude/commands/docs/` - Documentation generation
- `.claude/commands/analysis/` - Code analysis and review
- `.claude/commands/meta/` - Command/agent generation
- `.claude/commands/refactor/` - Refactoring operations
- `.claude/commands/deploy/` - Deployment and infrastructure

### 7. Validation Checklist

Before creating the command file, ensure:
- [ ] Command name is clear and follows naming conventions (lowercase, hyphens)
- [ ] Frontmatter includes all required fields
- [ ] allowed-tools list is minimal but sufficient
- [ ] Bash commands have specific permissions (not just `Bash`)
- [ ] Description is concise and informative
- [ ] Body includes clear instructions
- [ ] Arguments are properly documented if used
- [ ] File is placed in the correct subdirectory

## Workflow
1. Parse the user's command description
2. Determine required tools and capabilities
3. Select appropriate subdirectory under `.claude/commands/`
4. Generate frontmatter with precise tool permissions
5. Create command body with clear instructions
6. Include any necessary context gathering (bash commands, file references)
7. Write the command file to the correct location
8. Validate the command follows all guidelines

## Files:
@.claude/templates/command.md
@ai_docs/cc/anthropic_custom_slash_commands.md
