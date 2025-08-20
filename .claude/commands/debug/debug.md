---
allowed-tools: Read, Bash(ps:*), Bash(df:*), Bash(uptime:*), Bash(which:*), Glob, LS, Task
description: Debug tools overview and comprehensive system health check
model: sonnet
---

# Debug Tools Overview & System Health Check

Perform a comprehensive system health check and provide an overview of available debugging tools and current system status.

## Context Gathering
- System info: !`uname -a`
- Current time: !`date`
- Working directory: !`pwd`
- Memory usage: !`df -h 2>/dev/null || echo "df not available"`
- Process count: !`ps aux | wc -l`
- Claude config: @.claude/claude-config.json

## Task

1. **System Health Check**
   - Check available memory and disk space
   - Verify Claude Code configuration integrity
   - Check for agent configuration issues
   - Identify any file permission problems
   - Check for orphaned processes or resource leaks

2. **Configuration Validation**
   - Validate .claude directory structure
   - Check all agent definitions for syntax errors
   - Verify command configurations
   - Check hook scripts for issues
   - Validate environment settings

3. **Available Debug Commands**
   - List all /debug subcommands with descriptions
   - Highlight most relevant commands for current issues
   - Provide quick usage examples

4. **Quick Diagnostics**
   - Recent error patterns in logs
   - Performance bottlenecks
   - Integration issues between components
   - Common configuration problems

## Expected Output

Provide a structured report with:
1. **System Status Dashboard**
   - Overall health score (green/yellow/red)
   - Critical issues requiring immediate attention
   - Warnings about potential problems
   - System resource utilization

2. **Configuration Health**
   - Agent status summary
   - Command availability
   - Hook functionality
   - Environment compatibility

3. **Debug Command Reference**
   - Quick reference table of all /debug commands
   - Recommended commands based on current issues
   - Common troubleshooting workflows

4. **Actionable Recommendations**
   - Prioritized list of issues to address
   - Specific commands to run for deeper investigation
   - Performance optimization suggestions

## Constraints
- Use color coding for severity (🟢 OK, 🟡 Warning, 🔴 Critical)
- Keep initial report concise but comprehensive
- Provide clear next steps for any issues found
- Include timestamps for time-sensitive information