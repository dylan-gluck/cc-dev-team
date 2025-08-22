# App Router Guide

The App Router is Next.js's modern routing system introduced in Next.js 13, built on top of React Server Components.

## Overview

The App Router uses the `app/` directory for routing, replacing the legacy `pages/` directory approach.

### Key Benefits

- **React Server Components** - Better performance and SEO
- **Streaming** - Progressive loading of page segments
- **Nested Layouts** - Shared UI that preserves state
- **Colocation** - Keep related files together
- **Advanced Routing** - Parallel routes, intercepting routes

## Routing Fundamentals

### File Conventions

| File | Purpose |
|------|---------|
| `layout.js` | Shared UI for a segment and its children |
| `page.js` | Unique UI of a route and make routes publicly accessible |
| `loading.js` | Loading UI for a segment and its children |
| `not-found.js` | Not found UI for a segment and its children |
| `error.js` | Error UI for a segment and its children |
| `global-error.js` | Global error UI |
| `route.js` | Server-side API endpoint |
| `template.js` | Re-rendered layout UI |
| `default.js` | Fallback UI for Parallel Routes |

### Route Structure

```
app/
├── layout.tsx          # Root layout (required)
├── page.tsx           # Home page (/)
├── about/
│   └── page.tsx       # About page (/about)
├── blog/
│   ├── layout.tsx     # Blog layout
│   ├── page.tsx       # Blog index (/blog)
│   └── [slug]/
│       └── page.tsx   # Blog post (/blog/[slug])
└── dashboard/
    ├── layout.tsx     # Dashboard layout
    ├── page.tsx       # Dashboard (/dashboard)
    ├── analytics/
    │   └── page.tsx   # Analytics (/dashboard/analytics)
    └── settings/
        └── page.tsx   # Settings (/dashboard/settings)
```

## Dynamic Routes

### Single Dynamic Segment

```tsx
// app/blog/[slug]/page.tsx
export default function BlogPost({ params }: { params: { slug: string } }) {
  return <h1>Post: {params.slug}</h1>
}

// Matches: /blog/hello-world, /blog/my-post
```

### Multiple Dynamic Segments

```tsx
// app/shop/[...categories]/page.tsx
export default function Shop({ params }: { params: { categories: string[] } }) {
  return <h1>Categories: {params.categories.join('/')}</h1>
}

// Matches: /shop/clothes, /shop/clothes/tops, /shop/clothes/tops/t-shirts
```

### Optional Catch-all Routes

```tsx
// app/docs/[[...slug]]/page.tsx
export default function Docs({ params }: { params: { slug?: string[] } }) {
  return <h1>Docs: {params.slug?.join('/') || 'Home'}</h1>
}

// Matches: /docs, /docs/getting-started, /docs/api/reference
```

## Layouts

### Root Layout (Required)

```tsx
// app/layout.tsx
export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>
        <header>Global Header</header>
        {children}
        <footer>Global Footer</footer>
      </body>
    </html>
  )
}
```

### Nested Layouts

```tsx
// app/dashboard/layout.tsx
export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div className="dashboard">
      <nav>Dashboard Navigation</nav>
      <main>{children}</main>
    </div>
  )
}
```

### Layout Composition

Layouts compose automatically:

```
app/
├── layout.tsx          # Root layout
└── dashboard/
    ├── layout.tsx      # Dashboard layout
    ├── page.tsx        # Uses both root + dashboard layouts
    └── settings/
        ├── layout.tsx  # Settings layout
        └── page.tsx    # Uses root + dashboard + settings layouts
```

## Route Groups

Organize routes without affecting URL structure using parentheses:

```
app/
├── (marketing)/
│   ├── layout.tsx      # Marketing layout
│   ├── about/
│   │   └── page.tsx    # /about
│   └── contact/
│       └── page.tsx    # /contact
├── (shop)/
│   ├── layout.tsx      # Shop layout
│   ├── cart/
│   │   └── page.tsx    # /cart
│   └── checkout/
│       └── page.tsx    # /checkout
└── layout.tsx          # Root layout
```

## Parallel Routes

Display multiple pages in the same layout simultaneously:

