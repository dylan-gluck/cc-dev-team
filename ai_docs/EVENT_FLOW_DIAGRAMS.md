# Event Flow Diagrams & Communication Patterns

## Overview

This document provides visual representations of event flows and communication patterns across the Claude Code orchestration system. These diagrams help developers understand how events propagate through the system and how teams coordinate through event-driven architecture.

## High-Level System Architecture

```mermaid
graph TB
    subgraph "User Layer"
        U[User Commands]
        SC[Slash Commands]
    end
    
    subgraph "Orchestration Control Plane"
        EO[Engineering Orchestrator]
        PD[Product Director]
        QD[QA Director]
        DO[DevOps Manager]
        CD[Creative Director]
    end
    
    subgraph "Agent Execution Layer"
        EL[Engineering Lead]
        EF[Engineering Fullstack]
        EU[Engineering UX]
        QE[QA E2E]
        DI[DevOps Infrastructure]
        CC[Creative Copywriter]
    end
    
    subgraph "Communication Infrastructure"
        MB[Message Bus]
        ES[Event Stream]
        SM[State Manager]
    end
    
    subgraph "Observability Platform"
        M[Metrics Collector]
        D[Dashboard]
        A[Alerts]
    end
    
    U --> SC
    SC --> EO
    SC --> PD
    
    EO --> EL
    EO --> EF
    EO --> EU
    
    PD --> EO
    QD --> QE
    DO --> DI
    CD --> CC
    
    EL --> MB
    EF --> MB
    EU --> MB
    QE --> MB
    
    MB --> ES
    MB --> SM
    ES --> M
    SM --> M
    M --> D
    M --> A
    
    style U fill:#e1f5fe
    style EO fill:#fff3e0
    style MB fill:#f3e5f5
    style M fill:#e8f5e8
```

## Core Event Flow Patterns

### 1. Sprint Orchestration Flow

```mermaid
sequenceDiagram
    participant U as User
    participant EO as Engineering Orchestrator
    participant SM as State Manager
    participant ES as Event Stream
    participant EL as Engineering Lead
    participant EF as Engineering Fullstack
    participant QD as QA Director
    participant QE as QA E2E

    Note over U,QE: Sprint Start Sequence
    
    U->>EO: /orchestrate sprint start
    EO->>SM: Read sprint definition
    SM-->>EO: Sprint tasks & config
    
    EO->>ES: emit(sprint:started)
    EO->>SM: Update sprint status
    
    Note over EO,QE: Task Delegation Phase
    
    EO->>EL: spawn with planning tasks
    EL->>ES: emit(task:started, type=planning)
    EL->>ES: emit(task:completed, artifacts=specs)
    
    EO->>EF: spawn with implementation
    EF->>ES: emit(task:started, type=implementation)
    
    Note over EF,QE: Implementation & Testing
    
    loop Task Execution
        EF->>EF: Implementation work
        EF->>ES: emit(progress:update)
    end
    
    EF->>ES: emit(task:completed, artifacts=code)
    EO->>QD: emit(artifact:ready, type=testing)
    
    QD->>QE: spawn with testing tasks
    QE->>ES: emit(task:started, type=testing)
    QE->>ES: emit(task:completed, results=passed)
    
    Note over EO,QE: Sprint Completion
    
    EO->>ES: emit(sprint:completed)
    EO->>SM: Update final metrics
```

### 2. Cross-Team Communication Pattern

```mermaid
sequenceDiagram
    participant EF as Engineering Fullstack
    participant MB as Message Bus
    participant EL as Engineering Lead
    participant PM as Product Manager
    participant SM as State Manager
    participant ES as Event Stream

    Note over EF,ES: Question/Answer Flow
    
    EF->>MB: send(question:asked, to=engineering-lead)
    MB->>EL: deliver question
    EL->>MB: send(question:answered)
    MB->>EF: deliver answer
    
    EF->>SM: update task context
    SM->>ES: emit(state:updated)
    
    Note over EF,ES: Cross-Team Escalation
    
    EF->>MB: send(question:asked, to=product-manager)
    MB->>PM: deliver question (escalated)
    PM->>MB: send(question:answered, priority=high)
    MB->>EF: deliver priority answer
    
    PM->>ES: emit(requirement:clarified)
    ES->>SM: update requirements state
```

