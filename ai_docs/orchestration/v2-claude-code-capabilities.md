---
source: Claude Code Documentation Research
fetched: 2025-08-21
version: 1.0.80+
---

# Claude Code v2 Capabilities Documentation

## Overview

Claude Code is Anthropic's agentic coding tool that operates directly in the terminal, powered by Sonnet 4 and Opus 4.1 models. This document provides comprehensive technical details about session management, hooks system, output styles, and architectural constraints discovered through research of official documentation and community resources.

## Session Management Architecture

### Session Lifecycle

Claude Code sessions follow a distinct lifecycle with specific boundaries and isolation characteristics:

1. **Session Initialization**
   - Each `claude` command creates a new session or resumes existing
   - Sessions are identified by unique `session_id` (UUID format)
   - Sessions inherit the bash environment and current working directory
   - CLAUDE.md files are automatically loaded into context at startup

2. **Session Isolation**
   - **Strong Isolation**: Each CLI invocation operates independently by default
   - **No Native Inter-Session Communication**: Sessions cannot directly communicate
   - **Context Reset**: Each new session starts without memory of previous sessions
   - **Workarounds**: Shared files, git worktrees, and specialized tooling (e.g., ccswitch)

3. **Session Resume/Continue**
   - `--resume <session-id>`: Resume specific session
   - `--continue` or `-c`: Continue most recent conversation in current directory
   - Session state includes transcript path and working directory context

### Session Context Data

Every session maintains rich contextual information accessible through hooks and status line:

```json
{
  "session_id": "abc123...",
  "transcript_path": "/path/to/transcript.json",
  "cwd": "/current/working/directory",
  "model": {
    "id": "claude-opus-4-1",
    "display_name": "Opus"
  },
  "workspace": {
    "current_dir": "/current/working/directory",
    "project_dir": "/original/project/directory"
  },
  "version": "1.0.80",
  "output_style": {
    "name": "default"
  },
  "cost": {
    "total_cost_usd": 0.01234,
    "total_duration_ms": 45000,
    "total_api_duration_ms": 2300,
    "total_lines_added": 156,
    "total_lines_removed": 23
  }
}
```

### Environment Variables

Claude Code exposes several environment variables for customization and hook integration:

**Core Environment Variables:**
- `ANTHROPIC_API_KEY`: API authentication
- `CLAUDE_CODE_USE_BEDROCK`: Enable AWS Bedrock
- `CLAUDE_CODE_USE_VERTEX`: Enable Google Vertex AI
- `CLAUDE_PROJECT_DIR`: Project directory path

**Hook-Specific Variables:**
- `$CLAUDE_FILE_PATHS`: Space-separated list of file paths relevant to tool call
- `$CLAUDE_NOTIFICATION`: Notification message content (Notification events only)
- `$CLAUDE_TOOL_OUTPUT`: Tool execution output (PostToolUse events only)

## Hook System Architecture

### Hook Events and Execution Model

Claude Code provides 8 distinct hook events with specific trigger conditions:

1. **UserPromptSubmit**: Before processing user prompts
   - Add context, validate prompts, block certain prompt types
   - Special handling: stdout added to context instead of display

2. **SessionStart**: Session initialization/resume
   - Context: includes source ("startup", "resume", "clear")
   - Load development context (git status, issues, context files)
   - Special handling: stdout added to context

3. **PreToolUse**: Before any tool execution
   - Tool validation, permission checks, preprocessing

4. **PostToolUse**: After successful tool completion
   - Receives `$CLAUDE_TOOL_OUTPUT` environment variable
   - Post-processing, validation, cleanup

5. **Notification**: Tool permissions or idle periods
   - Receives `$CLAUDE_NOTIFICATION` environment variable
   - User notification handling

6. **Stop**: Main agent finishes responding
   - Can block continuation with exit code 2
   - Session cleanup, final validations

7. **SubagentStop**: Subagent completion
   - Independent from main agent Stop events
   - Subagent-specific cleanup

8. **PreCompact**: Before context compaction
   - Context optimization, preservation of critical data

### Hook Configuration and Execution

