# Agent Reference Guide

This document provides a comprehensive overview of all available agents in the orchestration-aware development team system.

## Overview

The agent ecosystem consists of specialized agents organized into teams that work together through an orchestration framework. Each agent has specific responsibilities, capabilities, and integration points with the broader system.

## Team Structure

### Engineering Team
**Orchestrator:** `engineering-director`
**Focus:** Core development, architecture, and implementation

| Agent | Role | Model | Capacity | Key Skills |
|-------|------|-------|----------|------------|
| `engineering-lead` | Technical Leadership | opus | 1 | architecture, code_review, technical_spec, data_model_design |
| `engineering-fullstack` | Full Stack Development | sonnet | 3 | frontend, backend, api, database, integration |
| `engineering-ux` | UX Engineering | sonnet | 2 | ui_components, responsive_design, accessibility, design_systems |
| `engineering-test` | Quality Assurance | haiku | 2 | unit_testing, integration_testing, e2e_testing, test_automation |
| `engineering-docs` | Documentation | haiku | 1 | technical_writing, api_documentation, user_guides |
| `engineering-api` | API Specialist | sonnet | 2 | REST, GraphQL, API design, microservices |
| `engineering-manager` | Engineering Management | opus | 1 | team_coordination, project_planning, resource_allocation |
| `engineering-writer` | Technical Writing | haiku | 1 | documentation, tutorials, user_guides |
| `engineering-cleanup` | Code Maintenance | haiku | 1 | refactoring, optimization, debt_reduction |
| `engineering-mcp` | MCP Integration | sonnet | 1 | MCP development, tool integration |

### Product Team
**Orchestrator:** `product-director`
**Focus:** Product strategy, requirements, and business analysis

| Agent | Role | Model | Capacity | Key Skills |
|-------|------|-------|----------|------------|
| `product-manager` | Product Management | opus | 1 | requirements, user_stories, acceptance_criteria, prioritization |
| `product-analyst` | Business Analysis | sonnet | 1 | requirements_analysis, process_mapping, data_analysis |

### QA Team
**Orchestrator:** `qa-director`
**Focus:** Quality assurance, testing, and validation

| Agent | Role | Model | Capacity | Key Skills |
|-------|------|-------|----------|------------|
| `qa-e2e` | End-to-End Testing | sonnet | 2 | e2e_testing, user_journey_validation, cross_browser_testing |
| `qa-scripts` | Test Automation | haiku | 2 | test_scripting, automation_frameworks, ci_integration |
| `qa-analyst` | Quality Analysis | haiku | 1 | test_reporting, metrics_analysis, quality_trends |

### DevOps Team
**Orchestrator:** `devops-manager`
**Focus:** Infrastructure, deployment, and operations

| Agent | Role | Model | Capacity | Key Skills |
|-------|------|-------|----------|------------|
| `devops-cicd` | CI/CD Pipeline Management | sonnet | 1 | github_actions, build_automation, deployment_workflows |
| `devops-infrastructure` | Infrastructure Management | sonnet | 1 | docker, kubernetes, terraform, cloud_platforms |
| `devops-release` | Release Coordination | haiku | 1 | version_management, changelog_generation, deployment_orchestration |

### Creative Team
**Orchestrator:** `creative-director`
**Focus:** Design, content creation, and visual assets

| Agent | Role | Model | Capacity | Key Skills |
|-------|------|-------|----------|------------|
| `creative-copywriter` | Content Writing | sonnet | 2 | copywriting, content_strategy, brand_voice |
| `creative-illustrator` | Visual Design | sonnet | 1 | illustration, graphics, visual_design |
| `creative-photographer` | Photography | haiku | 1 | photography, image_editing, visual_assets |
| `creative-ux-lead` | UX Leadership | opus | 1 | user_experience, design_strategy, prototyping |
| `creative-wireframe` | Wireframing | haiku | 1 | wireframes, prototypes, user_flows |
| `creative-logo` | Logo Design | haiku | 1 | logo_design, branding, identity |

### Research Team
**Orchestrator:** `research-general`
**Focus:** Research, analysis, and knowledge gathering

