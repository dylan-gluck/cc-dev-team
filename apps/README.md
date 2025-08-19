# Apps Directory

This directory contains individual project applications within the Claude Code development team scaffolding monorepo. Each app folder should be a self-contained project with its own dependencies, configuration, and deployment setup.

## Purpose

The `apps/` directory serves as the workspace for actual project development within the scaffolding framework. While the root directory provides development team infrastructure (agents, hooks, output styles), this directory houses the applications you build using those tools.

## Project Structure

Each application should follow this standardized structure:

```
apps/
├── project-name/
│   ├── src/                    # Source code
│   │   ├── main.py|js|ts       # Entry point
│   │   ├── components/         # Reusable components
│   │   ├── services/           # Business logic
│   │   └── utils/              # Helper functions
│   ├── tests/                  # Test files
│   │   ├── unit/               # Unit tests
│   │   ├── integration/        # Integration tests
│   │   └── fixtures/           # Test data
│   ├── docs/                   # Project documentation
│   │   ├── api.md              # API documentation
│   │   ├── deployment.md       # Deployment guide
│   │   └── architecture.md     # System design
│   ├── config/                 # Configuration files
│   │   ├── dev.json            # Development config
│   │   ├── prod.json           # Production config
│   │   └── test.json           # Test config
│   ├── scripts/                # Build and deployment scripts
│   │   ├── build.sh            # Build script
│   │   ├── deploy.sh           # Deployment script
│   │   └── test.sh             # Test runner
│   ├── package.json            # Node.js dependencies (if applicable)
│   ├── pyproject.toml          # Python dependencies (if applicable)
│   ├── Dockerfile              # Container configuration
│   ├── docker-compose.yml      # Multi-service orchestration
│   ├── .env.example            # Environment variables template
│   ├── .gitignore              # Project-specific ignores
│   └── README.md               # Project-specific documentation
```

## Technology Stack Guidelines

### Python Projects
For Python applications, use UV for dependency management:

```toml
# pyproject.toml
[project]
name = "your-app-name"
version = "0.1.0"
description = "Brief description"
dependencies = [
    "fastapi>=0.104.0",
    "uvicorn>=0.24.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "black>=23.0.0",
    "ruff>=0.1.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

### Node.js Projects
For JavaScript/TypeScript applications:

```json
{
  "name": "your-app-name",
  "version": "1.0.0",
  "description": "Brief description",
  "main": "src/main.js",
  "scripts": {
    "dev": "node src/main.js",
    "build": "tsc",
    "test": "jest",
    "lint": "eslint src/",
    "format": "prettier --write src/"
  },
  "dependencies": {
    "express": "^4.18.0"
  },
  "devDependencies": {
    "jest": "^29.0.0",
    "eslint": "^8.0.0",
    "prettier": "^3.0.0",
    "typescript": "^5.0.0"
  }
}
```

### Containerization
Each app should include Docker configuration:

```dockerfile
# Dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY src/ ./src/
EXPOSE 3000
CMD ["node", "src/main.js"]
```

```yaml
# docker-compose.yml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
    volumes:
      - ./config:/app/config:ro
```

## Development Workflow

### Creating a New App

1. **Create the project directory:**
   ```bash
   mkdir apps/my-new-app
   cd apps/my-new-app
   ```

2. **Initialize the project structure:**
   ```bash
   mkdir -p src tests docs config scripts
   touch README.md .gitignore .env.example
   ```

3. **Set up dependency management:**
   - Python: `uv init` or create `pyproject.toml`
   - Node.js: `npm init` or create `package.json`

4. **Create Dockerfile and docker-compose.yml**

5. **Write initial tests and documentation**

### Testing Strategy

Each app should implement comprehensive testing:

- **Unit Tests**: Test individual functions and components
- **Integration Tests**: Test service interactions
- **End-to-End Tests**: Test complete user workflows
- **Performance Tests**: Validate response times and throughput

### Code Quality Standards

All apps must maintain consistent code quality:

- **Formatting**: Use automated formatters (Black for Python, Prettier for JS)
- **Linting**: Use linters (Ruff for Python, ESLint for JS)
- **Type Checking**: Use type hints (Python) or TypeScript
- **Documentation**: Include docstrings and README files
- **Security**: Regular dependency updates and vulnerability scans

## Configuration Management

### Environment Variables
Use environment-specific configuration:

```bash
# .env.example
DATABASE_URL=postgresql://user:pass@localhost/db
API_KEY=your_api_key_here
DEBUG=false
LOG_LEVEL=info
PORT=3000
```

### Configuration Files
Organize configuration by environment:

```json
// config/dev.json
{
  "database": {
    "host": "localhost",
    "port": 5432,
    "name": "myapp_dev"
  },
  "logging": {
    "level": "debug",
    "format": "detailed"
  }
}
```

## Deployment Guidelines

### Container Registry
Build and push container images:

```bash
# Build image
docker build -t myapp:latest .

