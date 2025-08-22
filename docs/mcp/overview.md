---
source: https://modelcontextprotocol.io/docs, https://modelcontextprotocol.io/specification
fetched: 2025-08-20
version: 2025-06-18
---

# Model Context Protocol (MCP) - Overview

## Table of Contents
- [What is MCP?](#what-is-mcp)
- [Core Architecture](#core-architecture)
- [Key Participants](#key-participants)
- [Protocol Layers](#protocol-layers)
- [Core Components](#core-components)
- [Communication Flow](#communication-flow)
- [Version Management](#version-management)
- [Benefits and Use Cases](#benefits-and-use-cases)

## What is MCP?

The Model Context Protocol (MCP) is an open protocol that standardizes how AI applications provide context to large language models (LLMs). Released by Anthropic in November 2024, MCP is designed to be "like a USB-C port for AI applications" - providing a universal, standardized way to connect AI models to different data sources and tools.

### Core Philosophy
MCP solves the "M×N problem" where having M different AI applications and N different tools/systems would require building M×N different integrations. MCP transforms this into an "M+N problem" by providing a single standardized protocol.

## Core Architecture

MCP follows a **client-server architecture** where a host application can connect to multiple servers through dedicated clients.

### Client-Server Model
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  MCP Host   │◄──►│ MCP Client  │◄──►│ MCP Server  │
│             │    │             │    │             │
│ (AI App)    │    │ (Protocol)  │    │ (Tools/Data)│
└─────────────┘    └─────────────┘    └─────────────┘
```

## Key Participants

### MCP Host
- The AI application coordinating connections (e.g., Claude Desktop, IDE, custom AI tools)
- Manages multiple MCP clients
- Provides the user interface and LLM integration

### MCP Client  
- Maintains a dedicated 1:1 connection with an MCP server
- Handles protocol communication
- Translates between host requests and server responses

### MCP Server
- Lightweight programs exposing specific capabilities
- Can access local data sources (files, databases, services)
- Can connect to remote services (APIs, external systems)

## Protocol Layers

### 1. Transport Layer
Manages communication channels and authentication:
- **Stdio Transport**: Local process communication (pipes, processes)
- **HTTP Transport**: Remote server communication (SSE, streaming)

### 2. Protocol Layer  
Built on JSON-RPC 2.0, handles:
- Connection lifecycle management
- Capability negotiation between client/server
- Core primitive exchange
- Message routing and error handling

## Core Components

### Server-Side Primitives

#### Tools
- **Purpose**: Model-controlled actions that the AI can decide to take
- **Behavior**: Executable functions that can perform computations and side effects
- **Use Cases**: API calls, file operations, calculations, data transformations

#### Resources
- **Purpose**: Application-controlled context provided to the AI
- **Behavior**: Similar to GET endpoints - provide information without side effects
- **Use Cases**: File contents, database records, configuration data

#### Prompts
- **Purpose**: User-controlled specific interactions
- **Behavior**: Template-based interaction patterns
- **Use Cases**: Structured queries, guided conversations, specialized workflows

### Client-Side Primitives

#### Sampling
- Request language model completions from the host
- Enables servers to leverage the host's LLM capabilities

#### Elicitation  
- Request information from the user through the host interface
- Enables interactive workflows requiring user input

#### Logging
- Send debug and informational messages to the host
- Supports development and troubleshooting

## Communication Flow

### 1. Initialization
- Host application creates MCP clients
- Client-server handshake occurs
- Protocol version negotiation
- Capability exchange

### 2. Discovery
- Client requests available capabilities from server
- Server responds with tools, resources, and prompts
- Host parses capabilities for LLM integration

### 3. Context Provision
- Host makes resources available to LLM context
- Tools are formatted for LLM consumption
- Prompts become available for user interaction

### 4. Execution
- LLM decides to use a tool → Host sends invocation via client
- Host needs data → Client requests resource from server  
- User triggers prompt → Client executes prompt workflow

### 5. Real-time Updates
- Servers can send notifications about state changes
- Clients relay updates to hosts for context refresh

## Version Management

### Versioning Scheme
- Format: `YYYY-MM-DD` (date-based versioning)
- Indicates last date of backwards-incompatible changes
- Current version: `2025-06-18`

### Revision States
- **Draft**: In-progress, not ready for production
- **Current**: Ready for use, may receive compatible updates
- **Final**: Stable, no further changes

### Version Negotiation
- Occurs during initialization handshake
- Clients and servers may support multiple versions
- Must agree on single version for session
- Graceful error handling for version mismatches

## Benefits and Use Cases

### Key Advantages
1. **Standardization**: Unified integration approach across AI applications
2. **Flexibility**: Easy switching between AI models and vendors  
3. **Security**: Data stays within your infrastructure
4. **Modularity**: Compose complex workflows from simple components
5. **Interoperability**: Write once, use across multiple AI applications

### Common Use Cases
- **Development Tools**: IDE integrations, code analysis, project management
- **Data Access**: Database connectivity, file system access, API integrations  
- **Content Management**: Document processing, knowledge base access
- **System Integration**: DevOps tools, monitoring, automation workflows
- **Custom Workflows**: Domain-specific tools and specialized processes

### Ecosystem Growth
- Rapidly growing library of pre-built MCP servers
- Community-driven registry of available integrations
- Official SDKs in Python, TypeScript, and other languages
- Active development community and contributions

## Protocol Features

### Stateful Connections
- Persistent client-server sessions
- Context preservation across interactions
- Efficient resource management

### Dynamic Discovery
- Runtime capability detection
- Hot-swapping of tools and resources  
- Flexible server configurations

### Error Handling
- Robust error propagation
- Graceful degradation
- Comprehensive logging support

### Performance
- Efficient JSON-RPC communication
- Minimal protocol overhead
- Async operation support

This overview provides the foundational understanding needed to work with MCP. For implementation details, see the getting-started guide and SDK-specific documentation.