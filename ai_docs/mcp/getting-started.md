---
source: https://modelcontextprotocol.io/docs, https://github.com/modelcontextprotocol/python-sdk
fetched: 2025-08-20
version: 2025-06-18
---

# MCP Getting Started Guide

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Understanding MCP Components](#understanding-mcp-components)
- [Building Your First Server](#building-your-first-server)
- [Testing Your Server](#testing-your-server)
- [Connecting to a Client](#connecting-to-a-client)
- [Next Steps](#next-steps)

## Prerequisites

### System Requirements
- Python 3.8+ (recommended: Python 3.11+)
- pip or uv package manager
- Basic understanding of JSON-RPC and async programming

### Recommended Tools
- **uv**: Modern Python package manager (faster than pip)
- **Claude Desktop**: For testing MCP servers
- **IDE**: VS Code, PyCharm, or similar with Python support

## Installation

### Option 1: Using uv (Recommended)
```bash
# Install uv if you don't have it
curl -LsSf https://astral.sh/uv/install.sh | sh

# Add MCP to your project
uv add "mcp[cli]"

# For development with additional tools
uv add "mcp[cli,dev]"
```

### Option 2: Using pip
```bash
# Basic installation
pip install "mcp[cli]"

# With development dependencies
pip install "mcp[cli,dev]"
```

### Verify Installation
```bash
# Check MCP CLI tools
uv run mcp --help

# Or with pip
mcp --help
```

## Quick Start

### Create Your First MCP Server

Create a simple calculator server in `calculator.py`:

```python
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("Calculator")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers together."""
    return a * b

@mcp.resource("config://calculator")
def get_config() -> dict:
    """Get calculator configuration."""
    return {
        "name": "Simple Calculator",
        "version": "1.0.0",
        "operations": ["add", "multiply"]
    }

if __name__ == "__main__":
    mcp.run()
```

### Run Your Server
```bash
# Development mode with auto-reload
uv run mcp dev calculator.py

# Production mode
uv run python calculator.py
```

## Understanding MCP Components

### Tools
Tools are functions that the AI can call to perform actions:

```python
@mcp.tool()
def get_weather(city: str, units: str = "celsius") -> dict:
    """Get current weather for a city."""
    # Your implementation here
    return {
        "city": city,
        "temperature": 22,
        "units": units,
        "condition": "sunny"
    }
```

### Resources
Resources provide context and data to the AI:

```python
@mcp.resource("file://{path}")
def read_file(path: str) -> str:
    """Read contents of a file."""
    with open(path, 'r') as f:
        return f.read()

@mcp.resource("data://users")
def get_users() -> list:
    """Get list of users."""
    return [
        {"id": 1, "name": "Alice"},
        {"id": 2, "name": "Bob"}
    ]
```

### Prompts
Prompts define interaction templates:

```python
@mcp.prompt()
def analyze_code(code: str, language: str = "python") -> str:
    """Generate a prompt for code analysis."""
    return f"""
    Please analyze this {language} code:
    
    ```{language}
    {code}
    ```
    
    Provide feedback on:
    - Code quality
    - Potential issues
    - Improvement suggestions
    """
```

## Building Your First Server

Let's build a more comprehensive file management server:

```python
import os
import json
from pathlib import Path
from typing import List, Dict
from mcp.server.fastmcp import FastMCP

# Initialize server
mcp = FastMCP("FileManager")

@mcp.tool()
def list_directory(path: str) -> List[Dict[str, str]]:
    """List contents of a directory."""
    try:
        items = []
        for item in Path(path).iterdir():
            items.append({
                "name": item.name,
                "type": "directory" if item.is_dir() else "file",
                "size": str(item.stat().st_size) if item.is_file() else None
            })
        return items
    except Exception as e:
        raise ValueError(f"Error listing directory: {e}")

@mcp.tool()
def create_file(path: str, content: str) -> str:
    """Create a new file with specified content."""
    try:
        Path(path).write_text(content)
        return f"File created successfully: {path}"
    except Exception as e:
        raise ValueError(f"Error creating file: {e}")

@mcp.resource("file://{path}")
def read_file_resource(path: str) -> str:
    """Read file contents as a resource."""
    try:
        return Path(path).read_text()
    except Exception as e:
        raise ValueError(f"Error reading file: {e}")

@mcp.resource("directory://{path}")
def directory_info(path: str) -> Dict:
    """Get directory information."""
    try:
        dir_path = Path(path)
        files = sum(1 for x in dir_path.iterdir() if x.is_file())
        dirs = sum(1 for x in dir_path.iterdir() if x.is_dir())
        
        return {
            "path": str(dir_path.absolute()),
            "files": files,
            "directories": dirs,
            "total_items": files + dirs
        }
    except Exception as e:
        raise ValueError(f"Error accessing directory: {e}")

@mcp.prompt()
def file_analysis_prompt(file_path: str) -> str:
    """Generate a prompt for file analysis."""
    return f"""
    Please analyze the file at: {file_path}
    
    Consider:
    1. File structure and organization
    2. Content quality and clarity
    3. Potential improvements
    4. Security considerations
    
    Provide a comprehensive analysis.
    """

if __name__ == "__main__":
    mcp.run()
```

## Testing Your Server

### Using MCP CLI Tools
```bash
# Run in development mode
uv run mcp dev file_manager.py

# Test specific functionality
uv run mcp test file_manager.py
```

### Manual Testing
Create a test script `test_server.py`:

```python
import asyncio
from mcp.client.stdio import StdioServerParameters, stdio_client

async def test_server():
    # Connect to server
    server_params = StdioServerParameters(
        command="python",
        args=["file_manager.py"]
    )
    
    async with stdio_client(server_params) as client:
        # List available tools
        tools = await client.list_tools()
        print("Available tools:", [tool.name for tool in tools.tools])
        
        # Test a tool
        result = await client.call_tool("list_directory", {"path": "."})
        print("Directory listing:", result.content)

if __name__ == "__main__":
    asyncio.run(test_server())
```

## Connecting to a Client

### Claude Desktop Integration

1. **Find Claude Desktop Config**:
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%/Claude/claude_desktop_config.json`

2. **Add Your Server**:
```json
{
  "mcpServers": {
    "file-manager": {
      "command": "uv",
      "args": ["run", "python", "/path/to/your/file_manager.py"]
    }
  }
}
```

3. **Restart Claude Desktop** and your server will be available.

### VS Code Integration
Install the MCP extension and configure your workspace:

```json
// .vscode/settings.json
{
  "mcp.servers": [
    {
      "name": "file-manager",
      "command": "python",
      "args": ["file_manager.py"],
      "cwd": "${workspaceFolder}"
    }
  ]
}
```

## Next Steps

### Development Best Practices
1. **Error Handling**: Always wrap operations in try-catch blocks
2. **Type Hints**: Use proper type annotations for better integration
3. **Documentation**: Provide clear docstrings for all tools/resources
4. **Testing**: Write unit tests for your server functionality
5. **Logging**: Use proper logging for debugging and monitoring

### Advanced Features
- **Structured Output**: Return complex data types with Pydantic models
- **Authentication**: Implement security for sensitive operations  
- **Configuration**: Support environment-based configuration
- **Monitoring**: Add health checks and performance metrics

### Community Resources
- [MCP Server Registry](https://github.com/modelcontextprotocol/servers)
- [Official Examples](https://github.com/modelcontextprotocol/python-sdk/tree/main/examples)
- [Community Discord](https://discord.gg/modelcontextprotocol)
- [GitHub Discussions](https://github.com/modelcontextprotocol/python-sdk/discussions)

### Troubleshooting

#### Common Issues
1. **Import Errors**: Ensure MCP is properly installed
2. **Connection Failures**: Check server startup logs
3. **Tool Not Found**: Verify tool registration and spelling
4. **Permission Errors**: Check file system permissions

#### Debug Mode
Run servers with verbose logging:
```bash
uv run mcp dev --verbose your_server.py
```

#### Log Analysis
Check MCP logs for detailed error information:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

This guide covers the essentials for getting started with MCP. For more advanced topics, see the Python SDK documentation and API reference.