---
source: https://github.com/modelcontextprotocol/python-sdk
fetched: 2025-08-20
version: latest
---

# MCP Python SDK Reference

## Table of Contents
- [Installation and Setup](#installation-and-setup)
- [FastMCP Framework](#fastmcp-framework)
- [Server Implementation](#server-implementation)
- [Client Implementation](#client-implementation)
- [Type System and Structured Output](#type-system-and-structured-output)
- [Transport Layer](#transport-layer)
- [Error Handling](#error-handling)
- [Advanced Features](#advanced-features)
- [Performance and Best Practices](#performance-and-best-practices)

## Installation and Setup

### Package Installation
```bash
# Basic installation
uv add "mcp[cli]"
pip install "mcp[cli]"

# With development tools
uv add "mcp[cli,dev]"
pip install "mcp[cli,dev]"

# Minimal installation (no CLI tools)
uv add mcp
pip install mcp
```

### Import Structure
```python
# FastMCP (recommended for most use cases)
from mcp.server.fastmcp import FastMCP

# Low-level server implementation
from mcp.server import Server
from mcp.server.stdio import stdio_server

# Client implementation
from mcp.client.stdio import StdioServerParameters, stdio_client
from mcp.client.session import ClientSession

# Type definitions
from mcp.types import (
    Tool, Resource, Prompt,
    TextContent, ImageContent,
    CallToolResult, ListToolsResult
)
```

## FastMCP Framework

### Basic Server Setup
```python
from mcp.server.fastmcp import FastMCP

# Create server instance
mcp = FastMCP("MyServer", version="1.0.0")

# Start server (blocks)
if __name__ == "__main__":
    mcp.run()
```

### Configuration Options
```python
mcp = FastMCP(
    name="MyServer",
    version="1.0.0",
    description="My MCP server description",
    author="Your Name",
    license="MIT"
)
```

## Server Implementation

### Tools Implementation

#### Basic Tool Definition
```python
@mcp.tool()
def simple_tool(param: str) -> str:
    """A simple tool that processes a string parameter."""
    return f"Processed: {param}"
```

#### Tool with Complex Parameters
```python
from typing import List, Optional, Dict, Any

@mcp.tool()
def advanced_tool(
    required_param: str,
    optional_param: Optional[int] = None,
    list_param: List[str] = None,
    dict_param: Dict[str, Any] = None
) -> Dict[str, Any]:
    """Tool with various parameter types."""
    return {
        "required": required_param,
        "optional": optional_param,
        "list": list_param or [],
        "dict": dict_param or {}
    }
```

#### Async Tools
```python
import asyncio
import aiohttp

@mcp.tool()
async def fetch_url(url: str) -> str:
    """Fetch content from a URL asynchronously."""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()
```

### Resources Implementation

#### Static Resources
```python
@mcp.resource("config://server")
def get_server_config() -> Dict[str, Any]:
    """Get server configuration."""
    return {
        "version": "1.0.0",
        "features": ["tools", "resources", "prompts"]
    }
```

#### Dynamic Resources with Parameters
```python
@mcp.resource("user://{user_id}")
def get_user(user_id: str) -> Dict[str, Any]:
    """Get user information by ID."""
    # Simulated user data
    users = {
        "1": {"name": "Alice", "email": "alice@example.com"},
        "2": {"name": "Bob", "email": "bob@example.com"}
    }
    
    user = users.get(user_id)
    if not user:
        raise ValueError(f"User {user_id} not found")
    
    return user
```

#### File System Resources
```python
import os
from pathlib import Path

@mcp.resource("file://{path}")
def read_file(path: str) -> str:
    """Read file contents safely."""
    file_path = Path(path)
    
    # Security check
    if not file_path.exists():
        raise ValueError(f"File not found: {path}")
    
    if not file_path.is_file():
        raise ValueError(f"Path is not a file: {path}")
    
    try:
        return file_path.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        return file_path.read_text(encoding='latin-1')
```

### Prompts Implementation
```python
@mcp.prompt()
def analyze_data(
    data_source: str,
    analysis_type: str = "summary",
    include_visualization: bool = False
) -> str:
    """Generate a prompt for data analysis."""
    prompt = f"Please analyze the data from: {data_source}\n\n"
    
    if analysis_type == "summary":
        prompt += "Provide a comprehensive summary including key metrics and insights."
    elif analysis_type == "detailed":
        prompt += "Provide a detailed analysis with statistical breakdowns."
    
    if include_visualization:
        prompt += "\n\nPlease include suggestions for data visualization."
    
    return prompt

@mcp.prompt("code-review")
def code_review_prompt(
    language: str,
    complexity: str = "intermediate"
) -> str:
    """Generate a code review prompt."""
    return f"""
    Please review this {language} code with {complexity} complexity expectations:

    Focus on:
    - Code quality and best practices
    - Performance considerations
    - Security vulnerabilities
    - Maintainability
    
    Provide specific, actionable feedback.
    """
```

## Client Implementation

### Basic Client Usage
```python
import asyncio
from mcp.client.stdio import StdioServerParameters, stdio_client

async def main():
    server_params = StdioServerParameters(
        command="python",
        args=["my_server.py"],
        env={"PYTHONPATH": "/path/to/your/code"}
    )
    
    async with stdio_client(server_params) as client:
        # Initialize the client
        await client.initialize()
        
        # List available capabilities
        tools = await client.list_tools()
        resources = await client.list_resources()
        prompts = await client.list_prompts()
        
        print(f"Available tools: {[t.name for t in tools.tools]}")
        print(f"Available resources: {[r.uri for r in resources.resources]}")
        print(f"Available prompts: {[p.name for p in prompts.prompts]}")

if __name__ == "__main__":
    asyncio.run(main())
```

### Advanced Client Operations
```python
async def advanced_client_example():
    server_params = StdioServerParameters(
        command="python",
        args=["server.py"]
    )
    
    async with stdio_client(server_params) as client:
        await client.initialize()
        
        # Call a tool
        result = await client.call_tool(
            "my_tool",
            arguments={"param1": "value1", "param2": "value2"}
        )
        print(f"Tool result: {result.content}")
        
        # Read a resource
        resource = await client.read_resource("config://server")
        print(f"Resource content: {resource.contents}")
        
        # Get a prompt
        prompt_result = await client.get_prompt(
            "analyze_data",
            arguments={"data_source": "database.csv"}
        )
        print(f"Generated prompt: {prompt_result.messages}")
```

## Type System and Structured Output

### Pydantic Models
```python
from pydantic import BaseModel, Field
from typing import List, Optional

class User(BaseModel):
    id: int = Field(description="User ID")
    name: str = Field(description="User's full name")
    email: str = Field(description="User's email address")
    is_active: bool = Field(default=True, description="Whether user is active")

class UserSearchResult(BaseModel):
    users: List[User]
    total_count: int
    page: int

@mcp.tool()
def search_users(query: str, page: int = 1) -> UserSearchResult:
    """Search users with structured output."""
    # Mock data for example
    users = [
        User(id=1, name="Alice Smith", email="alice@example.com"),
        User(id=2, name="Bob Jones", email="bob@example.com")
    ]
    
    return UserSearchResult(
        users=users,
        total_count=len(users),
        page=page
    )
```

### TypedDict Support
```python
from typing import TypedDict, List

class WeatherData(TypedDict):
    temperature: float
    humidity: float
    condition: str
    wind_speed: Optional[float]

@mcp.tool()
def get_weather(city: str) -> WeatherData:
    """Get weather data using TypedDict."""
    return WeatherData(
        temperature=22.5,
        humidity=65.0,
        condition="partly cloudy",
        wind_speed=10.2
    )
```

### Dataclass Support
```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class TaskInfo:
    id: str
    title: str
    completed: bool
    priority: Optional[str] = None

@mcp.tool()
def create_task(title: str, priority: str = "medium") -> TaskInfo:
    """Create a new task."""
    import uuid
    return TaskInfo(
        id=str(uuid.uuid4()),
        title=title,
        completed=False,
        priority=priority
    )
```

## Transport Layer

### Stdio Transport (Local)
```python
# Server side
from mcp.server.stdio import stdio_server

async def main():
    async with stdio_server() as streams:
        await server.run(streams[0], streams[1])

# Client side  
from mcp.client.stdio import StdioServerParameters

server_params = StdioServerParameters(
    command="python",
    args=["server.py"],
    cwd="/path/to/server",
    env={"CUSTOM_VAR": "value"}
)
```

### HTTP Transport (Remote)
```python
# Server side (using FastMCP)
mcp = FastMCP("RemoteServer")

if __name__ == "__main__":
    # HTTP transport will be available in future versions
    mcp.run_http(host="localhost", port=8080)

# Client side
from mcp.client.http import HttpClientTransport

transport = HttpClientTransport("http://localhost:8080/mcp")
```

## Error Handling

### Server-Side Error Handling
```python
from mcp.server.exceptions import McpError

@mcp.tool()
def risky_operation(value: str) -> str:
    """Tool with proper error handling."""
    try:
        if not value:
            raise McpError("Value cannot be empty", code=-1)
        
        # Simulate risky operation
        result = perform_operation(value)
        return result
    
    except ValueError as e:
        raise McpError(f"Invalid input: {e}", code=-2)
    except Exception as e:
        raise McpError(f"Unexpected error: {e}", code=-32603)

def perform_operation(value: str) -> str:
    """Simulate an operation that might fail."""
    if value == "error":
        raise ValueError("Simulated error")
    return f"Processed: {value}"
```

### Client-Side Error Handling
```python
from mcp.client.exceptions import McpError

async def safe_client_operation():
    try:
        result = await client.call_tool("risky_tool", {"value": "test"})
        return result.content
    
    except McpError as e:
        print(f"MCP Error: {e.message} (code: {e.code})")
        return None
    
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
```

## Advanced Features

### Context Management
```python
from contextlib import contextmanager
import sqlite3

@contextmanager
def database_connection():
    """Context manager for database connections."""
    conn = sqlite3.connect("app.db")
    try:
        yield conn
    finally:
        conn.close()

@mcp.tool()
def query_database(sql: str) -> List[Dict[str, Any]]:
    """Execute SQL query safely."""
    with database_connection() as conn:
        cursor = conn.execute(sql)
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        
        return [dict(zip(columns, row)) for row in rows]
```

### Progress Tracking
```python
import asyncio
from mcp.server.fastmcp import FastMCP

@mcp.tool()
async def long_running_task(duration: int = 10) -> str:
    """Demonstrate progress tracking."""
    for i in range(duration):
        await asyncio.sleep(1)
        # Progress notifications (future feature)
        # await mcp.notify_progress(i / duration)
    
    return f"Task completed in {duration} seconds"
```

### Configuration Management
```python
import os
from typing import Dict, Any

class ServerConfig:
    def __init__(self):
        self.database_url = os.getenv("DATABASE_URL", "sqlite:///app.db")
        self.api_key = os.getenv("API_KEY")
        self.debug = os.getenv("DEBUG", "false").lower() == "true"

config = ServerConfig()

@mcp.resource("config://app")
def get_app_config() -> Dict[str, Any]:
    """Get application configuration."""
    return {
        "database_configured": bool(config.database_url),
        "api_key_configured": bool(config.api_key),
        "debug_mode": config.debug
    }
```

## Performance and Best Practices

### Async Best Practices
```python
import asyncio
from typing import List

@mcp.tool()
async def batch_operation(items: List[str]) -> List[str]:
    """Process items concurrently for better performance."""
    async def process_item(item: str) -> str:
        # Simulate async processing
        await asyncio.sleep(0.1)
        return f"processed_{item}"
    
    # Process all items concurrently
    tasks = [process_item(item) for item in items]
    results = await asyncio.gather(*tasks)
    
    return results
```

### Resource Caching
```python
from functools import lru_cache
from typing import Dict, Any

@lru_cache(maxsize=128)
def expensive_computation(param: str) -> Dict[str, Any]:
    """Cache expensive computations."""
    # Simulate expensive operation
    import time
    time.sleep(2)  # Don't actually do this in async code
    
    return {"result": f"computed_{param}", "cached": True}

@mcp.tool()
def cached_tool(param: str) -> Dict[str, Any]:
    """Tool using cached computation."""
    return expensive_computation(param)
```

### Memory Management
```python
import gc
from typing import Iterator, List

@mcp.tool()
def process_large_dataset(chunk_size: int = 1000) -> str:
    """Process large datasets efficiently."""
    def data_chunks() -> Iterator[List[str]]:
        # Simulate large dataset
        for i in range(0, 100000, chunk_size):
            yield [f"item_{j}" for j in range(i, min(i + chunk_size, 100000))]
    
    processed_count = 0
    
    for chunk in data_chunks():
        # Process chunk
        processed_count += len(chunk)
        
        # Periodic garbage collection for large datasets
        if processed_count % 10000 == 0:
            gc.collect()
    
    return f"Processed {processed_count} items"
```

### Logging and Monitoring
```python
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@mcp.tool()
def monitored_tool(param: str) -> str:
    """Tool with comprehensive logging."""
    start_time = datetime.now()
    logger.info(f"Starting monitored_tool with param: {param}")
    
    try:
        result = f"processed_{param}"
        duration = (datetime.now() - start_time).total_seconds()
        logger.info(f"Tool completed in {duration:.2f}s")
        return result
    
    except Exception as e:
        logger.error(f"Tool failed: {e}", exc_info=True)
        raise
```

This documentation covers the core functionality and advanced features of the MCP Python SDK. For additional examples and community contributions, check the official repository and examples directory.