### 3. Error Handling & Recovery Flow

```mermaid
sequenceDiagram
    participant EF as Engineering Fullstack
    participant EO as Engineering Orchestrator
    participant EL as Engineering Lead
    participant ES as Event Stream
    participant SM as State Manager
    participant RM as Resource Manager

    Note over EF,RM: Task Failure Scenario
    
    EF->>ES: emit(task:failed, error=dependency_conflict)
    ES->>EO: notify task failure
    ES->>SM: update task status
    
    EO->>EL: escalate(task:failed, requires_intervention)
    EL->>ES: emit(intervention:started)
    
    Note over EL,RM: Recovery Process
    
    EL->>SM: analyze failure context
    SM-->>EL: failure history & patterns
    
    EL->>RM: request(resource:reallocation)
    RM-->>EL: approve reallocation
    
    EL->>EO: emit(recovery:plan_ready)
    EO->>EF: spawn with recovery context
    
    EF->>ES: emit(task:resumed)
    EF->>ES: emit(task:completed)
    
    Note over EO,RM: Post-Recovery
    
    EO->>ES: emit(recovery:completed)
    ES->>SM: update recovery metrics
```

### 4. Review & Approval Workflow

```mermaid
sequenceDiagram
    participant EF as Engineering Fullstack
    participant EL as Engineering Lead
    participant QE as QA E2E
    participant PM as Product Manager
    participant ES as Event Stream
    participant SM as State Manager

    Note over EF,SM: Code Review Process
    
    EF->>ES: emit(task:completed, review_required=true)
    ES->>EL: notify completion
    
    EL->>ES: emit(review:requested, type=code_review)
    EL->>EL: Perform code review
    
    alt Review Approved
        EL->>ES: emit(review:approved)
        ES->>QE: notify for testing
        QE->>ES: emit(testing:started)
    else Review Rejected
        EL->>ES: emit(review:rejected, feedback=changes_needed)
        ES->>EF: notify changes required
        EF->>ES: emit(task:updated)
    end
    
    Note over QE,SM: QA Testing Phase
    
    QE->>ES: emit(testing:completed, result=passed)
    ES->>PM: notify for final approval
    
    PM->>ES: emit(approval:granted)
    ES->>SM: update task to approved
    SM->>ES: emit(state:updated, path=task.status)
```

## Team-Specific Event Patterns

### Engineering Team Internal Flow

```mermaid
graph TD
    EO[Engineering Orchestrator] -->|task:assigned| EL[Engineering Lead]
    EO -->|task:assigned| EF[Engineering Fullstack]
    EO -->|task:assigned| EU[Engineering UX]
    EO -->|task:assigned| EA[Engineering API]
    
    EL -->|review:requested| EF
    EL -->|review:requested| EU
    EL -->|review:requested| EA
    
    EF -->|question:asked| EL
    EU -->|question:asked| EL
    EA -->|question:asked| EL
    
    EF -->|artifact:ready| EU
    EA -->|artifact:ready| EF
    EU -->|artifact:ready| EF
    
    EL -->|task:completed| EO
    EF -->|task:completed| EO
    EU -->|task:completed| EO
    EA -->|task:completed| EO
    
    style EO fill:#ff9800
    style EL fill:#2196f3
    style EF fill:#4caf50
    style EU fill:#9c27b0
    style EA fill:#f44336
```

### Product Team Event Flow

```mermaid
graph TD
    PD[Product Director] -->|epic:created| PM[Product Manager]
    PD -->|epic:created| PA[Product Analyst]
    
    PM -->|requirements:defined| EO[Engineering Orchestrator]
    PA -->|analysis:completed| PM
    
    PM -->|acceptance:criteria| QD[QA Director]
    PM -->|feature:approved| EO
    
    EO -->|implementation:completed| PM
    QD -->|testing:completed| PM
    
    PM -->|release:approved| DO[DevOps Manager]
    
    style PD fill:#673ab7
    style PM fill:#3f51b5
    style PA fill:#009688
    style EO fill:#ff9800
    style QD fill:#795548
    style DO fill:#607d8b
```

