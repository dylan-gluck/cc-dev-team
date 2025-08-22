# Next.js Fundamentals

## What is Next.js?

Next.js is a React framework that provides:
- Server-side rendering (SSR)
- Static site generation (SSG)
- File-system based routing
- API routes
- Built-in optimization features

## Project Structure

### App Router Structure (Recommended - Next.js 13+)

```
my-app/
├── app/                    # App Router directory
│   ├── globals.css         # Global styles
│   ├── layout.tsx          # Root layout
│   ├── loading.tsx         # Loading UI
│   ├── error.tsx          # Error UI
│   ├── not-found.tsx      # 404 page
│   ├── page.tsx           # Home page
│   ├── about/
│   │   └── page.tsx       # /about route
│   ├── blog/
│   │   ├── page.tsx       # /blog route
│   │   └── [slug]/
│   │       └── page.tsx   # /blog/[slug] route
│   └── api/               # API routes
│       └── users/
│           └── route.ts   # /api/users endpoint
├── components/            # Reusable components
├── lib/                   # Utility functions
├── public/                # Static assets
├── next.config.js         # Next.js configuration
├── package.json
└── tsconfig.json
```

## Key Concepts

### 1. File-System Based Routing

Next.js automatically creates routes based on file structure:

- `app/page.tsx` → `/`
- `app/about/page.tsx` → `/about`
- `app/blog/[slug]/page.tsx` → `/blog/:slug`

### 2. React Server Components (RSC)

**Server Components** (default in App Router):
- Render on the server
- Can access backend resources directly
- Reduce bundle size
- Better SEO and initial page load

**Client Components** (opt-in with `"use client"`):
- Render on the client
- Can use browser-only APIs
- Support interactivity and event handlers

```tsx
// Server Component (default)
export default function BlogPost({ params }) {
  const post = await fetch(`/api/posts/${params.slug}`)
  return <article>{post.content}</article>
}

// Client Component
"use client"
export default function Counter() {
  const [count, setCount] = useState(0)
  return (
    <button onClick={() => setCount(count + 1)}>
      Count: {count}
    </button>
  )
}
```

### 3. Layouts

Layouts are shared UI that persist across multiple pages:

```tsx
// app/layout.tsx (Root Layout - Required)
export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>
        <header>My App</header>
        {children}
        <footer>© 2025</footer>
      </body>
    </html>
  )
}

// app/dashboard/layout.tsx (Nested Layout)
export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div className="flex">
      <nav>Dashboard Nav</nav>
      <main>{children}</main>
    </div>
  )
}
```

### 4. Special Files

- `layout.tsx` - Shared UI for a segment and its children
- `page.tsx` - Unique UI of a route and make routes publicly accessible
- `loading.tsx` - Loading UI for a segment and its children
- `error.tsx` - Error UI for a segment and its children
- `not-found.tsx` - Not found UI for a segment and its children
- `route.tsx` - Server-side API endpoint

## Environment Setup

### Installation

```bash
# Create new app
npx create-next-app@latest my-app

# With TypeScript
npx create-next-app@latest my-app --typescript

# With App Router (default)
npx create-next-app@latest my-app --app

# Development
cd my-app
npm run dev
```

### Configuration

```javascript
// next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    appDir: true, // Enable App Router (default in Next.js 13.4+)
  },
  images: {
    domains: ['example.com'],
  },
  env: {
    CUSTOM_KEY: process.env.CUSTOM_KEY,
  },
}

module.exports = nextConfig
```

### Environment Variables

```bash
# .env.local
DATABASE_URL=postgresql://...
NEXTAUTH_SECRET=your-secret-key
NEXTAUTH_URL=http://localhost:3000

# .env (committed to version control)
NEXT_PUBLIC_API_URL=https://api.example.com
```

## Best Practices

1. **Use App Router** for new projects (Next.js 13+)
2. **Server Components by default**, Client Components when needed
3. **Co-locate related files** in feature directories
4. **Use TypeScript** for better developer experience
5. **Optimize images** with `next/image`
6. **Implement proper error boundaries** with error.tsx files
7. **Use loading.tsx** for better UX during navigation

## Common Patterns

### Page Structure

```tsx
// app/blog/[slug]/page.tsx
import { notFound } from 'next/navigation'

export default async function BlogPost({ params }: { params: { slug: string } }) {
  const post = await getPost(params.slug)
  
  if (!post) {
    notFound()
  }
  
  return (
    <article>
      <h1>{post.title}</h1>
      <p>{post.content}</p>
    </article>
  )
}

export async function generateStaticParams() {
  const posts = await getAllPosts()
  return posts.map((post) => ({ slug: post.slug }))
}
```

### Error Handling

```tsx
// app/blog/error.tsx
'use client'

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  return (
    <div>
      <h2>Something went wrong!</h2>
      <button onClick={() => reset()}>Try again</button>
    </div>
  )
}
```

This foundation will help you understand the core concepts needed to build modern Next.js applications.