# Authentication Patterns

Comprehensive guide to implementing authentication in Next.js applications.

## Overview

Next.js supports various authentication patterns:

1. **NextAuth.js** - Full-featured authentication library
2. **Custom JWT** - Manual JSON Web Token implementation  
3. **Session-based** - Server-side session management
4. **OAuth/Social** - Third-party authentication providers
5. **Passwordless** - Email/SMS-based authentication

## NextAuth.js (Recommended)

NextAuth.js is the most popular authentication solution for Next.js.

### Installation and Setup

```bash
npm install next-auth
```

### Basic Configuration

```typescript
// app/api/auth/[...nextauth]/route.ts
import NextAuth from 'next-auth'
import GoogleProvider from 'next-auth/providers/google'
import CredentialsProvider from 'next-auth/providers/credentials'
import { PrismaAdapter } from '@next-auth/prisma-adapter'
import { prisma } from '@/lib/prisma'

const handler = NextAuth({
  adapter: PrismaAdapter(prisma),
  providers: [
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    }),
    CredentialsProvider({
      name: 'credentials',
      credentials: {
        email: { label: 'Email', type: 'email' },
        password: { label: 'Password', type: 'password' }
      },
      async authorize(credentials) {
        if (!credentials?.email || !credentials?.password) {
          return null
        }
        
        const user = await verifyCredentials(credentials.email, credentials.password)
        return user
      }
    })
  ],
  session: {
    strategy: 'jwt',
  },
  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.id = user.id
        token.role = user.role
      }
      return token
    },
    async session({ session, token }) {
      if (token) {
        session.user.id = token.id
        session.user.role = token.role
      }
      return session
    },
  },
  pages: {
    signIn: '/auth/signin',
    signUp: '/auth/signup',
  },
})

export { handler as GET, handler as POST }
```

### Environment Variables

```bash
# .env.local
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=your-secret-key-here

# OAuth Providers
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret

GITHUB_ID=your-github-client-id
GITHUB_SECRET=your-github-client-secret
```

### Using Sessions in Components

```typescript
// app/profile/page.tsx
import { getServerSession } from 'next-auth/next'
import { authOptions } from '@/app/api/auth/[...nextauth]/route'
import { redirect } from 'next/navigation'

export default async function ProfilePage() {
  const session = await getServerSession(authOptions)
  
  if (!session) {
    redirect('/auth/signin')
  }
  
  return (
    <div>
      <h1>Welcome, {session.user.name}</h1>
      <p>Email: {session.user.email}</p>
    </div>
  )
}
```

### Client-Side Session Hook

```typescript
'use client'
import { useSession, signIn, signOut } from 'next-auth/react'

export default function LoginButton() {
  const { data: session, status } = useSession()
  
  if (status === 'loading') return <p>Loading...</p>
  
  if (session) {
    return (
      <div>
        <p>Signed in as {session.user.email}</p>
        <button onClick={() => signOut()}>Sign out</button>
      </div>
    )
  }
  
  return (
    <div>
      <p>Not signed in</p>
      <button onClick={() => signIn()}>Sign in</button>
    </div>
  )
}
```

### Protecting Routes with Middleware

```typescript
// middleware.ts
import { withAuth } from 'next-auth/middleware'

export default withAuth(
  function middleware(req) {
    // Additional middleware logic
    console.log('Authenticated request:', req.nextauth.token)
  },
  {
    callbacks: {
      authorized: ({ token, req }) => {
        // Check if user has required permissions
        const { pathname } = req.nextUrl
        
        if (pathname.startsWith('/admin')) {
          return token?.role === 'admin'
        }
        
        if (pathname.startsWith('/dashboard')) {
          return !!token
        }
        
        return true
      },
    },
  }
)

export const config = {
  matcher: ['/dashboard/:path*', '/admin/:path*']
}
```

## Custom JWT Authentication

For more control over the authentication flow, implement custom JWT authentication.

### JWT Utilities

```typescript
// lib/auth.ts
import jwt from 'jsonwebtoken'
import bcrypt from 'bcryptjs'
import { cookies } from 'next/headers'

const JWT_SECRET = process.env.JWT_SECRET!

export interface User {
  id: string
  email: string
  name: string
  role: string
}

export function generateToken(user: User): string {
  return jwt.sign(
    { userId: user.id, email: user.email, role: user.role },
    JWT_SECRET,
    { expiresIn: '7d' }
  )
}

export function verifyToken(token: string): any {
  try {
    return jwt.verify(token, JWT_SECRET)
  } catch (error) {
    throw new Error('Invalid token')
  }
}

export async function hashPassword(password: string): Promise<string> {
  return await bcrypt.hash(password, 12)
}

export async function comparePasswords(password: string, hashedPassword: string): Promise<boolean> {
  return await bcrypt.compare(password, hashedPassword)
}

export function setAuthCookie(token: string) {
  const cookieStore = cookies()
  cookieStore.set('token', token, {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'lax',
    maxAge: 60 * 60 * 24 * 7, // 7 days
    path: '/',
  })
}

export function removeAuthCookie() {
  const cookieStore = cookies()
  cookieStore.delete('token')
}

export async function getCurrentUser(): Promise<User | null> {
  const cookieStore = cookies()
  const token = cookieStore.get('token')?.value
  
  if (!token) return null
  
  try {
    const decoded = verifyToken(token)
    const user = await getUserById(decoded.userId)
    return user
  } catch (error) {
    return null
  }
}
```

