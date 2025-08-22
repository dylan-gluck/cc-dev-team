# Data Fetching Patterns

Comprehensive guide to data fetching in Next.js with the App Router.

## Server Components Data Fetching

Server Components can fetch data directly using async/await.

### Basic Data Fetching

```tsx
// app/posts/page.tsx
export default async function PostsPage() {
  // Fetch data directly in Server Component
  const posts = await fetch('https://api.example.com/posts')
  
  if (!posts.ok) {
    throw new Error('Failed to fetch posts')
  }
  
  const data = await posts.json()
  
  return (
    <div>
      <h1>Blog Posts</h1>
      {data.map(post => (
        <article key={post.id}>
          <h2>{post.title}</h2>
          <p>{post.excerpt}</p>
        </article>
      ))}
    </div>
  )
}
```

### Parallel Data Fetching

```tsx
// app/dashboard/page.tsx
async function getUser() {
  const res = await fetch('https://api.example.com/user')
  return res.json()
}

async function getPosts() {
  const res = await fetch('https://api.example.com/posts')
  return res.json()
}

async function getAnalytics() {
  const res = await fetch('https://api.example.com/analytics')
  return res.json()
}

export default async function Dashboard() {
  // Fetch all data in parallel
  const [user, posts, analytics] = await Promise.all([
    getUser(),
    getPosts(),
    getAnalytics(),
  ])
  
  return (
    <div>
      <h1>Welcome, {user.name}</h1>
      <PostsList posts={posts} />
      <AnalyticsChart data={analytics} />
    </div>
  )
}
```

### Sequential Data Fetching

```tsx
// app/user/[id]/page.tsx
export default async function UserProfile({ params }: { params: { id: string } }) {
  // First fetch user
  const user = await fetch(`https://api.example.com/users/${params.id}`)
  const userData = await user.json()
  
  // Then fetch user's posts (depends on user data)
  const posts = await fetch(`https://api.example.com/users/${params.id}/posts`)
  const userPosts = await posts.json()
  
  return (
    <div>
      <h1>{userData.name}</h1>
      <UserPosts posts={userPosts} />
    </div>
  )
}
```

### Error Handling in Server Components

```tsx
// app/posts/page.tsx
async function fetchPosts() {
  try {
    const res = await fetch('https://api.example.com/posts')
    
    if (!res.ok) {
      throw new Error(`HTTP error! status: ${res.status}`)
    }
    
    return await res.json()
  } catch (error) {
    console.error('Failed to fetch posts:', error)
    throw error // Re-throw to trigger error.tsx
  }
}

export default async function PostsPage() {
  const posts = await fetchPosts()
  
  return (
    <div>
      {posts.map(post => (
        <PostCard key={post.id} post={post} />
      ))}
    </div>
  )
}
```

## Client Components Data Fetching

Client Components use traditional React patterns for data fetching.

### Using useEffect

```tsx
'use client'
import { useState, useEffect } from 'react'

export default function ClientPosts() {
  const [posts, setPosts] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  
  useEffect(() => {
    async function fetchPosts() {
      try {
        const res = await fetch('/api/posts')
        const data = await res.json()
        setPosts(data)
      } catch (err) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }
    
    fetchPosts()
  }, [])
  
  if (loading) return <div>Loading...</div>
  if (error) return <div>Error: {error}</div>
  
  return (
    <div>
      {posts.map(post => (
        <div key={post.id}>{post.title}</div>
      ))}
    </div>
  )
}
```

### Using SWR

```tsx
'use client'
import useSWR from 'swr'

const fetcher = (url: string) => fetch(url).then(res => res.json())

export default function PostsWithSWR() {
  const { data: posts, error, isLoading } = useSWR('/api/posts', fetcher)
  
  if (error) return <div>Failed to load</div>
  if (isLoading) return <div>Loading...</div>
  
  return (
    <div>
      {posts.map(post => (
        <div key={post.id}>{post.title}</div>
      ))}
    </div>
  )
}
```

### Using React Query (TanStack Query)

```tsx
'use client'
import { useQuery } from '@tanstack/react-query'

async function fetchPosts() {
  const res = await fetch('/api/posts')
  if (!res.ok) throw new Error('Network response was not ok')
  return res.json()
}

export default function PostsWithQuery() {
  const {
    data: posts,
    error,
    isLoading,
    refetch
  } = useQuery({
    queryKey: ['posts'],
    queryFn: fetchPosts,
  })
  
  if (isLoading) return <div>Loading...</div>
  if (error) return <div>Error: {error.message}</div>
  
  return (
    <div>
      <button onClick={() => refetch()}>Refresh</button>
      {posts.map(post => (
        <div key={post.id}>{post.title}</div>
      ))}
    </div>
  )
}
```

## Hybrid Data Fetching

Combine server and client data fetching for optimal performance.

### Server + Client Pattern

```tsx
// Server Component
export default async function ProductPage({ params }: { params: { id: string } }) {
  // Fetch critical data on server
  const product = await fetch(`https://api.example.com/products/${params.id}`)
  const productData = await product.json()
  
  return (
    <div>
      <ProductDetails product={productData} />
      <ClientReviews productId={params.id} />
    </div>
  )
}

