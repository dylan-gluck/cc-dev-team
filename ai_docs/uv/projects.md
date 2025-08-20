---
source: https://docs.astral.sh/uv/concepts/projects/
fetched: 2025-08-20
version: uv-latest
related_urls:
  - https://docs.astral.sh/uv/guides/projects/
  - https://docs.astral.sh/uv/concepts/projects/layout/
  - https://docs.astral.sh/uv/concepts/projects/dependencies/
  - https://docs.astral.sh/uv/concepts/projects/config/
---

# UV Projects Quick Reference

## Installation & Project Creation

```bash
# Create new project
uv init [project-name]

# Initialize in existing directory
uv init .

# Initialize with specific template
uv init --template package my-package
```

## Core Project Structure

```
my-project/
├── .gitignore              # Auto-generated
├── .python-version         # Python version specification
├── README.md              # Project documentation
├── pyproject.toml         # Project metadata and configuration
├── uv.lock               # Lockfile (auto-generated)
├── .venv/                # Virtual environment (auto-managed)
└── src/                  # Source code (for packages)
    └── my_project/
        └── __init__.py
```

## Essential Files

### pyproject.toml Configuration

```toml
[project]
name = "my-project"
version = "0.1.0"
description = "Project description"
readme = "README.md"
dependencies = [
    "requests>=2.31.0",
    "click>=8.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "black>=23.0.0",
]
network = ["httpx>=0.27.0"]

[dependency-groups]
test = ["pytest", "pytest-cov"]
lint = ["ruff", "mypy"]

[tool.uv]
dev-dependencies = [
    "pytest>=7.0.0",
    "ruff>=0.1.0",
]

[tool.uv.sources]
my-local-package = { path = "../my-local-package", editable = true }
experimental-pkg = { git = "https://github.com/user/repo.git" }

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

### .python-version

```
3.12
```

## Dependency Management

### Adding Dependencies

```bash
# Add runtime dependency
uv add requests

# Add with version constraint
uv add "django>=4.2,<5.0"

# Add optional dependency (extra)
uv add httpx --optional network

# Add development dependency
uv add pytest --dev

# Add to specific group
uv add pytest --group test

# Add editable local package
uv add --editable ./path/to/package

# Add from git
uv add git+https://github.com/user/repo.git

# Add from specific branch/tag
uv add git+https://github.com/user/repo.git@main
```

### Removing Dependencies

```bash
# Remove dependency
uv remove requests

# Remove from specific group
uv remove pytest --group test

# Remove optional dependency
uv remove httpx --optional network
```

### Upgrading Dependencies

```bash
# Upgrade all dependencies
uv lock --upgrade

# Upgrade specific package
uv lock --upgrade-package requests

# Upgrade to latest compatible versions
uv sync --upgrade
```

## Running Commands

```bash
# Run script in project environment
uv run python script.py
uv run pytest
uv run python -m my_module

# Run with specific Python version
uv run --python 3.11 python script.py

# Run isolated (temporary environment)
uv run --isolated python script.py

# Install and run command
uv run --with requests python -c "import requests; print('OK')"
```

## Environment Management

```bash
# Sync environment with lockfile
uv sync

# Sync with all optional dependencies
uv sync --all-extras

# Sync specific extras
uv sync --extra network --extra dev

# Sync only production dependencies
uv sync --no-dev

# Clean and recreate environment
uv sync --reinstall
```

## Project Workflow

### Development Workflow

```bash
# 1. Initialize project
uv init my-project
cd my-project

# 2. Add dependencies
uv add requests pytest --dev

# 3. Write code and tests
# Edit src/ and tests/

# 4. Run tests
uv run pytest

# 5. Sync environment
uv sync

# 6. Build package (if applicable)
uv build
```

### Lockfile Management

- `uv.lock` is automatically generated and updated
- Contains exact resolved versions for reproducibility
- Should be committed to version control
- Cross-platform compatible
- Automatically updated when dependencies change

## Dependency Sources

### Supported Source Types

```toml
[tool.uv.sources]
# Local path (editable)
local-pkg = { path = "../local-pkg", editable = true }

# Git repository
git-pkg = { git = "https://github.com/user/repo.git" }

# Git with branch/tag
git-branch = { git = "https://github.com/user/repo.git", branch = "main" }

# Git with commit
git-commit = { git = "https://github.com/user/repo.git", rev = "abc123" }

# URL archive
url-pkg = { url = "https://example.com/package.tar.gz" }

# Workspace member
workspace-pkg = { workspace = true }

# Index with authentication
private-pkg = { index = "https://pypi.company.com/simple/" }
```

## Configuration Options

### Tool Configuration

```toml
[tool.uv]
# Environment management
managed = true                    # Auto-manage .venv
package = false                   # Treat as virtual project

# Dependency resolution
resolution = "highest"            # or "lowest-direct"
prerelease = "disallow"          # or "allow", "if-necessary"

# Index configuration
index-url = "https://pypi.org/simple/"
extra-index-url = ["https://download.pytorch.org/whl/cpu"]

# Cache settings
cache-dir = ".uv-cache"
no-cache = false

# Build settings
no-build = ["tensorflow"]        # Don't build from source
no-binary = ["psycopg2"]        # Always build from source
```

## Building & Publishing

```bash
# Build source and wheel distributions
uv build

# Build to specific directory
uv build --out-dir dist/

# Build only wheel
uv build --wheel

# Build only source distribution
uv build --sdist

# Publish to PyPI (with twine)
uv run twine upload dist/*
```

## Common Patterns

### Multi-Environment Development

```bash
# Development with all extras
uv sync --all-extras

# Production deployment
uv sync --no-dev

# Testing environment
uv sync --extra test --no-dev
```

### CI/CD Configuration

```yaml
# GitHub Actions example
- name: Set up Python
  uses: actions/setup-python@v4
  with:
    python-version: '3.12'

- name: Install uv
  run: pip install uv

- name: Install dependencies
  run: uv sync --no-dev

- name: Run tests
  run: uv run pytest
```

## Troubleshooting

### Common Issues

1. **Environment not syncing**
   ```bash
   uv sync --reinstall
   ```

2. **Dependency conflicts**
   ```bash
   uv lock --resolution lowest-direct
   ```

3. **Clear cache**
   ```bash
   uv cache clean
   ```

4. **Python version mismatch**
   ```bash
   uv python install 3.12
   uv sync --python 3.12
   ```

5. **Lockfile out of sync**
   ```bash
   uv lock
   uv sync
   ```

### Project Types

- **Package Project**: Contains `[build-system]` in pyproject.toml, installed in editable mode
- **Virtual Project**: No build system, only dependencies are installed
- **Workspace**: Multiple related projects managed together

## Best Practices

1. **Always commit uv.lock** to version control
2. **Use specific version constraints** for production dependencies
3. **Separate dev and production dependencies** clearly
4. **Pin Python version** in .python-version
5. **Use dependency groups** for organization
6. **Regular dependency updates** with `uv lock --upgrade`
7. **Test with clean environments** using `uv sync --reinstall`