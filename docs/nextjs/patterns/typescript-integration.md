# TypeScript Integration

Complete guide to using TypeScript with Next.js for type-safe development.

## Setup and Configuration

### Installation

```bash
# Create new Next.js project with TypeScript
npx create-next-app@latest my-app --typescript

# Or add TypeScript to existing project
npm install --save-dev typescript @types/react @types/node
touch tsconfig.json
npm run dev # Next.js will populate tsconfig.json
```

### TypeScript Configuration

```json
// tsconfig.json
{
  "compilerOptions": {
    "lib": ["dom", "dom.iterable", "es6"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "forceConsistentCasingInFileNames": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "node",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [
      {
        "name": "next"
      }
    ],
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"],
      "@/components/*": ["./src/components/*"],
      "@/lib/*": ["./src/lib/*"],
      "@/types/*": ["./src/types/*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
```

## Page and Layout Types

### App Router Types

```typescript
// app/page.tsx
interface PageProps {
  params: { [key: string]: string | string[] }
  searchParams: { [key: string]: string | string[] | undefined }
}

export default function Page({ params, searchParams }: PageProps) {
  return <div>Page content</div>
}

// app/blog/[slug]/page.tsx
interface BlogPageProps {
  params: {
    slug: string
  }
  searchParams: {
    comment?: string
    page?: string
  }
}

export default function BlogPage({ params, searchParams }: BlogPageProps) {
  return <div>Blog post: {params.slug}</div>
}
```

### Layout Types

```typescript
// app/layout.tsx
interface RootLayoutProps {
  children: React.ReactNode
  modal?: React.ReactNode // For parallel routes
}

export default function RootLayout({ children, modal }: RootLayoutProps) {
  return (
    <html lang="en">
      <body>
        {children}
        {modal}
      </body>
    </html>
  )
}

// app/dashboard/layout.tsx
interface DashboardLayoutProps {
  children: React.ReactNode
  params: {
    team?: string
  }
}

export default function DashboardLayout({ children, params }: DashboardLayoutProps) {
  return <div className="dashboard">{children}</div>
}
```

### Metadata Types

```typescript
import { Metadata, ResolvingMetadata } from 'next'

// Static metadata
export const metadata: Metadata = {
  title: 'My App',
  description: 'App description',
  openGraph: {
    title: 'My App',
    description: 'App description',
    images: ['/og-image.jpg'],
  },
}

// Dynamic metadata
interface GenerateMetadataProps {
  params: { slug: string }
  searchParams: { [key: string]: string | string[] | undefined }
}

export async function generateMetadata(
  { params, searchParams }: GenerateMetadataProps,
  parent: ResolvingMetadata
): Promise<Metadata> {
  const post = await getPost(params.slug)
  const previousImages = (await parent).openGraph?.images || []
  
  return {
    title: post.title,
    description: post.excerpt,
    openGraph: {
      title: post.title,
      description: post.excerpt,
      images: [post.image, ...previousImages],
    },
  }
}
```

## API Route Types

### Request and Response Types

```typescript
// app/api/users/route.ts
import { NextRequest, NextResponse } from 'next/server'

interface User {
  id: string
  email: string
  name: string
  createdAt: Date
}

interface CreateUserRequest {
  email: string
  name: string
  password: string
}

export async function GET(request: NextRequest) {
  const users: User[] = await getUsers()
  return NextResponse.json({ users })
}

export async function POST(request: NextRequest) {
  const body: CreateUserRequest = await request.json()
  
  // Validate request body
  if (!body.email || !body.name || !body.password) {
    return NextResponse.json(
      { error: 'Missing required fields' },
      { status: 400 }
    )
  }
  
  const user: User = await createUser(body)
  return NextResponse.json({ user }, { status: 201 })
}
```

### Dynamic Route Types

```typescript
// app/api/users/[id]/route.ts
interface RouteParams {
  params: {
    id: string
  }
}

export async function GET(
  request: NextRequest,
  { params }: RouteParams
) {
  const user: User | null = await getUserById(params.id)
  
  if (!user) {
    return NextResponse.json(
      { error: 'User not found' },
      { status: 404 }
    )
  }
  
  return NextResponse.json({ user })
}

export async function PUT(
  request: NextRequest,
  { params }: RouteParams
) {
  const updates: Partial<User> = await request.json()
  const user = await updateUser(params.id, updates)
  return NextResponse.json({ user })
}
```

## Component Types

### Server Component Types

```typescript
// components/UserList.tsx
interface User {
  id: string
  name: string
  email: string
}

interface UserListProps {
  users: User[]
  showEmail?: boolean
}

export default function UserList({ users, showEmail = false }: UserListProps) {
  return (
    <ul>
      {users.map((user) => (
        <li key={user.id}>
          {user.name}
          {showEmail && <span> - {user.email}</span>}
        </li>
      ))}
    </ul>
  )
}
```

