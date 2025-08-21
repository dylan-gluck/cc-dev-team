# V2 Orchestration: Inter-Session Communication API

## Overview

The V2 orchestration system requires robust inter-session communication to enable seamless collaboration across multiple Claude sessions, terminals, and agent instances. This document defines the API specifications, communication patterns, and implementation strategies for achieving reliable, secure, and performant inter-session coordination.

## 1. Communication Patterns

### 1.1 Why Inter-Session Communication is Needed

**Multi-Terminal Workflows**
- Developer working across multiple terminal sessions
- Different agents running in parallel sessions
- Handoff scenarios between sessions
- Real-time coordination of long-running tasks

**State Synchronization Requirements**
- Shared project state across sessions
- Task queue coordination
- Resource locking and conflict resolution
- Progress tracking and status updates

**Team Coordination Scenarios**
- Multiple developers on same project
- Agent-to-agent communication across sessions
- Emergency broadcasting (stop all tasks, urgent updates)
- Workflow orchestration spanning multiple sessions

### 1.2 Indirect Communication via Shared State

**State Store Architecture**
```
┌─────────────┐    ┌─────────────────┐    ┌─────────────┐
│   Session A │ ──▶│  Shared State   │◀── │   Session B │
│             │    │     Store       │    │             │
│  Agent 1    │    │                 │    │  Agent 2    │
│  Agent 2    │    │ - Task Queue    │    │  Agent 3    │
└─────────────┘    │ - Project State │    └─────────────┘
                   │ - Message Bus   │
                   │ - Lock Registry │
                   └─────────────────┘
```

**State Update Patterns**
- Atomic writes with version control
- Event-driven state changes
- Optimistic locking with conflict resolution
- State snapshots for rollback scenarios

### 1.3 Message Queue Patterns

**Producer-Consumer Model**
```typescript
interface MessageQueue {
  publish(topic: string, message: Message): Promise<void>;
  subscribe(topic: string, handler: MessageHandler): Promise<void>;
  unsubscribe(topic: string, handler: MessageHandler): Promise<void>;
}

interface Message {
  id: string;
  timestamp: number;
  sessionId: string;
  agentId?: string;
  type: MessageType;
  payload: any;
  ttl?: number;
}

enum MessageType {
  TASK_CREATED = 'task_created',
  TASK_COMPLETED = 'task_completed',
  STATE_UPDATED = 'state_updated',
  EMERGENCY_STOP = 'emergency_stop',
  AGENT_HEARTBEAT = 'agent_heartbeat',
  HANDOFF_REQUEST = 'handoff_request'
}
```

**Topic Structure**
```
project.{project_id}.tasks.{task_type}
project.{project_id}.agents.{agent_id}
global.emergency
global.heartbeat
session.{session_id}.status
```

### 1.4 Event Broadcasting

**Event Types and Handlers**
```typescript
interface EventBroadcaster {
  broadcast(event: BroadcastEvent): Promise<void>;
  listen(eventType: string, handler: EventHandler): Promise<void>;
  stopListening(eventType: string, handler: EventHandler): Promise<void>;
}

interface BroadcastEvent {
  type: string;
  source: SessionInfo;
  target?: string; // specific session/agent or 'all'
  data: any;
  priority: 'low' | 'normal' | 'high' | 'critical';
}
```

## 2. API Design

### 2.1 RESTful Endpoints for State Queries

**Base URL Structure**
```
http://localhost:8765/api/v2/orchestration
```

**State Management Endpoints**

```http
# Get project state
GET /projects/{project_id}/state
Response: {
  "project_id": "string",
  "version": "number",
  "last_updated": "timestamp",
  "state": {
    "tasks": [],
    "agents": [],
    "resources": {}
  }
}

# Update project state
PATCH /projects/{project_id}/state
Request: {
  "version": "number", // for optimistic locking
  "updates": {
    "path": "string",
    "operation": "set|append|remove",
    "value": "any"
  }[]
}

# Get task queue
GET /projects/{project_id}/tasks
Query Parameters:
  - status: pending|running|completed|failed
  - agent_id: string
  - limit: number
  - offset: number

# Create new task
POST /projects/{project_id}/tasks
Request: {
  "type": "string",
  "priority": "low|normal|high|critical",
  "agent_requirements": [],
  "dependencies": [],
  "payload": {},
  "timeout": "duration"
}

# Update task status
PATCH /projects/{project_id}/tasks/{task_id}
Request: {
  "status": "string",
  "progress": "number",
  "result": "any",
  "error": "string"
}
```

