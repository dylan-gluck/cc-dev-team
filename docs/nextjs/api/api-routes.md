# API Routes

Complete guide to building API endpoints in Next.js with the App Router.

## Basic API Routes

API routes in the App Router use the `route.ts` (or `.js`) file convention.

### Simple GET Route

```typescript
// app/api/hello/route.ts
export async function GET() {
  return Response.json({ message: 'Hello, World!' })
}
```

### Multiple HTTP Methods

```typescript
// app/api/posts/route.ts
import { NextRequest } from 'next/server'

// GET /api/posts
export async function GET() {
  const posts = await getPosts()
  return Response.json(posts)
}

// POST /api/posts
export async function POST(request: NextRequest) {
  const body = await request.json()
  const post = await createPost(body)
  return Response.json(post, { status: 201 })
}

// PUT /api/posts
export async function PUT(request: NextRequest) {
  const body = await request.json()
  const post = await updatePost(body)
  return Response.json(post)
}

// DELETE /api/posts
export async function DELETE(request: NextRequest) {
  const { searchParams } = new URL(request.url)
  const id = searchParams.get('id')
  
  if (!id) {
    return Response.json({ error: 'ID required' }, { status: 400 })
  }
  
  await deletePost(id)
  return Response.json({ message: 'Post deleted' })
}
```

## Dynamic Routes

### Single Dynamic Segment

```typescript
// app/api/posts/[id]/route.ts
import { NextRequest } from 'next/server'

export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  const post = await getPost(params.id)
  
  if (!post) {
    return Response.json({ error: 'Post not found' }, { status: 404 })
  }
  
  return Response.json(post)
}

export async function PUT(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  const body = await request.json()
  const updatedPost = await updatePost(params.id, body)
  return Response.json(updatedPost)
}

export async function DELETE(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  await deletePost(params.id)
  return Response.json({ message: 'Post deleted' })
}
```

### Multiple Dynamic Segments

```typescript
// app/api/users/[userId]/posts/[postId]/route.ts
export async function GET(
  request: NextRequest,
  { params }: { params: { userId: string; postId: string } }
) {
  const post = await getUserPost(params.userId, params.postId)
  return Response.json(post)
}
```

### Catch-all Routes

```typescript
// app/api/files/[...path]/route.ts
export async function GET(
  request: NextRequest,
  { params }: { params: { path: string[] } }
) {
  const filePath = params.path.join('/')
  const file = await getFile(filePath)
  return Response.json(file)
}
```

## Request Handling

### Query Parameters

```typescript
// app/api/posts/route.ts
export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url)
  const page = searchParams.get('page') || '1'
  const limit = searchParams.get('limit') || '10'
  const category = searchParams.get('category')
  
  const posts = await getPosts({
    page: parseInt(page),
    limit: parseInt(limit),
    category,
  })
  
  return Response.json(posts)
}
```

### Request Body

```typescript
// app/api/users/route.ts
export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    
    // Validate required fields
    if (!body.email || !body.name) {
      return Response.json(
        { error: 'Email and name are required' },
        { status: 400 }
      )
    }
    
    const user = await createUser(body)
    return Response.json(user, { status: 201 })
  } catch (error) {
    return Response.json(
      { error: 'Invalid JSON' },
      { status: 400 }
    )
  }
}
```

### Headers

```typescript
// app/api/protected/route.ts
export async function GET(request: NextRequest) {
  const authorization = request.headers.get('authorization')
  const contentType = request.headers.get('content-type')
  
  if (!authorization) {
    return Response.json(
      { error: 'Unauthorized' },
      { status: 401 }
    )
  }
  
  // Process request...
  return Response.json({ data: 'Protected data' })
}
```

### Cookies