### Authentication API Routes

```typescript
// app/api/auth/register/route.ts
import { NextRequest } from 'next/server'
import { hashPassword, generateToken, setAuthCookie } from '@/lib/auth'
import { createUser } from '@/lib/users'

export async function POST(request: NextRequest) {
  try {
    const { email, password, name } = await request.json()
    
    // Validation
    if (!email || !password || !name) {
      return Response.json(
        { error: 'Missing required fields' },
        { status: 400 }
      )
    }
    
    // Check if user exists
    const existingUser = await getUserByEmail(email)
    if (existingUser) {
      return Response.json(
        { error: 'User already exists' },
        { status: 400 }
      )
    }
    
    // Create user
    const hashedPassword = await hashPassword(password)
    const user = await createUser({
      email,
      password: hashedPassword,
      name,
      role: 'user',
    })
    
    // Generate token and set cookie
    const token = generateToken(user)
    setAuthCookie(token)
    
    return Response.json({
      user: { id: user.id, email: user.email, name: user.name, role: user.role }
    })
  } catch (error) {
    return Response.json(
      { error: 'Registration failed' },
      { status: 500 }
    )
  }
}
```

```typescript
// app/api/auth/login/route.ts
import { NextRequest } from 'next/server'
import { comparePasswords, generateToken, setAuthCookie } from '@/lib/auth'
import { getUserByEmail } from '@/lib/users'

export async function POST(request: NextRequest) {
  try {
    const { email, password } = await request.json()
    
    // Validation
    if (!email || !password) {
      return Response.json(
        { error: 'Missing credentials' },
        { status: 400 }
      )
    }
    
    // Find user
    const user = await getUserByEmail(email)
    if (!user) {
      return Response.json(
        { error: 'Invalid credentials' },
        { status: 401 }
      )
    }
    
    // Verify password
    const isValid = await comparePasswords(password, user.password)
    if (!isValid) {
      return Response.json(
        { error: 'Invalid credentials' },
        { status: 401 }
      )
    }
    
    // Generate token and set cookie
    const token = generateToken(user)
    setAuthCookie(token)
    
    return Response.json({
      user: { id: user.id, email: user.email, name: user.name, role: user.role }
    })
  } catch (error) {
    return Response.json(
      { error: 'Login failed' },
      { status: 500 }
    )
  }
}
```

### Protected Route Helper

```typescript
// lib/auth-helpers.ts
import { redirect } from 'next/navigation'
import { getCurrentUser } from './auth'

export async function requireAuth() {
  const user = await getCurrentUser()
  
  if (!user) {
    redirect('/auth/login')
  }
  
  return user
}

export async function requireRole(requiredRole: string) {
  const user = await requireAuth()
  
  if (user.role !== requiredRole) {
    redirect('/unauthorized')
  }
  
  return user
}
```

### Using in Server Components

```typescript
// app/dashboard/page.tsx
import { requireAuth } from '@/lib/auth-helpers'

export default async function DashboardPage() {
  const user = await requireAuth()
  
  return (
    <div>
      <h1>Dashboard</h1>
      <p>Welcome back, {user.name}!</p>
    </div>
  )
}
```

## OAuth/Social Authentication

### Google OAuth

```typescript
// lib/oauth.ts
import { OAuth2Client } from 'google-auth-library'

const client = new OAuth2Client(
  process.env.GOOGLE_CLIENT_ID,
  process.env.GOOGLE_CLIENT_SECRET,
  `${process.env.NEXTAUTH_URL}/api/auth/callback/google`
)

export function getGoogleAuthUrl() {
  return client.generateAuthUrl({
    access_type: 'offline',
    scope: ['profile', 'email'],
    include_granted_scopes: true,
  })
}

export async function verifyGoogleToken(code: string) {
  try {
    const { tokens } = await client.getToken(code)
    client.setCredentials(tokens)
    
    const ticket = await client.verifyIdToken({
      idToken: tokens.id_token!,
      audience: process.env.GOOGLE_CLIENT_ID,
    })
    
    const payload = ticket.getPayload()
    return payload
  } catch (error) {
    throw new Error('Failed to verify Google token')
  }
}
```

