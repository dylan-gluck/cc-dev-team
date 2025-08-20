---
allowed-tools: Read, Edit, Write, Bash(jq:*), Bash(python:*), Task
description: Auto-fix common configuration issues
argument-hint: [--dry-run] [--interactive] [--category:all|syntax|references|structure]
model: sonnet
---

# Configuration Auto-Fix

Automatically detect and fix common configuration issues in the orchestration system.

## Context
- Configuration files: !`ls .claude/orchestration/*.json 2>/dev/null`
- Validation script: @.claude/scripts/validate_orchestration.py
- Arguments: $ARGUMENTS

## Task

Detect and fix configuration issues based on arguments:

### 1. Issue Detection
Run comprehensive checks for:

**Syntax Issues:**
- Invalid JSON syntax
- Missing commas, brackets, quotes
- Incorrect data types
- Trailing commas

**Reference Issues:**
- Non-existent agent references
- Missing team definitions
- Broken workflow assignments
- Orphaned configurations

**Structure Issues:**
- Missing required fields
- Incorrect nesting
- Invalid field names
- Schema violations

**Best Practice Issues:**
- Duplicate entries
- Unused configurations
- Inefficient patterns
- Security concerns

### 2. Fix Categories

If --category specified, focus on that category, otherwise fix all:

**Syntax Fixes:**
```python
- Parse and reformat JSON
- Fix quote inconsistencies  
- Remove trailing commas
- Correct bracket matching
```

**Reference Fixes:**
```python
- Remove references to deleted agents
- Update renamed agent references
- Link orphaned workflows to teams
- Clean up circular dependencies
```

**Structure Fixes:**
```python
- Add missing required fields with defaults
- Correct field naming conventions
- Fix nesting levels
- Align with schema requirements
```

### 3. Fix Process

If --dry-run:
- Show what would be fixed
- Display diffs for each file
- Report estimated impact
- No actual changes made

If --interactive:
- Present each fix for approval
- Show before/after comparison
- Allow skipping specific fixes
- Provide fix explanations

Default behavior:
- Create backup of all files
- Apply safe fixes automatically
- Log all changes made
- Generate fix report

### 4. Common Fixes to Apply

1. **Missing Version Field**
   - Add "version": "1.0.0" to settings.json

2. **Invalid Agent References**
   - Remove or comment out missing agents
   - Suggest alternatives if similar agents exist

3. **Empty Team Definitions**
   - Add default lead agent
   - Set minimal required fields

4. **Malformed Workflows**
   - Fix trigger pattern syntax
   - Ensure delegation field exists
   - Set default priority if missing

5. **Formatting Issues**
   - Standardize indentation (2 spaces)
   - Sort keys alphabetically
   - Remove duplicate entries

## Expected Output

Fix report showing:
```
Configuration Auto-Fix Report
==============================

🔍 Issues Found: 7
✅ Fixed: 5
⚠️  Manual Review: 2

Fixed Issues:
-------------
1. teams.json
   ✓ Added missing version field
   ✓ Removed reference to non-existent agent 'old-helper'

2. workflows.json
   ✓ Fixed JSON syntax error on line 45
   ✓ Added default priority to 3 workflows

3. settings.json
   ✓ Standardized indentation

Manual Review Required:
----------------------
1. teams.json: Circular dependency between team-a and team-b
   Suggestion: Review team hierarchy and remove one reference

2. workflows.json: Duplicate triggers in 'code-review' and 'pr-check'
   Suggestion: Merge workflows or differentiate triggers

Backup created: .claude/orchestration/.backup-20240120-103045/
```

If --dry-run:
```
DRY RUN - No changes made

Would fix:
----------
teams.json:
  - Line 15: Add missing comma
  - Line 23: Remove reference to 'missing-agent'
  
workflows.json:
  - Line 8: Fix unclosed bracket
  - Line 34-37: Reformat indentation

Run without --dry-run to apply fixes
```

## Constraints
- Always create backups before modifications
- Don't fix issues that require human decision
- Preserve comments where possible
- Maintain file permissions
- Log all operations for audit trail