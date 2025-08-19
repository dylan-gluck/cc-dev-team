# Claude Code Configuration Directory

This directory contains the complete configuration system for Claude Code, providing a comprehensive development environment with specialized agents, automation hooks, custom commands, and productivity enhancements.

## Overview

The `.claude/` directory serves as the control center for Claude Code's advanced functionality, enabling:

- **Specialized AI Agents** for different development roles and tasks
- **Automated Workflows** via lifecycle hooks and event-driven scripts
- **Custom Commands** for streamlined development operations
- **Productivity Tools** including status lines, output formatting, and TTS integration
- **Session Management** with persistent context and logging

## Directory Structure

```
.claude/
├── agents/                 # Specialized sub-agents for development tasks
├── commands/              # Custom commands organized by category
├── hooks/                 # Lifecycle event automation scripts
├── output-styles/         # Response formatting configurations
├── status_lines/          # Dynamic status line generators
├── templates/             # Reusable templates for agents and commands
├── data/                  # Session data and configuration storage
├── settings.json          # Core Claude Code configuration
└── TODO.md               # Development roadmap and tasks
```

## Core Components

### Agent System (`agents/`)

Specialized AI agents for different development roles and expertise areas:

**Meta and Framework Agents:**
- `meta-agent.md` - Creates new specialized agents with orchestration awareness
- `command-creator.md` - Generates custom commands and workflows

**Development Team Agents:**
- `tech-lead.md` - Technical leadership and architecture decisions
- `fullstack-eng.md` - Full-stack development implementation
- `ux-eng.md` - User experience and interface development
- `business-analyst.md` - Requirements analysis and business logic

**Specialized Task Agents:**
- `ai-research.md` - Research specialist for AI/ML innovations and best practices
- `doc-expert.md` - Documentation creation and maintenance specialist
- `readme-maintainer.md` - README file creation and updates
- `git-commit.md` - Git workflow and commit message optimization
- `python-script-composer.md` - Python script development and automation
- `work-completion-summary.md` - Audio summaries and next steps

Each agent includes:
- Clear delegation triggers and use cases
- Minimal but sufficient tool permissions
- Domain-specific workflows and best practices
- Structured output formats and quality standards

### Command System (`commands/`)

Custom commands organized by functional category:

**Meta Operations (`meta/`):**
- `generate-agent.md` - Create new specialized agents
- `generate-command.md` - Create new custom commands
- `all-tools.md` - List available tools and capabilities
- `update-status-line.md` - Update dynamic status display

**Development Workflow (`workflow/`):**
- `init-project.md` - Initialize new project structures
- `team-build.md` - Coordinate team-based development

**Implementation (`implementation/`):**
- `build-feature.md` - Feature development workflows
- `build-ui.md` - UI/UX implementation tasks
- `parallel-build.md` - Parallel development coordination

**Testing and Quality (`testing/`):**
- `review.md` - Code review processes
- `fix.md` - Bug fixing and issue resolution

**Research and Analysis (`research/`):**
- `analyze.md` - Code and system analysis

**Architecture and Design (`architecture/`):**
- `design.md` - System architecture and design decisions

**Project Management (`project/`):**
- `question.md` - Project-specific inquiries
- `auto-context.md` - Automatic context loading

**Git Operations (`git/`):**
- `commit.md` - Enhanced commit workflows
- `status.md` - Repository status analysis

### Hook System (`hooks/`)

Automated scripts that execute during Claude Code lifecycle events:

**Core Hooks:**
- `session_start.py` - Initialize sessions with context loading and announcements
- `user_prompt_submit.py` - Process user inputs with validation and logging
- `pre_tool_use.py` - Pre-execution validation and setup
- `post_tool_use.py` - Post-execution logging and cleanup
- `stop.py` - Session termination with chat summaries
- `subagent_stop.py` - Sub-agent completion notifications
- `pre_compact.py` - Pre-compaction preparation
- `notification.py` - System notification handling

**Utility Libraries (`hooks/utils/`):**

*Text-to-Speech Integration (`tts/`):*
- `openai_tts.py` - OpenAI TTS for high-quality voice synthesis
- `elevenlabs_tts.py` - ElevenLabs TTS integration
- `pyttsx3_tts.py` - Local TTS fallback

*LLM Integration (`llm/`):*
- `anth.py` - Anthropic Claude API integration
- `oai.py` - OpenAI API integration
- `ollama.py` - Local Ollama model integration

### Configuration and Settings

**`settings.json`** - Core Claude Code configuration:
- Tool permissions and security controls
- Hook event bindings and execution order
- MCP server integration settings
- Development workflow preferences