# Tag for registry
docker tag myapp:latest registry.example.com/myapp:v1.0.0

# Push to registry
docker push registry.example.com/myapp:v1.0.0
```

### Health Checks
Implement health check endpoints:

```python
# Python/FastAPI example
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}
```

### Monitoring and Logging
Include observability from the start:

- **Metrics**: Expose Prometheus metrics
- **Logging**: Structured JSON logs
- **Tracing**: OpenTelemetry instrumentation
- **Health Checks**: Kubernetes-compatible endpoints

## Multi-App Considerations

### Shared Dependencies
For common functionality across apps:

1. **Create a shared library directory:**
   ```
   apps/
   ├── shared/
   │   ├── auth/
   │   ├── database/
   │   └── utils/
   ├── web-app/
   └── api-service/
   ```

2. **Use local package installation:**
   ```bash
   # In each app directory
   pip install -e ../shared
   # or
   npm install file:../shared
   ```

### Inter-Service Communication
Design for service independence:

- **API Contracts**: Define clear interfaces
- **Message Queues**: Use for async communication
- **Service Discovery**: Implement health checks
- **Circuit Breakers**: Handle service failures gracefully

### Database Strategy
Choose appropriate data persistence:

- **Per-Service Databases**: Microservices pattern
- **Shared Database**: Simpler for monolithic apps
- **Database Migrations**: Version control schema changes

## Integration with Development Scaffolding

### Using Claude Code Agents
Leverage the development team agents for app development:

```bash
# Research best practices
"Research the latest FastAPI patterns with ai-research"

# Create specialized agents
"Create a testing agent for this API service with meta-agent"

# Get audio summaries
"Summarize the current development status with work-completion-summary"
```

### Hook Integration
Apps benefit from the development hooks:

- **Security Validation**: Automatic blocking of dangerous operations
- **TTS Feedback**: Audio notifications for long-running processes
- **Development Context**: Automatic loading of project state
- **Transcript Logging**: Complete audit trail of development decisions

### Custom Output Styles
Use appropriate output styles for different tasks:

- **genui**: Visual debugging and data exploration
- **table-based**: Status reports and comparisons
- **yaml-structured**: Configuration management
- **tts-summary**: Audio feedback for deployment status

## Best Practices

### Security
- Never commit secrets or API keys
- Use environment variables for configuration
- Implement proper input validation
- Regular dependency security audits
- Container image vulnerability scanning

### Performance
- Implement caching strategies
- Optimize database queries
- Use connection pooling
- Monitor resource usage
- Load testing before deployment

### Maintainability
- Write comprehensive tests
- Document architectural decisions
- Use semantic versioning
- Automate deployment pipelines
- Regular code reviews

### Scalability
- Design for horizontal scaling
- Implement proper logging and metrics
- Use asynchronous processing where appropriate
- Plan for database scaling
- Consider CDN for static assets

## Example Apps

This directory may contain reference implementations:

- **web-dashboard**: React/TypeScript frontend application
- **api-gateway**: FastAPI backend service
- **data-processor**: Python batch processing service
- **microservice-template**: Minimal service template

Each example demonstrates best practices and integration patterns with the development scaffolding framework.