### QA Team Testing Pipeline

```mermaid
graph TD
    QD[QA Director] -->|testing:assigned| QE[QA E2E]
    QD -->|testing:assigned| QS[QA Scripts]
    QD -->|testing:assigned| QA[QA Analyst]
    
    QE -->|tests:running| QD
    QS -->|automation:running| QD
    
    QE -->|test:failed| EO[Engineering Orchestrator]
    QE -->|test:passed| QA
    
    QS -->|script:completed| QA
    QA -->|report:generated| QD
    
    QD -->|quality:approved| PM[Product Manager]
    QD -->|quality:rejected| EO
    
    style QD fill:#795548
    style QE fill:#8bc34a
    style QS fill:#cddc39
    style QA fill:#ffeb3b
    style EO fill:#ff9800
    style PM fill:#3f51b5
```

## Event Priority & Routing Patterns

### Priority-Based Event Routing

```mermaid
graph TB
    subgraph "Event Sources"
        A1[Agent 1]
        A2[Agent 2]
        A3[Agent 3]
    end
    
    subgraph "Message Bus"
        PQ[Priority Queue]
        subgraph "Priority Levels"
            C[Critical Queue]
            H[High Queue]
            N[Normal Queue]
            L[Low Queue]
        end
    end
    
    subgraph "Event Processors"
        P1[Processor 1]
        P2[Processor 2]
        P3[Processor 3]
    end
    
    A1 -->|critical events| C
    A2 -->|high events| H
    A3 -->|normal events| N
    A1 -->|low events| L
    
    C --> P1
    H --> P1
    N --> P2
    L --> P3
    
    style C fill:#f44336
    style H fill:#ff9800
    style N fill:#4caf50
    style L fill:#9e9e9e
```

### Event Filtering & Subscription

```mermaid
graph TD
    subgraph "Event Stream"
        ES[Raw Event Stream]
        EF[Event Filter]
    end
    
    subgraph "Subscription Patterns"
        TS[Team Subscriptions]
        AS[Agent Subscriptions]
        CS[Category Subscriptions]
    end
    
    subgraph "Filtered Streams"
        ETS[Engineering Team Stream]
        PTS[Product Team Stream]
        QTS[QA Team Stream]
        SYS[System Events Stream]
    end
    
    ES --> EF
    
    EF -->|team=engineering| ETS
    EF -->|team=product| PTS
    EF -->|team=qa| QTS
    EF -->|category=system| SYS
    
    ETS --> TS
    PTS --> TS
    QTS --> TS
    SYS --> AS
    
    style ES fill:#2196f3
    style EF fill:#ff9800
    style ETS fill:#4caf50
    style PTS fill:#9c27b0
    style QTS fill:#795548
    style SYS fill:#607d8b
```

## State Management Event Flows

### State Synchronization Pattern

```mermaid
sequenceDiagram
    participant A as Agent
    participant SM as State Manager
    participant ES as Event Stream
    participant OA as Other Agents
    participant OB as Observability

    Note over A,OB: State Update Flow
    
    A->>SM: update_state(path, value)
    SM->>SM: Validate & apply change
    SM->>ES: emit(state:updated)
    
    ES->>OA: notify state change
    ES->>OB: log state change
    
    Note over A,OB: Conflict Resolution
    
    A->>SM: update_state(conflicting_path)
    SM->>SM: Detect conflict
    SM->>ES: emit(state:conflict_detected)
    
    ES->>A: notify conflict
    A->>SM: resolve_conflict(strategy)
    SM->>ES: emit(state:conflict_resolved)
```

### Distributed State Consistency

```mermaid
graph TD
    subgraph "State Sources"
        SA[State Agent A]
        SB[State Agent B]
        SC[State Agent C]
    end
    
    subgraph "State Management"
        SM[State Manager]
        SV[State Validator]
        SR[State Resolver]
    end
    
    subgraph "Consistency Mechanisms"
        VV[Vector Clocks]
        CL[Conflict Log]
        MR[Merge Resolution]
    end
    
    SA -->|state_update| SM
    SB -->|state_update| SM
    SC -->|state_update| SM
    
    SM --> SV
    SV --> VV
    SV -->|conflicts| CL
    
    CL --> SR
    SR --> MR
    MR --> SM
    
    style SM fill:#2196f3
    style SV fill:#ff9800
    style SR fill:#4caf50
    style VV fill:#9c27b0
```

