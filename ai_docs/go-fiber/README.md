---
source: https://docs.gofiber.io/
fetched: 2025-08-21
version: v2
framework: Go Fiber
---

# Go Fiber Documentation Reference

## Overview

Go Fiber is an Express-inspired web framework built on top of Fasthttp, the fastest HTTP engine for Go. It's designed for fast development with zero memory allocation and performance in mind.

### Key Features

- **High Performance**: Built on Fasthttp for maximum speed
- **Express-like API**: Familiar syntax for Node.js developers  
- **Zero Memory Allocation**: Optimized for performance
- **Extensive Middleware**: Rich ecosystem of middleware
- **Route Constraints**: Advanced parameter validation
- **Template Support**: Multiple template engines
- **WebSocket Support**: Real-time communication
- **Testing Utilities**: Built-in testing helpers

### Version Information

- **Fiber v2**: Stable (requires Go 1.17+)
- **Fiber v3**: Beta (requires Go 1.25+)
- **Official Docs**: https://docs.gofiber.io/

## Documentation Index

### Core Concepts

1. **[Getting Started](./getting-started.md)**
   - Installation and setup
   - Hello World example
   - Basic configuration
   - Performance considerations

2. **[Routing](./routing.md)**
   - HTTP methods
   - Route parameters
   - Wildcards and constraints
   - Route groups
   - Advanced patterns

3. **[Context API](./context-api.md)**
   - Request handling
   - Response methods
   - Parameter extraction
   - Headers and cookies
   - File operations

### Advanced Features

4. **[Middleware](./middleware.md)**
   - Built-in middleware
   - Custom middleware creation
   - Middleware patterns
   - Performance middleware

5. **[Error Handling](./error-handling.md)**
   - Error handling philosophy
   - Custom error handlers
   - Panic recovery
   - Validation errors

6. **[App Configuration](./app-configuration.md)**
   - App setup and configuration
   - Server management
   - Static file serving
   - Sub-app mounting
   - Testing utilities

## Quick Reference

### Installation
```bash
go get github.com/gofiber/fiber/v2
```

### Minimal Example
```go
package main

import "github.com/gofiber/fiber/v2"

func main() {
    app := fiber.New()
    
    app.Get("/", func(c *fiber.Ctx) error {
        return c.SendString("Hello, World!")
    })
    
    app.Listen(":3000")
}
```

### Common Patterns

#### JSON API
```go
app.Get("/api/users/:id", func(c *fiber.Ctx) error {
    userID := c.Params("id")
    
    user, err := getUserByID(userID)
    if err != nil {
        return c.Status(404).JSON(fiber.Map{
            "error": "User not found",
        })
    }
    
    return c.JSON(user)
})
```

#### Middleware Usage
```go
import "github.com/gofiber/fiber/v2/middleware/cors"
import "github.com/gofiber/fiber/v2/middleware/logger"

app.Use(logger.New())
app.Use(cors.New())
```

#### Route Groups
```go
api := app.Group("/api/v1")
api.Get("/users", getUsersHandler)
api.Post("/users", createUserHandler)
```

## Best Practices

1. **Performance**
   - Don't store context values beyond handler scope
   - Use `c.Locals()` for request-scoped data
   - Make copies if persistence is needed

2. **Error Handling**
   - Always return errors from handlers
   - Use `fiber.NewError()` for HTTP status codes
   - Implement global error handlers

3. **Middleware**
   - Apply middleware in logical order
   - Use built-in middleware when available
   - Test middleware independently

4. **Testing**
   - Use `app.Test()` for route testing
   - Test error scenarios
   - Validate middleware behavior

5. **Configuration**
   - Use environment-specific configurations
   - Implement graceful shutdown
   - Monitor performance metrics

## Common Use Cases

- **REST APIs**: High-performance API backends
- **Microservices**: Lightweight service architectures  
- **Web Applications**: Server-side rendered apps
- **Proxy Services**: Request routing and load balancing
- **Real-time Apps**: WebSocket-based applications

## Migration from Express.js

Fiber's API is designed to be familiar to Express.js developers:

| Express.js | Fiber |
|------------|--------|
| `app.get()` | `app.Get()` |
| `req.params` | `c.Params()` |
| `req.query` | `c.Query()` |
| `res.json()` | `c.JSON()` |
| `res.send()` | `c.SendString()` |
| `req.body` | `c.Body()` / `c.BodyParser()` |

## Resources

- **Official Documentation**: https://docs.gofiber.io/
- **GitHub Repository**: https://github.com/gofiber/fiber
- **Community Discord**: Active community support
- **Examples**: Comprehensive example repository
- **Benchmarks**: Performance comparisons available

## Contributing

Fiber is an open-source project welcoming contributions:
- Bug reports and feature requests
- Documentation improvements  
- Code contributions
- Community support

---

*This documentation was condensed from the official Fiber documentation for quick reference and practical implementation guidance.*