**Session Management Endpoints**

```http
# Register session
POST /sessions
Request: {
  "session_id": "string",
  "user_id": "string",
  "project_id": "string",
  "capabilities": [],
  "metadata": {}
}

# Get active sessions
GET /sessions
Query Parameters:
  - project_id: string
  - status: active|idle|disconnected

# Session heartbeat
POST /sessions/{session_id}/heartbeat
Request: {
  "status": "active|idle",
  "active_agents": [],
  "resource_usage": {}
}

# Request session handoff
POST /sessions/{session_id}/handoff
Request: {
  "target_session": "string",
  "context": {},
  "tasks": [],
  "message": "string"
}
```

**Agent Coordination Endpoints**

```http
# Register agent
POST /agents
Request: {
  "agent_id": "string",
  "session_id": "string",
  "type": "string",
  "capabilities": [],
  "status": "starting|ready|busy|error"
}

# Get agent status
GET /agents/{agent_id}

# Request agent lock
POST /agents/{agent_id}/lock
Request: {
  "resource": "string",
  "timeout": "duration",
  "reason": "string"
}

# Release agent lock
DELETE /agents/{agent_id}/locks/{lock_id}
```

### 2.2 WebSocket for Real-time Updates

**Connection Management**
```typescript
interface WebSocketConnection {
  url: 'ws://localhost:8765/api/v2/orchestration/ws';
  protocols: ['orchestration-v2'];
  
  // Authentication via query params or headers
  auth: {
    session_id: string;
    token: string;
  };
}

// WebSocket message format
interface WSMessage {
  id: string;
  type: WSMessageType;
  timestamp: number;
  data: any;
}

enum WSMessageType {
  // Subscription management
  SUBSCRIBE = 'subscribe',
  UNSUBSCRIBE = 'unsubscribe',
  
  // Real-time events
  TASK_UPDATE = 'task_update',
  STATE_CHANGE = 'state_change',
  AGENT_STATUS = 'agent_status',
  EMERGENCY_BROADCAST = 'emergency_broadcast',
  
  // Coordination
  HANDOFF_REQUEST = 'handoff_request',
  RESOURCE_CONFLICT = 'resource_conflict',
  
  // System
  HEARTBEAT = 'heartbeat',
  ERROR = 'error'
}
```

**Subscription Patterns**
```typescript
// Subscribe to project events
{
  "type": "subscribe",
  "data": {
    "topic": "project.myapp.tasks.*",
    "filters": {
      "agent_type": ["engineering-api", "engineering-fullstack"],
      "priority": ["high", "critical"]
    }
  }
}

// Subscribe to emergency broadcasts
{
  "type": "subscribe",
  "data": {
    "topic": "global.emergency",
    "priority": "critical"
  }
}
```

### 2.3 File-based Message Passing

**Directory Structure**
```
~/.claude/orchestration/
├── projects/
│   └── {project_id}/
│       ├── state.json
│       ├── tasks/
│       │   ├── pending/
│       │   ├── running/
│       │   └── completed/
│       └── messages/
│           ├── inbox/
│           ├── outbox/
│           └── archive/
├── sessions/
│   └── {session_id}/
│       ├── status.json
│       ├── heartbeat.json
│       └── handoff/
└── global/
    ├── emergency.json
    └── broadcasts/
```

**File Message Format**
```typescript
interface FileMessage {
  id: string;
  timestamp: number;
  from: {
    session_id: string;
    agent_id?: string;
  };
  to: {
    session_id?: string;
    agent_id?: string;
    broadcast?: boolean;
  };
  type: string;
  payload: any;
  ttl: number;
  processed: boolean;
}
```

