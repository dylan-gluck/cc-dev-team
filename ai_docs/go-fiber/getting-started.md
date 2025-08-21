---
source: https://docs.gofiber.io/
fetched: 2025-08-21
version: v2
framework: Go Fiber
---

# Go Fiber Quick Start Guide

## Overview

Go Fiber is an Express-inspired web framework built on top of Fasthttp, the fastest HTTP engine for Go. It's designed for fast development with zero memory allocation and performance in mind.

## Installation

### Prerequisites
- Go 1.17 or higher (for Fiber v2)
- Go 1.25 or higher (for Fiber v3 beta)

### Install Fiber v2 (Stable)
```bash
go get github.com/gofiber/fiber/v2
```

### Install Fiber v3 (Beta)
```bash
go get github.com/gofiber/fiber/v3
```

## Hello World Example

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

## Basic Concepts

### Creating an App
```go
app := fiber.New()

// With configuration
app := fiber.New(fiber.Config{
    CaseSensitive: true,
    StrictRouting: true,
    ServerHeader:  "Fiber",
    AppName:      "My App v1.0.0",
})
```

### Static File Serving
```go
// Serve files from ./public directory
app.Static("/", "./public")

// With prefix
app.Static("/static", "./public")

// With configuration
app.Static("/", "./public", fiber.Static{
    Compress:  true,
    ByteRange: true,
    Browse:    true,
})
```

### Starting the Server
```go
// Listen on port 3000
app.Listen(":3000")

// Listen with TLS
app.ListenTLS(":443", "./ssl/cert.pem", "./ssl/key.pem")

// Graceful shutdown
app.Shutdown()
```

## Key Features

- **High Performance**: Built on Fasthttp
- **Express-like**: Familiar API for Node.js developers
- **Zero Memory Allocation**: Optimized for performance
- **Middleware Support**: Extensive middleware ecosystem
- **Route Constraints**: Advanced parameter validation
- **Template Engines**: Support for multiple template engines

## Important Performance Notes

### Context Immutability
By default, context values are not immutable. For optimal performance:

- Use context values only within handlers
- Don't store context values beyond the handler scope
- Make copies if persistence is needed outside handlers

```go
// Correct usage within handler
app.Get("/user/:id", func(c *fiber.Ctx) error {
    userID := c.Params("id")
    return c.JSON(fiber.Map{"user_id": userID})
})

// If you need to store values, make a copy
app.Get("/async/:id", func(c *fiber.Ctx) error {
    userID := c.Params("id")
    userIDCopy := string(userID) // Make a copy
    
    go func() {
        // Use userIDCopy in goroutine
        processUser(userIDCopy)
    }()
    
    return c.SendStatus(202)
})
```

## Next Steps

- Learn about [routing patterns](./routing.md)
- Explore the [Context API](./context-api.md)
- Set up [middleware](./middleware.md)
- Handle [errors effectively](./error-handling.md)