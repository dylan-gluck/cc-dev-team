# Rendering Methods in Next.js

Next.js provides multiple rendering strategies to optimize performance and user experience.

## Overview

| Method | When | Where | Cache | Use Case |
|--------|------|-------|-------|----------|
| **SSG** | Build time | Server | Yes | Static content, blogs |
| **ISR** | Build + Runtime | Server | Yes | Semi-static content |
| **SSR** | Request time | Server | No | Dynamic content |
| **CSR** | Runtime | Client | No | Interactive apps |

## Static Site Generation (SSG)

Pre-render pages at build time. Best for content that doesn't change often.

### Basic SSG

```tsx
// app/blog/page.tsx
export default async function BlogPage() {
  // This fetch happens at build time
  const posts = await fetch('https://api.example.com/posts')
  
  return (
    <div>
      <h1>Blog Posts</h1>
      {posts.map(post => (
        <article key={post.id}>
          <h2>{post.title}</h2>
          <p>{post.excerpt}</p>
        </article>
      ))}
    </div>
  )
}
```

### Dynamic SSG with generateStaticParams

```tsx
// app/blog/[slug]/page.tsx
export default async function BlogPost({ params }: { params: { slug: string } }) {
  const post = await fetch(`https://api.example.com/posts/${params.slug}`)
  
  return (
    <article>
      <h1>{post.title}</h1>
      <div>{post.content}</div>
    </article>
  )
}

// Generate static params at build time
export async function generateStaticParams() {
  const posts = await fetch('https://api.example.com/posts')
  
  return posts.map((post) => ({
    slug: post.slug,
  }))
}
```

### Benefits of SSG
- Fastest loading times
- Great SEO
- CDN cacheable
- Reduced server load

### When to Use SSG
- Marketing pages
- Blog posts
- Documentation
- E-commerce product pages
- Any content that doesn't change frequently

## Incremental Static Regeneration (ISR)

Update static content after build without rebuilding the entire site.

### Time-based Revalidation

```tsx
// app/posts/page.tsx
export default async function Posts() {
  const posts = await fetch('https://api.example.com/posts', {
    next: { revalidate: 3600 } // Revalidate every hour
  })
  
  return (
    <div>
      {posts.map(post => (
        <div key={post.id}>{post.title}</div>
      ))}
    </div>
  )
}
```

### On-demand Revalidation

```tsx
// app/api/revalidate/route.ts
import { revalidatePath } from 'next/cache'
import { NextRequest } from 'next/server'

export async function POST(request: NextRequest) {
  const secret = request.nextUrl.searchParams.get('secret')
  
  if (secret !== process.env.REVALIDATE_SECRET) {
    return Response.json({ message: 'Invalid secret' }, { status: 401 })
  }
  
  try {
    // Revalidate the specific path
    revalidatePath('/posts')
    return Response.json({ revalidated: true })
  } catch (err) {
    return Response.json({ message: 'Error revalidating' }, { status: 500 })
  }
}
```

### Tag-based Revalidation

```tsx
// Fetch with tags
const posts = await fetch('https://api.example.com/posts', {
  next: { tags: ['posts'] }
})

// Revalidate by tag
import { revalidateTag } from 'next/cache'

export async function POST() {
  revalidateTag('posts')
  return Response.json({ revalidated: true })
}
```

### Benefits of ISR
- Fast like SSG
- Content stays fresh
- No full rebuilds needed
- Handles traffic spikes

### When to Use ISR
- News sites
- E-commerce catalogs
- Social media feeds
- Content that updates regularly

## Server-Side Rendering (SSR)

Render pages on each request. Best for highly dynamic content.

### Force Dynamic Rendering

```tsx
// app/dashboard/page.tsx
export const dynamic = 'force-dynamic'

export default async function Dashboard() {
  // This runs on every request
  const user = await getCurrentUser()
  const data = await getUserData(user.id)
  
  return (
    <div>
      <h1>Welcome, {user.name}</h1>
      <div>{data.content}</div>
    </div>
  )
}
```

### Conditional SSR

```tsx
// app/profile/page.tsx
export default async function Profile({ searchParams }: { 
  searchParams: { refresh?: string } 
}) {
  // Fresh data if refresh param is present
  const user = await fetch('/api/user', {
    cache: searchParams.refresh ? 'no-store' : 'default'
  })
  
  return <div>User: {user.name}</div>
}
```

### Benefits of SSR
- Always up-to-date content
- Good SEO
- Personalized content
- Secure data access

### When to Use SSR
- User dashboards
- Real-time data
- Personalized content
- Authentication-required pages

## Client-Side Rendering (CSR)

Render in the browser. Best for highly interactive applications.

### Using Client Components

```tsx
'use client'
import { useState, useEffect } from 'react'