**File Watching API**
```typescript
interface FileWatcher {
  watchDirectory(path: string, callback: FileChangeCallback): Promise<void>;
  unwatchDirectory(path: string): Promise<void>;
}

interface FileChangeCallback {
  (event: 'create' | 'modify' | 'delete', filename: string): void;
}
```

### 2.4 Shared Memory Approaches

**Memory-mapped File Structure**
```typescript
interface SharedMemoryRegion {
  // Header (fixed size)
  version: number;
  last_updated: number;
  writer_session: string;
  lock_count: number;
  
  // Dynamic sections
  project_state: ProjectState;
  task_queue: Task[];
  agent_registry: AgentInfo[];
  message_buffer: CircularBuffer<Message>;
}

interface MemoryLock {
  acquire(section: string, timeout?: number): Promise<boolean>;
  release(section: string): Promise<void>;
  isLocked(section: string): boolean;
}
```

## 3. Security Model

### 3.1 Session Authentication

**Token-based Authentication**
```typescript
interface SessionToken {
  session_id: string;
  user_id: string;
  project_id: string;
  issued_at: number;
  expires_at: number;
  permissions: Permission[];
  signature: string;
}

interface Permission {
  resource: string; // project.*, task.*, agent.*
  actions: string[]; // read, write, execute, admin
  conditions?: {
    time_range?: [number, number];
    ip_whitelist?: string[];
    agent_types?: string[];
  };
}
```

**Authentication Flow**
```typescript
// 1. Session registration
const token = await registerSession({
  user_id: getUserId(),
  project_id: getProjectId(),
  capabilities: getSessionCapabilities()
});

// 2. Token validation on each request
const isValid = await validateToken(token, {
  resource: 'project.myapp.tasks',
  action: 'write'
});

// 3. Token refresh
const newToken = await refreshToken(token);
```

### 3.2 Permission Boundaries

**Resource-based Access Control**
```typescript
enum ResourceType {
  PROJECT_STATE = 'project.state',
  TASK_QUEUE = 'project.tasks',
  AGENT_REGISTRY = 'project.agents',
  MESSAGE_BUS = 'project.messages',
  GLOBAL_EMERGENCY = 'global.emergency',
  SESSION_DATA = 'session.data'
}

interface AccessPolicy {
  resource: ResourceType;
  principal: {
    type: 'session' | 'agent' | 'user';
    id: string;
  };
  permissions: {
    read: boolean;
    write: boolean;
    admin: boolean;
  };
  conditions?: AccessCondition[];
}
```

**Permission Enforcement**
```typescript
class PermissionEnforcer {
  async checkAccess(
    token: SessionToken,
    resource: string,
    action: string
  ): Promise<boolean> {
    // 1. Validate token signature and expiry
    // 2. Extract permissions for resource
    // 3. Check action against permissions
    // 4. Evaluate any conditions
    // 5. Log access attempt
  }
  
  async enforceQuota(
    session_id: string,
    resource: string,
    operation: string
  ): Promise<boolean> {
    // Rate limiting and resource quotas
  }
}
```

### 3.3 Data Isolation Guarantees

**Project Isolation**
```typescript
interface ProjectBoundary {
  project_id: string;
  authorized_sessions: string[];
  data_encryption_key: string;
  access_logs: AccessLog[];
}

// Ensure sessions can only access authorized projects
function validateProjectAccess(
  session_id: string,
  project_id: string
): boolean {
  const boundary = getProjectBoundary(project_id);
  return boundary.authorized_sessions.includes(session_id);
}
```

**Data Encryption**
```typescript
interface EncryptionProvider {
  encrypt(data: any, project_id: string): Promise<string>;
  decrypt(encrypted: string, project_id: string): Promise<any>;
  rotateKey(project_id: string): Promise<void>;
}

// Encrypt sensitive state data
const encryptedState = await encryption.encrypt(
  projectState,
  project_id
);
```

## 4. Implementation Options

### 4.1 Option 1: File-based Message Queue

