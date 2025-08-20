---
allowed-tools: Bash(python:*), Bash(uv run:*), Read, Task
description: Validate all orchestration configurations
argument-hint: [--fix] [--verbose]
model: sonnet
---

# Configuration Validation

Run comprehensive validation of all orchestration configurations.

## Context
- Validation script: @.claude/scripts/validate_orchestration.py
- Configuration directory: !`ls -la .claude/orchestration/*.json 2>/dev/null | wc -l | xargs -I {} echo "{} config files found"`
- Arguments: $ARGUMENTS

## Task

Execute comprehensive configuration validation:

1. **Run Validation Script**
   Execute: `uv run .claude/scripts/validate_orchestration.py`
   
2. **Validation Checks to Perform**
   - JSON syntax validation for all config files
   - Agent reference validation (all agents exist)
   - Team structure validation:
     - Each team has a lead
     - No duplicate team names
     - Valid agent assignments
   - Workflow validation:
     - All referenced teams/agents exist
     - No circular dependencies
     - Valid trigger patterns
   - Settings validation:
     - Required fields present
     - Valid data types
     - Reasonable values

3. **If --fix flag provided**
   - Auto-fix common issues:
     - Remove references to non-existent agents
     - Fix JSON formatting issues
     - Add missing required fields with defaults
     - Sort configuration keys alphabetically
   - Show diff of changes before applying

4. **If --verbose flag provided**
   - Show detailed validation output
   - Include file-by-file analysis
   - Display validation rules being checked

5. **Error Reporting**
   - Group errors by severity (ERROR, WARNING, INFO)
   - Provide specific line numbers where possible
   - Suggest fixes for each issue

6. **Summary Report**
   Generate validation summary:
   - Total files validated
   - Errors found (by type)
   - Warnings found
   - Overall health score

## Expected Output

Structured validation report showing:
```
Configuration Validation Report
================================
✅ teams.json: Valid (3 teams configured)
⚠️  workflows.json: 2 warnings
❌ settings.json: 1 error

Errors (1):
- settings.json: Missing required field 'version'

Warnings (2):
- workflows.json: Agent 'old-agent' not found
- workflows.json: Workflow 'test' has no triggers

Overall Status: ⚠️ NEEDS ATTENTION
Run with --fix to auto-correct issues
```

## Constraints
- Don't modify files unless --fix is specified
- Always backup before auto-fixing
- Preserve comments and formatting where possible
- Exit with appropriate status code (0=success, 1=errors)