---
allowed-tools: Read, Grep, Glob, Task, Bash(find:*), Bash(stat:*)
description: Debug state management issues and data inconsistencies
argument-hint: [component] [--deep]
model: sonnet
---

# Debug State Management

Analyze and debug state management issues, data inconsistencies, and synchronization problems across the orchestration system.

## Context
- Target component: $ARGUMENTS
- Configuration files: !`find .claude -name "*.json" -o -name "*.yaml" 2>/dev/null | head -20`
- State files: !`find . -name "*.state" -o -name "*.cache" -o -name "*.lock" 2>/dev/null | head -20`

## Task

1. **State Inventory**
   - Identify all state storage locations (.state, .cache, .lock files)
   - Check for temporary state in /tmp or system temp directories
   - Analyze in-memory state indicators
   - Map state dependencies between components

2. **Consistency Analysis**
   - Check for state version mismatches
   - Identify stale or corrupted state files
   - Verify state serialization/deserialization
   - Detect race conditions in state updates
   - Check for orphaned state data

3. **Synchronization Issues**
   - Analyze lock file usage and conflicts
   - Check for concurrent access patterns
   - Verify transaction boundaries
   - Identify potential deadlocks

4. **State Recovery**
   - Provide state repair strategies
   - Suggest safe cleanup procedures
   - Recommend backup approaches
   - Document rollback procedures

## Deep Analysis Mode (if --deep flag present)
- Perform byte-level state file analysis
- Check state history and evolution
- Analyze state access patterns
- Generate state flow diagrams

## Expected Output

1. **State Health Report**
   ```
   Component State Analysis
   ========================
   Component: [name]
   State Files: [count]
   Last Modified: [timestamp]
   Size: [bytes]
   Status: [healthy/corrupted/stale]
   ```

2. **Inconsistency Detection**
   - List of mismatched states
   - Orphaned state files
   - Lock conflicts
   - Version discrepancies

3. **Recommended Actions**
   - Critical fixes (data loss risk)
   - Performance improvements
   - Cleanup operations
   - Migration strategies

4. **State Diagram** (if applicable)
   - Visual representation of state flow
   - Dependency relationships
   - Synchronization points

## Constraints
- Never modify state files directly without user confirmation
- Always suggest backups before state operations
- Highlight any data loss risks prominently
- Provide rollback instructions for all modifications