**Architecture**
```typescript
class FileBasedMessageQueue implements MessageQueue {
  private watchedDirs: Map<string, FileWatcher> = new Map();
  private messageHandlers: Map<string, MessageHandler[]> = new Map();
  
  async publish(topic: string, message: Message): Promise<void> {
    const filename = `${message.id}-${Date.now()}.json`;
    const filepath = this.getTopicPath(topic, 'outbox', filename);
    await fs.writeFile(filepath, JSON.stringify(message));
  }
  
  async subscribe(topic: string, handler: MessageHandler): Promise<void> {
    const topicPath = this.getTopicPath(topic, 'inbox');
    
    if (!this.watchedDirs.has(topicPath)) {
      const watcher = new FileWatcher();
      await watcher.watchDirectory(topicPath, (event, filename) => {
        if (event === 'create') {
          this.handleNewMessage(topicPath, filename);
        }
      });
      this.watchedDirs.set(topicPath, watcher);
    }
    
    this.addHandler(topic, handler);
  }
  
  private async handleNewMessage(path: string, filename: string): Promise<void> {
    const filepath = join(path, filename);
    const message = JSON.parse(await fs.readFile(filepath, 'utf8'));
    
    // Process message with registered handlers
    const topic = this.pathToTopic(path);
    const handlers = this.messageHandlers.get(topic) || [];
    
    for (const handler of handlers) {
      try {
        await handler(message);
      } catch (error) {
        console.error(`Handler error for topic ${topic}:`, error);
      }
    }
    
    // Archive processed message
    await this.archiveMessage(filepath, message);
  }
}
```

**Pros:**
- Simple implementation, no external dependencies
- Works across all platforms
- Built-in persistence and audit trail
- Easy debugging and monitoring

**Cons:**
- Higher latency than in-memory solutions
- File system overhead for high-frequency messages
- Potential race conditions with concurrent access
- Limited scalability for many sessions

### 4.2 Option 2: Local Redis Instance

**Architecture**
```typescript
class RedisMessageQueue implements MessageQueue {
  private redis: Redis;
  private subscribers: Map<string, Redis> = new Map();
  
  constructor(private config: RedisConfig) {
    this.redis = new Redis(config);
  }
  
  async publish(topic: string, message: Message): Promise<void> {
    const channel = this.topicToChannel(topic);
    await this.redis.publish(channel, JSON.stringify(message));
    
    // Also store in sorted set for persistence
    await this.redis.zadd(
      `messages:${topic}`,
      message.timestamp,
      JSON.stringify(message)
    );
  }
  
  async subscribe(topic: string, handler: MessageHandler): Promise<void> {
    if (!this.subscribers.has(topic)) {
      const subscriber = new Redis(this.config);
      await subscriber.subscribe(this.topicToChannel(topic));
      
      subscriber.on('message', (channel, data) => {
        const message = JSON.parse(data);
        this.notifyHandlers(topic, message);
      });
      
      this.subscribers.set(topic, subscriber);
    }
    
    this.addHandler(topic, handler);
  }
  
  async getMessageHistory(
    topic: string,
    since?: number,
    limit = 100
  ): Promise<Message[]> {
    const start = since || 0;
    const end = Date.now();
    
    const messages = await this.redis.zrangebyscore(
      `messages:${topic}`,
      start,
      end,
      'LIMIT',
      0,
      limit
    );
    
    return messages.map(msg => JSON.parse(msg));
  }
}
```

**Redis Configuration**
```bash
# Local Redis setup for development
redis-server --port 6379 --bind 127.0.0.1 --protected-mode yes
```

**Pros:**
- High performance, low latency
- Built-in pub/sub and persistence
- Atomic operations and transactions
- Rich data structures for complex coordination

**Cons:**
- External dependency (Redis server)
- Additional setup and maintenance
- Memory usage for message storage
- Single point of failure

### 4.3 Option 3: Unix Domain Sockets

