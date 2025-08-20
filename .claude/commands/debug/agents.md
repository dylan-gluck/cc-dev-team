---
allowed-tools: Read, Glob, Grep, Task, Bash(ps:*), LS
description: Debug agent status, configuration, and communication issues
argument-hint: [agent-name] [--validate] [--test]
model: sonnet
---

# Debug Agent Status

Comprehensive debugging for agent configuration, status, and inter-agent communication issues.

## Context
- Target agent: $ARGUMENTS
- Agent directory: @.claude/agents/
- Available agents: !`ls -la .claude/agents/*.md 2>/dev/null | wc -l`
- Agent config: @.claude/claude-config.json

## Task

1. **Agent Inventory**
   - List all configured agents with status
   - Check agent file permissions and ownership
   - Validate agent YAML frontmatter
   - Verify tool permissions and availability
   - Check for naming conflicts or duplicates

2. **Configuration Validation**
   - Validate each agent's YAML syntax
   - Check tool names against allowed tools
   - Verify delegation descriptions
   - Validate model specifications
   - Check for circular dependencies

3. **Communication Analysis**
   - Map agent interaction patterns
   - Check for broken delegation chains
   - Identify communication bottlenecks
   - Verify message routing
   - Analyze agent response times

4. **Health Checks**
   - Test agent invocation mechanisms
   - Verify agent can access required tools
   - Check for resource constraints
   - Validate output formatting
   - Test error handling

## Validation Mode (if --validate flag present)
- Deep validation of agent configurations
- Syntax checking for all agent files
- Tool permission verification
- Delegation chain validation
- Output format testing

## Test Mode (if --test flag present)
- Execute test invocations for each agent
- Measure response times
- Verify output correctness
- Test error scenarios
- Check resource usage

## Expected Output

1. **Agent Status Dashboard**
   ```
   Agent Registry Status
   =====================
   Total Agents: [count]
   Active: [count]
   Issues: [count]
   
   Agent Details:
   - [agent-name]: ✅ Healthy | ⚠️ Warning | ❌ Error
     Tools: [list]
     Model: [model]
     Last Modified: [date]
     Issues: [if any]
   ```

2. **Communication Map**
   - Visual representation of agent interactions
   - Delegation chains and dependencies
   - Communication patterns and frequencies
   - Bottlenecks and circular references

3. **Validation Results**
   - Syntax errors with line numbers
   - Tool permission issues
   - Missing dependencies
   - Configuration conflicts

4. **Performance Metrics**
   - Agent invocation times
   - Success/failure rates
   - Resource usage per agent
   - Queue depths and backlogs

5. **Remediation Steps**
   - Critical fixes for broken agents
   - Performance optimization suggestions
   - Configuration improvements
   - Best practice recommendations

## Constraints
- Never modify agent files without explicit confirmation
- Preserve agent file formatting and structure
- Highlight security concerns prominently
- Provide rollback instructions for changes