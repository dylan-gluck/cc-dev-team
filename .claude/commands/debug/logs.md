---
allowed-tools: Read, Grep, Bash(tail:*), Bash(head:*), Bash(find:*), Task
description: Show, filter, and analyze system logs
argument-hint: [filter] [--level=ERROR|WARN|INFO|DEBUG] [--tail=N]
model: haiku
---

# Debug Logs

Access, filter, and analyze system logs for troubleshooting and monitoring.

## Context
- Log filter: $ARGUMENTS
- Log locations: !`find ~/.claude -name "*.log" 2>/dev/null | head -10`
- Recent errors: !`grep -i "error\|fail\|exception" ~/.claude/logs/*.log 2>/dev/null | tail -5 || echo "No errors found"`

## Task

1. **Log Discovery**
   - Locate all log files in the system
   - Identify log formats and structures
   - Check log rotation status
   - Measure log file sizes
   - Verify write permissions

2. **Log Filtering**
   - Apply user-specified filters
   - Filter by severity level
   - Filter by timestamp range
   - Filter by component or module
   - Support regex patterns

3. **Error Analysis**
   - Extract and categorize errors
   - Identify error patterns
   - Count error frequencies
   - Trace error sources
   - Correlate related errors

4. **Log Visualization**
   - Format logs for readability
   - Highlight important entries
   - Group related messages
   - Show temporal patterns
   - Generate summary statistics

## Options Processing
- Parse --level flag for severity filtering
- Parse --tail flag for line limiting
- Support time range filtering
- Enable pattern matching
- Allow multiple filters

## Expected Output

1. **Log Summary**
   ```
   System Log Analysis
   ===================
   Time Range: [start] to [end]
   Total Entries: [count]
   
   Severity Breakdown:
   - ERROR:   [count] 🔴
   - WARNING: [count] 🟡
   - INFO:    [count] 🔵
   - DEBUG:   [count] ⚪
   ```

2. **Filtered Log Entries**
   ```
   [timestamp] [level] [component] message
   2024-01-15 10:23:45 ERROR agent-api Failed to connect: timeout
   2024-01-15 10:23:46 WARN  agent-api Retrying connection (1/3)
   2024-01-15 10:23:47 INFO  agent-api Connection restored
   ```

3. **Error Patterns**
   ```
   Top Error Patterns
   ==================
   1. Connection timeout (15 occurrences)
      - First: [timestamp]
      - Last: [timestamp]
      - Components: [list]
   
   2. File not found (8 occurrences)
      - Files: [list]
      - Requesting components: [list]
   ```

4. **Temporal Analysis**
   - Error frequency over time
   - Peak error periods
   - Correlation with events
   - Trending patterns

5. **Recommendations**
   - Log rotation needed for large files
   - Frequent errors requiring attention
   - Missing log coverage areas
   - Performance impact from verbose logging

## Constraints
- Limit output to prevent terminal overflow
- Use efficient filtering for large logs
- Preserve log file integrity (read-only)
- Handle compressed/rotated logs appropriately