# API Routes and Middleware

Next.js API routes and middleware documentation for building backend functionality.

## Contents

- **api-routes.md** - Creating and handling API endpoints
- **middleware.md** - Request/response middleware patterns
- **authentication.md** - Auth patterns and session management
- **webhooks.md** - Handling webhooks and external integrations

## Quick Reference

### API Route Structure
```
app/api/
├── route.ts              # /api (root API route)
├── posts/
│   ├── route.ts          # /api/posts
│   └── [id]/
│       └── route.ts      # /api/posts/[id]
├── auth/
│   └── route.ts          # /api/auth
└── webhooks/
    └── stripe/
        └── route.ts      # /api/webhooks/stripe
```

### HTTP Methods
- `GET` - Retrieve data
- `POST` - Create new resources
- `PUT` - Update entire resources
- `PATCH` - Partial updates
- `DELETE` - Remove resources