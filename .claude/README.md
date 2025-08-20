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

A comprehensive team of 44 specialized AI agents covering all aspects of modern software development, from technical implementation to creative design and business analysis. These agents are organized into functional teams that mirror real-world development organizations:

**Meta and Framework Agents:**
- `meta-agent.md` - Creates new specialized agents with orchestration awareness
- `meta-command.md` - Generates custom commands and workflows

**Leadership & Management Agents:**
- `engineering-director.md` - Engineering leadership and technical strategy
- `product-director.md` - Product strategy and roadmap management  
- `qa-director.md` - Quality assurance leadership and testing strategy
- `marketing-director.md` - Marketing strategy and growth initiatives
- `creative-director.md` - Creative strategy and brand management
- `devops-manager.md` - DevOps processes and infrastructure management
- `engineering-manager.md` - Engineering team management and process optimization
- `engineering-lead.md` - Technical leadership and architecture decisions
- `creative-ux-lead.md` - UX strategy and design leadership

**Core Development Agents:**
- `engineering-fullstack.md` - Full-stack development implementation spanning frontend to backend
- `engineering-ux.md` - UI component libraries, responsive design, and design systems
- `engineering-api.md` - API design, development, and integration
- `devops-infrastructure.md` - Infrastructure design and implementation
- `devops-cicd.md` - CI/CD pipeline development and automation

**Product & Analysis Agents:**
- `product-manager.md` - Product requirements and feature management
- `product-analyst.md` - Requirements analysis and business logic
- `data-scientist.md` - Data analysis and machine learning insights
- `data-analytics.md` - Team performance and development analytics

**Quality Assurance Agents:**
- `qa-analyst.md` - Quality analysis and testing strategy
- `qa-e2e.md` - End-to-end testing implementation
- `qa-scripts.md` - Test automation and scripting
- `engineering-test.md` - Comprehensive testing and validation

**Content & Creative Agents:**
- `marketing-content.md` - Content strategy and information architecture
- `creative-copywriter.md` - Marketing and technical copywriting
- `engineering-writer.md` - Documentation creation and technical writing
- `creative-wireframe.md` - Wireframing and design prototyping
- `creative-photographer.md` - Photography and visual content creation
- `creative-illustrator.md` - Illustration and graphic design
- `creative-logo.md` - Logo and brand identity design

**SEO & Marketing Agents:**
- `marketing-seo-researcher.md` - SEO research and competitive analysis
- `marketing-seo-engineer.md` - Technical SEO implementation
- `marketing-seo-analyst.md` - SEO performance analysis and optimization

**Operations & Release Agents:**
- `devops-release.md` - Release planning and deployment coordination
- `engineering-cleanup.md` - Code cleanup and technical debt management

**Specialized Task Agents:**
- `research-ai.md` - Research specialist for AI/ML innovations and best practices
- `research-deep.md` - Deep research and comprehensive analysis specialist
- `engineering-docs.md` - Documentation creation and maintenance specialist
- `meta-readme.md` - README file creation and updates
- `meta-commit.md` - Git workflow and commit message optimization
- `meta-script-uv.md` - Python UV script development and dependency management
- `meta-script-bun.md` - Bun JavaScript/TypeScript script development
- `meta-summary.md` - Audio summaries and next steps

Each agent includes:
- Clear delegation triggers and use cases
- Minimal but sufficient tool permissions
- Domain-specific workflows and best practices
- Structured output formats and quality standards

**Agent Delegation Patterns:**
- **Automatic Invocation**: Agents are triggered by specific keywords and phrases in user requests
- **Cross-functional Teams**: Agents collaborate across disciplines (e.g., fullstack-eng works with ux-eng for complete features)
- **Hierarchical Structure**: Directors manage their respective teams, with clear escalation paths
- **Specialized Expertise**: Each agent has deep domain knowledge while maintaining awareness of the broader system
- **Parallel Execution**: Multiple agents can work simultaneously on complex, multi-faceted tasks

### Command System (`commands/`)

Custom commands organized by functional category:

**Meta Operations (`meta/`):**
- `generate-agent.md` - Create new specialized agents
- `generate-command.md` - Create new custom commands  
- `gen-agent-command.md` - Generate agent-specific commands
- `list/tools.md` - List available tools and capabilities
- `update-status-line.md` - Update dynamic status display

**Task Management (`task/`):**
- `ai-research.md` - Trigger AI research and analysis tasks

**Research Operations (`research/`):**
- `quick.md` - Quick research tasks via agents
- `fetch.md` - Document fetching and analysis

**Specification (`spec/`):**
- `create.md` - Create technical specifications

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

## Development Team Organization

The agent system mirrors a complete software development organization with clear hierarchies and collaboration patterns:

### Executive Leadership
- **Engineering Director**: Oversees all technical decisions and architecture
- **Product Director**: Defines product strategy and roadmap
- **QA Director**: Ensures quality standards and testing strategy
- **Marketing Director**: Drives growth and market positioning
- **Creative Director**: Manages brand and creative output

### Middle Management
- **Engineering Manager**: Manages development processes and team coordination
- **DevOps Manager**: Handles infrastructure and deployment processes  
- **UX Lead**: Leads design strategy and user experience
- **Tech Lead**: Provides technical leadership and mentoring

### Development Teams
- **Core Engineering**: engineering-fullstack, engineering-ux, engineering-api, devops-infrastructure, devops-cicd
- **Quality Assurance**: qa-analyst, qa-e2e, qa-scripts, engineering-test
- **Product & Analysis**: product-manager, product-analyst, data-scientist, data-analytics
- **Content & Creative**: marketing-content, creative-copywriter, engineering-writer, creative-wireframe, creative-photographer, creative-illustrator, creative-logo
- **SEO & Marketing**: marketing-seo-researcher, marketing-seo-engineer, marketing-seo-analyst
- **Operations**: devops-release, engineering-cleanup

### Specialized Support
- **Research & Analysis**: research-ai, research-deep, engineering-docs
- **Automation & Tools**: meta-script-uv, meta-script-bun, meta-commit, meta-agent, meta-command
- **Communication**: meta-summary, meta-readme

## Usage Patterns

### Agent Delegation
```markdown
# Automatic agent invocation based on trigger phrases:
"Use research-ai to find current best practices"
"MUST BE USED when creating documentation" (engineering-writer, meta-readme)
"Specialist for code review and quality assurance" (qa-director, qa-e2e, qa-scripts)
"Use engineering-fullstack for complete feature implementation"
"Creative design needed" (creative-director, creative-illustrator, creative-logo)
"SEO optimization required" (marketing-seo-engineer, marketing-seo-analyst)
```

### Development Workflow Examples

**Feature Development:**
1. `product-manager` - Define requirements and user stories
2. `product-analyst` - Analyze business logic and processes  
3. `engineering-ux` - Create UI components and responsive design
4. `engineering-fullstack` - Implement end-to-end functionality
5. `qa-e2e` - Create comprehensive test coverage
6. `engineering-writer` - Document the feature for users

**Research Project:**
1. `research-ai` - Gather latest AI/ML developments
2. `research-deep` - Comprehensive competitive analysis
3. `data-scientist` - Analyze findings and metrics
4. `marketing-content` - Plan content and communication strategy

**Marketing Campaign:**
1. `marketing-director` - Define strategy and goals
2. `creative-copywriter` - Create compelling copy and messaging
3. `creative-director` - Oversee visual brand consistency
4. `marketing-seo-researcher` - Research keywords and competition  
5. `creative-photographer` - Create visual assets
6. `marketing-seo-engineer` - Implement technical SEO

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