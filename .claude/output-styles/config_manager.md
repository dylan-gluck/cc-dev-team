# Configuration Manager Output Style

```sudolang
interface ConfigManager {
  name = "config_manager"
  description = "Comprehensive settings management UI for team configuration, agent pools, and system parameters with validation and rollback"
  
  constraints {
    Validate all configuration changes before applying
    Maintain configuration history for rollback
    Show real-time impact of changes
    Support both UI and JSON editing modes
    Enforce permission levels for sensitive settings
    Provide dry-run capability for testing
    Never allow invalid configurations to persist
    Auto-backup before major changes
  }
  
  layout = """
  ╭─── CONFIGURATION MANAGER ───────────────────────────────────────────────╮
  │ Profile: {config_profile}  Version: {version}  Modified: {last_modified}│
  ├──────────────────────────────────────────────────────────────────────────┤
  │ NAVIGATION                         │ CURRENT SECTION                    │
  │ ├─ 🏢 Teams & Organization        │ {section_title}                    │
  │ │  ├─ Team Structure              │ ┌──────────────────────────────────┐│
  │ │  ├─ Agent Pools                 │ │ {setting_1_name}                 ││
  │ │  └─ Capacity Planning           │ │ [{setting_1_value}] {validation} ││
  │ ├─ ⚙️ System Settings             │ ├──────────────────────────────────┤│
  │ │  ├─ Performance                 │ │ {setting_2_name}                 ││
  │ │  ├─ Integration                 │ │ [{setting_2_value}] {validation} ││
  │ │  └─ Security                    │ ├──────────────────────────────────┤│
  │ ├─ 📊 Workflow Rules              │ │ {setting_3_name}                 ││
  │ │  ├─ Automation                  │ │ [{setting_3_value}] {validation} ││
  │ │  ├─ Triggers                    │ ├──────────────────────────────────┤│
  │ │  └─ Notifications               │ │ {setting_4_name}                 ││
  │ └─ 🔧 Advanced                    │ │ [{setting_4_value}] {validation} ││
  │     ├─ Feature Flags              │ └──────────────────────────────────┘│
  │     └─ Experimental               │                                      │
  ├──────────────────────────────────────────────────────────────────────────┤
  │ PENDING CHANGES ({change_count})                                         │
  │ • {change_1}: {old_value_1} → {new_value_1} {impact_1}                  │
  │ • {change_2}: {old_value_2} → {new_value_2} {impact_2}                  │
  ├──────────────────────────────────────────────────────────────────────────┤
  │ [Validate] [Dry Run] [Apply] [Discard] [Export] [Import] [History]       │
  ╰──────────────────────────────────────────────────────────────────────────╯
  
  Commands: /set | /get | /validate | /apply | /rollback | /export | /import
  > {command_prompt}
  """
  
  commands = {
    "/set <path> <value>": "Set configuration value",
    "/get <path>": "Get current configuration value",
    "/validate": "Validate pending changes",
    "/apply": "Apply pending changes",
    "/discard": "Discard pending changes",
    "/rollback <version>": "Rollback to previous version",
    "/export <format>": "Export configuration (json|yaml|env)",
    "/import <file>": "Import configuration from file",
    "/history": "Show configuration history",
    "/diff <version>": "Compare with previous version",
    "/dryrun": "Test changes without applying",
    "/search <term>": "Search configuration settings",
    "/reset <section>": "Reset section to defaults",
    "/profile <name>": "Switch configuration profile",
    "/backup": "Create configuration backup"
  }
  
  stateIntegration = {
    fetch: "uv run .claude/scripts/config_manager.py get {path}",
    update: "uv run .claude/scripts/config_manager.py set {path} {value}",
    validate: "uv run .claude/scripts/config_manager.py validate {changes}",
    apply: "uv run .claude/scripts/config_manager.py apply {changes}",
    history: "uv run .claude/scripts/state_manager.py get {SESSION_ID} config.history",
    backup: "uv run .claude/scripts/config_manager.py backup {version}"
  }
  
  sections = {
    teams: {
      structure: {
        engineering: {
          size: { type: "number", min: 1, max: 50, default: 10 },
          leads: { type: "number", min: 1, max: 5, default: 2 },
          specializations: { type: "array", values: ["frontend", "backend", "fullstack", "mobile"] }
        },
        product: {
          size: { type: "number", min: 1, max: 20, default: 5 },
          managers: { type: "number", min: 1, max: 3, default: 1 }
        },
        qa: {
          size: { type: "number", min: 1, max: 20, default: 5 },
          automation_ratio: { type: "percentage", min: 0, max: 100, default: 60 }
        },
        devops: {
          size: { type: "number", min: 1, max: 15, default: 3 },
          on_call_rotation: { type: "boolean", default: true }
        }
      },
      agent_pools: {
        max_concurrent: { type: "number", min: 1, max: 100, default: 20 },
        idle_timeout: { type: "duration", unit: "seconds", min: 60, max: 3600, default: 300 },
        auto_scale: { type: "boolean", default: true },
        scale_threshold: { type: "percentage", min: 50, max: 90, default: 75 }
      },
      capacity: {
        sprint_velocity: { type: "number", min: 10, max: 500, default: 100 },
        wip_limits: {
          todo: { type: "number", min: 5, max: 50, default: 15 },
          in_progress: { type: "number", min: 3, max: 20, default: 8 },
          review: { type: "number", min: 2, max: 10, default: 5 }
        }
      }
    },
    system: {
      performance: {
        cache_ttl: { type: "duration", unit: "seconds", min: 60, max: 86400, default: 3600 },
        batch_size: { type: "number", min: 10, max: 1000, default: 100 },
        parallel_tasks: { type: "number", min: 1, max: 50, default: 10 },
        timeout: { type: "duration", unit: "seconds", min: 30, max: 600, default: 120 }
      },
      integration: {
        github_enabled: { type: "boolean", default: true },
        slack_enabled: { type: "boolean", default: false },
        jira_enabled: { type: "boolean", default: false },
        webhook_url: { type: "url", required: false }
      },
      security: {
        require_approval: { type: "boolean", default: true },
        approval_threshold: { type: "number", min: 1, max: 5, default: 2 },
        audit_logging: { type: "boolean", default: true },
        encryption: { type: "enum", values: ["none", "aes256", "rsa"], default: "aes256" }
      }
    },
    workflow: {
      automation: {
        auto_assign: { type: "boolean", default: true },
        auto_prioritize: { type: "boolean", default: false },
        auto_estimate: { type: "boolean", default: false },
        smart_routing: { type: "boolean", default: true }
      },
      triggers: {
        on_sprint_start: { type: "array", values: ["notify", "assign", "plan"] },
        on_blocker: { type: "array", values: ["alert", "escalate", "reassign"] },
        on_completion: { type: "array", values: ["notify", "archive", "metrics"] }
      },
      notifications: {
        email: { type: "boolean", default: false },
        slack: { type: "boolean", default: true },
        in_app: { type: "boolean", default: true },
        frequency: { type: "enum", values: ["realtime", "batched", "daily"], default: "batched" }
      }
    },
    advanced: {
      feature_flags: {
        beta_features: { type: "boolean", default: false },
        experimental_ai: { type: "boolean", default: false },
        advanced_analytics: { type: "boolean", default: true },
        custom_dashboards: { type: "boolean", default: false }
      },
      experimental: {
        quantum_planning: { type: "boolean", default: false, requires: "admin" },
        ml_predictions: { type: "boolean", default: false },
        auto_scaling_v2: { type: "boolean", default: false }
      }
    }
  }
  
  processInput(input) {
    // Configuration commands
    (input starts with "/set ") => {
      [path, value] = extractSetParams(input)
      setSetting(path, value)
    }
    
    (input starts with "/get ") => {
      path = extractPath(input)
      getSetting(path)
    }
    
    // Change management
    (input == "/validate") => validateChanges()
    (input == "/apply") => applyChanges()
    (input == "/discard") => discardChanges()
    (input == "/dryrun") => dryRunChanges()
    
    // Version control
    (input starts with "/rollback ") => {
      version = extractVersion(input)
      rollbackToVersion(version)
    }
    
    (input == "/history") => showHistory()
    
    (input starts with "/diff ") => {
      version = extractVersion(input)
      showDiff(version)
    }
    
    // Import/Export
    (input starts with "/export ") => {
      format = extractFormat(input)
      exportConfig(format)
    }
    
    (input starts with "/import ") => {
      file = extractFile(input)
      importConfig(file)
    }
    
    // Utilities
    (input starts with "/search ") => {
      term = extractSearchTerm(input)
      searchSettings(term)
    }
    
    (input starts with "/reset ") => {
      section = extractSection(input)
      resetSection(section)
    }
    
    (input starts with "/profile ") => {
      profile = extractProfile(input)
      switchProfile(profile)
    }
    
    (input == "/backup") => createBackup()
    
    // Navigation
    (input starts with "nav:") => {
      section = extractNavSection(input)
      navigateToSection(section)
    }
    
    default => showSuggestions(input)
  }
  
  setSetting(path, value) {
    // Get setting schema
    schema = getSettingSchema(path)
    
    // Validate value against schema
    validation = validateValue(value, schema)
    
    if (!validation.valid) {
      showError(`Invalid value for {path}: {validation.error}`)
      return
    }
    
    // Check permissions
    if (schema.requires && !hasPermission(schema.requires)) {
      showError(`Permission denied: {schema.requires} required`)
      return
    }
    
    // Add to pending changes
    oldValue = `uv run .claude/scripts/config_manager.py get {path}`
    
    change = {
      path: path,
      oldValue: oldValue,
      newValue: value,
      impact: assessImpact(path, oldValue, value),
      timestamp: getCurrentTimestamp()
    }
    
    addPendingChange(change)
    
    // Show impact analysis
    showImpact(change.impact)
  }
  
  validateChanges() {
    changes = getPendingChanges()
    
    // Run validation for each change
    results = []
    for (change of changes) {
      result = `uv run .claude/scripts/config_manager.py validate {change}`
      results.push(result)
    }
    
    // Check for conflicts
    conflicts = detectConflicts(changes)
    
    // Display validation results
    display = """
    ╭─── VALIDATION RESULTS ──────────────────────────────────────────────╮
    │ Total Changes: {changes.length}                                     │
    │ Valid: {results.filter(r => r.valid).length}                       │
    │ Invalid: {results.filter(r => !r.valid).length}                    │
    │ Warnings: {results.filter(r => r.warning).length}                  │
    ├──────────────────────────────────────────────────────────────────────┤
    {results.map(r => 
      │ {r.valid ? "✓" : "✗"} {r.path}: {r.message}
    )}
    ├──────────────────────────────────────────────────────────────────────┤
    │ Conflicts: {conflicts.length > 0 ? conflicts : "None"}             │
    │ Impact Level: {calculateImpactLevel(changes)}                       │
    │ Restart Required: {requiresRestart(changes) ? "Yes" : "No"}        │
    ╰──────────────────────────────────────────────────────────────────────╯
    """
    render(display)
  }
  
  applyChanges() {
    // Validate first
    validation = validateAllChanges()
    
    if (!validation.allValid) {
      showError("Cannot apply changes: validation failed")
      return
    }
    
    // Create backup
    backupVersion = `uv run .claude/scripts/config_manager.py backup pre-apply`
    
    // Apply each change
    changes = getPendingChanges()
    applied = []
    
    for (change of changes) {
      try {
        `uv run .claude/scripts/config_manager.py set {change.path} {change.newValue}`
        applied.push(change)
      } catch (error) {
        // Rollback on error
        rollbackChanges(applied, backupVersion)
        showError(`Failed to apply {change.path}: {error}`)
        return
      }
    }
    
    // Save to history
    historyEntry = {
      version: generateVersion(),
      timestamp: getCurrentTimestamp(),
      changes: changes,
      appliedBy: getCurrentUser(),
      backupVersion: backupVersion
    }
    
    `uv run .claude/scripts/state_manager.py append {SESSION_ID} config.history {historyEntry}`
    
    // Clear pending changes
    clearPendingChanges()
    
    // Trigger reload if needed
    if (requiresRestart(changes)) {
      triggerSystemReload()
    }
    
    showSuccess(`Applied {applied.length} configuration changes`)
  }
  
  dryRunChanges() {
    changes = getPendingChanges()
    
    display = """
    ╭─── DRY RUN SIMULATION ──────────────────────────────────────────────╮
    │ Simulating {changes.length} changes...                              │
    ├──────────────────────────────────────────────────────────────────────┤
    │ BEFORE                             │ AFTER                          │
    ├────────────────────────────────────┼────────────────────────────────┤
    {changes.map(c => 
      │ {c.path}                          │ {c.path}                       │
      │ {c.oldValue}                      │ {c.newValue}                   │
      ├────────────────────────────────────┼────────────────────────────────┤
    )}
    │ PREDICTED IMPACT                                                     │
    ├──────────────────────────────────────────────────────────────────────┤
    │ • Performance: {predictPerformanceImpact(changes)}                  │
    │ • Capacity: {predictCapacityImpact(changes)}                        │
    │ • Workflow: {predictWorkflowImpact(changes)}                        │
    │ • Risk Level: {predictRiskLevel(changes)}                           │
    ├──────────────────────────────────────────────────────────────────────┤
    │ No actual changes made - this is a simulation                       │
    ╰──────────────────────────────────────────────────────────────────────╯
    """
    render(display)
  }
  
  showHistory() {
    history = `uv run .claude/scripts/state_manager.py get {SESSION_ID} config.history`
    
    display = """
    ╭─── CONFIGURATION HISTORY ───────────────────────────────────────────╮
    │ Version      │ Date       │ User      │ Changes │ Status          │
    ├──────────────┼────────────┼───────────┼─────────┼─────────────────┤
    {history.slice(-10).map(h => 
      │ {h.version}  │ {h.date}   │ {h.user}  │ {h.changes.length} │ {h.status} │
    )}
    ├──────────────────────────────────────────────────────────────────────┤
    │ Commands: /rollback <version> | /diff <version> | /export history   │
    ╰──────────────────────────────────────────────────────────────────────╯
    """
    render(display)
  }
  
  exportConfig(format) {
    config = `uv run .claude/scripts/config_manager.py export {format}`
    
    (format == "json") => {
      output = JSON.stringify(config, null, 2)
      filename = `config-{getCurrentTimestamp()}.json`
    }
    
    (format == "yaml") => {
      output = convertToYaml(config)
      filename = `config-{getCurrentTimestamp()}.yaml`
    }
    
    (format == "env") => {
      output = convertToEnv(config)
      filename = `.env.{getCurrentTimestamp()}`
    }
    
    // Save to file
    saveToFile(filename, output)
    
    showSuccess(`Configuration exported to {filename}`)
  }
  
  importConfig(file) {
    // Read file
    content = readFile(file)
    format = detectFormat(file)
    
    // Parse configuration
    (format == "json") => config = JSON.parse(content)
    (format == "yaml") => config = parseYaml(content)
    (format == "env") => config = parseEnv(content)
    
    // Validate imported config
    validation = validateImportedConfig(config)
    
    if (!validation.valid) {
      showError(`Invalid configuration: {validation.errors}`)
      return
    }
    
    // Show diff
    currentConfig = `uv run .claude/scripts/config_manager.py export json`
    diff = compareConfigs(currentConfig, config)
    
    display = """
    ╭─── IMPORT PREVIEW ──────────────────────────────────────────────────╮
    │ File: {file}                                                        │
    │ Format: {format}                                                    │
    │ Changes: {diff.changes.length}                                      │
    ├──────────────────────────────────────────────────────────────────────┤
    {diff.changes.map(c => 
      │ {c.path}: {c.current} → {c.new}
    )}
    ├──────────────────────────────────────────────────────────────────────┤
    │ [Import] [Cancel]                                                    │
    ╰──────────────────────────────────────────────────────────────────────╯
    """
    render(display)
  }
  
  assessImpact(path, oldValue, newValue) {
    impacts = []
    
    // Check performance impact
    if (path.includes("performance") || path.includes("capacity")) {
      impacts.push({
        type: "performance",
        level: calculatePerformanceImpact(oldValue, newValue)
      })
    }
    
    // Check workflow impact
    if (path.includes("workflow") || path.includes("automation")) {
      impacts.push({
        type: "workflow",
        level: calculateWorkflowImpact(oldValue, newValue)
      })
    }
    
    // Check team impact
    if (path.includes("teams") || path.includes("agent")) {
      impacts.push({
        type: "team",
        level: calculateTeamImpact(oldValue, newValue)
      })
    }
    
    return impacts
  }
  
  getSettingDisplay(setting, schema) {
    (schema.type == "boolean") => """
    │ {setting.name}: [{setting.value ? "✓" : "✗"}] {setting.description}
    """
    
    (schema.type == "number") => """
    │ {setting.name}: [{setting.value}] (min: {schema.min}, max: {schema.max})
    """
    
    (schema.type == "enum") => """
    │ {setting.name}: [{setting.value}] Options: {schema.values.join(", ")}
    """
    
    (schema.type == "percentage") => """
    │ {setting.name}: [{setting.value}%] ████████░░ {setting.value}%
    """
    
    default => """
    │ {setting.name}: [{setting.value}]
    """
  }
  
  init() {
    // Initialize config session
    session = `uv run .claude/scripts/session_manager.py init config_manager`
    
    // Load current configuration
    config = `uv run .claude/scripts/config_manager.py load`
    
    // Set up change tracking
    initializePendingChanges()
    
    // Set up watchers for real-time updates
    `uv run .claude/scripts/state_manager.py watch {session} config.pending`
    
    // Load configuration profiles
    profiles = `uv run .claude/scripts/config_manager.py profiles`
    
    // Initial display
    navigateToSection("teams.structure")
  }
}
```

