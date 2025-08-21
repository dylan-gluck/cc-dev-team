---
source: https://docs.gofiber.io/guide/error-handling
fetched: 2025-08-21
version: v2
framework: Go Fiber
---

# Fiber Error Handling Guide

## Error Handling Philosophy

Fiber uses Go's standard error handling approach but provides enhanced error management through:
- Custom error handlers
- Panic recovery middleware
- Structured error responses
- HTTP status code integration

## Basic Error Handling

### Returning Errors from Handlers

Always return errors from route handlers so Fiber can process them properly:

```go
app.Get("/user/:id", func(c *fiber.Ctx) error {
    userID := c.Params("id")
    
    // File operation that might fail
    if err := c.SendFile("./users/" + userID + ".json"); err != nil {
        return err // Let Fiber handle the error
    }
    
    return nil
})

app.Get("/data", func(c *fiber.Ctx) error {
    data, err := fetchDataFromAPI()
    if err != nil {
        return err // Return error to Fiber
    }
    
    return c.JSON(data)
})
```

## Custom Error Types

### Creating Fiber Errors

Use `fiber.NewError()` to create errors with specific HTTP status codes:

```go
import "github.com/gofiber/fiber/v2"

app.Get("/admin", func(c *fiber.Ctx) error {
    if !isAdmin(c) {
        return fiber.NewError(fiber.StatusForbidden, "Admin access required")
    }
    
    return c.SendString("Admin panel")
})

app.Get("/user/:id", func(c *fiber.Ctx) error {
    userID := c.Params("id")
    
    user, err := database.GetUser(userID)
    if err != nil {
        if errors.Is(err, database.ErrUserNotFound) {
            return fiber.NewError(fiber.StatusNotFound, "User not found")
        }
        return fiber.NewError(fiber.StatusInternalServerError, "Database error")
    }
    
    return c.JSON(user)
})
```

### Default Error Behavior

If you return a standard error (not `fiber.Error`):
- Status code defaults to `500 Internal Server Error`
- Error message becomes the response body

```go
app.Get("/fail", func(c *fiber.Ctx) error {
    return errors.New("something went wrong") // Returns 500 with "something went wrong"
})
```

## Custom Error Handler

Create a global error handler to customize error responses:

```go
app := fiber.New(fiber.Config{
    ErrorHandler: func(ctx *fiber.Ctx, err error) error {
        // Status code defaults to 500
        code := fiber.StatusInternalServerError
        message := "Internal Server Error"

        // Check if it's a Fiber error
        if e, ok := err.(*fiber.Error); ok {
            code = e.Code
            message = e.Message
        }

        // Log the error
        log.Printf("Error %d: %s", code, err.Error())

        // Send custom error page
        if code == fiber.StatusNotFound {
            return ctx.Status(code).SendFile("./errors/404.html")
        }

        // Send JSON error response
        return ctx.Status(code).JSON(fiber.Map{
            "success": false,
            "error":   message,
            "code":    code,
        })
    },
})
```

### Advanced Error Handler

```go
type ErrorResponse struct {
    Success   bool   `json:"success"`
    Error     string `json:"error"`
    Code      int    `json:"code"`
    Timestamp int64  `json:"timestamp"`
    RequestID string `json:"request_id,omitempty"`
}

app := fiber.New(fiber.Config{
    ErrorHandler: func(ctx *fiber.Ctx, err error) error {
        code := fiber.StatusInternalServerError
        message := "Internal Server Error"

        // Check error type
        var fiberErr *fiber.Error
        if errors.As(err, &fiberErr) {
            code = fiberErr.Code
            message = fiberErr.Message
        }

        // Get request ID if set
        requestID := ctx.Locals("requestId")
        var reqID string
        if requestID != nil {
            reqID = requestID.(string)
        }

        // Create error response
        errorResp := ErrorResponse{
            Success:   false,
            Error:     message,
            Code:      code,
            Timestamp: time.Now().Unix(),
            RequestID: reqID,
        }

        // Log error with context
        logger.WithFields(map[string]interface{}{
            "error":      err.Error(),
            "code":       code,
            "method":     ctx.Method(),
            "path":       ctx.Path(),
            "ip":         ctx.IP(),
            "request_id": reqID,
        }).Error("Request failed")

        return ctx.Status(code).JSON(errorResp)
    },
})
```

## Panic Recovery

Use the recover middleware to catch panics and prevent application crashes:

```go
import "github.com/gofiber/fiber/v2/middleware/recover"

app.Use(recover.New(recover.Config{
    EnableStackTrace: true,
}))

// This handler might panic
app.Get("/panic", func(c *fiber.Ctx) error {
    panic("something terrible happened!")
    return nil // This won't be reached
})
```

### Custom Panic Handler

```go
app.Use(recover.New(recover.Config{
    Handler: func(c *fiber.Ctx, err interface{}) {
        log.Printf("Panic caught: %v", err)
        c.Status(500).SendString("Internal Server Error")
    },
    EnableStackTrace: true,
}))
```

## Error Middleware

Create custom middleware for specific error handling:

```go
// Database error middleware
func DatabaseErrorMiddleware() fiber.Handler {
    return func(c *fiber.Ctx) error {
        err := c.Next()
        
        if err != nil {
            // Check for database-specific errors
            if strings.Contains(err.Error(), "connection refused") {
                return fiber.NewError(fiber.StatusServiceUnavailable, 
                    "Database temporarily unavailable")
            }
            
            if strings.Contains(err.Error(), "duplicate key") {
                return fiber.NewError(fiber.StatusConflict, 
                    "Resource already exists")
            }
        }
        
        return err
    }
}

// Apply middleware
app.Use("/api", DatabaseErrorMiddleware())
```

## Validation Errors

Handle validation errors with detailed responses:

```go
import "github.com/go-playground/validator/v10"

type CreateUserRequest struct {
    Name  string `json:"name" validate:"required,min=3"`
    Email string `json:"email" validate:"required,email"`
    Age   int    `json:"age" validate:"min=18"`
}

var validate = validator.New()

app.Post("/users", func(c *fiber.Ctx) error {
    var req CreateUserRequest
    
    if err := c.BodyParser(&req); err != nil {
        return fiber.NewError(fiber.StatusBadRequest, "Invalid JSON")
    }
    
    if err := validate.Struct(req); err != nil {
        var errors []string
        for _, err := range err.(validator.ValidationErrors) {
            errors = append(errors, fmt.Sprintf("%s is %s", 
                err.Field(), err.Tag()))
        }
        
        return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
            "success": false,
            "errors":  errors,
        })
    }
    
    // Create user
    user, err := createUser(req)
    if err != nil {
        return err
    }
    
    return c.Status(fiber.StatusCreated).JSON(user)
})
```

## Error Helpers

Create utility functions for common error scenarios:

```go
// Common error responses
func BadRequest(message string) error {
    return fiber.NewError(fiber.StatusBadRequest, message)
}

func NotFound(resource string) error {
    return fiber.NewError(fiber.StatusNotFound, fmt.Sprintf("%s not found", resource))
}

func Unauthorized(message string) error {
    return fiber.NewError(fiber.StatusUnauthorized, message)
}

func InternalError(message string) error {
    return fiber.NewError(fiber.StatusInternalServerError, message)
}

// Usage in handlers
app.Get("/user/:id", func(c *fiber.Ctx) error {
    userID := c.Params("id")
    
    if userID == "" {
        return BadRequest("User ID is required")
    }
    
    user, err := database.GetUser(userID)
    if err != nil {
        if errors.Is(err, database.ErrNotFound) {
            return NotFound("User")
        }
        return InternalError("Failed to fetch user")
    }
    
    return c.JSON(user)
})
```

## Testing Error Handling

Test your error handlers to ensure they work correctly:

```go
func TestErrorHandling(t *testing.T) {
    app := fiber.New(fiber.Config{
        ErrorHandler: customErrorHandler,
    })
    
    app.Get("/error", func(c *fiber.Ctx) error {
        return fiber.NewError(fiber.StatusBadRequest, "Test error")
    })
    
    req := httptest.NewRequest("GET", "/error", nil)
    resp, err := app.Test(req)
    
    assert.NoError(t, err)
    assert.Equal(t, fiber.StatusBadRequest, resp.StatusCode)
}
```

## Best Practices

1. **Always return errors** from handlers instead of handling them manually
2. **Use specific status codes** with `fiber.NewError()`
3. **Implement panic recovery** to prevent crashes
4. **Log errors** with sufficient context for debugging
5. **Provide meaningful error messages** to API consumers
6. **Use custom error handlers** for consistent error responses
7. **Validate input data** and return structured validation errors
8. **Don't expose internal errors** to clients in production