**Architecture**
```typescript
class UnixSocketMessageQueue implements MessageQueue {
  private server: net.Server;
  private clients: Map<string, net.Socket> = new Map();
  private handlers: Map<string, MessageHandler[]> = new Map();
  
  constructor(private socketPath: string) {
    this.startServer();
  }
  
  private startServer(): void {
    this.server = net.createServer((socket) => {
      const clientId = this.generateClientId();
      this.clients.set(clientId, socket);
      
      socket.on('data', (data) => {
        try {
          const message = JSON.parse(data.toString());
          this.routeMessage(message);
        } catch (error) {
          console.error('Failed to parse message:', error);
        }
      });
      
      socket.on('close', () => {
        this.clients.delete(clientId);
      });
    });
    
    this.server.listen(this.socketPath);
  }
  
  async publish(topic: string, message: Message): Promise<void> {
    const envelope = {
      type: 'publish',
      topic,
      message
    };
    
    // Broadcast to all connected clients
    for (const [clientId, socket] of this.clients) {
      try {
        socket.write(JSON.stringify(envelope));
      } catch (error) {
        console.error(`Failed to send to client ${clientId}:`, error);
        this.clients.delete(clientId);
      }
    }
  }
  
  async subscribe(topic: string, handler: MessageHandler): Promise<void> {
    this.addHandler(topic, handler);
    
    // Connect to server if not already connected
    if (!this.clientSocket) {
      await this.connectToServer();
    }
    
    // Send subscription request
    const envelope = {
      type: 'subscribe',
      topic
    };
    this.clientSocket.write(JSON.stringify(envelope));
  }
}
```

**Pros:**
- Very low latency, high performance
- No external dependencies
- Unix-native, secure by default
- Efficient for local communication

**Cons:**
- Unix/Linux only (not Windows)
- More complex implementation
- No built-in persistence
- Requires careful error handling

### 4.4 Comparison Matrix

| Feature | File-based | Redis | Unix Sockets |
|---------|------------|-------|--------------|
| **Performance** | Low | High | Very High |
| **Persistence** | Built-in | Configurable | Manual |
| **Dependencies** | None | Redis Server | None |
| **Platform Support** | All | All | Unix/Linux |
| **Setup Complexity** | Low | Medium | High |
| **Debugging** | Easy | Medium | Hard |
| **Scalability** | Limited | High | Medium |
| **Security** | File permissions | Redis AUTH | Unix permissions |

## 5. Use Cases

### 5.1 Multi-Terminal Team Coordination

**Scenario: Developer with Multiple Terminal Sessions**
```typescript
// Terminal 1: Main development session
await orchestrator.startSession({
  session_id: 'main-dev',
  project_id: 'myapp',
  agents: ['engineering-fullstack', 'engineering-api']
});

// Terminal 2: Testing session
await orchestrator.startSession({
  session_id: 'test-runner',
  project_id: 'myapp',
  agents: ['qa-e2e', 'qa-analyst']
});

// Coordinate test execution
await messageQueue.publish('project.myapp.testing', {
  type: 'run_tests',
  source: 'main-dev',
  target: 'test-runner',
  payload: {
    test_suite: 'api-integration',
    environment: 'staging'
  }
});
```

**Coordination Flow**
```typescript
// Terminal 1: Request test run
const testRequest = await createTask({
  type: 'run_integration_tests',
  requirements: ['qa-e2e'],
  priority: 'high',
  metadata: {
    branch: 'feature/api-auth',
    environment: 'staging'
  }
});

// Terminal 2: QA session picks up task
await subscribeToTasks('qa-*', async (task) => {
  if (task.type === 'run_integration_tests') {
    await executeTests(task.metadata);
    await updateTaskStatus(task.id, 'completed', {
      results: testResults,
      coverage: coverageReport
    });
  }
});

// Terminal 1: Receives test completion
await subscribeToTaskUpdates(testRequest.id, (update) => {
  if (update.status === 'completed') {
    console.log('Tests completed:', update.result);
    // Continue with next development step
  }
});
```

### 5.2 Handoff Between Sessions