```
app/
├── layout.tsx
├── page.tsx
├── @analytics/         # Parallel route slot
│   └── page.tsx
├── @team/              # Parallel route slot
│   └── page.tsx
└── dashboard/
    ├── @analytics/
    │   └── page.tsx
    └── @team/
        └── page.tsx
```

```tsx
// app/layout.tsx
export default function Layout({
  children,
  analytics,
  team,
}: {
  children: React.ReactNode
  analytics: React.ReactNode
  team: React.ReactNode
}) {
  return (
    <>
      {children}
      <div className="grid">
        {analytics}
        {team}
      </div>
    </>
  )
}
```

## Intercepting Routes

Intercept routes to show in modal or overlay:

```
app/
├── layout.tsx
├── page.tsx
├── photo/
│   └── [id]/
│       └── page.tsx    # Full page view
└── (..)photo/          # Intercept when navigating from parent
    └── [id]/
        └── page.tsx    # Modal view
```

Intercepting conventions:
- `(.)` - same level
- `(..)` - one level up
- `(..)(..)` - two levels up
- `(...)` - from root

## Navigation

### Link Component

```tsx
import Link from 'next/link'

export default function Navigation() {
  return (
    <nav>
      <Link href="/">Home</Link>
      <Link href="/about">About</Link>
      <Link href="/blog/hello-world">Blog Post</Link>
    </nav>
  )
}
```

### useRouter Hook

```tsx
'use client'
import { useRouter } from 'next/navigation'

export default function Button() {
  const router = useRouter()

  return (
    <button onClick={() => router.push('/dashboard')}>
      Go to Dashboard
    </button>
  )
}
```

### Programmatic Navigation

```tsx
import { redirect } from 'next/navigation'

export default async function Profile() {
  const session = await getSession()
  
  if (!session) {
    redirect('/login')
  }
  
  return <div>Profile Page</div>
}
```

## Loading UI

Create instant loading states:

```tsx
// app/dashboard/loading.tsx
export default function Loading() {
  return (
    <div className="flex justify-center items-center h-screen">
      <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-gray-900"></div>
    </div>
  )
}
```

## Error Handling

### Error Boundaries

```tsx
// app/dashboard/error.tsx
'use client'

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  return (
    <div className="error-boundary">
      <h2>Something went wrong!</h2>
      <p>{error.message}</p>
      <button onClick={reset}>Try again</button>
    </div>
  )
}
```

### Not Found Pages

```tsx
// app/not-found.tsx
import Link from 'next/link'

export default function NotFound() {
  return (
    <div>
      <h2>Not Found</h2>
      <p>Could not find requested resource</p>
      <Link href="/">Return Home</Link>
    </div>
  )
}
```

## Metadata

### Static Metadata

```tsx
// app/page.tsx
import { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'My App',
  description: 'Welcome to my app',
}

export default function Page() {
  return <h1>Hello World</h1>
}
```

### Dynamic Metadata

```tsx
// app/blog/[slug]/page.tsx
export async function generateMetadata(
  { params }: { params: { slug: string } }
): Promise<Metadata> {
  const post = await getPost(params.slug)
  
  return {
    title: post.title,
    description: post.excerpt,
    openGraph: {
      title: post.title,
      description: post.excerpt,
      images: [post.image],
    },
  }
}
```

## Best Practices

1. **Use layouts for shared UI** - Avoid duplication
2. **Colocate related files** - Keep components near pages
3. **Use loading.tsx** - Provide instant feedback
4. **Implement error boundaries** - Graceful error handling
5. **Optimize with Server Components** - Reduce bundle size
6. **Use route groups** - Organize without affecting URLs
7. **Implement proper metadata** - Better SEO and sharing

## Migration from Pages Router

Key differences when migrating:

| Pages Router | App Router |
|-------------|------------|
| `pages/` directory | `app/` directory |
| `_app.js` for layouts | `layout.js` files |
| `getStaticProps` | `fetch()` in Server Components |
| `getServerSideProps` | `fetch()` in Server Components |
| `pages/api/` | `app/api/route.js` |
| Client-side by default | Server Components by default |

The App Router provides a more powerful and flexible routing system that better aligns with modern React patterns and provides improved performance characteristics.