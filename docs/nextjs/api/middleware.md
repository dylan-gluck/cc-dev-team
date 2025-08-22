# Middleware

Complete guide to Next.js Middleware for handling requests before they reach your pages and API routes.

## What is Middleware?

Middleware allows you to run code before a request is completed. You can modify the response by rewriting, redirecting, modifying request/response headers, or responding directly.

## Basic Middleware

### Creating Middleware

Create a `middleware.ts` file in your project root:

```typescript
// middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  // Add custom header
  const response = NextResponse.next()
  response.headers.set('X-Custom-Header', 'Hello from middleware!')
  
  return response
}

// Configure which paths the middleware runs on
export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     */
    '/((?!api|_next/static|_next/image|favicon.ico).*)',
  ],
}
```

## Common Use Cases

### 1. Authentication

```typescript
// middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'
import { verify } from 'jsonwebtoken'

export async function middleware(request: NextRequest) {
  // Check if accessing protected routes
  if (request.nextUrl.pathname.startsWith('/dashboard')) {
    const token = request.cookies.get('token')?.value
    
    if (!token) {
      return NextResponse.redirect(new URL('/login', request.url))
    }
    
    try {
      await verify(token, process.env.JWT_SECRET!)
    } catch (error) {
      return NextResponse.redirect(new URL('/login', request.url))
    }
  }
  
  return NextResponse.next()
}

export const config = {
  matcher: ['/dashboard/:path*']
}
```

### 2. Redirects and Rewrites

```typescript
// middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  // Redirect old URLs
  if (request.nextUrl.pathname.startsWith('/old-blog')) {
    return NextResponse.redirect(
      new URL('/blog', request.url),
      301 // Permanent redirect
    )
  }
  
  // Rewrite API routes
  if (request.nextUrl.pathname.startsWith('/api/v1')) {
    return NextResponse.rewrite(
      new URL(request.nextUrl.pathname.replace('/api/v1', '/api'), request.url)
    )
  }
  
  // A/B testing
  if (request.nextUrl.pathname === '/') {
    const bucket = Math.random() < 0.5 ? 'a' : 'b'
    request.cookies.set('bucket', bucket)
    
    if (bucket === 'b') {
      return NextResponse.rewrite(new URL('/home-variant-b', request.url))
    }
  }
  
  return NextResponse.next()
}
```

### 3. Geolocation and Localization

```typescript
// middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

const locales = ['en', 'es', 'fr', 'de']

function getLocale(request: NextRequest): string {
  // Check URL pathname
  const pathname = request.nextUrl.pathname
  const pathnameIsMissingLocale = locales.every(
    (locale) => !pathname.startsWith(`/${locale}/`) && pathname !== `/${locale}`
  )
  
  if (pathnameIsMissingLocale) {
    // Check Accept-Language header
    const acceptLanguage = request.headers.get('Accept-Language')
    if (acceptLanguage) {
      const preferredLocale = acceptLanguage
        .split(',')[0]
        .split('-')[0]
        .toLowerCase()
      
      if (locales.includes(preferredLocale)) {
        return preferredLocale
      }
    }
    
    // Check geolocation (if using Vercel)
    const country = request.geo?.country?.toLowerCase()
    const countryToLocale: Record<string, string> = {
      'us': 'en',
      'gb': 'en',
      'es': 'es',
      'fr': 'fr',
      'de': 'de',
    }
    
    if (country && countryToLocale[country]) {
      return countryToLocale[country]
    }
  }
  
  return 'en' // Default locale
}

export function middleware(request: NextRequest) {
  const pathname = request.nextUrl.pathname
  const pathnameIsMissingLocale = locales.every(
    (locale) => !pathname.startsWith(`/${locale}/`) && pathname !== `/${locale}`
  )
  
  if (pathnameIsMissingLocale) {
    const locale = getLocale(request)
    return NextResponse.redirect(
      new URL(`/${locale}${pathname}`, request.url)
    )
  }
  
  return NextResponse.next()
}

export const config = {
  matcher: [
    // Skip all internal paths (_next)
    '/((?!_next/static|_next/image|favicon.ico).*)',
  ],
}
```

### 4. Rate Limiting