**Scenario: Context Transfer**
```typescript
interface HandoffRequest {
  from_session: string;
  to_session: string;
  context: {
    current_task: Task;
    project_state: any;
    agent_states: AgentState[];
    user_context: string;
  };
  handoff_reason: 'session_timeout' | 'manual_transfer' | 'error_recovery';
}

// Session A: Initiate handoff
await requestHandoff({
  to_session: 'backup-session',
  context: {
    current_task: getCurrentTask(),
    project_state: await getProjectState(),
    agent_states: await getAllAgentStates(),
    user_context: 'Working on API authentication, completed user registration'
  },
  handoff_reason: 'manual_transfer'
});

// Session B: Accept handoff
await acceptHandoff('session-a-handoff-123', async (context) => {
  // Restore context
  await restoreProjectState(context.project_state);
  await restoreAgentStates(context.agent_states);
  await resumeTask(context.current_task);
  
  console.log(`Resumed session: ${context.user_context}`);
});
```

**Handoff Protocol**
```typescript
class HandoffManager {
  async initiateHandoff(request: HandoffRequest): Promise<string> {
    // 1. Pause current session
    await this.pauseSession(request.from_session);
    
    // 2. Create handoff package
    const handoffId = await this.createHandoffPackage(request);
    
    // 3. Notify target session
    await this.notifyHandoffTarget(request.to_session, handoffId);
    
    // 4. Wait for acceptance
    return this.waitForHandoffAcceptance(handoffId);
  }
  
  async acceptHandoff(handoffId: string): Promise<HandoffContext> {
    // 1. Retrieve handoff package
    const context = await this.getHandoffContext(handoffId);
    
    // 2. Validate compatibility
    await this.validateHandoffCompatibility(context);
    
    // 3. Transfer state
    await this.transferSessionState(context);
    
    // 4. Confirm completion
    await this.confirmHandoffCompletion(handoffId);
    
    return context;
  }
}
```

### 5.3 Global State Synchronization

**Scenario: Project-wide State Updates**
```typescript
interface ProjectStateSync {
  project_id: string;
  version: number;
  state_type: 'dependency_update' | 'config_change' | 'schema_migration';
  changes: StateChange[];
  affected_sessions: string[];
}

// Centralized state manager
class ProjectStateSyncManager {
  async broadcastStateUpdate(update: ProjectStateSync): Promise<void> {
    // 1. Validate state change
    await this.validateStateChange(update);
    
    // 2. Create state snapshot
    const snapshot = await this.createStateSnapshot(update.project_id);
    
    // 3. Broadcast to all sessions
    await this.broadcast('project.state.update', {
      ...update,
      snapshot,
      timestamp: Date.now()
    });
    
    // 4. Wait for acknowledgments
    await this.waitForAcknowledgments(update.affected_sessions);
  }
  
  async handleStateUpdate(update: ProjectStateSync): Promise<void> {
    // 1. Check if update applies to this session
    if (!update.affected_sessions.includes(this.sessionId)) {
      return;
    }
    
    // 2. Pause current operations
    await this.pauseOperations();
    
    // 3. Apply state changes
    await this.applyStateChanges(update.changes);
    
    // 4. Validate new state
    await this.validateState();
    
    // 5. Resume operations
    await this.resumeOperations();
    
    // 6. Send acknowledgment
    await this.sendAcknowledgment(update);
  }
}
```

**State Conflict Resolution**
```typescript
interface StateConflict {
  project_id: string;
  conflicting_sessions: string[];
  conflict_type: 'concurrent_update' | 'version_mismatch' | 'resource_lock';
  resolution_strategy: 'manual' | 'automatic' | 'rollback';
}

class ConflictResolver {
  async resolveConflict(conflict: StateConflict): Promise<void> {
    switch (conflict.resolution_strategy) {
      case 'automatic':
        await this.autoResolveConflict(conflict);
        break;
      case 'manual':
        await this.requestManualResolution(conflict);
        break;
      case 'rollback':
        await this.rollbackToLastKnownGood(conflict);
        break;
    }
  }
  
  private async autoResolveConflict(conflict: StateConflict): Promise<void> {
    // Last-write-wins with timestamp ordering
    const updates = await this.getConflictingUpdates(conflict);
    const latestUpdate = updates.sort((a, b) => b.timestamp - a.timestamp)[0];
    
    await this.applyUpdate(latestUpdate);
    await this.notifyResolution(conflict, latestUpdate);
  }
}
```

### 5.4 Emergency Broadcast Messages

