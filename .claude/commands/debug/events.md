---
allowed-tools: Read, Grep, Task, Bash(tail:*), Bash(grep:*)
description: Debug event flows, subscriptions, and message patterns
argument-hint: [event-type] [--trace] [--live]
model: sonnet
---

# Debug Event Flows

Analyze event flows, subscription patterns, and message routing throughout the orchestration system.

## Context
- Event filter: $ARGUMENTS
- Recent logs: !`tail -50 ~/.claude/logs/*.log 2>/dev/null || echo "No logs found"`
- Hook scripts: @.claude/hooks/

## Task

1. **Event Discovery**
   - Map all event types in the system
   - Identify event sources and sinks
   - Document event payload structures
   - Trace event propagation paths

2. **Subscription Analysis**
   - List all active event subscriptions
   - Check for duplicate subscriptions
   - Identify missing subscriptions
   - Analyze subscription filters

3. **Event Flow Tracing**
   - Trace specific event from source to destination
   - Measure event latency at each hop
   - Identify bottlenecks in event processing
   - Detect dropped or lost events

4. **Pattern Analysis**
   - Identify event storms or floods
   - Detect circular event dependencies
   - Find dead letter queues
   - Analyze retry patterns

## Trace Mode (if --trace flag present)
- Enable detailed event tracing
- Capture full event payloads
- Log all transformations
- Record timing information

## Live Mode (if --live flag present)
- Monitor events in real-time
- Display event stream with filtering
- Show event rates and throughput
- Highlight anomalies as they occur

## Expected Output

1. **Event Flow Map**
   ```
   Event: [type]
   Source → Handler₁ → Handler₂ → Sink
           ↓
         Handler₃ → Sink₂
   
   Latency: [ms per hop]
   Success Rate: [%]
   ```

2. **Subscription Health**
   - Active subscriptions with status
   - Subscription error rates
   - Queue depths and backlogs
   - Handler performance metrics

3. **Event Metrics**
   - Events per second by type
   - Average processing time
   - Error rates and retry counts
   - Queue utilization

4. **Issues & Recommendations**
   - Critical: Event loops detected
   - Warning: High latency paths
   - Info: Optimization opportunities
   - Debug: Detailed trace logs

## Constraints
- Minimize performance impact during live monitoring
- Protect sensitive data in event payloads
- Limit trace data volume to prevent overflow
- Provide clear visualization of complex flows