| Agent | Role | Model | Capacity | Key Skills |
|-------|------|-------|----------|------------|
| `research-ai` | AI Research Specialist | sonnet | 1 | ai_research, llm_trends, technology_analysis |
| `research-deep` | Deep Research | opus | 1 | comprehensive_research, analysis, synthesis |
| `research-docs` | Documentation Research | haiku | 1 | technical_documentation, research, compilation |

### Marketing Team
**Orchestrator:** `marketing-director`
**Focus:** Marketing strategy, content, and promotion

| Agent | Role | Model | Capacity | Key Skills |
|-------|------|-------|----------|------------|
| `marketing-content` | Content Marketing | sonnet | 2 | content_creation, marketing_copy, campaigns |
| `marketing-seo-analyst` | SEO Analysis | haiku | 1 | seo_analysis, keyword_research, optimization |
| `marketing-seo-engineer` | SEO Implementation | sonnet | 1 | technical_seo, site_optimization, performance |
| `marketing-seo-researcher` | SEO Research | haiku | 1 | market_research, competitor_analysis, trends |

### Data Team
**Orchestrator:** (No dedicated orchestrator)
**Focus:** Data analysis, science, and analytics

| Agent | Role | Model | Capacity | Key Skills |
|-------|------|-------|----------|------------|
| `data-scientist` | Data Science | opus | 1 | machine_learning, statistical_analysis, modeling |
| `data-analytics` | Data Analytics | sonnet | 1 | data_analysis, reporting, visualization |

### Meta Team
**Orchestrator:** `meta-agent`
**Focus:** System configuration, automation, and meta-operations

| Agent | Role | Model | Capacity | Key Skills |
|-------|------|-------|----------|------------|
| `meta-agent` | Agent Generation | opus | 1 | agent_creation, system_design, orchestration |
| `meta-summary` | Summary Generation | sonnet | 1 | summarization, reporting, audio_summaries |
| `meta-readme` | Documentation Generation | haiku | 1 | readme_creation, documentation_maintenance |
| `meta-commit` | Commit Management | haiku | 1 | git_commits, version_control, changelog |
| `meta-command` | Command Generation | sonnet | 1 | slash_commands, workflow_automation |
| `meta-config` | Configuration Management | haiku | 1 | config_management, settings_optimization |
| `meta-script-uv` | Python Script Generation | sonnet | 1 | python_scripts, uv_projects, automation |
| `meta-script-bun` | JavaScript Script Generation | sonnet | 1 | javascript_scripts, bun_projects, automation |

## Orchestration Integration

### Team Hierarchies

The orchestration system uses a hierarchical structure where:

1. **Team Orchestrators** (Directors/Managers) coordinate their team members
2. **Team Members** perform specialized tasks and report status
3. **Cross-Team Coordination** happens through orchestrator communication
4. **State Management** tracks progress across all agents and teams

### Communication Patterns

**Message Bus Integration:**
- Agents emit events for state changes and task completion
- Orchestrators subscribe to relevant events from their team members
- Cross-team communication happens through standardized event protocols

**State Management:**
- Each agent can read/write to shared orchestration state
- Sprint progress, epic status, and team metrics are tracked centrally
- State changes trigger appropriate notifications and workflows

### Task Delegation

**Automatic Delegation:**
- Orchestrators analyze incoming tasks and delegate to appropriate team members
- Task complexity determines agent model selection (haiku/sonnet/opus)
- Parallel execution is used when tasks are independent

**Manual Orchestration:**
- User can explicitly invoke specific agents using the Task tool
- Slash commands provide direct access to orchestration features
- Confirmation required for resource-intensive operations

## Agent Selection Guide

### When to Use Each Agent

**For Feature Development:**
1. Start with `product-director` for requirements and planning
2. Use `engineering-lead` for technical architecture
3. Delegate to `engineering-fullstack` for implementation
4. Involve `engineering-ux` for UI components
5. Coordinate testing with `qa-director`

**For Bug Fixes:**
1. Use `engineering-lead` for analysis and planning
2. Delegate to appropriate specialist (fullstack, ux, api)
3. Ensure `qa-e2e` validates the fix