**Scenario: Critical System Events**
```typescript
enum EmergencyType {
  STOP_ALL_TASKS = 'stop_all_tasks',
  SECURITY_BREACH = 'security_breach',
  RESOURCE_EXHAUSTION = 'resource_exhaustion',
  DATA_CORRUPTION = 'data_corruption',
  SYSTEM_SHUTDOWN = 'system_shutdown'
}

interface EmergencyBroadcast {
  type: EmergencyType;
  severity: 'warning' | 'critical' | 'fatal';
  message: string;
  action_required: string;
  auto_execute: boolean;
  timeout: number;
}

// Emergency broadcast system
class EmergencyBroadcastSystem {
  async sendEmergencyBroadcast(broadcast: EmergencyBroadcast): Promise<void> {
    // 1. Validate emergency authority
    await this.validateEmergencyAuthority();
    
    // 2. Log emergency event
    await this.logEmergencyEvent(broadcast);
    
    // 3. Send to all active sessions immediately
    await this.broadcastToAllSessions('global.emergency', broadcast);
    
    // 4. Execute automatic actions if enabled
    if (broadcast.auto_execute) {
      await this.executeEmergencyActions(broadcast);
    }
    
    // 5. Monitor response status
    await this.monitorEmergencyResponse(broadcast);
  }
  
  async handleEmergencyBroadcast(broadcast: EmergencyBroadcast): Promise<void> {
    // 1. Immediately acknowledge receipt
    await this.sendEmergencyAck(broadcast);
    
    // 2. Execute required actions based on type
    switch (broadcast.type) {
      case EmergencyType.STOP_ALL_TASKS:
        await this.stopAllTasks();
        break;
      case EmergencyType.SECURITY_BREACH:
        await this.lockdownSession();
        break;
      case EmergencyType.RESOURCE_EXHAUSTION:
        await this.reduceResourceUsage();
        break;
      case EmergencyType.SYSTEM_SHUTDOWN:
        await this.gracefulShutdown();
        break;
    }
    
    // 3. Report action completion
    await this.reportEmergencyActionComplete(broadcast);
  }
}
```

**Emergency Response Flow**
```typescript
// 1. Emergency detection
const emergency = {
  type: EmergencyType.STOP_ALL_TASKS,
  severity: 'critical',
  message: 'Critical error detected in payment processing',
  action_required: 'Stop all payment-related tasks immediately',
  auto_execute: true,
  timeout: 30000 // 30 seconds
};

// 2. Broadcast to all sessions
await emergencySystem.sendEmergencyBroadcast(emergency);

// 3. Each session responds
await emergencySystem.onEmergencyBroadcast(async (broadcast) => {
  if (broadcast.type === EmergencyType.STOP_ALL_TASKS) {
    // Stop current tasks
    await taskManager.stopAllTasks();
    
    // Preserve state for recovery
    await stateManager.createEmergencySnapshot();
    
    // Notify completion
    await emergencySystem.reportTasksstopped();
  }
});

// 4. Monitor and confirm all sessions responded
const responses = await emergencySystem.waitForAllResponses(emergency.timeout);
if (responses.allResponded) {
  console.log('Emergency action completed successfully');
} else {
  console.error('Some sessions did not respond to emergency broadcast');
}
```

## Implementation Recommendations

### Phase 1: File-based Foundation
Start with file-based message passing for initial implementation:
- Simple to implement and debug
- No external dependencies
- Built-in persistence
- Good for development and testing

### Phase 2: Redis Enhancement
Add Redis option for production environments:
- Better performance for high-frequency coordination
- Rich pub/sub capabilities
- Built-in clustering for scalability

### Phase 3: Hybrid Approach
Combine both systems based on use case:
- File-based for persistent state and handoffs
- Redis for real-time coordination and events
- Emergency broadcasts via both channels

### Security First
Implement security model from the beginning:
- Token-based authentication
- Resource-based permissions
- Data encryption for sensitive state
- Audit logging for all inter-session communication

This API specification provides a comprehensive foundation for robust inter-session communication in the V2 orchestration system, enabling seamless collaboration across multiple Claude sessions while maintaining security and performance.