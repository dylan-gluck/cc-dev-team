---
allowed-tools: Read, Grep, Task, Bash(tail:*), Bash(wc:*)
description: Debug message queue, routing, and delivery issues
argument-hint: [message-id] [--follow] [--stats]
model: sonnet
---

# Debug Message Queue & Routing

Analyze message queues, routing patterns, and delivery issues in the orchestration system.

## Context
- Message filter: $ARGUMENTS
- Queue status: !`ls -la /tmp/*queue* 2>/dev/null || echo "No queue files found"`
- Recent messages: !`tail -20 ~/.claude/logs/messages.log 2>/dev/null || echo "No message log"`

## Task

1. **Queue Analysis**
   - Identify all message queues in the system
   - Check queue depths and growth rates
   - Analyze message age and staleness
   - Detect stuck or poison messages
   - Monitor queue memory usage

2. **Routing Inspection**
   - Map message routing rules
   - Verify routing table integrity
   - Check for routing loops
   - Identify dead letter queues
   - Analyze routing performance

3. **Delivery Tracking**
   - Trace message delivery paths
   - Measure delivery latency
   - Identify failed deliveries
   - Check retry mechanisms
   - Analyze acknowledgment patterns

4. **Message Diagnostics**
   - Validate message formats
   - Check message size limits
   - Verify serialization/deserialization
   - Detect corruption or truncation
   - Analyze message patterns

## Follow Mode (if --follow flag present)
- Live tail of message activity
- Real-time routing decisions
- Delivery confirmations
- Error notifications

## Stats Mode (if --stats flag present)
- Message throughput metrics
- Queue performance statistics
- Routing efficiency analysis
- Delivery success rates

## Expected Output

1. **Queue Health Dashboard**
   ```
   Message Queue Status
   ====================
   Active Queues: [count]
   Total Messages: [count]
   Oldest Message: [age]
   
   Queue Details:
   - [queue-name]:
     Depth: [count]
     Rate: [msgs/sec]
     Avg Age: [seconds]
     Status: [healthy/degraded/critical]
   ```

2. **Routing Analysis**
   ```
   Route: [source] → [destination]
   Messages/Hour: [count]
   Avg Latency: [ms]
   Success Rate: [%]
   Failed: [count]
   ```

3. **Message Flow Diagram**
   - Visual representation of message paths
   - Queue interconnections
   - Bottleneck identification
   - Dead letter queue paths

4. **Performance Metrics**
   - Messages per second by type
   - Queue processing times
   - Routing decision latency
   - Delivery success rates
   - Retry statistics

5. **Issues & Alerts**
   - 🔴 Critical: Stuck messages blocking queue
   - 🟡 Warning: High queue depth
   - 🔵 Info: Routing optimization available
   - Recommended actions for each issue

## Constraints
- Protect message content privacy
- Limit memory usage when analyzing large queues
- Provide safe cleanup procedures for stuck messages
- Include recovery procedures for queue corruption