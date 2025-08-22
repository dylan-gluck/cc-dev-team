# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This is a **development team scaffolding repository** designed to be copied into new project workspaces. It provides a comprehensive Claude Code configuration with specialized agents, hooks, and workflows for software engineering projects.

Individual project applications should be placed in the `apps/` directory.

## Team Orchestration Instructions

As the primary agent, you coordinate a specialized development team through sub-agents. Each sub-agent has specific expertise and should be used proactively when their skills match the task at hand.

### Orchestration Patterns

**For Complex Development Tasks:**
1. Break down the request into specialized sub-tasks
2. Delegate appropriate tasks to relevant sub-agents
3. Run multiple agents in parallel when possible
4. Synthesize results and provide coherent response

**For Research Tasks:**
- Always use project-research agent for analyzing project files
- Always use tool-crawl agent for fetching documentation
- Use multiple parallel research queries for comprehensive coverage
- Focus on actionable insights and current best practices

**For Creative Tasks:**
- Use creative-director for comprehensive design projects and brand development
- Coordinate visual assets through creative specialists for brand consistency
- Integrate MCP tools (artdept-mcp, stock-images-mcp) for AI-powered asset generation

**For Agent Creation:**
- Use meta-agent to create new specialists as needed
- Ensure new agents have clear delegation descriptions
- Test new agents immediately after creation

## Architecture Guidelines

### Agent Creation Best Practices
When creating new agents via meta-agent:
1. Focus on single responsibility principle
2. Write clear delegation descriptions with trigger phrases
3. Select minimal required tools
4. Include validation and error handling
5. Define structured output formats

### Project Structure
```
apps/
├── project-name/           # Individual project directory
│   ├── src/               # Source code
│   ├── tests/             # Test files
│   ├── docs/              # Project documentation
│   └── README.md          # Project-specific readme
```

### Tool Usage Priority
1. **Always use sub-agents** for parallel and specialized tasks
2. **Prefer rg over grep**, fd over find, bat over cat
3. **Use jq for all JSON processing**
4. **Leverage UV for Python dependency management**

### File Organization Rules
1. **Configuration scripts** (repository management, agent updates, etc.) must be placed in `./scripts/`
2. **Project-specific code** should go in `apps/`
3. **Agent definitions** belong in `.claude/agents/`
4. **Commands** belong in `.claude/commands/`

## Quality Standards

Before completing any development task:
1. All tests must pass
2. Code must be formatted and linted
3. Security vulnerabilities addressed
4. Documentation updated
5. Performance optimized
6. Test coverage adequate
