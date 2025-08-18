# Agentic Dev Team
This document outlines the general plan and requirements for a claude-code configuration to support multi-agent coordination using specialized sub-agents with explicit system instructions and tool access.

## MCP Configuration
- Global MCP servers are defined in `/Users/dylan/.claude.json`
- Project MCP servers are defined in `.mcp.json`
- Agents have access to individual MCP tools in the format `mcp__${server}__${function_name}` eg: `mcp__firecrawl__firecrawl_search`
- Prefer specific MCP servers/functions than allowing raw Bash access

## Global Tools
- `Task` Is for assigning sub-agents
- `TodoWrite` Allows agent to create and manage structured task lists
- `Read` Allows an agent to read files in the project
- `Glob, Grep, LS` Allow an agent to search through project files
- `Edit, MultiEdit` Allow an agent to update project files
- `Write` Allows the creation or overriding of files
- `WebFetch, WebSearch` Enable agent to fetch specific pages or conduct general search queries
- `Bash` Allow arbitrary shell execution and working with cli tools

**Notes:**
- Almost all agents should have access to `TodoWrite` to track multi-step assignments
- If an agent is expected to write a report or any kind of document to the project they will need `Write` access and most likely `Read, Edit, LS` to understand context.
- Some agents may be ultra-specific and may not need read/write access to project files.
- Most coding agents will need full read, write edit, search and bash tools.

## Agents
Each agent is defined in a markdown file in `.claude/agents/` with a unique name in kebab-case as the file name. There is a custom slash command to generate new agent definitions in `.claude/commands/meta/generate-agent.md`.

Agents should have specific responsibilities. A parent claude-code instance will fire one or more agents in parallel, providing each with specific context and instructions. The sub-agent will work until complete and provide a summary for the parent agent on stop.

## Hooks
Hooks are claude-code lifecycle events that can extend the functionality of sub-agents and enable observibility and cross-agent communication. Hooks can run commands or scripts and have a standard JSON api for managing and consuming state. Hook scripts are defined as single-file python scripts that are run using `uv`, they live in `.claude/hooks/`. Commands are mapped to specific hooks in `.claude/settings.json`, multiple commands can be run for the same hook.

The current agent-scaffolding includes hooks that enable logging and observibility into the sub-agent workflow. The goal is to extend this functionality with cross-agent communication, session management, and reusable task/workflow definitions.

## Commands
Slash commands enable the user to trigger specific actions or workflows defined in `.claude/commands/`. Commands are grouped by folder for organization. Commands can be simple like `/git:status` & `/git:commit` or can be extremely detailed with conditional logic, prompt snippets, and specific instructions for tool use.

Arguments are passed into the command definition by string replace of $ARGUMENTS, this could be a single string prompt or multiple arguments like `/meta:agent new [description]` or `/workflow:new parallel --agents=8 --heirarchy=mesh`.

There should be commands for each phase of development with sub-commands for specific tasks & argumets to customize behavior.

Phases of Development:
- Research / Analysis / Investigation
- Spec / Planning
- Architecture / Data Model
- Implementation / Bug Fix
- Testing / Refinement

---

# Tech Stack & Project Structure

## Project
- Main project folder contains claude-code configuration, docker-compose config & project documentation. - App project folders live in `apps/`. Each app should have a Dockerfile for containerization. Each app should have its own package manager, scripts and documentation.
- Additional services will be defined in docker-compose.

## Front-end
- Web apps should be created using `bun`. Always use `bun` commands to manage dependencies & run scripts.
- New projects: Sveltekit latest version should be initialized with bun `cd apps && bunx sv create [app-name]`. Add the bun adapter `bun add -D svelte-adapter-bun` and update `svelte.config.js`.
- Add tailwind with `bunx sv add tailwindcss` then initialize shadcn-svelte with `bunx shadcn-svelte@latest init`. Add components using `bunx shadcn-svelte@latest add [component]` or `shadcn-ui` mcp.
- Code follows best-practices and uses Svelte v5 syntax including runes & new template syntax.
- doc-expert agent is responsible for maintaining svelte 5 specific documentation in the repo

## Back-end
- Backend APIs and services should be written in Python with FastAPI
- Always use `uv` to initialize and manage project, dependencies and run scripts
- Always use Pydantic types and Ruff for linting & formatting

---

# Agents