**Configuration Structure:**
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write",  // Exact tool name, "*" for all, "" for none
        "commands": ["echo 'Before write'", "validate-file.sh"],
        "timeout": 60,  // seconds, default 60
        "run_in_background": false  // default false
      }
    ]
  }
}
```

**Execution Characteristics:**
- **Parallel Execution**: Multiple matching hooks run concurrently
- **60-second Default Timeout**: Configurable per hook
- **Input via stdin**: JSON payload with session context
- **Environment Variables**: Hook-specific variables available
- **Update Frequency**: Status hooks update at most every 300ms

### Hook Communication Protocol

**Exit Code Behavior:**
- `0`: Success - stdout shown to user (except UserPromptSubmit/SessionStart)
- `2`: Blocking error - stderr fed back to Claude, operation blocked
- `Other`: Non-blocking error - stderr shown to user, operation continues

**JSON Control Flow:**
Hooks can return structured JSON for sophisticated control:
```json
{
  "continue": true,
  "stopReason": "Custom reason",
  "block": false,
  "additionalContext": "Context to add"
}
```

## Output Styles Implementation

### Architecture

Output Styles provide complete personality transformation while preserving all tools and capabilities:

- **System Prompt Replacement**: Core functionality preserved, personality changed
- **Domain Adaptation**: Extend beyond software engineering to any domain
- **Format Flexibility**: HTML, Markdown, custom formats supported

### Available Styles

1. **HTML Output Style**
   - Retro terminal theme with dark gray/white contrast
   - Ideal for archival and sharing
   - Enhanced readability

2. **Markdown Output Style**
   - Structured, compressed information
   - Bullet points and hierarchical organization
   - Quick-reference format

3. **Custom Styles**
   - Completely configurable through `/output-style` command
   - Domain-specific adaptations possible

### Configuration

Output styles are activated through:
- `/output-style` command for selection
- Settings configuration for persistence
- Runtime switching supported

## Status Line Implementation

### Technical Architecture

The status line system provides real-time, context-aware terminal display:

**Update Mechanism:**
- Maximum update frequency: 300ms
- JSON input via stdin
- ANSI color code support
- First line of stdout becomes status text

**Configuration:**
```json
{
  "statusLine": {
    "type": "command",
    "command": "your-status-script.sh",
    "padding": 0  // Optional: edge-to-edge display
  }
}
```

### Integration Points

**Input Data Structure:**
- Session metadata (session_id, transcript_path, cwd)
- Model information and workspace details
- Real-time cost and performance metrics
- Version and output style information

**Implementation Languages:**
- Bash, Python, Node.js, any executable script
- Cross-platform compatibility
- Git integration for branch detection
- Custom metrics and calculations

### Community Implementations

**ccstatusline**: Highly customizable with powerline support, themes, and real-time metrics
**claude-powerline**: Vim-style powerline with git integration and custom themes

## Constraints and Limitations

### Session Isolation Constraints

1. **No Native Inter-Session Communication**
   - Each session operates independently
   - Context must be re-established per session
   - No shared state between sessions

2. **Memory Limitations**
   - 200K token context window affects usage limits
   - Large context usage accelerates rate limiting
   - Context compaction occurs automatically

3. **Coordination Overhead**
   - Subagent coordination introduces latency
   - Not suitable for time-critical tasks
   - Parallel processing requires careful orchestration

### Hook System Limitations

1. **Security Responsibility**
   - Users solely responsible for hook security
   - Arbitrary shell command execution
   - Input validation and sanitization required

2. **Execution Constraints**
   - 60-second timeout default (configurable)
   - Background execution optional
   - Error handling through exit codes only

3. **Context Scope**
   - Hook context limited to current session
   - No cross-session hook communication
   - Limited to provided environment variables

### MCP Integration Constraints

1. **Client-Server Architecture**
   - 1:1 client-server relationships
   - Connection isolation enforced
   - Strict lifecycle management

2. **Capability Negotiation**
   - Initialization phase required
   - Capability discovery process
   - State management complexity

## Best Practices and Patterns

### Session Management

1. **Context Loading**
   - Use CLAUDE.md for project bootstrap
   - Implement SessionStart hooks for development context
   - Leverage git status and recent issues integration

2. **Multi-Session Coordination**
   - Use git worktrees for parallel development
   - Implement shared file coordination patterns
   - Consider ccswitch for workflow management

### Hook Development

1. **Security**
   - Validate and sanitize all inputs
   - Use allow/deny lists for file access
   - Implement timeout handling

2. **Performance**
   - Cache expensive operations in status line hooks
   - Use background execution for long-running tasks
   - Minimize context window impact

3. **Error Handling**
   - Implement proper exit code usage
   - Provide meaningful error messages
   - Handle timeout scenarios gracefully

### Output and Status Customization

1. **Status Line Design**
   - Keep information concise and relevant
   - Use colors and emojis for readability
   - Include critical metrics (cost, model, git status)

2. **Output Style Usage**
   - Match style to use case and audience
   - Leverage domain-specific adaptations
   - Maintain tool capability awareness

## Undocumented Features and Community Insights

### Advanced Capabilities

1. **Subagent Architecture**
   - Independent context maintenance
   - Specialized role assignment
   - Microservices-like patterns

2. **Git Worktree Integration**
   - Multiple Claude instances per project
   - Isolated development environments
   - Parallel task execution

3. **Context Optimization**
   - Automatic context compaction
   - CLAUDE.md file prioritization
   - Environment inheritance

### Community Tools and Extensions

1. **Session Management**
   - ccswitch for worktree management
   - Custom session tracking implementations
   - Community hook libraries

2. **Enhanced Status Lines**
   - Powerline integrations
   - Real-time metrics display
   - Custom theme systems

3. **Workflow Automation**
   - Custom slash commands
   - Hook-based automation
   - Development lifecycle integration

## Future Considerations

### Potential Enhancements

1. **Inter-Session Communication**
   - Native session sharing mechanisms
   - Persistent context across sessions
   - Coordinated multi-session workflows

2. **Advanced Hook Features**
   - Conditional hook execution
   - Hook dependency management
   - Cross-hook communication

3. **Enhanced Status Integration**
   - Widget-based status composition
   - Real-time collaboration indicators
   - Advanced metrics and analytics

This documentation represents the current understanding of Claude Code v2 capabilities based on official documentation and community research as of August 2025. The system continues to evolve with regular updates and community contributions.