```typescript
// app/api/auth/route.ts
import { cookies } from 'next/headers'

export async function GET() {
  const cookieStore = cookies()
  const sessionId = cookieStore.get('sessionId')
  
  if (!sessionId) {
    return Response.json({ error: 'No session' }, { status: 401 })
  }
  
  return Response.json({ session: sessionId.value })
}

export async function POST(request: NextRequest) {
  const body = await request.json()
  const session = await createSession(body)
  
  return Response.json(
    { success: true },
    {
      status: 200,
      headers: {
        'Set-Cookie': `sessionId=${session.id}; HttpOnly; Path=/; Max-Age=86400`,
      },
    }
  )
}
```

## Response Handling

### JSON Responses

```typescript
// app/api/data/route.ts
export async function GET() {
  const data = await getData()
  
  return Response.json(
    { data, timestamp: new Date().toISOString() },
    {
      status: 200,
      headers: {
        'Cache-Control': 'max-age=60, s-maxage=60',
      },
    }
  )
}
```

### File Downloads

```typescript
// app/api/download/[filename]/route.ts
import { NextRequest } from 'next/server'
import fs from 'fs'
import path from 'path'

export async function GET(
  request: NextRequest,
  { params }: { params: { filename: string } }
) {
  const filePath = path.join(process.cwd(), 'files', params.filename)
  
  if (!fs.existsSync(filePath)) {
    return Response.json({ error: 'File not found' }, { status: 404 })
  }
  
  const file = fs.readFileSync(filePath)
  
  return new Response(file, {
    headers: {
      'Content-Type': 'application/octet-stream',
      'Content-Disposition': `attachment; filename="${params.filename}"`,
    },
  })
}
```

### Streaming Responses

```typescript
// app/api/stream/route.ts
export async function GET() {
  const encoder = new TextEncoder()
  
  const stream = new ReadableStream({
    start(controller) {
      // Send initial data
      controller.enqueue(encoder.encode('data: {"message": "Starting stream"}\n\n'))
      
      // Send periodic updates
      const interval = setInterval(() => {
        const data = { timestamp: Date.now(), message: 'Update' }
        controller.enqueue(encoder.encode(`data: ${JSON.stringify(data)}\n\n`))
      }, 1000)
      
      // Clean up after 30 seconds
      setTimeout(() => {
        clearInterval(interval)
        controller.enqueue(encoder.encode('data: {"message": "Stream ended"}\n\n'))
        controller.close()
      }, 30000)
    },
  })
  
  return new Response(stream, {
    headers: {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive',
    },
  })
}
```

## Error Handling

### Custom Error Handler

```typescript
// lib/api-error.ts
export class APIError extends Error {
  constructor(
    public message: string,
    public status: number = 500,
    public code?: string
  ) {
    super(message)
    this.name = 'APIError'
  }
}

export function handleAPIError(error: unknown) {
  console.error('API Error:', error)
  
  if (error instanceof APIError) {
    return Response.json(
      { error: error.message, code: error.code },
      { status: error.status }
    )
  }
  
  return Response.json(
    { error: 'Internal Server Error' },
    { status: 500 }
  )
}
```

### Using Error Handler

```typescript
// app/api/posts/[id]/route.ts
import { APIError, handleAPIError } from '@/lib/api-error'

export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    if (!params.id) {
      throw new APIError('Post ID is required', 400, 'MISSING_ID')
    }
    
    const post = await getPost(params.id)
    
    if (!post) {
      throw new APIError('Post not found', 404, 'POST_NOT_FOUND')
    }
    
    return Response.json(post)
  } catch (error) {
    return handleAPIError(error)
  }
}
```

## Validation

### Input Validation with Zod

```typescript
// app/api/users/route.ts
import { z } from 'zod'

const createUserSchema = z.object({
  email: z.string().email('Invalid email format'),
  name: z.string().min(2, 'Name must be at least 2 characters'),
  age: z.number().int().min(18, 'Must be at least 18 years old').optional(),
})

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    
    // Validate input
    const validatedData = createUserSchema.parse(body)
    
    const user = await createUser(validatedData)
    return Response.json(user, { status: 201 })
  } catch (error) {
    if (error instanceof z.ZodError) {
      return Response.json(
        { error: 'Validation failed', details: error.errors },
        { status: 400 }
      )
    }
    
    return handleAPIError(error)
  }
}
```

