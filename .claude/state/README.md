# Orchestration State Directory

This directory contains runtime state files for the orchestration system. These files are automatically managed by the orchestration framework and should not be edited manually.

## Contents

- `orchestration.json` - Current orchestration state (auto-generated)
- `orchestration.*.bak` - Backup files (auto-generated)
- Session state files (auto-generated)

## Important Notes

1. **DO NOT** manually edit files in this directory
2. **DO NOT** commit state files to version control (see .gitignore)
3. State files are automatically cleaned up after 30 days
4. Backups are retained for 7 days

## State Management

The orchestration system automatically:
- Creates state files when orchestration begins
- Updates state during operations
- Creates hourly backups
- Cleans up old state files

For configuration, see `.claude/orchestration/settings.json`