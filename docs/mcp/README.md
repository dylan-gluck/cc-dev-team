---
source: https://modelcontextprotocol.io, https://github.com/modelcontextprotocol/python-sdk
fetched: 2025-08-20
version: 2025-06-18
---

# Model Context Protocol (MCP) Documentation

Comprehensive documentation for the Model Context Protocol (MCP) - an open protocol that standardizes how AI applications provide context to large language models.

## Quick Navigation

### 📚 Core Documentation
- **[Overview](overview.md)** - Core concepts, architecture, and protocol fundamentals
- **[Getting Started](getting-started.md)** - Installation, setup, and your first MCP server
- **[Python SDK](python-sdk.md)** - Comprehensive Python SDK reference and implementation guide
- **[API Reference](api-reference.md)** - Complete API documentation and method signatures
- **[Examples](examples.md)** - Practical code examples and implementation patterns

### 🚀 Quick Start

1. **Install MCP Python SDK**:
   ```bash
   uv add "mcp[cli]"
   # or
   pip install "mcp[cli]"
   ```

2. **Create a simple server**:
   ```python
   from mcp.server.fastmcp import FastMCP
   
   mcp = FastMCP("MyServer")
   
   @mcp.tool()
   def add(a: int, b: int) -> int:
       """Add two numbers."""
       return a + b
   
   if __name__ == "__main__":
       mcp.run()
   ```

3. **Run your server**:
   ```bash
   uv run mcp dev server.py
   ```

## What is MCP?

The Model Context Protocol (MCP) is an open protocol released by Anthropic in November 2024 that provides a standardized way for AI applications to connect with external data sources and tools. Think of it as "USB-C for AI applications."

### Key Benefits
- **Standardization**: One protocol for all AI tool integrations
- **Flexibility**: Easy switching between AI models and vendors
- **Security**: Keep data within your infrastructure
- **Modularity**: Compose complex workflows from simple components

### Core Architecture

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  MCP Host   │◄──►│ MCP Client  │◄──►│ MCP Server  │
│             │    │             │    │             │
│ (AI App)    │    │ (Protocol)  │    │ (Tools/Data)│
└─────────────┘    └─────────────┘    └─────────────┘
```

## Documentation Structure

### [Overview](overview.md)
- Protocol fundamentals and core concepts
- Client-server architecture details
- Communication flow and message handling
- Version management and capabilities

### [Getting Started](getting-started.md)
- Installation and environment setup
- Building your first MCP server
- Testing and debugging techniques
- Integration with Claude Desktop and other clients

### [Python SDK](python-sdk.md)
- FastMCP framework for rapid development
- Server and client implementation patterns
- Type system and structured output
- Advanced features and performance optimization

### [Examples](examples.md)
- File system management server
- Database integration examples
- API integration patterns
- Production deployment templates

### [API Reference](api-reference.md)
- Complete class and method documentation
- Type definitions and schemas
- Error handling and exception types
- Protocol message formats

## Common Use Cases

### Development Tools
- IDE integrations and code analysis
- Project management and task tracking
- Git operations and repository management
- Testing and deployment automation

### Data Access
- Database connectivity and queries
- File system operations
- API integrations and external services
- Content management systems

### Business Applications
- Customer relationship management
- Document processing and analysis
- Workflow automation
- Analytics and reporting

## Implementation Patterns

### Server Development
```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("BusinessServer")

@mcp.tool()
def query_database(sql: str) -> list:
    """Execute database query safely."""
    # Implementation here
    pass

@mcp.resource("customer://{id}")
def get_customer(id: str) -> dict:
    """Get customer information."""
    # Implementation here
    pass

@mcp.prompt()
def generate_report(data_source: str) -> str:
    """Generate analysis prompt for data."""
    return f"Please analyze data from: {data_source}"
```

### Client Integration
```python
import asyncio
from mcp.client.stdio import StdioServerParameters, stdio_client

async def use_mcp_server():
    params = StdioServerParameters(
        command="python",
        args=["business_server.py"]
    )
    
    async with stdio_client(params) as client:
        await client.initialize()
        
        # Use tools
        result = await client.call_tool("query_database", {
            "sql": "SELECT * FROM customers LIMIT 10"
        })
        
        # Read resources
        customer = await client.read_resource("customer://123")
```

## Version Information

- **Protocol Version**: 2025-06-18
- **Python SDK**: Latest stable release
- **Documentation Last Updated**: 2025-08-20

## Getting Help

### Official Resources
- [MCP Official Website](https://modelcontextprotocol.io)
- [Python SDK Repository](https://github.com/modelcontextprotocol/python-sdk)
- [Protocol Specification](https://modelcontextprotocol.io/specification)
- [Server Registry](https://github.com/modelcontextprotocol/servers)

### Community
- [GitHub Discussions](https://github.com/modelcontextprotocol/python-sdk/discussions)
- [Community Discord](https://discord.gg/modelcontextprotocol)
- [Example Servers](https://github.com/modelcontextprotocol/servers)

### Development Support
- [Issue Tracker](https://github.com/modelcontextprotocol/python-sdk/issues)
- [Contributing Guide](https://github.com/modelcontextprotocol/python-sdk/blob/main/CONTRIBUTING.md)
- [SDK Examples](https://github.com/modelcontextprotocol/python-sdk/tree/main/examples)

## Best Practices

### Security
- Validate all inputs in tools and resources
- Implement proper authentication for sensitive operations
- Use environment variables for API keys and secrets
- Limit file system access to allowed directories

### Performance
- Use async/await for I/O operations
- Implement caching for expensive computations
- Batch operations when possible
- Monitor memory usage for large datasets

### Error Handling
- Provide meaningful error messages
- Use appropriate HTTP status codes
- Log errors for debugging
- Implement graceful degradation

### Testing
- Write unit tests for all tools and resources
- Use integration tests for client-server interactions
- Mock external dependencies
- Test error conditions and edge cases

## Migration and Updates

### Staying Current
- Monitor the official repository for updates
- Subscribe to release notifications
- Review changelog for breaking changes
- Test updates in development environment first

### Version Compatibility
- MCP uses date-based versioning (YYYY-MM-DD)
- Backward compatibility maintained within versions
- Version negotiation during client-server handshake
- Graceful handling of version mismatches

This documentation provides everything needed to understand, implement, and deploy MCP servers and clients. Start with the [Getting Started](getting-started.md) guide for hands-on implementation, or dive into [Overview](overview.md) for conceptual understanding.