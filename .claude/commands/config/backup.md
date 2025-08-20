---
allowed-tools: Bash(cp:*), Bash(tar:*), Bash(ls:*), Bash(rm:*), Read, Write, Task
description: Backup and restore configuration states
argument-hint: [action:create|restore|list|clean] [backup-name]
model: sonnet
---

# Configuration Backup Management

Create, restore, and manage configuration backups for the orchestration system.

## Context
- Configuration directory: .claude/orchestration/
- Backup directory: .claude/orchestration/.backups/
- Current backups: !`ls -la .claude/orchestration/.backups/ 2>/dev/null | tail -n +2 | wc -l | xargs -I {} echo "{} backups found"`
- Arguments: $ARGUMENTS

## Task

Manage configuration backups based on the action specified:

### If "create" or no action:
1. **Create New Backup**
   - Generate timestamp: YYYYMMDD-HHMMSS
   - Create backup name: backup-[timestamp] or use provided name
   - Create backup directory: `.claude/orchestration/.backups/[backup-name]/`
   - Copy all JSON files from orchestration directory
   - Create manifest file with:
     - Backup timestamp
     - File checksums
     - Configuration versions
     - Reason/description (if provided)
   - Compress if over 1MB

2. **Backup Validation**
   - Verify all files copied successfully
   - Check file integrity
   - Record backup in history log

### If "restore" with backup-name:
1. **Pre-Restore Checks**
   - Verify backup exists
   - Check backup integrity
   - Create safety backup of current state
   - Show differences between current and backup

2. **Restore Process**
   - Confirm restore action
   - Copy files from backup to orchestration directory
   - Validate restored configurations
   - Update state files
   - Log restore operation

3. **Post-Restore**
   - Run validation on restored configs
   - Report any compatibility issues
   - Offer rollback if problems detected

### If "list":
1. **Display Available Backups**
   Show table with:
   - Backup name
   - Creation date/time
   - Size
   - Files included
   - Description/reason
   - Configuration version

2. **Backup Details**
   For each backup show:
   - Age (e.g., "2 days ago")
   - Restore compatibility
   - Notable differences from current

### If "clean":
1. **Cleanup Old Backups**
   - Keep last 10 backups by default
   - Keep all backups from last 7 days
   - Keep weekly backups for last month
   - Keep monthly backups for last year
   - Show what will be deleted
   - Confirm before deletion

### Additional Features:

1. **Backup Comparison**
   If two backup names provided:
   - Show diff between backups
   - Highlight configuration changes
   - Display migration path

2. **Auto-Backup Triggers**
   Create automatic backups before:
   - Major configuration changes
   - Version upgrades
   - Bulk modifications

3. **Backup Export/Import**
   - Export backup as tar.gz
   - Import external backup
   - Validate imported configurations

## Expected Output

For create:
```
Configuration Backup Created
============================
📦 Backup: backup-20240120-103045
📁 Location: .claude/orchestration/.backups/backup-20240120-103045/

Files Backed Up:
  ✅ teams.json (3.2 KB)
  ✅ workflows.json (5.1 KB)
  ✅ settings.json (1.5 KB)

Manifest:
  - Total Size: 9.8 KB
  - Files: 3
  - Version: 1.2.0
  - Checksum: a3f4b5c7...

✅ Backup completed successfully!
```

For list:
```
Available Configuration Backups
================================

Recent Backups:
  1. backup-20240120-103045 (2 hours ago)
     Size: 9.8 KB | Files: 3 | v1.2.0
     Description: Before workflow update

  2. backup-20240119-150230 (yesterday)
     Size: 9.5 KB | Files: 3 | v1.2.0
     Description: Daily backup

  3. backup-20240115-093012 (5 days ago)
     Size: 8.9 KB | Files: 3 | v1.1.0
     Description: Before version upgrade

Storage: 28.2 KB used (10 backups)
Retention: Keeping last 10 + weekly/monthly
```

For restore:
```
Configuration Restore
=====================
🔄 Restoring from: backup-20240119-150230

Changes to be applied:
  teams.json:
    - Team 'new-team' will be removed
    - Agent 'old-agent' will be restored
  
  workflows.json:
    - 2 workflows will be modified
    - 1 workflow will be removed

⚠️  Warning: This will overwrite current configuration

Proceed with restore? [y/N]

[After confirmation]
✅ Configuration restored successfully!
📋 Validation: All configurations valid
📦 Safety backup created: backup-pre-restore-20240120-104500
```

## Constraints
- Never overwrite backups
- Always validate before restore
- Maintain backup integrity
- Implement retention policy
- Create safety backups before restore
- Use atomic operations where possible