# Template System Documentation

The Claude Code template system provides pre-configured project scaffolding for rapid application development. Templates include best practices, standard tooling, and agent coordination for various project types.

## Available Templates

### Application Templates (`app/`)

#### 1. **web** - Full-Stack Web Application
- **Stack**: SvelteKit + FastAPI + PostgreSQL
- **Features**: JWT auth, Redis caching, Docker Compose, Tailwind CSS
- **Use Case**: Modern web applications with real-time features
- **Command**: `/init-project myapp --template web`

#### 2. **api** - REST API Service
- **Stack**: FastAPI + PostgreSQL + Redis + Alembic
- **Features**: OpenAPI docs, JWT auth, rate limiting, structured logging
- **Use Case**: Production-ready microservices and APIs
- **Command**: `/init-project myservice --template api`

#### 3. **cli** - Command-Line Tool
- **Stack**: Python + Click + Rich
- **Features**: Beautiful output, configuration management, PyPI ready
- **Use Case**: Developer tools and automation scripts
- **Command**: `/init-project mytool --template cli`

#### 4. **library** - Reusable Package
- **Stack**: Python or TypeScript with comprehensive testing
- **Features**: API docs, benchmarking, CI/CD, package publishing
- **Use Case**: Open-source libraries and internal packages
- **Command**: `/init-project mylib --template library`

#### 5. **static** - Static Website
- **Stack**: Astro + Tailwind CSS + MDX
- **Features**: SEO optimized, blog support, zero JavaScript by default
- **Use Case**: Marketing sites, documentation, portfolios
- **Command**: `/init-project mysite --template static`

### Service Templates (`service/`)

#### 1. **mcp** - Model Context Protocol Server
- **Stack**: Python + UV + MCP SDK
- **Features**: Tools, resources, prompts, SSE transport, async operations
- **Use Case**: Creating MCP servers for Claude and other LLM integrations
- **Command**: `/init-project mymcp --template mcp`
- **Special**: Includes pre-setup research phase for integration documentation

#### 2. **microservice** - Kubernetes Microservice
- **Stack**: FastAPI + Kubernetes + Service Mesh
- **Features**: Health checks, distributed tracing, circuit breakers
- **Use Case**: Cloud-native microservices
- **Command**: `/init-project myservice --template microservice`

### Tool Templates (`tool/`)
*Coming soon: DevOps and utility tool templates*

### Data Templates (`data/`)
*Coming soon: Data pipeline and analytics templates*

### Custom Templates (`custom/`)
*For organization-specific templates*

## Research Phase

Templates with external integrations (like MCP) automatically trigger a research phase before setup:

1. **Integration Detection**: Template config specifies services/packages to research
2. **Parallel Research**: Multiple `research-docs` agents gather documentation
3. **Documentation Compilation**: Results saved to `INTEGRATIONS.md` at project root
4. **Reference Storage**: Condensed docs available for agents during setup

This ensures agents have up-to-date documentation and best practices when implementing your project.

## Usage

### Quick Start

```bash
# Create a new project with a specific template
/init-project myproject --template api

# Interactive template selection
/init-project myproject
# > Select a template: 
#   1. web - Full-Stack Web Application
#   2. api - REST API Service
#   3. cli - Command-Line Tool
#   4. library - Reusable Package
#   5. static - Static Website
```

### Template Options

Each template supports various configuration options that can be specified during initialization:

```bash
# Example: Create an API with specific features
/init-project myapi --template api --options "authentication-jwt,caching-redis,metrics-prometheus"
```

### Custom Templates

Create your own templates by adding JSON files to `.claude/templates/custom/`:

```json
{
  "name": "my-template",
  "displayName": "My Custom Template",
  "description": "Description of your template",
  "category": "custom",
  "stack": {
    "primary": "Main technology",
    "secondary": ["Supporting", "technologies"],
    "infrastructure": "Deployment method"
  },
  "structure": {
    "root": "apps/{project}",
    "directories": ["src", "tests", "docs"]
  },
  "dependencies": {
    "system": ["required", "system", "tools"],
    "development": {},
    "production": {}
  },
  "scripts": {
    "dev": "Development command",
    "test": "Test command",
    "build": "Build command"
  },
  "agents": {
    "setup": ["engineering-fullstack"],
    "enhance": ["engineering-test"],
    "review": ["engineering-lead"]
  }
}
```

## Template Schema

### Required Fields

- **name**: Unique identifier for the template
- **displayName**: Human-readable name shown in selection
- **description**: Brief description of the template's purpose
- **category**: Template category (app, service, tool, data, custom)
- **stack**: Technology stack information
- **structure**: Directory structure to create

### Optional Fields

- **dependencies**: System and package dependencies
- **scripts**: Common development scripts
- **options**: Configuration flags
- **notes**: Implementation guidance
- **agents**: Agents to involve in setup
- **files**: Pre-configured files to create

## Agent Integration

Templates automatically spawn appropriate agents for setup:

1. **Setup Phase**: Initial project creation
   - Assigned agents create the project structure
   - Install dependencies and configure tools

2. **Enhancement Phase**: Adding features
   - Test engineers add testing infrastructure
   - API engineers implement endpoints
   - UX engineers enhance interfaces

3. **Review Phase**: Quality assurance
   - Tech leads review architecture
   - QA analysts validate testing

## Best Practices

### Choosing a Template

1. **Web Applications**: Use `web` template for full-stack apps with UI
2. **APIs/Microservices**: Use `api` template for backend services
3. **Developer Tools**: Use `cli` template for command-line utilities
4. **Packages**: Use `library` template for reusable code
5. **Marketing/Docs**: Use `static` template for content sites

### Customizing Templates

After initialization, templates can be customized:

```bash
# Add authentication to an API project
/enhance-project --feature authentication

# Add testing to any project
/add-testing --framework pytest --coverage 80

# Add CI/CD pipeline
/setup-ci --platform github-actions
```

### Template Development

When creating new templates:

1. Start with the simplest working configuration
2. Include only essential dependencies
3. Provide clear documentation in notes
4. Test the template end-to-end
5. Include example code/tests
6. Define appropriate agent assignments

## Examples

### Creating a Full-Stack Application

```bash
/init-project social-app --template web
```

This creates:
- Frontend with SvelteKit and Tailwind
- Backend API with FastAPI
- PostgreSQL database with migrations
- Redis for caching and sessions
- Docker Compose for local development
- JWT authentication setup
- Testing infrastructure

### Creating a Microservice

```bash
/init-project user-service --template api
```

This creates:
- FastAPI application with versioned APIs
- PostgreSQL with Alembic migrations
- Redis caching layer
- OpenAPI documentation
- Health check endpoints
- Structured logging
- Docker configuration
- Comprehensive testing setup

### Creating a CLI Tool

```bash
/init-project devtool --template cli
```

This creates:
- Click-based command structure
- Rich terminal output formatting
- Configuration file support
- Plugin system architecture
- Testing utilities
- PyPI publishing configuration

## Template Maintenance

Templates are versioned and updated regularly to include:
- Latest framework versions
- Security patches
- Best practice updates
- New feature patterns
- Performance optimizations

To update templates in your project:
```bash
/update-templates
```

## Contributing Templates

To contribute a new template:

1. Create template JSON in appropriate category folder
2. Test template with init-project command
3. Document template usage and options
4. Submit via pull request

## Support

For template issues or suggestions:
- Check template JSON for configuration options
- Review agent logs for setup errors
- Consult specific framework documentation
- Request enhancements via GitHub issues