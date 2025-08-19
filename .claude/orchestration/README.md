# Orchestration Configuration

This directory contains user-editable configuration files that control the orchestration system's behavior. Modify these JSON files to customize teams, workflows, and settings.

## Configuration Files

### `teams.json`
Defines your team structure, agent members, and capabilities.

**Key sections:**
- `teams` - Define each team with its orchestrator, members, and settings
- `orchestration_settings` - Global settings for confirmation and resource limits

**To modify teams:**
1. Edit the team definition under the `teams` object
2. Add/remove members in the `members` array
3. Adjust `capacity` to control how many instances of each agent can run
4. Update `skills` to define agent capabilities

### `workflows.json` 
Templates for sprints, epics, and task workflows.

**Key sections:**
- `sprint` - Two-week sprint workflow with phases and ceremonies
- `epic` - Large feature development workflow with gates
- `task` - Individual task types and delegation rules

**To modify workflows:**
1. Edit phase durations and required roles
2. Add/remove workflow phases
3. Update delegation rules for task assignment

### `settings.json`
Global orchestration preferences and operational settings.

**Key sections:**
- `orchestration_mode` - Control automation level (manual/assisted/auto)
- `resource_limits` - Set maximum agents, tokens, and runtime
- `confirmation_settings` - Configure when user confirmation is required
- `slash_commands` - Available orchestration commands

**To modify settings:**
1. Change `orchestration_mode.default_mode` to adjust automation level
2. Update `resource_limits` to control resource usage
3. Adjust `confirmation_thresholds` to set when confirmation is needed

## How to Apply Changes

Configuration changes are loaded when orchestration commands are invoked. No restart required.

### Validate Configuration
```bash
# Check if your JSON is valid
.claude/scripts/validate_config.py

# Or use jq to validate
jq . .claude/orchestration/*.json
```

### Reload Configuration
```bash
# Reload all configurations
/orchestrate config reload

# View current configuration
/orchestrate config show
```

## Configuration Principles

1. **Start Conservative**: Begin with `manual` mode and low resource limits
2. **Increase Gradually**: As you get comfortable, increase automation and limits
3. **Team-Specific**: Each team can have different settings and workflows
4. **User Control**: All automation can be overridden with slash commands

## Examples

### Add a New Team Member
```json
// In teams.json, under engineering.members:
{
  "agent": "backend-specialist",
  "role": "Backend Development",
  "capacity": 2,
  "skills": ["api", "database", "microservices"],
  "model": "sonnet"
}
```

### Change Confirmation Threshold
```json
// In settings.json, under confirmation_thresholds:
"agents": {
  "warning": 2,    // Warn when spawning 2+ agents
  "require": 3     // Require confirmation for 3+ agents
}
```

### Disable Auto-Documentation
```json
// In teams.json, under engineering.settings:
"auto_documentation": false
```

## Important Notes

- These files are version-controlled - commit your changes
- Invalid JSON will prevent orchestration from starting
- Use the slash commands to test changes incrementally
- State files (in `.claude/state/`) are separate and should not be edited

## Getting Help

- Run `/orchestrate help` for command documentation
- Check `.claude/orchestration/schema/` for JSON schemas
- Review `ai_docs/ORCHESTRATION_SPEC.md` for full details