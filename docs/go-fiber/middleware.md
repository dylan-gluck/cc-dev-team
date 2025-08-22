---
source: https://docs.gofiber.io/
fetched: 2025-08-21
version: v2
framework: Go Fiber
---

# Fiber Middleware Guide

## Middleware Concept

Middleware functions are executed sequentially in the order they are registered. They can:
- Execute code before the next middleware/handler
- Modify the request or response
- End the request-response cycle
- Call the next middleware in the stack

## Built-in Middleware

Fiber provides many built-in middleware packages for common functionality:

```go
import (
    "github.com/gofiber/fiber/v2"
    "github.com/gofiber/fiber/v2/middleware/cors"
    "github.com/gofiber/fiber/v2/middleware/logger"
    "github.com/gofiber/fiber/v2/middleware/recover"
    "github.com/gofiber/fiber/v2/middleware/compress"
)

app := fiber.New()

// Logger middleware
app.Use(logger.New())

// Panic recovery
app.Use(recover.New())

// CORS
app.Use(cors.New(cors.Config{
    AllowOrigins: "https://example.com",
    AllowHeaders: "Origin, Content-Type, Accept",
}))

// Compression
app.Use(compress.New(compress.Config{
    Level: compress.LevelBestSpeed,
}))
```

## Common Built-in Middleware

### Logger Middleware
```go
app.Use(logger.New(logger.Config{
    Format: "[${ip}]:${port} ${status} - ${method} ${path}\n",
    TimeFormat: "15:04:05",
    TimeZone: "Local",
}))
```

### CORS Middleware
```go
app.Use(cors.New(cors.Config{
    AllowOrigins:     "https://example.com, https://app.example.com",
    AllowMethods:     "GET,POST,HEAD,PUT,DELETE,PATCH",
    AllowHeaders:     "Origin, Content-Type, Accept, Authorization",
    AllowCredentials: true,
    ExposeHeaders:    "Content-Length",
    MaxAge:          86400,
}))
```

### Rate Limiting
```go
import "github.com/gofiber/fiber/v2/middleware/limiter"

app.Use(limiter.New(limiter.Config{
    Max:        20,           // 20 requests
    Expiration: time.Minute,  // per minute
    KeyGenerator: func(c *fiber.Ctx) string {
        return c.IP() // Rate limit by IP
    },
    LimitReached: func(c *fiber.Ctx) error {
        return c.Status(429).JSON(fiber.Map{
            "error": "Too many requests",
        })
    },
}))
```

### Authentication Middleware
```go
import "github.com/gofiber/fiber/v2/middleware/basicauth"

app.Use(basicauth.New(basicauth.Config{
    Users: map[string]string{
        "admin": "password123",
        "user":  "user123",
    },
}))

// JWT middleware example (third-party)
import "github.com/gofiber/jwt/v3"

app.Use(jwtware.New(jwtware.Config{
    SigningKey: []byte("secret"),
    ErrorHandler: func(c *fiber.Ctx, err error) error {
        return c.Status(401).JSON(fiber.Map{
            "error": "Unauthorized",
        })
    },
}))
```

## Custom Middleware

### Simple Custom Middleware

```go
// Custom logging middleware
func CustomLogger() fiber.Handler {
    return func(c *fiber.Ctx) error {
        start := time.Now()
        
        // Process request
        err := c.Next()
        
        // Log after processing
        duration := time.Since(start)
        log.Printf("%s %s - %v", c.Method(), c.Path(), duration)
        
        return err
    }
}

// Usage
app.Use(CustomLogger())
```

### Authentication Middleware

```go
func AuthMiddleware() fiber.Handler {
    return func(c *fiber.Ctx) error {
        token := c.Get("Authorization")
        
        if token == "" {
            return c.Status(401).JSON(fiber.Map{
                "error": "Missing authorization token",
            })
        }
        
        // Validate token
        userID, err := validateToken(token)
        if err != nil {
            return c.Status(401).JSON(fiber.Map{
                "error": "Invalid token",
            })
        }
        
        // Store user info in context
        c.Locals("userID", userID)
        
        return c.Next()
    }
}

// Usage
app.Use("/api/protected", AuthMiddleware())
```

### Request Validation Middleware

```go
func ValidateJSON() fiber.Handler {
    return func(c *fiber.Ctx) error {
        if c.Method() == "POST" || c.Method() == "PUT" {
            contentType := c.Get("Content-Type")
            if !strings.Contains(contentType, "application/json") {
                return c.Status(400).JSON(fiber.Map{
                    "error": "Content-Type must be application/json",
                })
            }
        }
        
        return c.Next()
    }
}

func ValidateAPIKey() fiber.Handler {
    return func(c *fiber.Ctx) error {
        apiKey := c.Get("X-API-Key")
        
        if !isValidAPIKey(apiKey) {
            return c.Status(403).JSON(fiber.Map{
                "error": "Invalid API key",
            })
        }
        
        return c.Next()
    }
}
```