### Client Component Types

```typescript
'use client'
import { useState, useEffect, FormEvent } from 'react'

interface FormData {
  name: string
  email: string
}

interface FormErrors {
  name?: string
  email?: string
}

interface ContactFormProps {
  onSubmit: (data: FormData) => Promise<void>
  initialData?: Partial<FormData>
}

export default function ContactForm({ onSubmit, initialData }: ContactFormProps) {
  const [formData, setFormData] = useState<FormData>({
    name: initialData?.name || '',
    email: initialData?.email || '',
  })
  
  const [errors, setErrors] = useState<FormErrors>({})
  const [isSubmitting, setIsSubmitting] = useState(false)
  
  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    setIsSubmitting(true)
    
    try {
      await onSubmit(formData)
    } catch (error) {
      console.error('Submission error:', error)
    } finally {
      setIsSubmitting(false)
    }
  }
  
  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={formData.name}
        onChange={(e) => setFormData(prev => ({ ...prev, name: e.target.value }))}
        disabled={isSubmitting}
      />
      <input
        type="email"
        value={formData.email}
        onChange={(e) => setFormData(prev => ({ ...prev, email: e.target.value }))}
        disabled={isSubmitting}
      />
      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Submitting...' : 'Submit'}
      </button>
    </form>
  )
}
```

## Custom Hooks with Types

```typescript
// hooks/useApi.ts
import { useState, useEffect } from 'react'

interface ApiState<T> {
  data: T | null
  loading: boolean
  error: string | null
}

type ApiResponse<T> = {
  data: T
  error?: never
} | {
  data?: never
  error: string
}

export function useApi<T>(url: string): ApiState<T> {
  const [state, setState] = useState<ApiState<T>>({
    data: null,
    loading: true,
    error: null,
  })
  
  useEffect(() => {
    async function fetchData() {
      try {
        const response = await fetch(url)
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }
        const result: ApiResponse<T> = await response.json()
        
        if (result.error) {
          setState({ data: null, loading: false, error: result.error })
        } else {
          setState({ data: result.data, loading: false, error: null })
        }
      } catch (error) {
        setState({
          data: null,
          loading: false,
          error: error instanceof Error ? error.message : 'Unknown error',
        })
      }
    }
    
    fetchData()
  }, [url])
  
  return state
}

// Usage
interface User {
  id: string
  name: string
  email: string
}

function UserProfile({ userId }: { userId: string }) {
  const { data: user, loading, error } = useApi<User>(`/api/users/${userId}`)
  
  if (loading) return <div>Loading...</div>
  if (error) return <div>Error: {error}</div>
  if (!user) return <div>User not found</div>
  
  return (
    <div>
      <h1>{user.name}</h1>
      <p>{user.email}</p>
    </div>
  )
}
```

## Database and ORM Types

### Prisma Types

```typescript
// lib/prisma.ts
import { PrismaClient } from '@prisma/client'

const globalForPrisma = globalThis as unknown as {
  prisma: PrismaClient | undefined
}

export const prisma = globalForPrisma.prisma ?? new PrismaClient()

if (process.env.NODE_ENV !== 'production') globalForPrisma.prisma = prisma

// Export Prisma types
export type { User, Post, Comment } from '@prisma/client'

// Custom types with relations
export type UserWithPosts = User & {
  posts: Post[]
}

export type PostWithAuthor = Post & {
  author: User
  comments: Comment[]
}
```

### Database Functions with Types

```typescript
// lib/users.ts
import { prisma, User, UserWithPosts } from './prisma'

export async function getUsers(): Promise<User[]> {
  return prisma.user.findMany()
}

export async function getUserById(id: string): Promise<User | null> {
  return prisma.user.findUnique({
    where: { id },
  })
}

export async function getUserWithPosts(id: string): Promise<UserWithPosts | null> {
  return prisma.user.findUnique({
    where: { id },
    include: { posts: true },
  })
}

export async function createUser(data: {
  email: string
  name: string
  password: string
}): Promise<User> {
  return prisma.user.create({
    data,
  })
}

export async function updateUser(
  id: string,
  data: Partial<Pick<User, 'name' | 'email'>>
): Promise<User> {
  return prisma.user.update({
    where: { id },
    data,
  })
}
```

## Environment Variables with Types

```typescript
// lib/env.ts
import { z } from 'zod'

const envSchema = z.object({
  DATABASE_URL: z.string().url(),
  NEXTAUTH_SECRET: z.string().min(1),
  NEXTAUTH_URL: z.string().url(),
  GOOGLE_CLIENT_ID: z.string().min(1),
  GOOGLE_CLIENT_SECRET: z.string().min(1),
  NEXT_PUBLIC_API_URL: z.string().url(),
  NODE_ENV: z.enum(['development', 'production', 'test']),
})

export const env = envSchema.parse(process.env)

// Usage - fully typed environment variables
console.log(env.DATABASE_URL) // TypeScript knows this is a string
```