## Database Integration

### With Prisma

```typescript
// app/api/posts/route.ts
import { prisma } from '@/lib/prisma'

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url)
  const page = parseInt(searchParams.get('page') || '1')
  const limit = parseInt(searchParams.get('limit') || '10')
  
  try {
    const [posts, total] = await Promise.all([
      prisma.post.findMany({
        skip: (page - 1) * limit,
        take: limit,
        include: {
          author: {
            select: { id: true, name: true, email: true },
          },
        },
        orderBy: { createdAt: 'desc' },
      }),
      prisma.post.count(),
    ])
    
    return Response.json({
      posts,
      pagination: {
        page,
        limit,
        total,
        pages: Math.ceil(total / limit),
      },
    })
  } catch (error) {
    return handleAPIError(error)
  }
}

export async function POST(request: NextRequest) {
  try {
    const { title, content, authorId } = await request.json()
    
    const post = await prisma.post.create({
      data: { title, content, authorId },
      include: {
        author: {
          select: { id: true, name: true, email: true },
        },
      },
    })
    
    return Response.json(post, { status: 201 })
  } catch (error) {
    return handleAPIError(error)
  }
}
```

## Authentication

### JWT Authentication

```typescript
// app/api/protected/route.ts
import jwt from 'jsonwebtoken'

export async function GET(request: NextRequest) {
  const authorization = request.headers.get('authorization')
  
  if (!authorization || !authorization.startsWith('Bearer ')) {
    return Response.json({ error: 'Unauthorized' }, { status: 401 })
  }
  
  const token = authorization.split(' ')[1]
  
  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET!) as any
    const userId = decoded.userId
    
    // Fetch user data or proceed with authenticated request
    const userData = await getUserById(userId)
    
    return Response.json({ user: userData })
  } catch (error) {
    return Response.json({ error: 'Invalid token' }, { status: 401 })
  }
}
```

## Rate Limiting

```typescript
// lib/rate-limit.ts
const attempts = new Map()

export function rateLimit(identifier: string, maxAttempts: number = 5, windowMs: number = 60000) {
  const now = Date.now()
  const window = now - windowMs
  
  if (!attempts.has(identifier)) {
    attempts.set(identifier, [])
  }
  
  const userAttempts = attempts.get(identifier)
  const recentAttempts = userAttempts.filter((time: number) => time > window)
  
  if (recentAttempts.length >= maxAttempts) {
    return false
  }
  
  recentAttempts.push(now)
  attempts.set(identifier, recentAttempts)
  
  return true
}
```

```typescript
// app/api/login/route.ts
import { rateLimit } from '@/lib/rate-limit'

export async function POST(request: NextRequest) {
  const ip = request.ip || 'anonymous'
  
  if (!rateLimit(ip, 5, 60000)) {
    return Response.json(
      { error: 'Too many attempts. Please try again later.' },
      { status: 429 }
    )
  }
  
  // Process login...
}
```

## Testing API Routes

### Unit Testing with Jest

```typescript
// __tests__/api/posts.test.ts
import { GET, POST } from '@/app/api/posts/route'
import { createMockRequest } from '@/test/utils'

describe('/api/posts', () => {
  describe('GET', () => {
    it('should return posts', async () => {
      const response = await GET()
      const data = await response.json()
      
      expect(response.status).toBe(200)
      expect(Array.isArray(data.posts)).toBe(true)
    })
  })
  
  describe('POST', () => {
    it('should create a new post', async () => {
      const request = createMockRequest({
        method: 'POST',
        body: {
          title: 'Test Post',
          content: 'Test content',
          authorId: '1',
        },
      })
      
      const response = await POST(request)
      const data = await response.json()
      
      expect(response.status).toBe(201)
      expect(data.title).toBe('Test Post')
    })
  })
})
```

This comprehensive guide covers the essential patterns for building robust API routes in Next.js with proper error handling, validation, authentication, and testing.