## Error Handling Event Patterns

### Circuit Breaker Pattern for Events

```mermaid
stateDiagram-v2
    [*] --> Closed
    Closed --> Open: failures >= threshold
    Open --> HalfOpen: timeout elapsed
    HalfOpen --> Closed: success
    HalfOpen --> Open: failure
    
    state Closed {
        [*] --> ProcessingEvents
        ProcessingEvents --> RecordingFailures: event failure
        RecordingFailures --> ProcessingEvents: continue
    }
    
    state Open {
        [*] --> RejectingEvents
        RejectingEvents --> WaitingTimeout: timeout active
        WaitingTimeout --> RejectingEvents: still waiting
    }
    
    state HalfOpen {
        [*] --> TestingEvents
        TestingEvents --> EvaluatingResult: event processed
        EvaluatingResult --> TestingEvents: need more tests
    }
```

### Event Retry and Recovery

```mermaid
sequenceDiagram
    participant P as Producer
    participant MB as Message Bus
    participant C as Consumer
    participant DLQ as Dead Letter Queue
    participant RM as Recovery Manager

    Note over P,RM: Normal Processing
    
    P->>MB: send event
    MB->>C: deliver event
    C-->>MB: ack success
    
    Note over P,RM: Failure & Retry
    
    P->>MB: send event
    MB->>C: deliver event
    C--xMB: processing failed
    
    MB->>MB: increment retry count
    MB->>C: retry delivery (backoff)
    C--xMB: still failing
    
    MB->>DLQ: move to dead letter queue
    DLQ->>RM: notify recovery needed
    
    Note over P,RM: Manual Recovery
    
    RM->>DLQ: analyze failed events
    RM->>MB: replay events (fixed)
    MB->>C: redeliver events
    C-->>MB: ack success
```

## Performance Monitoring Event Flows

### Real-time Metrics Collection

```mermaid
graph TD
    subgraph "Event Sources"
        T1[Task Events]
        A1[Agent Events]
        S1[System Events]
    end
    
    subgraph "Metrics Pipeline"
        MC[Metrics Collector]
        MA[Metrics Aggregator]
        MS[Metrics Store]
    end
    
    subgraph "Monitoring Outputs"
        RT[Real-time Dashboard]
        AL[Alerts]
        RP[Reports]
    end
    
    T1 --> MC
    A1 --> MC
    S1 --> MC
    
    MC --> MA
    MA --> MS
    
    MS --> RT
    MS --> AL
    MS --> RP
    
    AL -->|critical| RT
    
    style MC fill:#2196f3
    style MA fill:#ff9800
    style MS fill:#4caf50
    style RT fill:#f44336
    style AL fill:#ff5722
```

## Event Debugging & Tracing

### Distributed Event Tracing

```mermaid
sequenceDiagram
    participant U as User Action
    participant EO as Engineering Orchestrator
    participant EF as Engineering Fullstack
    participant QE as QA E2E
    participant T as Trace Collector

    Note over U,T: Request Tracing
    
    U->>EO: /orchestrate task delegate (trace_id: abc123)
    EO->>T: trace_event(abc123, orchestrator_start)
    
    EO->>EF: spawn agent (trace_id: abc123)
    EF->>T: trace_event(abc123, agent_spawned)
    
    EF->>EF: process task (trace_id: abc123)
    EF->>T: trace_event(abc123, task_processing)
    
    EF->>QE: handoff artifact (trace_id: abc123)
    QE->>T: trace_event(abc123, artifact_received)
    
    QE->>T: trace_event(abc123, testing_completed)
    
    Note over U,T: Trace Analysis
    
    T->>T: correlate events by trace_id
    T->>U: display complete trace timeline
```

---

This comprehensive set of event flow diagrams provides visual guidance for understanding how events propagate through the Claude Code orchestration system. These patterns can be used as references for implementing event-driven features and debugging communication issues between agents and teams.

**Last Updated**: 2025-01-20  
**Diagram Count**: 15  
**Coverage**: All major event patterns and flows