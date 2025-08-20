---
allowed-tools: Read, Task, Grep, Bash(curl:*), Bash(nc:*), Bash(ping:*)
description: Test integration between orchestration components
argument-hint: [component1] [component2] [--full-test]
model: sonnet
---

# Debug Integration

Test and validate integration between orchestration components, APIs, and external services.

## Context
- Components to test: $ARGUMENTS
- Config files: @.claude/claude-config.json
- Environment: !`env | grep -E "CLAUDE|API|PATH" | head -10`

## Task

1. **Component Discovery**
   - Identify all system components
   - Map component dependencies
   - Check component versions
   - Verify component availability
   - Test component connectivity

2. **Integration Testing**
   - Test agent-to-agent communication
   - Verify hook script execution
   - Check command invocation chains
   - Test tool integration
   - Validate API connections

3. **Contract Validation**
   - Verify API contracts between components
   - Check data format compatibility
   - Validate schema versions
   - Test backward compatibility
   - Check for breaking changes

4. **End-to-End Testing**
   - Execute complete workflows
   - Measure end-to-end latency
   - Verify data integrity through pipeline
   - Test error propagation
   - Check rollback mechanisms

## Full Test Mode (if --full-test flag present)
- Run comprehensive integration test suite
- Execute all workflow paths
- Stress test integrations
- Generate detailed test report

## Expected Output

1. **Integration Matrix**
   ```
   Component Integration Status
   ============================
   
   From/To    | Agent | Command | Hook | API |
   -----------+-------+---------+------+-----|
   Agent      |  ✅   |   ✅    |  ✅  | ✅  |
   Command    |  ✅   |   ✅    |  ⚠️  | ✅  |
   Hook       |  ✅   |   ❌    |  ✅  | ✅  |
   API        |  ✅   |   ✅    |  ✅  | ✅  |
   
   Legend: ✅ Working | ⚠️ Degraded | ❌ Failed
   ```

2. **Dependency Graph**
   - Visual component dependency map
   - Critical path identification
   - Circular dependency detection
   - Version compatibility matrix

3. **Test Results**
   ```
   Integration Test Suite
   ======================
   Tests Run: [count]
   Passed: [count]
   Failed: [count]
   Skipped: [count]
   
   Failed Tests:
   - [test-name]: [error-message]
     Component: [name]
     Expected: [value]
     Actual: [value]
   ```

4. **Performance Report**
   - Component response times
   - Integration latency measurements
   - Throughput statistics
   - Resource utilization

5. **Compatibility Issues**
   - Version mismatches
   - Schema incompatibilities
   - Missing dependencies
   - Configuration conflicts

6. **Remediation Plan**
   - Priority 1: Critical integration failures
   - Priority 2: Performance bottlenecks
   - Priority 3: Minor incompatibilities
   - Upgrade/migration paths

## Constraints
- Test in isolation to prevent side effects
- Use timeouts to prevent hanging tests
- Rollback any test data modifications
- Provide clear reproduction steps for failures