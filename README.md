# Claude Code Development Team Scaffolding

A comprehensive enterprise orchestration framework for building AI-powered development teams using Claude Code. This repository provides a production-ready scaffolding system with specialized agents, intelligent hooks, multi-team orchestration, and comprehensive state management for large-scale software development projects.

## Overview

This scaffolding transforms Claude Code into a sophisticated development team coordination platform. Rather than working with a single AI assistant, you get access to a complete team of specialized agents, each with specific expertise and tools, all orchestrated through an intelligent workflow system.


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

### External Resources
- **[Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)**: Official Claude Code docs
- **[UV Documentation](https://docs.astral.sh/uv/)**: Python package management
- **[Claude Code Hooks](https://docs.anthropic.com/en/docs/claude-code/hooks)**: Hook system reference
- **[Sub-Agents Guide](https://docs.anthropic.com/en/docs/claude-code/sub-agents)**: Agent delegation patterns

---

**Transform your development workflow with enterprise-scale AI orchestration. This scaffolding provides everything you need to coordinate multiple AI teams, manage complex software projects, and scale development operations with specialized agents, intelligent automation, and comprehensive observability.**
