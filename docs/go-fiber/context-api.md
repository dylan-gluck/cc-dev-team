---
source: https://docs.gofiber.io/api/ctx
fetched: 2025-08-21
version: v2
framework: Go Fiber
---

# Fiber Context API Reference

The Fiber Context (`*fiber.Ctx`) is the most important part of Fiber. It contains all the HTTP request and response functionality.

## Request Information

### Parameters and Query Strings

```go
// Route parameters
userID := c.Params("id")           // /user/:id
name := c.Params("name", "Guest")  // with default value

// Query parameters
page := c.Query("page")            // ?page=1
limit := c.Query("limit", "10")    // with default value

// All query parameters
queries := c.Queries()             // map[string]string

// Form values
email := c.FormValue("email")
password := c.FormValue("password", "default")
```

### Request Body

```go
// Get raw body
body := c.Body()

// Parse JSON into struct
type User struct {
    Name  string `json:"name"`
    Email string `json:"email"`
}

var user User
if err := c.BodyParser(&user); err != nil {
    return c.Status(400).SendString("Invalid JSON")
}

// Parse form data
var user User
if err := c.BodyParser(&user); err != nil {
    return c.Status(400).SendString("Invalid form data")
}

// Parse multipart form
form, err := c.MultipartForm()
if err != nil {
    return err
}
```

### Headers

```go
// Get request headers
contentType := c.Get("Content-Type")
auth := c.Get("Authorization")

// Get all headers
headers := c.GetReqHeaders()

// Check if header exists
if c.Get("X-Custom-Header") != "" {
    // Header exists
}
```

### Request Metadata

```go
// Client IP address
ip := c.IP()

// Request method
method := c.Method()

// Original URL
originalURL := c.OriginalURL()

// Protocol (http/https)
protocol := c.Protocol()

// Host
host := c.Hostname()

// Path
path := c.Path()

// Base URL
baseURL := c.BaseURL()

// Subdomains
subdomains := c.Subdomains()
```

## Response Methods

### Status Codes

```go
// Set status code
c.Status(200)
c.Status(404)
c.Status(fiber.StatusOK)
c.Status(fiber.StatusNotFound)

// Send status without body
return c.SendStatus(204) // No Content

// Status with chaining
return c.Status(201).JSON(user)
```

### Response Body

```go
// Send string
return c.SendString("Hello World")

// Send bytes
return c.Send([]byte("Hello World"))

// Send file
return c.SendFile("./static/index.html")

// Download file
return c.Download("./files/report.pdf", "monthly-report.pdf")

// Send stream
return c.SendStream(reader)
```

### JSON and XML

```go
// JSON response
return c.JSON(fiber.Map{
    "name":  "John",
    "email": "john@example.com",
})

// JSON with status
return c.Status(201).JSON(user)

// Pretty JSON (formatted)
return c.JSON(data, "  ") // 2-space indent

// XML response
return c.XML(data)

// JSONP response
return c.JSONP(data, "callback")
```

### Templates and Views

```go
// Render template
return c.Render("index", fiber.Map{
    "Title": "Home Page",
    "User":  user,
})

// Render with layout
return c.Render("profile", data, "layouts/main")
```

## Headers and Cookies

### Response Headers

```go
// Set response header
c.Set("Content-Type", "application/json")
c.Set("X-Custom-Header", "value")

// Set multiple headers
c.Set("Cache-Control", "no-cache")
c.Set("X-Frame-Options", "DENY")

// Append to existing header
c.Append("Set-Cookie", "session=abc123")

// Remove header
c.Remove("X-Powered-By")
```

### Cookies

```go
// Set cookie
c.Cookie(&fiber.Cookie{
    Name:     "session",
    Value:    "abc123",
    Expires:  time.Now().Add(24 * time.Hour),
    HTTPOnly: true,
    Secure:   true,
    SameSite: "Lax",
})

// Get cookie
sessionID := c.Cookies("session")
sessionID := c.Cookies("session", "default-value")

// Clear cookie
c.ClearCookie("session")

// Clear cookie with options
c.ClearCookie("session", "example.com", "/admin")
```

## Redirects

```go
// Redirect (302 Found)
return c.Redirect("/login")

// Redirect with custom status
return c.Redirect("/login", 301) // Moved Permanently

// Redirect back
return c.RedirectBack("/fallback")

// Redirect to route
return c.RedirectToRoute("user.profile", fiber.Map{
    "id": userID,
})
```

## Context Storage

### Local Storage (Request-scoped)

```go
// Store data for current request
c.Locals("user", user)
c.Locals("authenticated", true)

// Retrieve data
user := c.Locals("user").(User)
isAuth := c.Locals("authenticated").(bool)

// Check if exists
if val := c.Locals("key"); val != nil {
    // Key exists
}
```

### User Context (with timeout)

```go
// Get context with timeout
ctx, cancel := context.WithTimeout(c.UserContext(), 5*time.Second)
defer cancel()

// Use with database operations
user, err := db.GetUserWithContext(ctx, userID)
```

## File Handling

### File Uploads

```go
// Single file upload
file, err := c.FormFile("document")
if err != nil {
    return c.Status(400).SendString("File upload failed")
}

// Save file
err = c.SaveFile(file, "./uploads/"+file.Filename)
if err != nil {
    return c.Status(500).SendString("Save failed")
}

// Multiple files
form, err := c.MultipartForm()
if err != nil {
    return err
}

files := form.File["documents"]
for _, file := range files {
    c.SaveFile(file, "./uploads/"+file.Filename)
}
```

## Utility Methods

### Next Middleware

```go
// Continue to next middleware/handler
return c.Next()

// Skip remaining middleware and go to next route
return c.Route("GET", "/fallback")
```

### Format Responses

```go
// Content negotiation
return c.Format(fiber.Map{
    "text/plain":       "Hello World",
    "text/html":        "<h1>Hello World</h1>",
    "application/json": fiber.Map{"message": "Hello World"},
})

// Auto-format based on Accept header
c.AutoFormat(data)
```

### Binding and Validation

```go
type CreateUserRequest struct {
    Name  string `json:"name" validate:"required"`
    Email string `json:"email" validate:"required,email"`
}

var req CreateUserRequest

// Bind and validate
if err := c.BodyParser(&req); err != nil {
    return c.Status(400).JSON(fiber.Map{"error": "Invalid request body"})
}

// Manual validation (with validator package)
if err := validator.New().Struct(req); err != nil {
    return c.Status(400).JSON(fiber.Map{"error": err.Error()})
}
```

## Performance Tips

1. **Avoid storing `c.Params()` values** beyond the handler scope
2. **Make copies** if you need to use values in goroutines
3. **Use `c.Locals()`** for request-scoped data sharing
4. **Leverage context pooling** - don't store context references
5. **Use streaming** for large responses

## Common Patterns

### API Response Helper

```go
func JSONResponse(c *fiber.Ctx, status int, data interface{}) error {
    return c.Status(status).JSON(fiber.Map{
        "success": status < 400,
        "data":    data,
        "timestamp": time.Now().Unix(),
    })
}

// Usage
return JSONResponse(c, 200, user)
```

### Error Response Helper

```go
func ErrorResponse(c *fiber.Ctx, status int, message string) error {
    return c.Status(status).JSON(fiber.Map{
        "success": false,
        "error":   message,
        "timestamp": time.Now().Unix(),
    })
}

// Usage
return ErrorResponse(c, 400, "Invalid user input")
```