## Middleware with Types

```typescript
// middleware.ts
import { NextRequest, NextResponse } from 'next/server'
import { getToken } from 'next-auth/jwt'

interface AuthenticatedRequest extends NextRequest {
  auth?: {
    user: {
      id: string
      email: string
      role: string
    }
  }
}

export async function middleware(request: NextRequest) {
  // Add type safety to JWT token
  const token = await getToken({ req: request })
  
  if (request.nextUrl.pathname.startsWith('/admin')) {
    if (!token || token.role !== 'admin') {
      return NextResponse.redirect(new URL('/login', request.url))
    }
  }
  
  // Add user info to request headers for API routes
  if (token && request.nextUrl.pathname.startsWith('/api/protected')) {
    const requestHeaders = new Headers(request.headers)
    requestHeaders.set('x-user-id', token.sub!)
    requestHeaders.set('x-user-role', token.role as string)
    
    return NextResponse.next({
      request: {
        headers: requestHeaders,
      },
    })
  }
  
  return NextResponse.next()
}
```

## Error Handling with Types

```typescript
// lib/errors.ts
export class APIError extends Error {
  constructor(
    public message: string,
    public statusCode: number = 500,
    public code?: string
  ) {
    super(message)
    this.name = 'APIError'
  }
}

export class ValidationError extends APIError {
  constructor(
    message: string,
    public field: string
  ) {
    super(message, 400, 'VALIDATION_ERROR')
    this.name = 'ValidationError'
  }
}

export class NotFoundError extends APIError {
  constructor(resource: string) {
    super(`${resource} not found`, 404, 'NOT_FOUND')
    this.name = 'NotFoundError'
  }
}

// Error handler with types
export function handleAPIError(error: unknown): NextResponse {
  console.error('API Error:', error)
  
  if (error instanceof ValidationError) {
    return NextResponse.json(
      {
        error: error.message,
        code: error.code,
        field: error.field,
      },
      { status: error.statusCode }
    )
  }
  
  if (error instanceof APIError) {
    return NextResponse.json(
      {
        error: error.message,
        code: error.code,
      },
      { status: error.statusCode }
    )
  }
  
  // Unknown error
  return NextResponse.json(
    { error: 'Internal Server Error' },
    { status: 500 }
  )
}
```

## Form Validation with Types

```typescript
// lib/validation.ts
import { z } from 'zod'

export const userSchema = z.object({
  name: z.string().min(2, 'Name must be at least 2 characters'),
  email: z.string().email('Invalid email format'),
  age: z.number().int().min(18, 'Must be at least 18 years old').optional(),
})

export const postSchema = z.object({
  title: z.string().min(1, 'Title is required').max(100, 'Title too long'),
  content: z.string().min(10, 'Content must be at least 10 characters'),
  published: z.boolean().default(false),
  tags: z.array(z.string()).max(5, 'Maximum 5 tags allowed'),
})

export type UserInput = z.infer<typeof userSchema>
export type PostInput = z.infer<typeof postSchema>

// API route with validation
export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const validatedData: UserInput = userSchema.parse(body)
    
    const user = await createUser(validatedData)
    return NextResponse.json({ user }, { status: 201 })
  } catch (error) {
    if (error instanceof z.ZodError) {
      return NextResponse.json(
        { error: 'Validation failed', details: error.errors },
        { status: 400 }
      )
    }
    
    return handleAPIError(error)
  }
}
```

## Testing with Types

```typescript
// __tests__/api/users.test.ts
import { createMocks } from 'node-mocks-http'
import { NextApiRequest, NextApiResponse } from 'next'
import handler from '@/pages/api/users'

interface MockApiRequest extends NextApiRequest {
  body: {
    name: string
    email: string
  }
}

interface MockApiResponse extends NextApiResponse {
  _getData: () => string
  _getStatusCode: () => number
}

describe('/api/users', () => {
  it('should create a user', async () => {
    const { req, res } = createMocks<MockApiRequest, MockApiResponse>({
      method: 'POST',
      body: {
        name: 'John Doe',
        email: 'john@example.com',
      },
    })

    await handler(req, res)

    expect(res._getStatusCode()).toBe(201)
    
    const data = JSON.parse(res._getData())
    expect(data.user).toBeDefined()
    expect(data.user.email).toBe('john@example.com')
  })
})
```

## Best Practices

1. **Use strict TypeScript configuration**
2. **Define interfaces for all data structures**
3. **Use generic types for reusable components**
4. **Validate runtime data with libraries like Zod**
5. **Type your API responses consistently**
6. **Use discriminated unions for complex state**
7. **Leverage TypeScript's utility types**
8. **Keep types close to their usage**
9. **Use branded types for IDs and sensitive data**
10. **Implement proper error handling with typed errors**

This comprehensive guide covers the essential TypeScript patterns for building type-safe Next.js applications.