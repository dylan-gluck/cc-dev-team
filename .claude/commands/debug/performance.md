---
allowed-tools: Read, Task, Bash(time:*), Bash(top:*), Bash(ps:*), Bash(df:*), Grep
description: Performance profiling and bottleneck analysis
argument-hint: [component] [--profile] [--benchmark]
model: opus
---

# Debug Performance

Comprehensive performance profiling, bottleneck analysis, and optimization recommendations.

## Context
- Target component: $ARGUMENTS
- System resources: !`df -h / | tail -1`
- Process count: !`ps aux | wc -l`
- Load average: !`uptime`

## Task

1. **Performance Profiling**
   - Profile agent execution times
   - Measure command invocation overhead
   - Analyze tool usage patterns
   - Track resource consumption
   - Monitor memory allocation

2. **Bottleneck Detection**
   - Identify slow operations
   - Find resource contention points
   - Detect I/O bottlenecks
   - Analyze network latency
   - Check CPU utilization patterns

3. **Resource Analysis**
   - Memory usage by component
   - Disk I/O patterns
   - Network bandwidth usage
   - Process/thread counts
   - File handle usage

4. **Optimization Analysis**
   - Identify optimization opportunities
   - Suggest caching strategies
   - Recommend parallelization
   - Propose algorithm improvements
   - Suggest resource tuning

## Profile Mode (if --profile flag present)
- Enable detailed profiling
- Capture call stacks
- Record timing for all operations
- Generate flame graphs
- Track memory allocations

## Benchmark Mode (if --benchmark flag present)
- Run standardized benchmarks
- Compare with baseline metrics
- Stress test components
- Measure scalability limits
- Generate performance reports

## Expected Output

1. **Performance Dashboard**
   ```
   System Performance Overview
   ===========================
   
   Resource Utilization:
   - CPU Usage: [%] ████████░░ 80%
   - Memory: [GB/GB] ██████░░░░ 60%
   - Disk I/O: [MB/s] ███░░░░░░░ 30%
   - Network: [Mbps] ██░░░░░░░░ 20%
   
   Component Performance:
   - Agents: [avg response time]
   - Commands: [avg execution time]
   - Hooks: [avg processing time]
   - Tools: [avg latency]
   ```

2. **Bottleneck Analysis**
   ```
   Performance Bottlenecks
   ======================
   
   🔴 Critical Bottlenecks:
   1. Agent "research-ai" - 5.2s avg response
      - Cause: Network API calls
      - Impact: 40% of total latency
      - Fix: Implement caching layer
   
   🟡 Performance Warnings:
   1. File I/O operations - 500ms avg
      - Cause: Large file scanning
      - Impact: 15% of total time
      - Fix: Use indexed search
   ```

3. **Call Graph Analysis**
   ```
   Execution Timeline (most expensive path):
   
   main() ──2.1s──> agent_invoke() ──1.8s──> tool_exec()
                           │                      │
                        0.3s│                   0.5s│
                           ↓                      ↓
                    validate()              api_call()
   
   Total: 4.7s (target: <2s)
   ```

4. **Resource Trends**
   - Memory growth over time
   - CPU usage patterns
   - I/O operation frequency
   - Network request patterns
   - Cache hit/miss ratios

5. **Optimization Recommendations**
   ```
   Performance Optimization Plan
   =============================
   
   High Impact (>50% improvement):
   1. ✅ Cache frequent API responses
   2. ✅ Parallelize independent operations
   3. ✅ Batch database queries
   
   Medium Impact (20-50% improvement):
   1. ⚡ Optimize file search algorithms
   2. ⚡ Reduce serialization overhead
   3. ⚡ Implement lazy loading
   
   Low Impact (<20% improvement):
   1. 🔧 Tune garbage collection
   2. 🔧 Optimize regex patterns
   3. 🔧 Reduce log verbosity
   ```

6. **Benchmark Results** (if applicable)
   - Baseline vs current performance
   - Regression detection
   - Scalability metrics
   - Comparative analysis

## Constraints
- Minimize performance impact of profiling itself
- Use sampling for long-running operations
- Provide actionable optimization steps
- Include before/after estimates for optimizations