**For Research Tasks:**
1. Use `research-ai` for AI/ML related topics
2. Use `research-deep` for comprehensive analysis
3. Use `product-analyst` for business requirements research

**For Documentation:**
1. Use `engineering-docs` for technical documentation
2. Use `meta-readme` for README files
3. Use `creative-copywriter` for user-facing content

**For Infrastructure:**
1. Use `devops-manager` for overall strategy
2. Use `devops-cicd` for pipeline work
3. Use `devops-infrastructure` for deployment and scaling

## Orchestration Events

### Event Types

**Task Events:**
- `task:created` - New task assigned to agent
- `task:started` - Agent begins work on task
- `task:completed` - Task finished successfully
- `task:failed` - Task encountered errors
- `task:blocked` - Task waiting on dependencies

**State Events:**
- `state:updated` - Orchestration state modified
- `epic:created` - New epic planned
- `sprint:started` - Sprint begins
- `sprint:completed` - Sprint finished

**Team Events:**
- `team:activated` - Team begins coordinated work
- `team:status` - Team progress update
- `team:blocked` - Team waiting on external dependencies

### Event Handling

Agents can:
- **Emit Events** to notify the system of status changes
- **Subscribe to Events** to react to external changes
- **Query State** to understand current system status
- **Update State** to record progress and decisions

## Configuration Management

### Team Configuration

Teams are defined in `.claude/orchestration/teams.json` with:
- **Members:** List of agents and their capabilities
- **Settings:** Team-specific behavior and limits
- **Workflows:** Default task flows and review requirements
- **Resources:** Capacity limits and model preferences

### Agent Configuration

Individual agents are defined in `.claude/agents/` with:
- **Frontmatter:** Name, description, tools, color, model
- **Purpose:** Role definition and core responsibilities
- **Workflow:** Step-by-step execution process
- **Integration:** Orchestration and state management hooks

### Orchestration Settings

Global settings in `.claude/orchestration/settings.json` control:
- **Automation Level:** Manual, assisted, or automatic delegation
- **Resource Limits:** Maximum agents, tokens, and runtime
- **Confirmation Rules:** When user approval is required
- **Communication:** Message bus and event streaming settings

## Usage Examples

### Starting a Sprint

```bash
/orchestrate sprint start "Epic: User Authentication"
```

This command:
1. Activates relevant teams (Engineering, Product, QA)
2. Creates sprint state in orchestration system
3. Delegates planning tasks to team orchestrators
4. Sets up communication channels between teams

### Delegating a Feature

```bash
/orchestrate task delegate "Implement user login form"
```

This command:
1. Analyzes task requirements
2. Determines appropriate team (Engineering)
3. Routes to engineering-director orchestrator
4. Delegates to engineering-fullstack for implementation
5. Involves engineering-ux for UI components
6. Coordinates with qa-e2e for testing

### Generating Documentation

```bash
/meta:readme "Document the authentication system"
```

This command:
1. Invokes meta-readme agent
2. Analyzes existing authentication code
3. Generates comprehensive README
4. Updates relevant documentation files

## Best Practices

### Agent Development

1. **Single Responsibility:** Each agent should have a clear, focused purpose
2. **Minimal Tools:** Include only necessary tools for the agent's function
3. **Clear Triggers:** Description should clearly state when to use the agent
4. **State Integration:** Include state management for progress tracking
5. **Error Handling:** Comprehensive error handling and recovery strategies

### Orchestration Usage

1. **Start Small:** Begin with manual mode and simple tasks
2. **Build Trust:** Gradually increase automation as confidence grows
3. **Monitor Resources:** Keep track of token usage and execution time
4. **Document Decisions:** Record architectural and design decisions
5. **Iterate Quickly:** Use small, focused iterations for better outcomes

### Team Coordination

1. **Clear Handoffs:** Define clear deliverables between team phases
2. **Shared Context:** Ensure all team members have necessary context
3. **Progress Tracking:** Use state management to track progress
4. **Quality Gates:** Define clear quality criteria before advancement
5. **Continuous Communication:** Maintain open channels between teams

This agent ecosystem provides a flexible, scalable foundation for orchestrated software development with clear specialization, strong integration, and comprehensive coordination capabilities.