Outline of project-specific agents that should be created.

## business-analyst
- Tools: Read, Write, Edit, Glob, Grep, LS, TodoWrite, WebSearch, WebFetch
- Primary responsibility is to analyze business requirements, conduct deep-research and provide consolidated insights to the team.
- Secondary responsibility is to provide recommendations for business solutions based on insights, review business logic and provide feedback on potential risks and opportunities.

## doc-expert
- Tools: Read, Write, Edit, TodoWrite, WebSearch, WebFetch, mcp__firecrawl__*
- Primary responsibility is to fetch relevant and up-to-date technical documentation and condense into a single reference file that can be stored locally for other agents to consume.
- Secondary responsibility is to maintain project documentation
- Fetch latest vendor documentation using `WebSearch, WebFetch`. Scrape, crawl and extract using `firecrawl` mcp tools eg: `mcp__firecrawl__firecrawl_scrape`, `mcp__firecrawl__firecrawl_map`, `mcp__firecrawl__firecrawl_crawl`.
- Agent should determine what tools to use based on task assignment. For example crawl vs simple fetch.
- Condensed usage guide should be stored in project `ai_docs/` folder
- Once complete agent should return a summary of research & paths to any new docs

## ux-eng
- Tools: Read, Write, Edit, MultiEdit, Glob, Grep, LS, TodoWrite, mcp__playwright__*, mcp__shadcn-ui__*, mcp__docker-mcp__*
- Primary responsibility is building and maintaining library of beautiful ui components. Not responsible for integrating business logic.
- Secondary responsibility is building and editing front-end page templates & using `playwright` mcp to confirm valid implementation. All views and components must be responsive across all devices.
- Always utilizes design system and `shadcn-ui` mcp server to search/describe/edit components.
- Always follows specification in terms of requirements and when mocking placeholder data. Placeholder data should match described Data model as closely as possible.
- Always writes documentation for new components & updates existing docs after making changes.
- Returns a summary of completed work including paths to any new / updated components and any issues or errors encountered.

## fullstack-eng
- Tools: Bash, Read, Write, Edit, MultiEdit, Glob, Grep, LS, TodoWrite, mcp__playwright__*, mcp__docker-mcp__*,
- Primary responsibility is integrating business logic into the application. This includes writing and maintaining service architecture, building complex views and end-to-end features based on project SPEC and assigned task.
- Secondary responsibility is building and maintaining back-end APIs. All APIs must follow a strict data model and expose a schema. All APIs and endpoints must be secure and scalable.
- Always utilizes existing components or templates created by ux-eng.
- Always follows specification when integrating business logic or 3rd party services
- Always writes clear and accurate tests and runs them before marking work as complete. Always iterates on changes until tests are passing.
- Always writes documentation for new endpoints and updates existing docs after making changes.
- Returns a summary of completed work including paths to any new / updated files and any issues or errors encountered.

## tech-lead
- Tools: Bash, Read, Write, Edit, Glob, Grep, LS, TodoWrite, mcp__playwright__*, mcp__docker-mcp__*,
- Primary responsibility is writing technical implementation plans & specs. Depends on accurate vendor & project documentation from `doc-expert`.
- Secondary responsibility is code review after all agents have finished their tasks. Conducts a thorough analysis of code consistency, quality, and security.
- Prefers well structured code that is not overly-abstracted. SOLID principles, atomic patterns.
- Always checks for consistency across codebase and newly completed work. Each sub-agent may not have full-context or visibility across peer workstreams. tech-lead is responsible for checking collective changes after all agents have finished their work.
- If the tech-lead does not approve changes at the end of a parallel task cycle he should provide a report to the orchestrator agent including detailed requirements.
- Once approved tech-lead updates TODO and relevant planning documents with progress, returning a summary of completed work and passing requirements.

---

# References & Examples
**Docs:**
@ai_docs/cc/

**Orchestration POC:**
@../../../projects/atspro/.claude/ORCHESTRATION.md

**Claude-flow:**
@../claude-flow/
- https://github.com/ruvnet/claude-flow/wiki/SPARC-Methodology
- https://github.com/ruvnet/claude-flow/wiki/Development-Patterns
- https://github.com/ruvnet/claude-flow/wiki/CLAUDE-MD-Web-Development
- https://github.com/ruvnet/claude-flow/wiki/CLAUDE-MD-Templates
