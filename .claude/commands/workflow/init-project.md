---
description: Initialize a new project with proper structure and configuration
argument-hint: [project-name]
---

## Initialize New Project

Set up a new project: $ARGUMENTS

### Project Setup Workflow

1. **Create Project Structure**
```
apps/
└── $ARGUMENTS/
    ├── src/
    ├── tests/
    ├── docs/
    ├── Dockerfile
    └── README.md
```

2. **Frontend Setup (if web app)**
Use Bun and SvelteKit:
```bash
cd apps
bunx sv create $ARGUMENTS
cd $ARGUMENTS
bun add -D svelte-adapter-bun
bunx sv add tailwindcss
bunx shadcn-svelte@latest init
```

3. **Backend Setup (if API needed)**
Use UV and FastAPI:
```bash
cd apps/$ARGUMENTS
uv init
uv add fastapi pydantic uvicorn sqlalchemy alembic pytest ruff
```

4. **Docker Configuration**
Create multi-stage Dockerfile:
- Development stage with hot reload
- Production stage optimized for size
- Health checks configured
- Environment variables managed

5. **Documentation Structure**
Create initial documentation:
- README.md with project overview
- API documentation template
- Architecture decisions record
- Development setup guide

6. **Testing Setup**
Configure testing framework:
- Unit test structure
- Integration test setup
- E2E test configuration
- Coverage reporting

7. **Git Configuration**
- Initialize git repository
- Create .gitignore
- Set up pre-commit hooks
- Create initial commit

### Parallel Agent Execution

After setup, run agents in parallel:

**DOC-EXPERT**: Fetch relevant framework documentation
**BUSINESS-ANALYST**: Document project requirements
**TECH-LEAD**: Create initial technical specification

### Deliverables
- Project scaffolding complete
- Dependencies installed
- Docker configuration ready
- Documentation structure created
- Testing framework configured
- Git repository initialized

The project is ready for development with all necessary tooling and structure in place.