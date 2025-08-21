---
source: https://fly.io/docs/flyctl/
fetched: 2025-08-21
version: latest
---

# flyctl Command Reference

## Core Deployment Commands

### fly launch
**Purpose**: Initialize and deploy a new Fly.io application

```bash
fly launch [flags]
```

**What it does**:
- Detects project type automatically
- Creates new app in your organization
- Generates `fly.toml` configuration
- Builds Docker image
- Provisions resources (databases, IPs)
- Performs initial deployment

**Key Features**:
- Interactive configuration
- Language-specific scanners
- Good defaults for most projects
- Customizable through flags

### fly deploy
**Purpose**: Deploy application from source or image

```bash
fly deploy [WORKING_DIRECTORY] [flags]
```

**Key Options**:
- `-a, --app`: Specify application name
- `--image`: Deploy specific Docker image
- `--strategy`: Deployment strategy (canary, rolling, bluegreen, immediate)
- `--remote-only`: Build on remote builder (default)
- `--local-only`: Use local Docker daemon
- `--build-only`: Build without deploying
- `--detach`: Return immediately
- `--ha`: Enable high availability (default: true)
- `--vm-size`: Set VM size
- `--regions`: Deploy to specific regions
- `--now`: Deploy without confirmation

**Deployment Strategies**:
- **rolling** (default): Replace machines gradually
- **canary**: Deploy to subset, then rollout
- **bluegreen**: Deploy to new machines, switch traffic
- **immediate**: Replace all machines at once

## Monitoring & Debugging

### fly status
**Purpose**: Show application deployment status

```bash
fly status [flags]
```

**Options**:
- `--all`: Show completed instances
- `-a, --app`: Specify application
- `-j, --json`: JSON output
- `--watch`: Continuous refresh
- `--rate`: Refresh rate (default 5s)

**Information Displayed**:
- Application details
- Machine status and health
- Recent deployment details
- Regional allocation
- Resource usage

### fly logs
**Purpose**: View application logs

```bash
fly logs [flags]
```

**Options**:
- `-a, --app`: Specify application
- `-i, --instance`: Filter by instance
- `-r, --region`: Filter by region
- `-j, --json`: JSON format
- `-n, --no-tail`: No streaming (buffered only)
- `--machine`: Filter by machine ID

**Examples**:
```bash
fly logs                    # Stream all logs
fly logs --no-tail          # Just buffered logs
fly logs -r us-east         # Region-specific
fly logs --machine abc123   # Specific machine
```

## Configuration Management

### fly secrets
**Purpose**: Manage application secrets

```bash
fly secrets <command> [flags]
```

**Commands**:
```bash
fly secrets list            # List all secrets
fly secrets set KEY=value   # Set secret
fly secrets unset KEY       # Remove secret
fly secrets import < file   # Import from file
```

**Best Practices**:
- Use for sensitive data (passwords, API keys)
- Don't commit secrets to version control
- Import from secure files when possible
- Secrets are encrypted at rest

### fly scale
**Purpose**: Adjust application resources

```bash
fly scale <command> [options]
```

**Commands**:
```bash
fly scale count 3           # Set machine count
fly scale memory 1gb        # Set memory per machine
fly scale count 2 --region lax  # Scale specific region
fly scale show              # Show current scaling
```

**Scaling Options**:
- Count: Number of machines
- Memory: RAM per machine (256mb, 512mb, 1gb, 2gb, 4gb, 8gb)
- CPU: Shared vs dedicated cores

## Regional Management

### fly regions
**Purpose**: Manage deployment regions

```bash
fly regions <command>
```

**Commands**:
```bash
fly regions list            # List all available regions
fly regions add lax sea     # Add regions to app
fly regions remove lax      # Remove region
fly regions set lax sea ord # Set specific regions only
```

**Popular Regions**:
- `lax`: Los Angeles
- `sea`: Seattle  
- `ord`: Chicago
- `iad`: Ashburn (Virginia)
- `lhr`: London
- `nrt`: Tokyo

## Access & Debugging

### fly ssh console
**Purpose**: Interactive shell access

```bash
fly ssh console [flags]
```

**Options**:
- `-a, --app`: Specify application
- `--select`: Choose specific machine
- `-C, --command`: Run specific command
- `--user`: SSH as specific user

**Examples**:
```bash
fly ssh console              # Interactive shell
fly ssh console --select    # Choose machine
fly ssh console -C "ps aux" # Run command
```

## Advanced Commands

### fly machine
**Purpose**: Direct machine management

```bash
fly machine list            # List all machines
fly machine status <id>     # Machine details
fly machine start <id>      # Start machine
fly machine stop <id>       # Stop machine
fly machine destroy <id>    # Destroy machine
```

### fly apps
**Purpose**: Application management

```bash
fly apps list              # List your apps
fly apps create <name>     # Create app
fly apps destroy <name>    # Delete app
fly apps open              # Open app in browser
```

## Common Flag Patterns

**Global Flags** (work with most commands):
- `-a, --app`: Specify application name
- `-o, --org`: Specify organization
- `-j, --json`: JSON output format
- `-v, --verbose`: Verbose output
- `--access-token`: Use specific access token

**Output Control**:
- `--json`: Machine-readable JSON
- `--no-color`: Disable colored output
- `--quiet`: Minimal output
- `--verbose`: Detailed output