---
source: https://docs.gofiber.io/api/app
fetched: 2025-08-21
version: v2
framework: Go Fiber
---

# Fiber App Configuration & Advanced Features

## App Creation and Configuration

### Basic App Creation

```go
app := fiber.New()
```

### App with Configuration

```go
app := fiber.New(fiber.Config{
    // Server settings
    ServerHeader:          "Fiber",
    AppName:              "My App v1.0.0",
    CaseSensitive:        true,
    StrictRouting:        true,
    UnescapePath:         false,
    
    // Body limits
    BodyLimit:            4 * 1024 * 1024, // 4MB
    
    // Timeouts
    ReadTimeout:          time.Second * 10,
    WriteTimeout:         time.Second * 10,
    IdleTimeout:          time.Second * 120,
    
    // Error handling
    ErrorHandler:         customErrorHandler,
    
    // Template engine
    Views:               engine,
    ViewsLayout:         "embed",
    
    // JSON settings
    JSONEncoder:         json.Marshal,
    JSONDecoder:         json.Unmarshal,
    
    // Network settings
    Network:             "tcp",
    EnableIPValidation:  false,
    EnableTrustedProxyCheck: false,
    TrustedProxies:      []string{"127.0.0.1"},
    
    // Performance
    Prefork:             false,
    DisableKeepalive:    false,
    DisableDefaultDate:  false,
    DisableDefaultContentType: false,
    
    // Compression
    CompressedFileSuffix: ".fiber.gz",
    
    // Request ID
    EnablePrintRoutes:   false,
})
```

## Server Management

### Starting the Server

```go
// Basic listen
app.Listen(":3000")

// Listen with custom address
app.Listen("127.0.0.1:8080")

// Listen with TLS
app.ListenTLS(":443", "./ssl/cert.pem", "./ssl/key.pem")

// Listen with mutual TLS
app.ListenMutualTLS(":443", "./ssl/cert.pem", "./ssl/key.pem", "./ssl/ca.pem")

// Listen with custom listener
ln, _ := net.Listen("tcp", ":3000")
app.Listener(ln)
```

### Graceful Shutdown

```go
// Basic shutdown
app.Shutdown()

// Shutdown with timeout
app.ShutdownWithTimeout(30 * time.Second)

// Shutdown with context
ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
defer cancel()
app.ShutdownWithContext(ctx)

// Graceful shutdown pattern
c := make(chan os.Signal, 1)
signal.Notify(c, os.Interrupt, syscall.SIGTERM)

go func() {
    <-c
    log.Println("Gracefully shutting down...")
    app.Shutdown()
}()

app.Listen(":3000")
```

## Static File Serving

### Basic Static Files

```go
// Serve files from ./public
app.Static("/", "./public")

// Serve with prefix
app.Static("/static", "./public")
```

### Advanced Static Configuration

```go
app.Static("/", "./public", fiber.Static{
    // Enable compression
    Compress:      true,
    
    // Enable byte range requests
    ByteRange:     true,
    
    // Enable directory browsing
    Browse:        true,
    
    // Custom index files
    Index:         "index.html",
    
    // Cache control
    CacheDuration: 10 * time.Second,
    MaxAge:        3600,
    
    // File modification
    ModifyResponse: func(c *fiber.Ctx) error {
        c.Set("Custom-Header", "value")
        return nil
    },
    
    // File serving rules
    Next: func(c *fiber.Ctx) bool {
        // Skip for API routes
        return strings.HasPrefix(c.Path(), "/api")
    },
})
```

## Mounting Sub-Applications

### Basic Mounting

```go
// Create micro-service
microApp := fiber.New()
microApp.Get("/health", healthHandler)
microApp.Get("/status", statusHandler)

// Mount at prefix
app.Mount("/micro", microApp)

// Now accessible at:
// /micro/health
// /micro/status
```

### Complex Mounting Example

```go
// API v1
apiV1 := fiber.New()
apiV1.Get("/users", getUsersV1)
apiV1.Get("/posts", getPostsV1)

// API v2
apiV2 := fiber.New()
apiV2.Get("/users", getUsersV2)
apiV2.Get("/posts", getPostsV2)

// Admin panel
admin := fiber.New()
admin.Use(authMiddleware)
admin.Get("/dashboard", dashboardHandler)

// Mount all sub-apps
app.Mount("/api/v1", apiV1)
app.Mount("/api/v2", apiV2)
app.Mount("/admin", admin)
```

## Route Groups

### Basic Grouping

```go
api := app.Group("/api")
api.Get("/users", getUsersHandler)
api.Post("/users", createUserHandler)

v1 := api.Group("/v1")
v1.Get("/health", healthHandler)
```

### Groups with Middleware

```go
api := app.Group("/api", func(c *fiber.Ctx) error {
    c.Set("API-Version", "1.0")
    return c.Next()
})

protected := api.Group("/protected", authMiddleware)
protected.Get("/profile", profileHandler)
protected.Put("/profile", updateProfileHandler)

admin := app.Group("/admin", 
    authMiddleware,
    adminMiddleware,
    auditLogMiddleware,
)
admin.Get("/users", adminUsersHandler)
admin.Delete("/users/:id", deleteUserHandler)
```

