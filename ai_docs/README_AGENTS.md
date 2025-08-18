# Agent Workflows Development Team

This repository contains a comprehensive Claude Code configuration with specialized AI agents for collaborative software development.

## 🤖 Available Agents

### Core Development Team

#### business-analyst
- **Purpose**: Business requirements analysis and market research
- **Tools**: Read, Write, Edit, Glob, Grep, LS, TodoWrite, WebSearch, WebFetch
- **Use for**: Requirements gathering, market analysis, risk assessment

#### doc-expert
- **Purpose**: Technical documentation fetching and maintenance
- **Tools**: Read, Write, Edit, TodoWrite, WebSearch, WebFetch, mcp__firecrawl__*
- **Use for**: Vendor documentation, API references, maintaining ai_docs/

#### ux-eng
- **Purpose**: UI/UX component development and responsive design
- **Tools**: Read, Write, Edit, MultiEdit, Glob, Grep, LS, TodoWrite, mcp__playwright__*, mcp__shadcn-ui__*, mcp__docker-mcp__*
- **Use for**: Component libraries, responsive templates, UI testing

#### fullstack-eng
- **Purpose**: Full-stack feature implementation and API development
- **Tools**: Bash, Read, Write, Edit, MultiEdit, Glob, Grep, LS, TodoWrite, mcp__playwright__*, mcp__docker-mcp__*
- **Use for**: Business logic, API endpoints, integration, testing

#### tech-lead
- **Purpose**: Technical planning and code review
- **Tools**: Bash, Read, Write, Edit, Glob, Grep, LS, TodoWrite, mcp__playwright__*, mcp__docker-mcp__*
- **Use for**: Technical specs, architecture design, final code review

#### ai-research
- **Purpose**: AI/ML research and technical trends
- **Tools**: Bash, Read, Write, Edit, WebSearch, WebFetch, mcp__firecrawl__*
- **Use for**: Latest AI developments, best practices, tool discovery

#### work-completion-summary
- **Purpose**: Audio summaries and completion reports
- **Tools**: Bash, mcp__ElevenLabs__*
- **Use for**: TTS summaries, work completion announcements

#### meta-agent
- **Purpose**: Generate new specialized agents
- **Tools**: Read, Write, Edit, MultiEdit, LS, WebSearch, WebFetch, mcp__firecrawl__*
- **Use for**: Creating custom agents for specific needs

## 📝 Available Commands

### Research Phase
- `/research/analyze` - Comprehensive business and technical research

### Specification Phase
- `/spec/create` - Create technical specification

### Architecture Phase
- `/architecture/design` - Design system architecture and data models

### Implementation Phase
- `/implementation/build-ui` - Build UI components
- `/implementation/build-feature` - Implement complete feature
- `/implementation/parallel-build` - Parallel UI and backend development

### Testing Phase
- `/testing/review` - Comprehensive code review
- `/testing/fix` - Fix failing tests and issues

### Workflow Commands
- `/workflow/init-project` - Initialize new project
- `/workflow/team-build` - Full team development workflow
- `/agent/quick-research` - Quick parallel research

### Git Commands
- `/git/status` - Check git status
- `/git/commit` - Create git commit

### Meta Commands
- `/meta/generate-agent` - Create new agent
- `/meta/generate-command` - Create new command

## 🚀 Quick Start

### Full Feature Development
```bash
/workflow/team-build "user authentication system"
```

### Quick Research
```bash
/agent/quick-research "microservices vs monolith"
```

### Create Technical Spec
```bash
/spec/create "payment processing"
```

### Build UI Components
```bash
/implementation/build-ui "dashboard components"
```

## 🔄 Development Workflow

### Typical Feature Development Flow

1. **Research & Analysis**
   - Business requirements (business-analyst)
   - Technical research (ai-research)
   - Documentation gathering (doc-expert)

2. **Planning & Architecture**
   - Technical specification (tech-lead)
   - System architecture (tech-lead)

3. **Implementation**
   - UI components (ux-eng)
   - Backend APIs (fullstack-eng)
   - Integration (fullstack-eng)

4. **Quality Assurance**
   - Code review (tech-lead)
   - Test fixing (fullstack-eng)
   - Final approval (tech-lead)

## 🛠️ MCP Servers

The following MCP servers are configured:

- **firecrawl**: Web scraping and documentation extraction
- **playwright**: Browser automation and testing
- **shadcn-ui**: UI component library
- **docker-mcp**: Docker container management
- **ElevenLabs**: Text-to-speech and audio

## 📁 Project Structure

```
.claude/
├── agents/           # Agent definitions
├── commands/         # Slash commands
├── hooks/           # Lifecycle hooks
├── settings.json    # Configuration
└── data/           # Agent state/logs

apps/               # Application projects
ai_docs/           # Condensed documentation
```

## 💡 Best Practices

1. **Use Parallel Agents**: Run independent agents simultaneously for efficiency
2. **Clear Task Definition**: Provide specific, detailed task descriptions
3. **Leverage Specialization**: Use the right agent for each task
4. **Document Everything**: Each agent documents their work
5. **Quality Gates**: Tech-lead reviews ensure consistency

## 🔧 Configuration

### Environment Variables
- `FIRECRAWL_API_KEY`: For web scraping
- `ELEVENLABS_API_KEY`: For text-to-speech

### Hooks
The project includes hooks for:
- Tool use logging
- Session management
- Notification handling
- Subagent coordination

## 📊 Efficiency Metrics

Using this multi-agent approach typically achieves:
- **50-70%** time reduction vs sequential development
- **Better consistency** through specialized expertise
- **Higher quality** through dedicated review
- **Comprehensive documentation** from each phase

## 🤝 Team Collaboration

This configuration is designed for team use:
- Check agent definitions into version control
- Share commands across the team
- Maintain consistent workflows
- Build on each other's work

## 📚 Further Reading

- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)
- [MCP Protocol](https://modelcontextprotocol.io/)
- [SPARC Methodology](https://github.com/ruvnet/claude-flow/wiki/SPARC-Methodology)