// Client Component for non-critical data
'use client'
function ClientReviews({ productId }: { productId: string }) {
  const { data: reviews } = useSWR(`/api/products/${productId}/reviews`, fetcher)
  
  return (
    <div>
      <h3>Reviews</h3>
      {reviews?.map(review => (
        <ReviewCard key={review.id} review={review} />
      ))}
    </div>
  )
}
```

### Progressive Enhancement

```tsx
// app/posts/page.tsx - Server Component
export default async function PostsPage() {
  // Initial data from server
  const initialPosts = await fetch('https://api.example.com/posts?page=1')
  const posts = await initialPosts.json()
  
  return (
    <div>
      <h1>Blog Posts</h1>
      <PostsList initialData={posts} />
    </div>
  )
}

// Client Component with progressive loading
'use client'
function PostsList({ initialData }: { initialData: Post[] }) {
  const [posts, setPosts] = useState(initialData)
  const [page, setPage] = useState(1)
  const [loading, setLoading] = useState(false)
  
  const loadMore = async () => {
    setLoading(true)
    const res = await fetch(`/api/posts?page=${page + 1}`)
    const newPosts = await res.json()
    setPosts(prev => [...prev, ...newPosts])
    setPage(prev => prev + 1)
    setLoading(false)
  }
  
  return (
    <div>
      {posts.map(post => (
        <PostCard key={post.id} post={post} />
      ))}
      <button onClick={loadMore} disabled={loading}>
        {loading ? 'Loading...' : 'Load More'}
      </button>
    </div>
  )
}
```

## Database Integration

### Direct Database Queries in Server Components

```tsx
// lib/db.ts
import { Pool } from 'pg'

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
})

export async function getPosts() {
  const { rows } = await pool.query('SELECT * FROM posts ORDER BY created_at DESC')
  return rows
}

export async function getPost(id: string) {
  const { rows } = await pool.query('SELECT * FROM posts WHERE id = $1', [id])
  return rows[0]
}
```

```tsx
// app/posts/page.tsx
import { getPosts } from '@/lib/db'

export default async function PostsPage() {
  const posts = await getPosts()
  
  return (
    <div>
      {posts.map(post => (
        <article key={post.id}>
          <h2>{post.title}</h2>
          <p>{post.content}</p>
        </article>
      ))}
    </div>
  )
}
```

### Using Prisma

```tsx
// lib/prisma.ts
import { PrismaClient } from '@prisma/client'

const globalForPrisma = globalThis as unknown as {
  prisma: PrismaClient | undefined
}

export const prisma = globalForPrisma.prisma ?? new PrismaClient()

if (process.env.NODE_ENV !== 'production') globalForPrisma.prisma = prisma
```

```tsx
// app/posts/page.tsx
import { prisma } from '@/lib/prisma'

export default async function PostsPage() {
  const posts = await prisma.post.findMany({
    orderBy: { createdAt: 'desc' },
    include: { author: true },
  })
  
  return (
    <div>
      {posts.map(post => (
        <article key={post.id}>
          <h2>{post.title}</h2>
          <p>By {post.author.name}</p>
          <p>{post.content}</p>
        </article>
      ))}
    </div>
  )
}
```

## Data Fetching Best Practices

### 1. Use Server Components by Default

```tsx
// ✅ Good - Server Component
export default async function Page() {
  const data = await fetch('/api/data')
  return <div>{data}</div>
}

// ❌ Avoid - Client Component for static data
'use client'
export default function Page() {
  const [data, setData] = useState(null)
  useEffect(() => {
    fetch('/api/data').then(setData)
  }, [])
  return <div>{data}</div>
}
```

### 2. Handle Loading and Error States

```tsx
// app/posts/loading.tsx
export default function Loading() {
  return <PostsSkeleton />
}

// app/posts/error.tsx
'use client'
export default function Error({ error, reset }: {
  error: Error
  reset: () => void
}) {
  return (
    <div>
      <h2>Something went wrong!</h2>
      <button onClick={reset}>Try again</button>
    </div>
  )
}
```

### 3. Implement Proper Caching

```tsx
// Static data (cached indefinitely)
const staticData = await fetch('/api/static', { cache: 'force-cache' })

// Dynamic data (no caching)
const dynamicData = await fetch('/api/dynamic', { cache: 'no-store' })

// Revalidate periodically
const periodicData = await fetch('/api/periodic', { 
  next: { revalidate: 3600 } 
})
```

### 4. Use Type Safety

```tsx
interface Post {
  id: string
  title: string
  content: string
  author: {
    name: string
    email: string
  }
}

export default async function PostsPage() {
  const posts: Post[] = await fetch('/api/posts').then(res => res.json())
  
  return (
    <div>
      {posts.map(post => (
        <article key={post.id}>
          <h2>{post.title}</h2>
          <p>By {post.author.name}</p>
        </article>
      ))}
    </div>
  )
}
```

### 5. Optimize Data Fetching

```tsx
// ✅ Good - Parallel fetching
const [user, posts, comments] = await Promise.all([
  getUser(id),
  getPosts(id),
  getComments(id),
])

// ❌ Avoid - Sequential fetching
const user = await getUser(id)
const posts = await getPosts(id)
const comments = await getComments(id)
```

This comprehensive guide covers the main data fetching patterns in Next.js 13+ with the App Router, helping you choose the right approach for your specific use case.