## Authentication Context

```typescript
// contexts/auth-context.tsx
'use client'
import { createContext, useContext, useEffect, useState } from 'react'

interface User {
  id: string
  email: string
  name: string
  role: string
}

interface AuthContextType {
  user: User | null
  login: (email: string, password: string) => Promise<void>
  logout: () => Promise<void>
  loading: boolean
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)
  
  useEffect(() => {
    checkAuth()
  }, [])
  
  async function checkAuth() {
    try {
      const response = await fetch('/api/auth/me')
      if (response.ok) {
        const userData = await response.json()
        setUser(userData.user)
      }
    } catch (error) {
      console.error('Auth check failed:', error)
    } finally {
      setLoading(false)
    }
  }
  
  async function login(email: string, password: string) {
    const response = await fetch('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    })
    
    if (!response.ok) {
      throw new Error('Login failed')
    }
    
    const userData = await response.json()
    setUser(userData.user)
  }
  
  async function logout() {
    await fetch('/api/auth/logout', { method: 'POST' })
    setUser(null)
  }
  
  return (
    <AuthContext.Provider value={{ user, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
```

## Role-Based Access Control (RBAC)

```typescript
// lib/permissions.ts
export const PERMISSIONS = {
  CREATE_POST: 'create_post',
  DELETE_POST: 'delete_post',
  MANAGE_USERS: 'manage_users',
  VIEW_ANALYTICS: 'view_analytics',
} as const

export const ROLES = {
  ADMIN: 'admin',
  MODERATOR: 'moderator',
  USER: 'user',
} as const

export const ROLE_PERMISSIONS = {
  [ROLES.ADMIN]: [
    PERMISSIONS.CREATE_POST,
    PERMISSIONS.DELETE_POST,
    PERMISSIONS.MANAGE_USERS,
    PERMISSIONS.VIEW_ANALYTICS,
  ],
  [ROLES.MODERATOR]: [
    PERMISSIONS.CREATE_POST,
    PERMISSIONS.DELETE_POST,
    PERMISSIONS.VIEW_ANALYTICS,
  ],
  [ROLES.USER]: [
    PERMISSIONS.CREATE_POST,
  ],
}

export function hasPermission(userRole: string, permission: string): boolean {
  return ROLE_PERMISSIONS[userRole]?.includes(permission) || false
}

export function requirePermission(userRole: string, permission: string): void {
  if (!hasPermission(userRole, permission)) {
    throw new Error(`Permission denied: ${permission}`)
  }
}
```

### Permission Component

```typescript
'use client'
import { useAuth } from '@/contexts/auth-context'
import { hasPermission } from '@/lib/permissions'

interface PermissionGuardProps {
  permission: string
  children: React.ReactNode
  fallback?: React.ReactNode
}

export function PermissionGuard({ permission, children, fallback = null }: PermissionGuardProps) {
  const { user } = useAuth()
  
  if (!user || !hasPermission(user.role, permission)) {
    return <>{fallback}</>
  }
  
  return <>{children}</>
}
```

## Password Reset Flow

```typescript
// lib/password-reset.ts
import crypto from 'crypto'

export function generateResetToken(): string {
  return crypto.randomBytes(32).toString('hex')
}

export async function createPasswordResetToken(email: string): Promise<string> {
  const token = generateResetToken()
  const expiresAt = new Date(Date.now() + 60 * 60 * 1000) // 1 hour
  
  await prisma.passwordResetToken.create({
    data: {
      email,
      token,
      expiresAt,
    },
  })
  
  return token
}

export async function verifyResetToken(token: string): Promise<string | null> {
  const resetToken = await prisma.passwordResetToken.findFirst({
    where: {
      token,
      expiresAt: { gt: new Date() },
      used: false,
    },
  })
  
  return resetToken?.email || null
}
```

## Best Practices

1. **Use HTTPS in Production** - Always encrypt authentication traffic
2. **Implement Rate Limiting** - Prevent brute force attacks
3. **Hash Passwords Properly** - Use bcrypt with proper salt rounds
4. **Secure Session Storage** - Use httpOnly cookies
5. **Implement CSRF Protection** - Prevent cross-site request forgery
6. **Add Two-Factor Authentication** - Extra security layer
7. **Log Authentication Events** - Monitor for suspicious activity
8. **Use Strong JWT Secrets** - Generate cryptographically secure secrets
9. **Implement Proper Logout** - Clear all authentication traces
10. **Handle Token Expiration** - Implement refresh token patterns

This comprehensive guide covers the most common authentication patterns in Next.js, from simple implementations to enterprise-grade solutions.