**Permission System:**
```json
{
  "permissions": {
    "allow": [
      "Bash(mkdir:*)", "Bash(uv:*)", "Bash(git:*)",
      "MultiEdit", "Write", "Edit"
    ]
  }
}
```

**Hook Event Bindings:**
- `PreToolUse` - Validation and logging before tool execution
- `PostToolUse` - Cleanup and logging after tool execution
- `UserPromptSubmit` - Input processing and session management
- `SessionStart` - Initialization and context loading
- `Stop` - Session termination and summaries
- `SubagentStop` - Sub-agent completion handling

### Output Styling (`output-styles/`)

Response formatting configurations for different use cases:

- `markdown-focused.md` - Comprehensive markdown for readability
- `yaml-structured.md` - YAML-formatted responses
- `table-based.md` - Tabular data presentation
- `html-structured.md` - HTML formatting for web contexts
- `ultra-concise.md` - Minimal, condensed responses
- `bullet-points.md` - Bulleted list formatting
- `tts-summary.md` - Audio-optimized summaries
- `genui.md` - UI generation formatting

### Status Lines (`status_lines/`)

Dynamic status line generators providing real-time development context:

- `status_line_v4.py` - Latest status line implementation with comprehensive logging
- Version progression showing iterative improvements
- Integration with session data and git status
- Customizable display formats and information density

### Templates (`templates/`)

Reusable templates for consistent component creation:

- `agent.md` - Standard agent configuration template
- `command.md` - Command definition template
- `commit-message.md` - Git commit message formatting

### Data Management (`data/`)

Persistent storage for session information and configurations:

- `sessions/` - Individual session data files with prompts and context
- JSON-structured session management
- Agent naming and context persistence
- Development history and analytics

## Development Productivity Features

### Automated Context Loading
- Git status and branch information
- Recent GitHub issues integration
- Project-specific context files
- Development history and session continuity

### Audio Integration
- Text-to-speech announcements for session events
- Multiple TTS provider support (OpenAI, ElevenLabs, local)
- Audio summaries for work completion
- Notification sounds for agent completion

### Session Management
- Persistent session data with unique identifiers
- Automatic agent naming and role assignment
- Prompt history and context preservation
- Cross-session development continuity

### Logging and Analytics
- Comprehensive event logging for all hooks
- Tool usage tracking and analysis
- Session data persistence and retrieval
- Development pattern analysis

## Integration Points

### MCP Server Support
Full integration with Model Context Protocol servers for extended capabilities:
- Browser automation via Playwright
- Web scraping with Firecrawl
- Audio processing with ElevenLabs
- Custom MCP server integration

### Git Workflow Enhancement
- Automated commit message generation
- Branch status monitoring
- Change tracking and analysis
- Repository health monitoring

### Development Tool Integration
- UV for Python dependency management
- Bun and npm for JavaScript projects
- Modern CLI tool preferences (rg, fd, bat, eza)
- Security-conscious permission system

## Usage Patterns

### Agent Delegation
```markdown
# Automatic agent invocation based on trigger phrases:
"Use ai-research to find current best practices"
"MUST BE USED when creating documentation"
"Specialist for code review and quality assurance"
```

### Command Execution
```bash
# Custom commands via Claude Code interface:
/generate-agent "test-automation specialist"
/team-build "parallel feature development"
/git-commit "implement user authentication"
```

### Hook Automation
- Automatic session initialization with development context
- Real-time logging and monitoring of all development activities
- Intelligent agent naming and role assignment
- Audio feedback for significant development events

## Quality Assurance

### Security Features
- Restricted tool permissions with explicit allow lists
- Input validation and sanitization
- Safe command execution patterns
- Isolated script execution environments

### Error Handling
- Graceful degradation for missing dependencies
- Comprehensive logging for debugging
- Fallback mechanisms for external service failures
- User-friendly error reporting

### Performance Optimization
- Efficient tool selection and minimal permission sets
- Optimized hook execution order
- Cached session data and context loading
- Streamlined agent delegation patterns

## Configuration Customization

The Claude Code configuration system is designed for extensibility:

1. **Add New Agents** - Use the meta-agent to create specialized sub-agents
2. **Create Custom Commands** - Define new workflows using command templates
3. **Extend Hooks** - Add custom automation scripts for development events
4. **Configure Output Styles** - Create new formatting patterns for different contexts
5. **Customize Status Lines** - Modify status information display and content

This configuration system transforms Claude Code into a comprehensive development environment with intelligent automation, specialized expertise, and productivity enhancements tailored for modern software engineering workflows.