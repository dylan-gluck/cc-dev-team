---
source: https://github.com/modelcontextprotocol/python-sdk, https://modelcontextprotocol.io/specification
fetched: 2025-08-20
version: 2025-06-18
---

# MCP API Reference

## Table of Contents
- [FastMCP Framework](#fastmcp-framework)
- [Server Classes](#server-classes)
- [Client Classes](#client-classes)
- [Type Definitions](#type-definitions)
- [Transport Layer](#transport-layer)
- [Error Handling](#error-handling)
- [Protocol Messages](#protocol-messages)
- [Decorators and Annotations](#decorators-and-annotations)

## FastMCP Framework

### FastMCP Class

```python
class FastMCP:
    """High-level MCP server framework for rapid development."""
    
    def __init__(
        self,
        name: str,
        version: str = "1.0.0",
        description: Optional[str] = None,
        author: Optional[str] = None,
        license: Optional[str] = None
    ) -> None:
        """Initialize FastMCP server.
        
        Args:
            name: Server name (required)
            version: Server version
            description: Server description
            author: Author name
            license: License type
        """
```

#### Methods

```python
def tool(
    self,
    name: Optional[str] = None,
    description: Optional[str] = None
) -> Callable:
    """Decorator to register a tool.
    
    Args:
        name: Tool name (defaults to function name)
        description: Tool description (defaults to docstring)
    
    Returns:
        Decorated function
        
    Example:
        @mcp.tool()
        def my_tool(param: str) -> str:
            return f"Result: {param}"
    """

def resource(
    self,
    uri: str,
    name: Optional[str] = None,
    description: Optional[str] = None
) -> Callable:
    """Decorator to register a resource.
    
    Args:
        uri: Resource URI template (supports {param} placeholders)
        name: Resource name (defaults to function name)
        description: Resource description (defaults to docstring)
    
    Returns:
        Decorated function
        
    Example:
        @mcp.resource("file://{path}")
        def read_file(path: str) -> str:
            return Path(path).read_text()
    """

def prompt(
    self,
    name: Optional[str] = None,
    description: Optional[str] = None
) -> Callable:
    """Decorator to register a prompt.
    
    Args:
        name: Prompt name (defaults to function name)
        description: Prompt description (defaults to docstring)
    
    Returns:
        Decorated function
        
    Example:
        @mcp.prompt()
        def analyze_code(code: str) -> str:
            return f"Please analyze this code: {code}"
    """

def run(self, **kwargs) -> None:
    """Run the MCP server.
    
    Args:
        **kwargs: Additional arguments for server configuration
    """

def run_http(
    self,
    host: str = "localhost",
    port: int = 8080,
    **kwargs
) -> None:
    """Run the MCP server with HTTP transport.
    
    Args:
        host: Server host
        port: Server port
        **kwargs: Additional server arguments
    """
```

## Server Classes

### Server

```python
class Server:
    """Low-level MCP server implementation."""
    
    def __init__(
        self,
        name: str,
        version: str,
        request_timeout: Optional[float] = None
    ) -> None:
        """Initialize MCP Server.
        
        Args:
            name: Server name
            version: Server version
            request_timeout: Request timeout in seconds
        """
    
    async def run(
        self,
        read_stream: anyio.abc.ByteReceiveStream,
        write_stream: anyio.abc.ByteSendStream,
        initialization_options: Optional[Dict[str, Any]] = None
    ) -> None:
        """Run the server with provided streams.
        
        Args:
            read_stream: Input stream
            write_stream: Output stream
            initialization_options: Server initialization options
        """
```

#### Server Event Handlers

```python
@server.call_tool()
async def handle_call_tool(
    name: str,
    arguments: Optional[Dict[str, Any]]
) -> List[types.TextContent | types.ImageContent]:
    """Handle tool calls.
    
    Args:
        name: Tool name
        arguments: Tool arguments
        
    Returns:
        List of content objects
    """

@server.list_tools()
async def handle_list_tools() -> List[types.Tool]:
    """Handle list tools requests.
    
    Returns:
        List of available tools
    """

@server.read_resource()
async def handle_read_resource(
    uri: str
) -> str | bytes:
    """Handle resource read requests.
    
    Args:
        uri: Resource URI
        
    Returns:
        Resource content
    """

@server.list_resources()
async def handle_list_resources() -> List[types.Resource]:
    """Handle list resources requests.
    
    Returns:
        List of available resources
    """

@server.get_prompt()
async def handle_get_prompt(
    name: str,
    arguments: Optional[Dict[str, Any]]
) -> types.GetPromptResult:
    """Handle prompt requests.
    
    Args:
        name: Prompt name
        arguments: Prompt arguments
        
    Returns:
        Prompt result with messages
    """

@server.list_prompts()
async def handle_list_prompts() -> List[types.Prompt]:
    """Handle list prompts requests.
    
    Returns:
        List of available prompts
    """
```

### Transport Utilities

```python
async def stdio_server() -> Tuple[
    anyio.abc.ByteReceiveStream,
    anyio.abc.ByteSendStream
]:
    """Create stdio transport streams.
    
    Returns:
        Tuple of (read_stream, write_stream)
    """
```

## Client Classes

### StdioServerParameters

```python
@dataclass
class StdioServerParameters:
    """Parameters for stdio server connection."""
    
    command: str
    args: Optional[List[str]] = None
    env: Optional[Dict[str, str]] = None
    cwd: Optional[str] = None
```

### Client Session

```python
class ClientSession:
    """MCP client session for communicating with servers."""
    
    async def initialize(
        self,
        client_info: Optional[types.Implementation] = None
    ) -> types.InitializeResult:
        """Initialize the client session.
        
        Args:
            client_info: Client implementation details
            
        Returns:
            Server initialization result
        """
    
    async def call_tool(
        self,
        name: str,
        arguments: Optional[Dict[str, Any]] = None
    ) -> types.CallToolResult:
        """Call a tool on the server.
        
        Args:
            name: Tool name
            arguments: Tool arguments
            
        Returns:
            Tool execution result
        """
    
    async def list_tools(self) -> types.ListToolsResult:
        """List available tools.
        
        Returns:
            List of available tools
        """
    
    async def read_resource(self, uri: str) -> types.ReadResourceResult:
        """Read a resource from the server.
        
        Args:
            uri: Resource URI
            
        Returns:
            Resource content
        """
    
    async def list_resources(self) -> types.ListResourcesResult:
        """List available resources.
        
        Returns:
            List of available resources
        """
    
    async def get_prompt(
        self,
        name: str,
        arguments: Optional[Dict[str, Any]] = None
    ) -> types.GetPromptResult:
        """Get a prompt from the server.
        
        Args:
            name: Prompt name
            arguments: Prompt arguments
            
        Returns:
            Prompt with messages
        """
    
    async def list_prompts(self) -> types.ListPromptsResult:
        """List available prompts.
        
        Returns:
            List of available prompts
        """
    
    async def send_log_message(
        self,
        level: types.LoggingLevel,
        message: str,
        logger: Optional[str] = None
    ) -> None:
        """Send a log message to the client.
        
        Args:
            level: Log level
            message: Log message
            logger: Logger name
        """
```

### Client Context Manager

```python
async def stdio_client(
    server_params: StdioServerParameters
) -> AsyncContextManager[ClientSession]:
    """Create stdio client context manager.
    
    Args:
        server_params: Server connection parameters
        
    Returns:
        Async context manager for client session
        
    Example:
        async with stdio_client(params) as client:
            await client.initialize()
            result = await client.call_tool("my_tool", {})
    """
```

## Type Definitions

### Core Types

```python
class TextContent(BaseModel):
    """Text content object."""
    type: Literal["text"]
    text: str

class ImageContent(BaseModel):
    """Image content object."""
    type: Literal["image"]
    data: str  # Base64 encoded image data
    mimeType: str

class Tool(BaseModel):
    """Tool definition."""
    name: str
    description: Optional[str] = None
    inputSchema: Dict[str, Any]  # JSON Schema for parameters

class Resource(BaseModel):
    """Resource definition."""
    uri: str
    name: Optional[str] = None
    description: Optional[str] = None
    mimeType: Optional[str] = None

class Prompt(BaseModel):
    """Prompt definition."""
    name: str
    description: Optional[str] = None
    arguments: Optional[List[PromptArgument]] = None

class PromptArgument(BaseModel):
    """Prompt argument definition."""
    name: str
    description: Optional[str] = None
    required: Optional[bool] = None
```

### Result Types

```python
class CallToolResult(BaseModel):
    """Result of tool execution."""
    content: List[TextContent | ImageContent]
    isError: Optional[bool] = None

class ReadResourceResult(BaseModel):
    """Result of resource reading."""
    contents: List[TextContent | ImageContent]

class GetPromptResult(BaseModel):
    """Result of prompt retrieval."""
    description: Optional[str] = None
    messages: List[PromptMessage]

class ListToolsResult(BaseModel):
    """Result of listing tools."""
    tools: List[Tool]

class ListResourcesResult(BaseModel):
    """Result of listing resources."""
    resources: List[Resource]

class ListPromptsResult(BaseModel):
    """Result of listing prompts."""
    prompts: List[Prompt]
```

### Message Types

```python
class PromptMessage(BaseModel):
    """Prompt message."""
    role: Literal["user", "assistant", "system"]
    content: TextContent | ImageContent

class LoggingLevel(str, Enum):
    """Logging levels."""
    DEBUG = "debug"
    INFO = "info"
    NOTICE = "notice"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"
    ALERT = "alert"
    EMERGENCY = "emergency"
```

### Implementation Info

```python
class Implementation(BaseModel):
    """Implementation information."""
    name: str
    version: str

class InitializeResult(BaseModel):
    """Initialization result."""
    protocolVersion: str
    capabilities: ServerCapabilities
    serverInfo: Implementation
```

### Capabilities

```python
class ServerCapabilities(BaseModel):
    """Server capabilities."""
    logging: Optional[bool] = None
    prompts: Optional[PromptsCapability] = None
    resources: Optional[ResourcesCapability] = None
    tools: Optional[ToolsCapability] = None

class PromptsCapability(BaseModel):
    """Prompts capability."""
    listChanged: Optional[bool] = None

class ResourcesCapability(BaseModel):
    """Resources capability."""
    subscribe: Optional[bool] = None
    listChanged: Optional[bool] = None

class ToolsCapability(BaseModel):
    """Tools capability."""
    listChanged: Optional[bool] = None
```

## Transport Layer

### Stdio Transport

```python
# Server side
from mcp.server.stdio import stdio_server

async def run_stdio_server():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream)

# Client side
from mcp.client.stdio import StdioServerParameters, stdio_client

params = StdioServerParameters(
    command="python",
    args=["server.py"],
    env={"CUSTOM_VAR": "value"},
    cwd="/path/to/server"
)

async with stdio_client(params) as client:
    await client.initialize()
    # Use client...
```

### HTTP Transport (Future)

```python
# Server side (planned)
from mcp.server.http import run_http_server

await run_http_server(host="localhost", port=8080)

# Client side (planned)
from mcp.client.http import http_client

async with http_client("http://localhost:8080/mcp") as client:
    await client.initialize()
    # Use client...
```

## Error Handling

### Exception Classes

```python
class McpError(Exception):
    """Base MCP error."""
    def __init__(self, message: str, code: int = -32603):
        self.message = message
        self.code = code
        super().__init__(message)

class InvalidRequestError(McpError):
    """Invalid request error."""
    def __init__(self, message: str):
        super().__init__(message, -32600)

class MethodNotFoundError(McpError):
    """Method not found error."""
    def __init__(self, method: str):
        super().__init__(f"Method not found: {method}", -32601)

class InvalidParamsError(McpError):
    """Invalid parameters error."""
    def __init__(self, message: str):
        super().__init__(message, -32602)

class InternalError(McpError):
    """Internal error."""
    def __init__(self, message: str):
        super().__init__(message, -32603)
```

### Error Handling Patterns

```python
# Server-side error handling
@mcp.tool()
def risky_tool(param: str) -> str:
    try:
        # Risky operation
        result = process_data(param)
        return result
    except ValueError as e:
        raise InvalidParamsError(f"Invalid parameter: {e}")
    except Exception as e:
        raise InternalError(f"Processing failed: {e}")

# Client-side error handling
try:
    result = await client.call_tool("risky_tool", {"param": "value"})
except McpError as e:
    print(f"MCP error: {e.message} (code: {e.code})")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Protocol Messages

### JSON-RPC Message Format

All MCP messages follow JSON-RPC 2.0 format:

```python
# Request message
{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
        "name": "my_tool",
        "arguments": {"param": "value"}
    }
}

# Response message
{
    "jsonrpc": "2.0",
    "id": 1,
    "result": {
        "content": [
            {
                "type": "text",
                "text": "Tool result"
            }
        ]
    }
}

# Error response
{
    "jsonrpc": "2.0",
    "id": 1,
    "error": {
        "code": -32602,
        "message": "Invalid params",
        "data": "Additional error details"
    }
}
```

### Method Names

Standard MCP methods:

- `initialize` - Initialize connection
- `tools/list` - List available tools
- `tools/call` - Call a tool
- `resources/list` - List available resources
- `resources/read` - Read a resource
- `prompts/list` - List available prompts
- `prompts/get` - Get a prompt
- `logging/setLevel` - Set logging level

### Notifications

```python
# Server can send notifications to client
{
    "jsonrpc": "2.0",
    "method": "notifications/tools/list_changed"
}

{
    "jsonrpc": "2.0",
    "method": "notifications/resources/list_changed"
}

{
    "jsonrpc": "2.0",
    "method": "notifications/resources/updated",
    "params": {
        "uri": "file:///path/to/file"
    }
}
```

## Decorators and Annotations

### Type Annotations for Structured Output

```python
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from dataclasses import dataclass

# Pydantic models
class UserData(BaseModel):
    id: int = Field(description="User ID")
    name: str = Field(description="User name")
    email: str = Field(description="User email")

@mcp.tool()
def get_user(user_id: int) -> UserData:
    """Get user data with structured output."""
    return UserData(id=user_id, name="John", email="john@example.com")

# Dataclasses
@dataclass
class TaskInfo:
    id: str
    title: str
    completed: bool

@mcp.tool()
def create_task(title: str) -> TaskInfo:
    """Create task with dataclass output."""
    return TaskInfo(id="123", title=title, completed=False)

# Generic types
@mcp.tool()
def get_items() -> List[Dict[str, Any]]:
    """Get items with generic types."""
    return [{"id": 1, "name": "Item 1"}]
```

### Parameter Validation

```python
from typing import Literal

@mcp.tool()
def process_data(
    data: str,
    format: Literal["json", "csv", "xml"] = "json",
    validate: bool = True
) -> str:
    """Tool with parameter validation."""
    if validate and not data.strip():
        raise ValueError("Data cannot be empty")
    
    return f"Processed {len(data)} characters as {format}"
```

### Documentation Patterns

```python
@mcp.tool()
def complex_tool(
    required_param: str,
    optional_param: Optional[int] = None,
    config: Dict[str, Any] = None
) -> Dict[str, Any]:
    """Complex tool with comprehensive documentation.
    
    This tool demonstrates comprehensive parameter documentation
    and return value specification.
    
    Args:
        required_param: A required string parameter that must be provided
        optional_param: An optional integer parameter with default None
        config: Optional configuration dictionary for advanced settings
    
    Returns:
        Dictionary containing:
        - result: The processed result
        - metadata: Processing metadata
        - status: Operation status
    
    Raises:
        ValueError: If required_param is empty
        TypeError: If config is not a dictionary
    
    Example:
        result = complex_tool("test", optional_param=42, config={"debug": True})
    """
    if not required_param:
        raise ValueError("required_param cannot be empty")
    
    if config is not None and not isinstance(config, dict):
        raise TypeError("config must be a dictionary")
    
    return {
        "result": f"Processed: {required_param}",
        "metadata": {"optional_used": optional_param is not None},
        "status": "success"
    }
```

This API reference provides comprehensive documentation for all major components of the MCP Python SDK. Use it as a reference when building MCP servers and clients.