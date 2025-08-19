# Claude Code Development Team Scaffolding

A comprehensive framework for building AI-powered development teams using Claude Code. This repository provides a production-ready scaffolding system with specialized agents, intelligent hooks, enhanced workflows, and extensive customization options.

## Overview

This scaffolding transforms Claude Code into a sophisticated development team coordination platform. Rather than working with a single AI assistant, you get access to a complete team of specialized agents, each with specific expertise and tools, all orchestrated through an intelligent workflow system.

### Key Features

**🤖 Specialized Agent Team**
- **AI Research Specialist**: Stays current with latest AI/ML developments
- **Meta-Agent**: Creates new agents from natural language descriptions
- **Fullstack Engineer**: Handles comprehensive application development
- **Tech Lead**: Provides architectural guidance and code reviews
- **Business Analyst**: Translates requirements into technical specifications
- **UX Engineer**: Focuses on user experience and interface design

**🔗 Intelligent Hook System**
- Complete lifecycle automation with 8 hook types
- Security validation and dangerous command blocking
- AI-generated completion messages with TTS feedback
- Automatic development context loading
- Comprehensive audit logging and transcript management

**⚡ Enhanced Development Experience**
- Custom slash commands for rapid task execution
- Dynamic status lines with real-time project information
- Multiple output styles (visual HTML, tables, YAML, TTS)
- Automatic session management with agent naming
- Priority-based TTS system (ElevenLabs, OpenAI, pyttsx3)

**📋 Production-Ready Infrastructure**
- UV single-file scripts for isolated hook logic
- Comprehensive logging system with JSON structured data
- MCP server integrations (Firecrawl, ElevenLabs)
- Git workflow integration with status tracking
- Session state persistence and recovery