export default function ClientDashboard() {
  const [data, setData] = useState(null)
  
  useEffect(() => {
    fetch('/api/data')
      .then(res => res.json())
      .then(setData)
  }, [])
  
  if (!data) return <div>Loading...</div>
  
  return (
    <div>
      <h1>Client Dashboard</h1>
      <InteractiveChart data={data} />
    </div>
  )
}
```

### Hybrid Approach

```tsx
// Server Component (default)
export default async function Page() {
  const initialData = await fetch('/api/initial-data')
  
  return (
    <div>
      <h1>Page Title</h1>
      <StaticContent data={initialData} />
      <ClientInteractiveComponent initialData={initialData} />
    </div>
  )
}

// Client Component for interactivity
'use client'
function ClientInteractiveComponent({ initialData }) {
  const [data, setData] = useState(initialData)
  
  return (
    <div>
      <button onClick={() => updateData()}>Update</button>
      {/* Interactive UI */}
    </div>
  )
}
```

### Benefits of CSR
- Highly interactive
- Fast subsequent navigation
- Rich user interactions
- Real-time updates

### When to Use CSR
- Interactive dashboards
- Real-time applications
- Complex forms
- Games and interactive tools

## Streaming and Suspense

Progressively render parts of the page as they become ready.

### Streaming with Suspense

```tsx
// app/dashboard/page.tsx
import { Suspense } from 'react'
import { Analytics } from './analytics'
import { UserProfile } from './user-profile'

export default function Dashboard() {
  return (
    <div>
      <h1>Dashboard</h1>
      
      <Suspense fallback={<div>Loading user profile...</div>}>
        <UserProfile />
      </Suspense>
      
      <Suspense fallback={<div>Loading analytics...</div>}>
        <Analytics />
      </Suspense>
    </div>
  )
}
```

### Loading Components

```tsx
// app/dashboard/loading.tsx
export default function Loading() {
  return (
    <div className="animate-pulse">
      <div className="h-8 bg-gray-200 rounded w-1/4 mb-4"></div>
      <div className="h-4 bg-gray-200 rounded w-full mb-2"></div>
      <div className="h-4 bg-gray-200 rounded w-3/4"></div>
    </div>
  )
}
```

## Performance Optimization

### Caching Strategies

```tsx
// Cache for 1 hour, revalidate in background
const data = await fetch('/api/data', {
  next: { 
    revalidate: 3600,
    tags: ['data']
  }
})

// No caching (always fresh)
const realTimeData = await fetch('/api/realtime', {
  cache: 'no-store'
})

// Cache indefinitely until manually revalidated
const staticData = await fetch('/api/static', {
  cache: 'force-cache'
})
```

### Partial Prerendering (Experimental)

```tsx
// next.config.js
module.exports = {
  experimental: {
    ppr: true,
  },
}

// app/dashboard/page.tsx
export default function Dashboard() {
  return (
    <div>
      {/* Static shell renders immediately */}
      <nav>Static Navigation</nav>
      
      {/* Dynamic content streams in */}
      <Suspense fallback={<Skeleton />}>
        <DynamicContent />
      </Suspense>
    </div>
  )
}
```

## Choosing the Right Strategy

### Decision Matrix

**Use SSG when:**
- Content rarely changes
- SEO is important
- Performance is critical
- Content is public

**Use ISR when:**
- Content updates periodically
- You need SSG benefits with fresh content
- You have many pages
- Content has predictable update patterns

**Use SSR when:**
- Content is highly dynamic
- You need real-time data
- Content is personalized
- SEO is important for dynamic content

**Use CSR when:**
- Highly interactive applications
- Real-time user interactions
- Complex state management
- Private, authenticated content

### Hybrid Approach

Most applications benefit from combining strategies:

```tsx
// Static marketing pages (SSG)
app/
├── page.tsx              # SSG
├── about/
│   └── page.tsx          # SSG
├── blog/
│   ├── page.tsx          # ISR
│   └── [slug]/
│       └── page.tsx      # ISR with generateStaticParams
├── dashboard/
│   ├── page.tsx          # SSR (personalized)
│   └── analytics/
│       └── page.tsx      # CSR (interactive)
└── api/                  # Server-side APIs
```

## Best Practices

1. **Start with SSG** - Use the fastest option by default
2. **Use ISR for semi-dynamic content** - Best of both worlds
3. **Reserve SSR for truly dynamic content** - Only when necessary
4. **Combine strategies** - Different pages can use different strategies
5. **Use Suspense for better UX** - Progressive loading
6. **Implement proper caching** - Optimize data fetching
7. **Monitor Core Web Vitals** - Measure real performance impact
8. **Consider edge rendering** - For global applications

The key is to choose the right rendering strategy for each part of your application based on your specific requirements for performance, freshness, and interactivity.