## Testing Utilities

### Basic Testing

```go
func TestRoutes(t *testing.T) {
    app := fiber.New()
    app.Get("/test", func(c *fiber.Ctx) error {
        return c.SendString("test response")
    })
    
    req := httptest.NewRequest("GET", "/test", nil)
    resp, err := app.Test(req)
    
    assert.NoError(t, err)
    assert.Equal(t, 200, resp.StatusCode)
    
    body, _ := io.ReadAll(resp.Body)
    assert.Equal(t, "test response", string(body))
}
```

### Advanced Testing

```go
func TestWithTimeout(t *testing.T) {
    app := fiber.New()
    app.Get("/slow", func(c *fiber.Ctx) error {
        time.Sleep(2 * time.Second)
        return c.SendString("slow response")
    })
    
    req := httptest.NewRequest("GET", "/slow", nil)
    
    // Test with custom timeout
    resp, err := app.Test(req, 5000) // 5 second timeout
    
    assert.NoError(t, err)
    assert.Equal(t, 200, resp.StatusCode)
}

func TestJSONAPI(t *testing.T) {
    app := fiber.New()
    app.Post("/api/users", func(c *fiber.Ctx) error {
        var user User
        if err := c.BodyParser(&user); err != nil {
            return c.Status(400).JSON(fiber.Map{"error": "Invalid JSON"})
        }
        return c.Status(201).JSON(user)
    })
    
    userData := `{"name":"John","email":"john@example.com"}`
    req := httptest.NewRequest("POST", "/api/users", strings.NewReader(userData))
    req.Header.Set("Content-Type", "application/json")
    
    resp, err := app.Test(req)
    
    assert.NoError(t, err)
    assert.Equal(t, 201, resp.StatusCode)
}
```

## App Introspection

### Route Information

```go
// Get all registered routes
routes := app.GetRoutes()
for _, route := range routes {
    fmt.Printf("%s %s -> %s\n", route.Method, route.Path, route.Name)
}

// Get route stack
stack := app.Stack()
for method, routes := range stack {
    fmt.Printf("Method: %s\n", method)
    for _, route := range routes {
        fmt.Printf("  %s\n", route.Path)
    }
}
```

### App Configuration

```go
// Get read-only config
config := app.Config()
fmt.Printf("App Name: %s\n", config.AppName)
fmt.Printf("Body Limit: %d\n", config.BodyLimit)
```

## Hooks System

```go
// Get hooks instance
hooks := app.Hooks()

// Add hooks for lifecycle events
hooks.OnRoute(func(route fiber.Route) error {
    fmt.Printf("Route registered: %s %s\n", route.Method, route.Path)
    return nil
})

hooks.OnName(func(route fiber.Route) error {
    fmt.Printf("Route named: %s -> %s\n", route.Path, route.Name)
    return nil
})

hooks.OnGroup(func(group fiber.Group) error {
    fmt.Printf("Group created: %s\n", group.Prefix)
    return nil
})

hooks.OnGroupName(func(group fiber.Group) error {
    fmt.Printf("Group named: %s\n", group.Prefix)
    return nil
})

hooks.OnListen(func() error {
    fmt.Println("Server is starting...")
    return nil
})

hooks.OnShutdown(func() error {
    fmt.Println("Server is shutting down...")
    return nil
})
```

## Custom Listeners

### TCP Listener

```go
ln, err := net.Listen("tcp", ":3000")
if err != nil {
    log.Fatal(err)
}

app.Listener(ln)
```

### Unix Socket

```go
ln, err := net.Listen("unix", "/tmp/app.sock")
if err != nil {
    log.Fatal(err)
}

app.Listener(ln)
```

### TLS Listener

```go
cert, err := tls.LoadX509KeyPair("cert.pem", "key.pem")
if err != nil {
    log.Fatal(err)
}

config := &tls.Config{Certificates: []tls.Certificate{cert}}
ln, err := tls.Listen("tcp", ":443", config)
if err != nil {
    log.Fatal(err)
}

app.Listener(ln)
```

## Performance Optimization

### Prefork Mode

```go
app := fiber.New(fiber.Config{
    Prefork: true, // Enable prefork for production
})
```

### Disable Features for Performance

```go
app := fiber.New(fiber.Config{
    DisableKeepalive:           true,  // Disable HTTP keep-alive
    DisableDefaultDate:         true,  // Don't send Date header
    DisableDefaultContentType:  true,  // Don't set default Content-Type
    DisableHeaderNormalizing:   true,  // Don't normalize headers
    DisableStartupMessage:      true,  // Don't show startup banner
})
```

## Best Practices

1. **Use configuration** for production vs development settings
2. **Implement graceful shutdown** for production deployments
3. **Mount sub-apps** for microservice architectures
4. **Use route groups** to organize related endpoints
5. **Test your routes** with the built-in test utilities
6. **Monitor route registration** with hooks in development
7. **Configure static serving** appropriately for your use case
8. **Optimize settings** for your specific performance requirements