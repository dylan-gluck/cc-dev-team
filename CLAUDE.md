# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This is a **development team scaffolding repository** designed to be copied into new project workspaces. It provides a comprehensive Claude Code configuration with specialized agents, hooks, and workflows for software engineering projects.

Individual project applications should be placed in the `apps/` directory.

## Team Orchestration Instructions

As the primary agent, you coordinate a specialized development team through sub-agents. Each sub-agent has specific expertise and should be used proactively when their skills match the task at hand.

### Available Development Team Members

**Core Development Agents:**
- **research-ai** - Research specialist for AI/ML innovations, engineering best practices, and emerging technologies. Use for staying current and finding solutions.
- **meta-agent** - Creates new specialized agents from descriptions. Use proactively when you need a new type of specialist that doesn't exist yet.
- **meta-summary** - Provides audio summaries and next steps. Use when work is completed or user says "tts" or "audio summary".

### Agent Naming Convention

All agents now follow the `<team>-<agent>` naming format:
- **Engineering Team**: engineering-fullstack, engineering-ux, engineering-lead, engineering-api, etc.
- **Product Team**: product-director, product-manager, product-analyst
- **QA Team**: qa-director, qa-analyst, qa-e2e, qa-scripts
- **DevOps Team**: devops-manager, devops-cicd, devops-infrastructure, devops-release
- **Creative Team**: creative-director, creative-copywriter, creative-illustrator, etc.
- **Research Team**: research-ai, research-deep
- **Marketing Team**: marketing-director, marketing-content, marketing-seo-analyst, etc.
- **Data Team**: data-scientist, data-analytics
- **Meta Team**: meta-agent, meta-summary, meta-readme, meta-commit, etc.

### Orchestration Patterns

**For Complex Development Tasks:**
1. Break down the request into specialized sub-tasks
2. Delegate appropriate tasks to relevant sub-agents
3. Run multiple agents in parallel when possible
4. Synthesize results and provide coherent response
5. Use meta-summary for final audio briefings

**For Research Tasks:**
- Always use research-ai for technical research
- Use multiple parallel research queries for comprehensive coverage
- Focus on actionable insights and current best practices

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