Based on [claude-code-hooks-mastery](https://github.com/disler/claude-code-hooks-mastery) with extensive enhancements for team coordination and production workflows.

## Quick Start

### 1. Install Scaffolding to Your Project

#### Option A: Using the Install Script (Recommended)
```bash
# Clone this repository
git clone https://github.com/dylan-gluck/cc-dev-team.git
cd cc-dev-team

# Run the installer with your project path
uv run scripts/install.py /path/to/your-project

# Preview changes without installing (dry run)
uv run scripts/install.py --dry-run /path/to/your-project

# Force overwrite existing files if needed
uv run scripts/install.py --force /path/to/your-project
```

#### Option B: Manual Installation
```bash
# Clone or copy this directory to your new project
cp -r /path/to/cc-dev-team /path/to/your-project/.claude-scaffolding
cd /path/to/your-project

# Copy the .claude configuration
cp -r .claude-scaffolding/.claude .

# Copy project files
cp .claude-scaffolding/CLAUDE.md .
cp .claude-scaffolding/README.md ./README-scaffolding.md
```

## Prerequisites

### Required
- **[Claude Code](https://docs.anthropic.com/en/docs/claude-code)** - Anthropic's CLI for Claude AI
- **[Astral UV](https://docs.astral.sh/uv/getting-started/installation/)** - Fast Python package installer and resolver
- **[Git](https://git-scm.com/)** - Version control system

### Optional Integrations
- **[ElevenLabs](https://elevenlabs.io/)** - Premium text-to-speech (requires API key)
- **[OpenAI](https://openai.com/)** - GPT models and TTS fallback (requires API key)
- **[Ollama](https://ollama.com/)** - Local LLM for agent naming and completion messages
- **[GitHub CLI](https://cli.github.com/)** - Enhanced git workflow integration

### MCP Servers (Optional)
- **[ElevenLabs MCP Server](https://github.com/elevenlabs/elevenlabs-mcp)** - Advanced audio features
- **[Firecrawl MCP Server](https://www.firecrawl.dev/mcp)** - Web scraping for research agents
- **Custom MCP servers** - Extend functionality as needed

## Project Structure

```
project-root/
├── .claude/                    # Claude Code configuration
│   ├── agents/                 # Specialized sub-agents
│   ├── commands/               # Custom slash commands
│   ├── hooks/                  # Lifecycle automation scripts
│   ├── output-styles/          # Response formatting options
│   ├── status_lines/           # Dynamic terminal status displays
│   ├── data/sessions/          # Session state persistence
│   └── settings.json           # Main configuration
├── apps/                       # Your project applications
├── ai_docs/                    # AI-curated documentation
│   ├── cc/                     # Claude Code references
│   ├── bun/                    # Bun runtime documentation
│   └── uv/                     # UV Python documentation
├── logs/                       # Structured event logs
└── CLAUDE.md                   # Project-specific instructions
```

### Directory Overview

**[`.claude/`](.claude/README.md)** - Core scaffolding infrastructure
- **[`agents/`](.claude/agents/)** - Team of specialized AI agents
- **[`hooks/`](.claude/hooks/README.md)** - Lifecycle automation and workflow enhancement
- **[`commands/`](.claude/commands/)** - Custom slash commands for rapid task execution
- **[`output-styles/`](.claude/output-styles/)** - Response formatting configurations
- **[`status_lines/`](.claude/status_lines/)** - Real-time session information displays

**[`apps/`](apps/README.md)** - Your actual project applications and services

**[`ai_docs/`](ai_docs/README.md)** - Curated documentation for agent reference

**[`logs/`](logs/README.md)** - Comprehensive audit trail and session management

## Development Team Agents

The scaffolding includes a comprehensive team of specialized agents, each designed for specific development tasks:

### Core Development Team

**AI Research (`ai-research`)**
- Proactively gathers latest developments in AI/ML and engineering
- Searches across multiple sources for actionable insights
- Provides structured reports with practical recommendations
- Tools: WebSearch, WebFetch, Firecrawl integration

**Meta-Agent (`meta-agent`)**
- Creates new specialized agents from natural language descriptions
- Ensures consistent agent structure and best practices
- Automatically determines minimal required tools
- Essential for scaling your agent capabilities

**Fullstack Engineer (`fullstack-eng`)**
- Handles end-to-end application development
- Frontend and backend integration expertise
- Database design and API development
- Testing and deployment workflows

**Tech Lead (`tech-lead`)**
- Provides architectural guidance and technical direction
- Code review and quality assurance
- Performance optimization and scaling decisions
- Team coordination and technical mentoring

**Business Analyst (`business-analyst`)**
- Translates business requirements into technical specifications
- Creates user stories and acceptance criteria
- Stakeholder communication and requirement gathering
- Project planning and scope management

**UX Engineer (`ux-eng`)**
- User experience design and interface development
- Accessibility and usability optimization
- Design system implementation
- User research and testing coordination

### Utility Agents

**Work Completion Summary (`work-completion-summary`)**
- Generates audio summaries of completed work
- Triggered by "tts" command or task completion
- Provides next steps and status updates

**README Maintainer (`readme-maintainer`)**
- Specialized in creating and updating documentation
- Analyzes code to ensure documentation accuracy
- Maintains consistent documentation standards

**Git Commit (`git-commit`)**
- Generates semantic commit messages
- Analyzes git diff and suggests appropriate message structure
- Ensures consistent commit history

## Intelligent Hook System

The scaffolding implements all 8 Claude Code hook types with enhanced functionality:

### Hook Lifecycle Events

**1. SessionStart Hook**
- **Triggers**: New session, resume, or clear
- **Enhanced Features**: Development context loading, git status integration, TTS session announcements
- **Data Loaded**: Project files, GitHub issues, recent commits, session state

**2. UserPromptSubmit Hook**
- **Triggers**: User submits prompt (before Claude processes it)
- **Enhanced Features**: Prompt validation, security filtering, agent naming, session tracking
- **Capabilities**: Block dangerous prompts, inject context, generate unique agent names

**3. PreToolUse Hook**
- **Triggers**: Before any tool execution
- **Enhanced Features**: Security validation, dangerous command blocking
- **Protection**: Blocks `rm -rf`, `.env` access, suspicious operations

**4. PostToolUse Hook**
- **Triggers**: After successful tool completion
- **Enhanced Features**: Result logging, transcript conversion, execution tracking
- **Data**: Complete audit trail of all tool usage and results

**5. Notification Hook**
- **Triggers**: Claude Code notifications (waiting for input, etc.)
- **Enhanced Features**: TTS alerts with personalization
- **Smart Features**: "Your agent needs your input" with engineer name inclusion

**6. Stop Hook**
- **Triggers**: Claude Code finishes responding
- **Enhanced Features**: AI-generated completion messages, TTS playback, transcript archival
- **Intelligence**: LLM priority (OpenAI > Anthropic > Ollama), personalized messages

**7. SubagentStop Hook**
- **Triggers**: Subagents complete their tasks
- **Enhanced Features**: Multi-agent workflow tracking, completion announcements
- **Coordination**: Supports complex orchestrated development workflows

**8. PreCompact Hook**
- **Triggers**: Before conversation history compaction
- **Enhanced Features**: Automatic transcript backup, compaction logging
- **Safety**: Preserves conversation history before context compression

### Hook Capabilities

**Security & Validation**
- Dangerous command detection and blocking
- Environment file protection
- Prompt validation and filtering
- Comprehensive audit logging

**Development Context**
- Automatic git status loading
- Project file integration
- GitHub issues synchronization
- Session state management

**Audio Feedback System**
- Priority-based TTS: ElevenLabs → OpenAI → pyttsx3
- Personalized completion messages
- Smart notification system
- Work completion summaries

## Architecture & Design

### UV Single-File Scripts
All hooks use **[UV single-file scripts](https://docs.astral.sh/uv/guides/scripts/)** for clean separation:

**Benefits:**
- **Isolation**: Hook logic separate from project dependencies
- **Portability**: Each script declares dependencies inline
- **No Environment Management**: UV handles everything automatically
- **Fast Execution**: Lightning-fast dependency resolution
- **Self-Contained**: Each hook can be understood independently

### Multi-Agent Orchestration
The scaffolding supports sophisticated team coordination:

**Agent Communication**
- Task delegation between agents
- State sharing and coordination
- Parallel execution workflows
- Result aggregation and reporting

**Session Management**
- Persistent agent identities
- Context preservation across interactions
- Session state recovery
- Conversation history management

**Quality Assurance**
- Comprehensive audit logging
- Security validation at multiple levels
- Graceful error handling
- Development context integration


## Monitoring & Observability

### Structured Logging
All events are logged as structured JSON in the `logs/` directory:

```bash
# View recent user prompts
cat logs/user_prompt_submit.json | jq '.[-5:]'

# Monitor tool usage
cat logs/post_tool_use.json | jq '.[] | select(.tool_name == "Task")'

# Track agent completions
cat logs/subagent_stop.json | jq '.'
```

### Session Management
Session state is preserved in `.claude/data/sessions/`:

```json
{
  "session_id": "unique-session-id",
  "agent_name": "Phoenix",
  "prompts": ["Recent prompts..."],
  "extras": {
    "project": "myapp",
    "status": "development"
  }
}
```

### Real-time Status
Status lines provide live information:
- Current agent name and model
- Recent prompts and task types
- Git branch and project status
- Custom metadata and tags

## Hook System Deep Dive

The scaffolding implements sophisticated flow control through hooks:

### Exit Code Behavior

Hooks communicate status and control flow through exit codes:

| Exit Code | Behavior           | Description                                                                                  |
| --------- | ------------------ | -------------------------------------------------------------------------------------------- |
| **0**     | Success            | Hook executed successfully. `stdout` shown to user in transcript mode (Ctrl-R)               |
| **2**     | Blocking Error     | **Critical**: `stderr` is fed back to Claude automatically. See hook-specific behavior below |
| **Other** | Non-blocking Error | `stderr` shown to user, execution continues normally                                         |

### Hook-Specific Flow Control

Each hook type has different capabilities for blocking and controlling Claude Code's behavior:

#### UserPromptSubmit Hook - **CAN BLOCK PROMPTS & ADD CONTEXT**
- **Primary Control Point**: Intercepts user prompts before Claude processes them
- **Exit Code 2 Behavior**: Blocks the prompt entirely, shows error message to user
- **Use Cases**: Prompt validation, security filtering, context injection, audit logging
- **Example**: Our `user_prompt_submit.py` logs all prompts and can validate them

#### PreToolUse Hook - **CAN BLOCK TOOL EXECUTION**
- **Primary Control Point**: Intercepts tool calls before they execute
- **Exit Code 2 Behavior**: Blocks the tool call entirely, shows error message to Claude
- **Use Cases**: Security validation, parameter checking, dangerous command prevention
- **Example**: Our `pre_tool_use.py` blocks `rm -rf` commands with exit code 2

```python
# Block dangerous commands
if is_dangerous_rm_command(command):
    print("BLOCKED: Dangerous rm command detected", file=sys.stderr)
    sys.exit(2)  # Blocks tool call, shows error to Claude
```

#### PostToolUse Hook - **CANNOT BLOCK (Tool Already Executed)**
- **Primary Control Point**: Provides feedback after tool completion
- **Exit Code 2 Behavior**: Shows error to Claude (tool already ran, cannot be undone)
- **Use Cases**: Validation of results, formatting, cleanup, logging
- **Limitation**: Cannot prevent tool execution since it fires after completion

#### Notification Hook - **CANNOT BLOCK**
- **Primary Control Point**: Handles Claude Code notifications
- **Exit Code 2 Behavior**: N/A - shows stderr to user only, no blocking capability
- **Use Cases**: Custom notifications, logging, user alerts
- **Limitation**: Cannot control Claude Code behavior, purely informational

#### Stop Hook - **CAN BLOCK STOPPING**
- **Primary Control Point**: Intercepts when Claude Code tries to finish responding
- **Exit Code 2 Behavior**: Blocks stoppage, shows error to Claude (forces continuation)
- **Use Cases**: Ensuring tasks complete, validation of final state use this to FORCE CONTINUATION
- **Caution**: Can cause infinite loops if not properly controlled

#### SubagentStop Hook - **CAN BLOCK SUBAGENT STOPPING**
- **Primary Control Point**: Intercepts when Claude Code subagents try to finish
- **Exit Code 2 Behavior**: Blocks subagent stoppage, shows error to subagent
- **Use Cases**: Ensuring subagent tasks complete properly
- **Example**: Our `subagent_stop.py` logs events and announces completion

#### PreCompact Hook - **CANNOT BLOCK**
- **Primary Control Point**: Fires before compaction operations
- **Exit Code 2 Behavior**: N/A - shows stderr to user only, no blocking capability
- **Use Cases**: Transcript backup, context preservation, pre-compaction logging
- **Example**: Our `pre_compact.py` creates transcript backups before compaction

#### SessionStart Hook - **CANNOT BLOCK**
- **Primary Control Point**: Fires when new sessions start or resume
- **Exit Code 2 Behavior**: N/A - shows stderr to user only, no blocking capability
- **Use Cases**: Loading development context, session initialization, environment setup
- **Example**: Our `session_start.py` loads git status, recent issues, and context files

### Advanced JSON Output Control

Beyond simple exit codes, hooks can return structured JSON for sophisticated control:

#### Common JSON Fields (All Hook Types)
```json
{
  "continue": true,           // Whether Claude should continue (default: true)
  "stopReason": "string",     // Message when continue=false (shown to user)
  "suppressOutput": true      // Hide stdout from transcript (default: false)
}
```

#### PreToolUse Decision Control
```json
{
  "decision": "approve" | "block" | undefined,
  "reason": "Explanation for decision"
}
```

- **"approve"**: Bypasses permission system, `reason` shown to user
- **"block"**: Prevents tool execution, `reason` shown to Claude
- **undefined**: Normal permission flow, `reason` ignored

#### PostToolUse Decision Control
```json
{
  "decision": "block" | undefined,
  "reason": "Explanation for decision"
}
```

- **"block"**: Automatically prompts Claude with `reason`
- **undefined**: No action, `reason` ignored

#### Stop Decision Control
```json
{
  "decision": "block" | undefined,
  "reason": "Must be provided when blocking Claude from stopping"
}
```

- **"block"**: Prevents Claude from stopping, `reason` tells Claude how to proceed
- **undefined**: Allows normal stopping, `reason` ignored

### Flow Control Priority

When multiple control mechanisms are used, they follow this priority:

1. **`"continue": false`** - Takes precedence over all other controls
2. **`"decision": "block"`** - Hook-specific blocking behavior
3. **Exit Code 2** - Simple blocking via stderr
4. **Other Exit Codes** - Non-blocking errors

### Security Implementation Examples

#### 1. Command Validation (PreToolUse)
```python
# Block dangerous patterns
dangerous_patterns = [
    r'rm\s+.*-[rf]',           # rm -rf variants
    r'sudo\s+rm',              # sudo rm commands
    r'chmod\s+777',            # Dangerous permissions
    r'>\s*/etc/',              # Writing to system directories
]

for pattern in dangerous_patterns:
    if re.search(pattern, command, re.IGNORECASE):
        print(f"BLOCKED: {pattern} detected", file=sys.stderr)
        sys.exit(2)
```

#### 2. Result Validation (PostToolUse)
```python
# Validate file operations
if tool_name == "Write" and not tool_response.get("success"):
    output = {
        "decision": "block",
        "reason": "File write operation failed, please check permissions and retry"
    }
    print(json.dumps(output))
    sys.exit(0)
```

#### 3. Completion Validation (Stop Hook)
```python
# Ensure critical tasks are complete
if not all_tests_passed():
    output = {
        "decision": "block",
        "reason": "Tests are failing. Please fix failing tests before completing."
    }
    print(json.dumps(output))
    sys.exit(0)
```

### Hook Execution Environment

- **Timeout**: 60-second execution limit per hook
- **Parallelization**: All matching hooks run in parallel
- **Environment**: Inherits Claude Code's environment variables
- **Working Directory**: Runs in current project directory
- **Input**: JSON via stdin with session and tool data
- **Output**: Processed via stdout/stderr with exit codes

### Flow Control & Security

**Prompt-Level Control**
- Security validation before Claude processes prompts
- Context injection for enhanced responses
- Audit logging for compliance
- Agent naming and session management

**Tool-Level Security**
- Dangerous command detection (`rm -rf`, `.env` access)
- Real-time blocking of suspicious operations
- Comprehensive tool usage logging
- Permission-based access control

**Completion Management**
- AI-generated completion messages
- Task validation and verification
- Transcript backup before compaction
- Multi-agent workflow coordination

### Hook Configuration Examples

```json
// Enable security validation
"UserPromptSubmit": [{
  "hooks": [{
    "type": "command",
    "command": "uv run .claude/hooks/user_prompt_submit.py --validate --name-agent"
  }]
}]

// Enhanced completion with TTS
"Stop": [{
  "hooks": [{
    "type": "command",
    "command": "uv run .claude/hooks/stop.py --chat --notify"
  }]
}]
```

## Advanced Features

### Agent Orchestration

> See the [Claude Code Sub-Agents documentation](https://docs.anthropic.com/en/docs/claude-code/sub-agents) for more details.

Claude Code supports specialized sub-agents that handle specific tasks with custom system prompts, tools, and separate context windows. Sub-agents are AI assistants that your primary Claude Code agent can delegate tasks to.

Sub-agents enable sophisticated team coordination with automatic delegation:

**Information Flow:**
```
You → Primary Claude → Specialized Agent → Primary Claude → You
```

**Key Concepts:**
- Agent files contain **system prompts** that define agent behavior
- The `description` field tells Claude when to automatically delegate
- Sub-agents report back to primary agent, not directly to you
- Each agent starts fresh with specific context and tools

**Automatic Delegation:**
```yaml
description: "Use proactively when researching AI/ML developments"
description: "MUST BE USED for creating new agents"
description: "Specialist for React testing and quality assurance"
```

### Creating Custom Agents

Use the meta-agent to create new specialized agents:

```bash
# Create a testing specialist
"Create a new agent that specializes in automated testing with pytest and Jest"

# Create a deployment expert
"Build an agent focused on Docker and Kubernetes deployment"

# Create a security auditor
"Generate an agent that performs security audits and vulnerability scanning"
```

**Agent Structure:**
```yaml
---
name: testing-specialist
description: "Use for automated testing, test coverage, and quality assurance"
tools: Read, Write, Edit, Bash(pytest:*), Bash(jest:*), Grep
color: green
model: sonnet
---

# Purpose
You are a testing specialist focused on automated testing and quality assurance.

## Workflow
1. **Analyze Test Requirements**
2. **Create Test Plans**
3. **Implement Tests**
4. **Generate Reports**
```

### Agent Best Practices

**Critical Success Factors:**
1. **Clear Descriptions**: Use trigger phrases like "Use proactively when..." or "MUST BE USED for..."
2. **Minimal Tools**: Only include necessary tools to avoid permission complexity
3. **Structured Workflows**: Define clear step-by-step processes
4. **Output Formats**: Specify exactly how agents should report results

**Common Patterns:**
- **Research Agents**: WebSearch, WebFetch, Write for documentation
- **Code Agents**: Read, Edit, Bash commands for specific tools
- **Testing Agents**: Bash testing tools, Read, Write for reports
- **Deployment Agents**: Docker/K8s Bash commands, Read configs

### Complex Workflow Examples

**Multi-Agent Development:**
```bash
# Research → Design → Implementation → Testing
"Research modern React patterns with ai-research, then have ux-eng design a component architecture, fullstack-eng implement it, and testing-specialist create comprehensive tests"
```

**Code Review Pipeline:**
```bash
# Development → Review → Fix → Deploy
"Have fullstack-eng implement the API, tech-lead review for architecture, apply fixes, then deployment-agent handle the release"
```

**Documentation Workflow:**
```bash
# Analysis → Documentation → Validation
"Analyze the codebase structure, have readme-maintainer create documentation, then tech-lead validate technical accuracy"
```

### The Meta-Agent: Agent Factory

The meta-agent creates new agents from natural language descriptions:

**Capabilities:**
- Generates complete agent configurations
- Selects appropriate tools and permissions
- Creates structured workflows and best practices
- Ensures consistent formatting and standards

**Usage Examples:**
```bash
"Create an agent for database migrations and schema management"
"Build a security-focused agent for vulnerability scanning"
"Generate an agent that specializes in performance optimization"
```

**Meta-Agent Workflow:**
1. Analyzes your requirements
2. Selects appropriate tools and model
3. Creates structured system prompt
4. Defines clear delegation triggers
5. Writes complete agent file
6. Validates configuration

## Troubleshooting

### Common Issues

**Hooks Not Working**
```bash
# Check UV installation
uv --version

# Verify hook permissions
ls -la .claude/hooks/

# Test hooks manually
echo '{}' | uv run .claude/hooks/user_prompt_submit.py
```

**Agent Not Responding**
```bash
# Check agent file syntax
cat .claude/agents/your-agent.md

# Verify agent is loaded
ls .claude/agents/

# Check logs for errors
cat logs/subagent_stop.json | jq '.[-1]'
```

**TTS Not Working**
```bash
# Check environment variables
echo $ELEVENLABS_API_KEY
echo $OPENAI_API_KEY

# Test TTS directly
uv run .claude/hooks/utils/tts/elevenlabs_tts.py "test message"
```

### Performance Optimization

**Hook Performance**
- Use minimal dependencies in hook scripts
- Cache frequently accessed data
- Implement timeout handling

**Agent Efficiency**
- Assign minimal required tools only
- Use appropriate model sizes (haiku for simple tasks)
- Design clear, focused system prompts

**Session Management**
- Regular compaction of conversation history
- Periodic cleanup of session data
- Monitor log file sizes

### Debug Mode
```bash
# Enable verbose logging
export CLAUDE_DEBUG=1

# Monitor hook execution
tail -f logs/*.json

# Test individual components
uv run .claude/hooks/session_start.py --debug
```


## Contributing & Extension

### Adding New Agents
1. Use meta-agent to generate the initial structure
2. Customize the system prompt and tools
3. Test with simple tasks first
4. Add to your team workflows

### Creating Custom Hooks
1. Copy an existing hook as template
2. Follow UV single-file script format
3. Add appropriate error handling
4. Test thoroughly before deployment

### Custom Output Styles
1. Create new markdown file in `.claude/output-styles/`
2. Add YAML frontmatter with name and description
3. Define formatting instructions
4. Test with `/output-style your-style-name`

### Extending Commands
1. Create new command file in appropriate `.claude/commands/` subdirectory
2. Follow existing patterns for agent delegation
3. Include clear descriptions and examples
4. Test command execution

## Documentation & Resources

### Comprehensive Documentation
- **[Main Documentation](ai_docs/README.md)**: Complete technical references
- **[Hook System](/.claude/hooks/README.md)**: Detailed hook implementation guide
- **[Agent Framework](/.claude/agents/)**: Agent development patterns
- **[Applications](apps/README.md)**: Project development guidelines

### External Resources
- **[Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)**: Official Claude Code docs
- **[UV Documentation](https://docs.astral.sh/uv/)**: Python package management
- **[Claude Code Hooks](https://docs.anthropic.com/en/docs/claude-code/hooks)**: Hook system reference
- **[Sub-Agents Guide](https://docs.anthropic.com/en/docs/claude-code/sub-agents)**: Agent delegation patterns


---

**Transform your development workflow with AI-powered team coordination. This scaffolding provides everything you need to build sophisticated applications with the support of specialized AI agents, intelligent automation, and comprehensive development tooling.**

*Based on [claude-code-hooks-mastery](https://github.com/disler/claude-code-hooks-mastery) with extensive enhancements for production development workflows.*