```typescript
// middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

// Simple in-memory store (use Redis in production)
const requests = new Map<string, { count: number; resetTime: number }>()

function rateLimit(ip: string, limit: number = 100, windowMs: number = 60000) {
  const now = Date.now()
  const record = requests.get(ip)
  
  if (!record || now > record.resetTime) {
    requests.set(ip, { count: 1, resetTime: now + windowMs })
    return true
  }
  
  if (record.count >= limit) {
    return false
  }
  
  record.count++
  return true
}

export function middleware(request: NextRequest) {
  const ip = request.ip ?? 'unknown'
  
  // Apply rate limiting to API routes
  if (request.nextUrl.pathname.startsWith('/api/')) {
    if (!rateLimit(ip, 100, 60000)) {
      return new NextResponse(
        JSON.stringify({ error: 'Too Many Requests' }),
        {
          status: 429,
          headers: {
            'Content-Type': 'application/json',
            'Retry-After': '60',
          },
        }
      )
    }
  }
  
  return NextResponse.next()
}
```

### 5. Security Headers

```typescript
// middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  const response = NextResponse.next()
  
  // Security headers
  response.headers.set('X-Frame-Options', 'DENY')
  response.headers.set('X-Content-Type-Options', 'nosniff')
  response.headers.set('Referrer-Policy', 'strict-origin-when-cross-origin')
  response.headers.set(
    'Content-Security-Policy',
    "default-src 'self'; script-src 'self' 'unsafe-eval' 'unsafe-inline'; style-src 'self' 'unsafe-inline';"
  )
  response.headers.set(
    'Strict-Transport-Security',
    'max-age=31536000; includeSubDomains; preload'
  )
  
  // CORS headers for API routes
  if (request.nextUrl.pathname.startsWith('/api/')) {
    response.headers.set('Access-Control-Allow-Origin', process.env.ALLOWED_ORIGIN || '*')
    response.headers.set('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
    response.headers.set('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    
    // Handle preflight requests
    if (request.method === 'OPTIONS') {
      return new NextResponse(null, { status: 200, headers: response.headers })
    }
  }
  
  return response
}
```

## Advanced Patterns

### 1. User Agent Detection

```typescript
// middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  const userAgent = request.headers.get('User-Agent') || ''
  
  // Detect mobile devices
  const isMobile = /Mobile|Android|iPhone|iPad|iPod|Windows Phone/i.test(userAgent)
  
  // Detect bots
  const isBot = /bot|crawler|spider|crawling/i.test(userAgent)
  
  if (isBot) {
    // Serve simplified version for bots
    return NextResponse.rewrite(new URL('/bot-version', request.url))
  }
  
  if (isMobile && request.nextUrl.pathname === '/') {
    // Serve mobile-optimized homepage
    return NextResponse.rewrite(new URL('/mobile-home', request.url))
  }
  
  return NextResponse.next()
}
```

### 2. Feature Flags

```typescript
// middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

const featureFlags = {
  newDashboard: {
    enabled: true,
    rolloutPercentage: 50, // 50% of users
  },
  betaFeatures: {
    enabled: true,
    allowedUsers: ['user1@example.com', 'user2@example.com'],
  },
}

export async function middleware(request: NextRequest) {
  const pathname = request.nextUrl.pathname
  
  // Check for new dashboard feature
  if (pathname.startsWith('/dashboard') && featureFlags.newDashboard.enabled) {
    const userId = request.cookies.get('userId')?.value
    
    if (userId) {
      // Consistent experience for the same user
      const hash = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(userId))
      const hashArray = Array.from(new Uint8Array(hash))
      const hashNumber = hashArray.reduce((a, b) => a + b, 0)
      const bucket = hashNumber % 100
      
      if (bucket < featureFlags.newDashboard.rolloutPercentage) {
        return NextResponse.rewrite(new URL('/new-dashboard', request.url))
      }
    }
  }
  
  return NextResponse.next()
}
```

### 3. Dynamic Routing with Database

```typescript
// middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

// Cache for performance (use Redis in production)
const slugCache = new Map<string, string>()

async function getPageBySlug(slug: string): Promise<string | null> {
  if (slugCache.has(slug)) {
    return slugCache.get(slug)!
  }
  
  try {
    // In production, use your database client
    const response = await fetch(`${process.env.API_URL}/pages/by-slug/${slug}`, {
      headers: { 'Authorization': `Bearer ${process.env.API_TOKEN}` }
    })
    
    if (response.ok) {
      const page = await response.json()
      slugCache.set(slug, page.type)
      return page.type
    }
  } catch (error) {
    console.error('Error fetching page:', error)
  }
  
  return null
}

export async function middleware(request: NextRequest) {
  const pathname = request.nextUrl.pathname
  
  // Handle dynamic pages
  if (pathname.length > 1 && !pathname.startsWith('/api') && !pathname.includes('.')) {
    const slug = pathname.slice(1) // Remove leading slash
    const pageType = await getPageBySlug(slug)
    
    if (pageType) {
      // Rewrite to the appropriate page type
      return NextResponse.rewrite(new URL(`/templates/${pageType}?slug=${slug}`, request.url))
    }
  }
  
  return NextResponse.next()
}
```