## Middleware Patterns

### Conditional Middleware

```go
func ConditionalAuth() fiber.Handler {
    return func(c *fiber.Ctx) error {
        // Skip auth for public endpoints
        if strings.HasPrefix(c.Path(), "/public") {
            return c.Next()
        }
        
        // Apply authentication for protected routes
        return AuthMiddleware()(c)
    }
}
```

### Middleware with Configuration

```go
type LoggerConfig struct {
    SkipPaths []string
    Format    string
}

func NewLogger(config LoggerConfig) fiber.Handler {
    return func(c *fiber.Ctx) error {
        // Skip logging for certain paths
        for _, path := range config.SkipPaths {
            if c.Path() == path {
                return c.Next()
            }
        }
        
        // Custom logging logic
        log.Printf(config.Format, c.Method(), c.Path())
        
        return c.Next()
    }
}

// Usage
app.Use(NewLogger(LoggerConfig{
    SkipPaths: []string{"/health", "/metrics"},
    Format:    "%s %s",
}))
```

### Request ID Middleware

```go
import "github.com/google/uuid"

func RequestID() fiber.Handler {
    return func(c *fiber.Ctx) error {
        // Generate unique request ID
        requestID := uuid.New().String()
        
        // Set in response header
        c.Set("X-Request-ID", requestID)
        
        // Store in context for use in handlers
        c.Locals("requestID", requestID)
        
        return c.Next()
    }
}
```

## Middleware Execution Order

```go
app := fiber.New()

// Global middleware (executed for all routes)
app.Use(logger.New())
app.Use(recover.New())
app.Use(cors.New())

// Group-specific middleware
api := app.Group("/api", ValidateAPIKey())
api.Use(RequestID()) // Only for /api routes

v1 := api.Group("/v1", AuthMiddleware()) // Only for /api/v1 routes

// Route-specific middleware
app.Get("/admin", AdminAuthMiddleware(), adminHandler)

// Multiple middleware for a single route
app.Post("/upload", 
    ValidateFileType(),
    CheckFileSize(),
    uploadHandler,
)
```

## Error Handling in Middleware

```go
func ErrorHandlingMiddleware() fiber.Handler {
    return func(c *fiber.Ctx) error {
        err := c.Next()
        
        if err != nil {
            // Log the error
            log.Printf("Error in %s %s: %v", c.Method(), c.Path(), err)
            
            // Don't modify the error, just log it
            return err
        }
        
        return nil
    }
}

func DatabaseMiddleware() fiber.Handler {
    return func(c *fiber.Ctx) error {
        // Setup database connection
        db, err := connectToDatabase()
        if err != nil {
            return fiber.NewError(503, "Database unavailable")
        }
        defer db.Close()
        
        // Store in context
        c.Locals("db", db)
        
        return c.Next()
    }
}
```

## Performance Middleware

### Caching Middleware

```go
import "github.com/gofiber/fiber/v2/middleware/cache"

app.Use(cache.New(cache.Config{
    Expiration:   30 * time.Minute,
    CacheControl: true,
    KeyGenerator: func(c *fiber.Ctx) string {
        return c.Path() + "?" + c.Request().URI().QueryString()
    },
}))
```

### Compression Middleware

```go
import "github.com/gofiber/fiber/v2/middleware/compress"

app.Use(compress.New(compress.Config{
    Level: compress.LevelBestSpeed, // -1 default, 0-9
}))
```

## Testing Middleware

```go
func TestAuthMiddleware(t *testing.T) {
    app := fiber.New()
    app.Use(AuthMiddleware())
    app.Get("/test", func(c *fiber.Ctx) error {
        return c.SendString("success")
    })
    
    // Test without token
    req := httptest.NewRequest("GET", "/test", nil)
    resp, _ := app.Test(req)
    assert.Equal(t, 401, resp.StatusCode)
    
    // Test with valid token
    req = httptest.NewRequest("GET", "/test", nil)
    req.Header.Set("Authorization", "Bearer valid-token")
    resp, _ = app.Test(req)
    assert.Equal(t, 200, resp.StatusCode)
}
```

## Best Practices

1. **Order matters**: Apply middleware in logical order (logging → recovery → auth → business logic)
2. **Use `c.Next()`** to continue the middleware chain
3. **Handle errors properly** by returning them or creating new ones
4. **Store data** in `c.Locals()` for request-scoped sharing
5. **Keep middleware focused** on single responsibilities
6. **Test your middleware** independently
7. **Consider performance** impact of middleware order
8. **Use built-in middleware** when possible instead of rolling your own