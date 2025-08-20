---
description: Initialize a new project with templates and proper configuration
argument-hint: [project-name] [--template <template-name>]
---

## Initialize New Project

Set up a new project: $ARGUMENTS

### Template-Based Project Initialization

#### Available Templates
- **web**: Full-stack web application (SvelteKit + FastAPI + PostgreSQL)
- **api**: REST API service (FastAPI + PostgreSQL + Redis)
- **cli**: Command-line tool (Python + Click + Rich)
- **library**: Reusable package (Python/TypeScript)
- **static**: Static website (Astro + Tailwind CSS)
- **mcp**: Model Context Protocol server with tools/resources/prompts

#### Usage Examples
```bash
# With specific template
/init-project myapp --template web
/init-project myservice --template api
/init-project mytool --template cli

# Interactive template selection
/init-project myproject
```

### Project Setup Workflow

1. **Template Selection**
   - Parse --template flag or show interactive selection
   - Load template configuration from `.claude/templates/{category}/{template}.json`
   - Validate template requirements

2. **Research Phase** (for templates with integrations/dependencies)
   - Extract services, packages, and integrations from template config
   - Spawn research-docs agents in parallel for each integration
   - Gather latest documentation, best practices, and API references
   - Compile research into `INTEGRATIONS.md` at project root
   - Store condensed reference docs for agent use during setup

3. **Project Structure Creation**
   - Create root directory: `apps/$ARGUMENTS/`
   - Generate directory structure from template specification
   - Apply naming conventions and project-specific replacements

4. **Dependency Installation**
   Based on template configuration:
   - System dependencies check
   - Development dependencies installation
   - Production dependencies setup
   - Package manager configuration (UV, npm, bun)

5. **File Generation**
   Create template-specific files:
   - Configuration files (pyproject.toml, package.json, etc.)
   - Docker/Docker Compose setup
   - CI/CD pipeline configuration
   - Initial source code structure
   - Test scaffolding
   - Documentation templates
   - INTEGRATIONS.md from research phase

6. **Script Configuration**
   Set up development scripts from template:
   - `dev`: Start development server
   - `test`: Run test suite
   - `build`: Build for production
   - `format`: Code formatting
   - `lint`: Code linting
   - Custom template-specific scripts

7. **Agent Coordination**
   Spawn template-specified agents:
   - **Research Phase**: Documentation gathering agents (pre-setup)
   - **Setup Phase**: Initial configuration agents
   - **Enhancement Phase**: Feature implementation agents
   - **Review Phase**: Quality assurance agents

8. **Git Initialization**
   - Initialize repository
   - Create appropriate .gitignore
   - Configure pre-commit hooks
   - Make initial commit with template

### Template Processing Logic

```python
def init_project(project_name, template=None):
    # 1. Template selection
    if not template:
        template = show_template_selector()
    
    # 2. Load template configuration
    template_path = f".claude/templates/{category}/{template}.json"
    config = load_template_config(template_path)
    
    # 3. Research phase (if integrations present)
    if 'research' in config.agents or config.get('config', {}).get('services'):
        integrations = extract_integrations(config)
        research_tasks = []
        for integration in integrations:
            research_tasks.append(spawn_research_agent(integration))
        research_results = await_all(research_tasks)
        create_integrations_doc(project_name, research_results)
    
    # 4. Create project structure
    create_directories(project_name, config.structure)
    
    # 5. Process dependencies
    install_dependencies(config.dependencies)
    
    # 6. Generate files
    for file_spec in config.files:
        create_file(project_name, file_spec)
    
    # 7. Configure scripts
    setup_scripts(project_name, config.scripts)
    
    # 8. Spawn agents
    for phase, agents in config.agents.items():
        spawn_agents(agents, project_name, phase)
```

### Parallel Agent Execution

Based on selected template, coordinate agents:

**Web Template**:
- engineering-fullstack: Set up full-stack structure
- engineering-ux: Configure UI components
- engineering-api: Implement backend services

**API Template**:
- engineering-api: Create API structure
- engineering-test: Set up testing framework
- devops-infrastructure: Configure deployment

**CLI Template**:
- engineering-fullstack: Build CLI structure
- documentation-writer: Create usage docs
- engineering-test: Add test suite

**Library Template**:
- engineering-fullstack: Package structure
- engineering-test: Comprehensive testing
- documentation-writer: API documentation

**Static Template**:
- engineering-ux: Design implementation
- creative-copywriter: Content structure
- marketing-seo-analyst: SEO optimization

**MCP Template**:
- research-docs: Gather integration documentation
- engineering-mcp: MCP server implementation
- engineering-api: API structure and endpoints
- engineering-test: Testing framework

### Deliverables

- ✅ Project scaffolding from template
- ✅ All dependencies installed
- ✅ Development environment configured
- ✅ Testing framework ready
- ✅ Documentation structure created
- ✅ Git repository initialized
- ✅ Agent tasks assigned
- ✅ Ready for immediate development

### Post-Initialization

After project creation:
1. Display next steps specific to template
2. Show available enhancement commands
3. List development scripts
4. Provide quick start instructions

The project is ready with template-specific tooling, best practices, and coordinated agent support.