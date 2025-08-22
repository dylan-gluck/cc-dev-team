---
source: https://docs.gofiber.io/guide/routing
fetched: 2025-08-21
version: v2
framework: Go Fiber
---

# Fiber Routing Guide

## HTTP Methods

Fiber supports all standard HTTP methods for defining routes:

```go
app.Get("/", handler)      // GET requests
app.Post("/", handler)     // POST requests
app.Put("/", handler)      // PUT requests
app.Delete("/", handler)   // DELETE requests
app.Patch("/", handler)    // PATCH requests
app.Options("/", handler)  // OPTIONS requests
app.Head("/", handler)     // HEAD requests
```

## Route Parameters

### Named Parameters
Use `:name` syntax for capturing URL segments:

```go
// Route: /user/:name
app.Get("/user/:name", func(c *fiber.Ctx) error {
    name := c.Params("name")
    return c.SendString("Hello " + name)
})

// Route: /user/:id/profile
app.Get("/user/:id/profile", func(c *fiber.Ctx) error {
    userID := c.Params("id")
    return c.JSON(fiber.Map{"user_id": userID})
})
```

### Optional Parameters
Add `?` to make parameters optional:

```go
// Route: /user/:name? (matches /user and /user/john)
app.Get("/user/:name?", func(c *fiber.Ctx) error {
    name := c.Params("name")
    if name == "" {
        return c.SendString("Hello Guest")
    }
    return c.SendString("Hello " + name)
})
```

### Wildcard Routes
Use `*` or `+` for greedy parameter matching:

```go
// Route: /files/* (matches /files/docs/readme.txt)
app.Get("/files/*", func(c *fiber.Ctx) error {
    path := c.Params("*")
    return c.SendString("File path: " + path)
})

// Route: /api/+ (requires at least one segment)
app.Get("/api/+", func(c *fiber.Ctx) error {
    path := c.Params("+")
    return c.SendString("API path: " + path)
})
```

## Route Constraints (v2.37.0+)

Add validation constraints to route parameters:

### Constraint Types
- `int`: Numeric values only
- `bool`: True/false values
- `min(value)`: Minimum value
- `max(value)`: Maximum value
- `minLen(length)`: Minimum string length
- `maxLen(length)`: Maximum string length
- `regex(pattern)`: Regular expression matching

### Examples

```go
// Age must be an integer
app.Get("/user/:age<int>", func(c *fiber.Ctx) error {
    age := c.Params("age")
    return c.SendString("Age: " + age)
})

// Age must be at least 18
app.Get("/adult/:age<min(18)>", func(c *fiber.Ctx) error {
    age := c.Params("age")
    return c.SendString("Adult age: " + age)
})

// Multiple constraints
app.Get("/product/:id<min(100);maxLen(5)>", func(c *fiber.Ctx) error {
    id := c.Params("id")
    return c.SendString("Product ID: " + id)
})

// Boolean parameter
app.Get("/feature/:enabled<bool>", func(c *fiber.Ctx) error {
    enabled := c.Params("enabled")
    return c.SendString("Feature enabled: " + enabled)
})

// Regex constraint
app.Get("/code/:zip<regex(^[0-9]{5}$)>", func(c *fiber.Ctx) error {
    zip := c.Params("zip")
    return c.SendString("ZIP code: " + zip)
})
```

## Route Groups

Group related routes with shared prefixes and middleware:

```go
// Create a route group
api := app.Group("/api")

// Add routes to the group
api.Get("/users", getUsersHandler)
api.Post("/users", createUserHandler)
api.Get("/users/:id", getUserHandler)

// Nested groups
v1 := api.Group("/v1")
v1.Get("/health", healthCheckHandler)

// Group with middleware
admin := app.Group("/admin", authMiddleware)
admin.Get("/dashboard", dashboardHandler)
admin.Delete("/users/:id", deleteUserHandler)
```

## Multiple Handlers

Chain multiple handlers for a single route:

```go
// Multiple middleware functions
app.Get("/protected", 
    authMiddleware,
    logMiddleware,
    protectedHandler,
)

// Using anonymous functions
app.Post("/upload",
    func(c *fiber.Ctx) error {
        // Validation middleware
        if c.Get("Content-Type") != "multipart/form-data" {
            return c.Status(400).SendString("Invalid content type")
        }
        return c.Next()
    },
    uploadHandler,
)
```

## Route Patterns

### Complex Route Examples

```go
// API versioning
app.Get("/api/v:version<int>/users/:id<int>", func(c *fiber.Ctx) error {
    version := c.Params("version")
    userID := c.Params("id")
    return c.JSON(fiber.Map{
        "version": version,
        "user_id": userID,
    })
})

// File extensions
app.Get("/files/:name.:ext", func(c *fiber.Ctx) error {
    name := c.Params("name")
    ext := c.Params("ext")
    return c.SendString("File: " + name + "." + ext)
})

// Subdomain routing (with middleware)
app.Use("subdomain", func(c *fiber.Ctx) error {
    subdomain := c.Subdomains()[0]
    c.Locals("subdomain", subdomain)
    return c.Next()
})
```

## Route Utilities

### Route Testing
```go
// Test routes without starting server
req := httptest.NewRequest("GET", "/user/123", nil)
resp, err := app.Test(req)
```

### Route Information
```go
// Get all registered routes
routes := app.GetRoutes()
for _, route := range routes {
    fmt.Printf("%s %s\n", route.Method, route.Path)
}
```

## Best Practices

1. **Use constraints** for parameter validation
2. **Group related routes** for better organization
3. **Apply middleware at group level** when possible
4. **Use descriptive parameter names** for clarity
5. **Test your routes** with the built-in test utilities