## Configuration

### Matcher Patterns

```typescript
export const config = {
  matcher: [
    // Match all paths
    '/(.*)',
    
    // Match specific paths
    '/dashboard/:path*',
    
    // Match multiple patterns
    ['/dashboard/:path*', '/admin/:path*'],
    
    // Exclude patterns (negative lookahead)
    '/((?!api|_next/static|_next/image|favicon.ico).*)',
    
    // Include specific file extensions
    '/api/(.*).json',
    
    // Complex patterns
    {
      source: '/((?!api|_next|.*\\.).*)',
      missing: [
        { type: 'header', key: 'next-router-prefetch' },
        { type: 'header', key: 'purpose', value: 'prefetch' },
      ],
    },
  ],
}
```

## Error Handling

```typescript
// middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export async function middleware(request: NextRequest) {
  try {
    // Your middleware logic here
    const result = await someAsyncOperation()
    
    if (!result) {
      throw new Error('Operation failed')
    }
    
    return NextResponse.next()
  } catch (error) {
    console.error('Middleware error:', error)
    
    // Return error response or continue
    if (process.env.NODE_ENV === 'production') {
      // Log error and continue in production
      return NextResponse.next()
    } else {
      // Show error in development
      return new NextResponse(
        JSON.stringify({ error: 'Middleware error', message: error.message }),
        { status: 500, headers: { 'Content-Type': 'application/json' } }
      )
    }
  }
}
```

## Testing Middleware

```typescript
// __tests__/middleware.test.ts
import { NextRequest } from 'next/server'
import { middleware } from '../middleware'

// Mock NextRequest
function createRequest(url: string, options: RequestInit = {}) {
  return new NextRequest(url, options)
}

describe('Middleware', () => {
  it('should redirect unauthenticated users from protected routes', async () => {
    const request = createRequest('http://localhost:3000/dashboard')
    const response = await middleware(request)
    
    expect(response.status).toBe(307)
    expect(response.headers.get('location')).toContain('/login')
  })
  
  it('should add security headers', async () => {
    const request = createRequest('http://localhost:3000/')
    const response = await middleware(request)
    
    expect(response.headers.get('X-Frame-Options')).toBe('DENY')
    expect(response.headers.get('X-Content-Type-Options')).toBe('nosniff')
  })
  
  it('should handle rate limiting', async () => {
    const request = createRequest('http://localhost:3000/api/test')
    // Simulate multiple requests...
    
    const response = await middleware(request)
    expect(response.status).toBe(429)
  })
})
```

## Best Practices

1. **Keep it Fast**: Middleware runs on every request, so optimize for speed
2. **Use Edge Runtime**: Middleware runs on the Edge, so use compatible APIs
3. **Implement Caching**: Cache expensive operations (database lookups, external API calls)
4. **Handle Errors Gracefully**: Don't let middleware errors break your site
5. **Test Thoroughly**: Middleware affects all routes, so test edge cases
6. **Monitor Performance**: Track middleware execution time
7. **Use Matcher Wisely**: Only run middleware where needed
8. **Avoid Heavy Operations**: Keep database queries and external API calls minimal

## Deployment Considerations

### Edge Runtime Limitations

```typescript
// ✅ Supported in Edge Runtime
- fetch()
- Headers, Request, Response APIs
- URL, URLSearchParams
- Web Crypto API
- TextEncoder, TextDecoder
- setTimeout, clearTimeout

// ❌ Not supported in Edge Runtime
- Node.js APIs (fs, path, etc.)
- Native modules
- Large libraries
- Synchronous operations
```

### Environment Variables

```typescript
// middleware.ts
export function middleware(request: NextRequest) {
  // Edge runtime environment variables
  const secret = process.env.MIDDLEWARE_SECRET
  const apiUrl = process.env.NEXT_PUBLIC_API_URL
  
  // Note: Only NEXT_PUBLIC_ variables are available in client-side code
  // but all variables are available in middleware
}
```

This comprehensive guide covers the essential patterns for implementing powerful middleware in Next.js applications.