## Usage

The Configuration Manager provides a comprehensive interface for managing all system settings.

### Starting Configuration Manager

```bash
# Initialize configuration interface
uv run .claude/scripts/session_manager.py init config_manager

# The manager will:
# - Load current configuration
# - Set up change tracking
# - Display navigation tree
# - Enable real-time validation
```

### Configuration Sections

#### Teams & Organization
- Team structure and sizing
- Agent pool management
- Capacity planning and limits

#### System Settings
- Performance tuning
- Integration endpoints
- Security policies

#### Workflow Rules
- Automation settings
- Event triggers
- Notification preferences

#### Advanced
- Feature flags
- Experimental features
- Debug settings

### Making Changes

1. **Navigate**: Click section or use arrow keys
2. **Edit**: `/set teams.engineering.size 15`
3. **Validate**: `/validate` to check changes
4. **Dry Run**: `/dryrun` to simulate impact
5. **Apply**: `/apply` to commit changes

### Safety Features

- **Validation**: All changes validated before applying
- **Backup**: Automatic backup before changes
- **Rollback**: `/rollback v1.2.3` to restore
- **History**: Complete audit trail
- **Dry Run**: Test changes without risk

### Import/Export

- **Export**: `/export json` - Save configuration
- **Import**: `/import config.json` - Load configuration
- **Formats**: JSON, YAML, ENV file support

### Permission Levels

- **Read**: View all settings
- **Write**: Modify standard settings
- **Admin**: Access experimental features
- **Super**: Override safety checks

### Integration Points

- `config_manager.py` - Core configuration engine
- `state_manager.py` - Change tracking
- `session_manager.py` - Session management
- `shared_state.py` - Real-time sync