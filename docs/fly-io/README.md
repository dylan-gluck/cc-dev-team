---
source: https://fly.io/docs/
fetched: 2025-08-21
version: latest
---

# Fly.io Deployment Quick Reference

## Installation

### macOS
```bash
# Using Homebrew (recommended)
brew install flyctl

# Using curl
curl -L https://fly.io/install.sh | sh
```

### Linux
```bash
curl -L https://fly.io/install.sh | sh
```

### Windows
```powershell
# Using PowerShell
pwsh -Command "iwr https://fly.io/install.ps1 -useb | iex"

# If pwsh not found, use powershell
powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"
```

## Essential Commands

### Initial Setup & Deployment
```bash
# Create and deploy new app
fly launch

# Deploy existing app
fly deploy

# Deploy with specific options
fly deploy --strategy rolling --ha=false
fly deploy --image myimage:latest --detach
fly deploy --build-only  # Build without deploying
```

### Application Management
```bash
# Check app status
fly status
fly status --all          # Show completed instances
fly status --watch        # Continuous refresh

# View logs
fly logs                  # Stream logs
fly logs --no-tail        # Just buffered logs
fly logs --region us-east  # Region-specific logs
fly logs --json           # JSON format
```

### Secrets & Configuration
```bash
# Manage secrets
fly secrets list
fly secrets set DATABASE_URL=postgres://...
fly secrets unset OLD_SECRET

# Scale application
fly scale count 3          # Set machine count
fly scale memory 1gb       # Set memory per machine
fly scale show             # Show current scaling
```

### Region & SSH Management
```bash
# List and manage regions
fly regions list
fly regions add lax sea    # Add regions
fly regions remove lax     # Remove region

# SSH access
fly ssh console           # Interactive shell
fly ssh console --select # Choose specific machine
```

## Go Application Deployment

### Quick Start
1. Navigate to Go project directory
2. Ensure `go.mod` exists
3. Run `fly launch` (creates `fly.toml` and Dockerfile)
4. Configure as needed
5. Deploy with `fly deploy`

### Configuration Tips
- Default internal port: 8080
- Use Go's `embed` package for static files
- Set `PORT` environment variable
- Default Dockerfile uses Debian (can switch to Alpine)

### Best Practices
- Use `flyctl launch` for initial setup
- Configure secrets for sensitive data
- Test locally before deploying
- Monitor with `fly status` and `fly logs`
- Use rolling deployments for zero-downtime updates

## Common Workflow

```bash
# 1. Initial deployment
fly launch                # Interactive setup
fly deploy                # First deployment

# 2. Ongoing development
fly deploy                # Deploy changes
fly status                # Check deployment
fly logs                  # View logs

# 3. Production management
fly secrets set KEY=value # Manage secrets
fly scale count 2         # Scale for availability
fly regions add sea       # Add regions for performance
```

## Troubleshooting

```bash
# Debug deployment issues
fly status --all
fly logs --no-tail

# Access running application
fly ssh console

# View detailed machine info
fly machine list
fly machine status <machine-id>
```