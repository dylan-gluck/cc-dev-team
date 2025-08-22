# Performance Optimization

Comprehensive guide to optimizing Next.js applications for maximum performance and Core Web Vitals.

## Core Web Vitals

### Largest Contentful Paint (LCP)
Target: < 2.5 seconds

**Optimization Strategies:**

1. **Optimize Images**
```tsx
import Image from 'next/image'

// ✅ Optimized
<Image
  src="/hero.jpg"
  alt="Hero image"
  width={1200}
  height={600}
  priority // Load above-the-fold images with priority
  placeholder="blur"
  blurDataURL="data:image/jpeg;base64,/9j/4AAQSkZJRgABAQ..."
/>

// ❌ Not optimized
<img src="/hero.jpg" alt="Hero image" />
```

2. **Preload Critical Resources**
```tsx
// app/layout.tsx
export default function RootLayout({ children }) {
  return (
    <html>
      <head>
        <link rel="preload" href="/fonts/inter.woff2" as="font" type="font/woff2" crossOrigin="" />
        <link rel="preload" href="/api/critical-data" as="fetch" crossOrigin="" />
      </head>
      <body>{children}</body>
    </html>
  )
}
```

3. **Optimize Server-Side Rendering**
```tsx
// Use ISR for better performance
export const revalidate = 3600 // Revalidate every hour

export default async function Page() {
  // Fast database query
  const data = await fastQuery()
  return <Content data={data} />
}
```

### First Input Delay (FID) / Interaction to Next Paint (INP)
Target: < 100ms (FID) / < 200ms (INP)

**Optimization Strategies:**

1. **Code Splitting**
```tsx
import dynamic from 'next/dynamic'

// Lazy load heavy components
const HeavyChart = dynamic(() => import('./HeavyChart'), {
  loading: () => <ChartSkeleton />,
  ssr: false, // Skip SSR for client-only components
})

// Route-based splitting (automatic in Next.js)
// Each page is automatically code-split
```

2. **Reduce JavaScript Bundle Size**
```javascript
// next.config.js
module.exports = {
  experimental: {
    optimizePackageImports: ['lodash', 'date-fns'], // Tree-shake large libraries
  },
  compiler: {
    removeConsole: process.env.NODE_ENV === 'production', // Remove console.log in production
  },
}
```

3. **Use Web Workers for Heavy Tasks**
```tsx
// lib/worker.ts
export function performHeavyCalculation(data: any[]) {
  return new Promise((resolve) => {
    const worker = new Worker('/workers/calculation.js')
    worker.postMessage(data)
    worker.onmessage = (e) => {
      resolve(e.data)
      worker.terminate()
    }
  })
}

// Usage in component
'use client'
export default function DataProcessor() {
  const [result, setResult] = useState(null)
  
  useEffect(() => {
    performHeavyCalculation(largeDataset).then(setResult)
  }, [])
  
  return <div>{result}</div>
}
```

### Cumulative Layout Shift (CLS)
Target: < 0.1

**Optimization Strategies:**

1. **Reserve Space for Dynamic Content**
```tsx
// ✅ Good - Reserve space
<div className="h-64 w-full bg-gray-200 animate-pulse">
  {image ? (
    <Image src={image} alt="Content" fill className="object-cover" />
  ) : (
    <div>Loading...</div>
  )}
</div>

// ❌ Bad - Layout shift
{image && <Image src={image} alt="Content" />}
```

2. **Use Aspect Ratio for Images**
```css
/* styles/globals.css */
.aspect-video {
  aspect-ratio: 16 / 9;
}

.aspect-square {
  aspect-ratio: 1 / 1;
}
```

```tsx
<div className="aspect-video relative">
  <Image
    src="/video-thumbnail.jpg"
    alt="Video thumbnail"
    fill
    className="object-cover"
  />
</div>
```

3. **Preload Fonts**
```tsx
// app/layout.tsx
import { Inter } from 'next/font/google'

const inter = Inter({
  subsets: ['latin'],
  display: 'swap', // Prevent invisible text during font swap
  preload: true,
})

export default function RootLayout({ children }) {
  return (
    <html className={inter.className}>
      <body>{children}</body>
    </html>
  )
}
```

## Image Optimization

### Next.js Image Component Best Practices

```tsx
import Image from 'next/image'

// Hero images (above the fold)
<Image
  src="/hero.jpg"
  alt="Hero"
  width={1200}
  height={600}
  priority
  sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
/>

// Gallery images (lazy loaded)
<Image
  src="/gallery/image.jpg"
  alt="Gallery image"
  width={400}
  height={300}
  loading="lazy"
  placeholder="blur"
  blurDataURL="data:image/jpeg;base64,..."
/>

// Responsive images
<Image
  src="/responsive.jpg"
  alt="Responsive image"
  fill
  sizes="(max-width: 768px) 100vw, 50vw"
  style={{ objectFit: 'cover' }}
/>
```

### Custom Image Loader

```javascript
// next.config.js
module.exports = {
  images: {
    loader: 'custom',
    loaderFile: './lib/image-loader.js',
    domains: ['example.com'],
    formats: ['image/webp', 'image/avif'],
  },
}
```

```javascript
// lib/image-loader.js
export default function cloudinaryLoader({ src, width, quality }) {
  const params = ['f_auto', 'c_limit', `w_${width}`, `q_${quality || 'auto'}`]
  return `https://res.cloudinary.com/demo/image/fetch/${params.join(',')}/${src}`
}
```

## Bundle Optimization

### Analyzing Bundle Size

```bash
# Install bundle analyzer
npm install @next/bundle-analyzer

# Add to next.config.js
const withBundleAnalyzer = require('@next/bundle-analyzer')({
  enabled: process.env.ANALYZE === 'true',
})

module.exports = withBundleAnalyzer({
  // Your Next.js config
})

# Analyze bundle
ANALYZE=true npm run build
```

### Tree Shaking

```tsx
// ✅ Good - Import only what you need
import { format } from 'date-fns'
import debounce from 'lodash/debounce'

// ❌ Bad - Imports entire library
import * as dateFns from 'date-fns'
import _ from 'lodash'
```

### Dynamic Imports

```tsx
// Lazy load components
const LazyComponent = dynamic(() => import('./LazyComponent'), {
  loading: () => <Skeleton />,
})

// Conditional loading
const AdminPanel = dynamic(() => import('./AdminPanel'), {
  ssr: false, // Don't render on server
})

// Load with conditions
const AdvancedEditor = dynamic(
  () => import('./AdvancedEditor').then(mod => mod.AdvancedEditor),
  { 
    loading: () => <SimpleEditor />,
    ssr: false,
  }
)

export default function Page({ isAdmin, needsAdvanced }) {
  return (
    <div>
      {isAdmin && <AdminPanel />}
      {needsAdvanced ? <AdvancedEditor /> : <SimpleEditor />}
    </div>
  )
}
```

## Font Optimization

### Google Fonts Optimization

```tsx
// app/layout.tsx
import { Inter, Roboto_Mono } from 'next/font/google'

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-inter',
  display: 'swap',
})

const robotoMono = Roboto_Mono({
  subsets: ['latin'],
  variable: '--font-roboto-mono',
  display: 'swap',
})

export default function RootLayout({ children }) {
  return (
    <html className={`${inter.variable} ${robotoMono.variable}`}>
      <body>{children}</body>
    </html>
  )
}
```

### Local Fonts

```tsx
import localFont from 'next/font/local'

const myFont = localFont({
  src: [
    {
      path: './fonts/MyFont-Regular.woff2',
      weight: '400',
      style: 'normal',
    },
    {
      path: './fonts/MyFont-Bold.woff2',
      weight: '700',
      style: 'normal',
    },
  ],
  variable: '--font-my-font',
  display: 'swap',
})
```

## Caching Strategies

### HTTP Caching Headers

```javascript
// next.config.js
module.exports = {
  async headers() {
    return [
      {
        source: '/:all*(svg|jpg|png|webp|avif|gif)',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=31536000, immutable',
          },
        ],
      },
      {
        source: '/api/static/:path*',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=3600, s-maxage=3600',
          },
        ],
      },
    ]
  },
}
```

### Data Fetching Caching

```tsx
// Static caching
const staticData = await fetch('https://api.example.com/static', {
  cache: 'force-cache' // Cache indefinitely
})

// Time-based revalidation
const periodicData = await fetch('https://api.example.com/data', {
  next: { revalidate: 3600 } // Revalidate every hour
})

// Tag-based revalidation
const taggedData = await fetch('https://api.example.com/posts', {
  next: { tags: ['posts'] }
})

// No caching
const dynamicData = await fetch('https://api.example.com/realtime', {
  cache: 'no-store'
})
```

## Database Optimization

### Query Optimization

```tsx
// ✅ Good - Efficient queries
const posts = await prisma.post.findMany({
  select: {
    id: true,
    title: true,
    excerpt: true,
    author: {
      select: { name: true }
    }
  },
  take: 10,
  skip: (page - 1) * 10,
  orderBy: { createdAt: 'desc' },
})

// ❌ Bad - Over-fetching
const posts = await prisma.post.findMany({
  include: { 
    author: true,
    comments: { include: { author: true } },
    tags: true,
  }
})
```

### Connection Pooling

```typescript
// lib/db.ts
import { PrismaClient } from '@prisma/client'

const globalForPrisma = globalThis as unknown as {
  prisma: PrismaClient | undefined
}

export const prisma = globalForPrisma.prisma ?? new PrismaClient({
  datasources: {
    db: {
      url: process.env.DATABASE_URL + '?connection_limit=5&pool_timeout=20'
    }
  }
})

if (process.env.NODE_ENV !== 'production') globalForPrisma.prisma = prisma
```

## Third-party Scripts

### Optimized Script Loading

```tsx
import Script from 'next/script'

export default function Page() {
  return (
    <div>
      {/* Critical scripts */}
      <Script
        src="https://www.googletagmanager.com/gtag/js?id=GA_TRACKING_ID"
        strategy="afterInteractive"
      />
      
      {/* Non-critical scripts */}
      <Script
        src="https://widget.example.com/script.js"
        strategy="lazyOnload"
      />
      
      {/* Inline scripts */}
      <Script id="gtag-config" strategy="afterInteractive">
        {`
          window.dataLayer = window.dataLayer || [];
          function gtag(){dataLayer.push(arguments);}
          gtag('js', new Date());
          gtag('config', 'GA_TRACKING_ID');
        `}
      </Script>
    </div>
  )
}
```

## Performance Monitoring

### Core Web Vitals Measurement

```tsx
// app/layout.tsx
import { SpeedInsights } from '@vercel/speed-insights/next'
import { Analytics } from '@vercel/analytics/react'

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <SpeedInsights />
        <Analytics />
      </body>
    </html>
  )
}
```

### Custom Performance Metrics

```tsx
'use client'
import { useEffect } from 'react'

export function PerformanceMonitor() {
  useEffect(() => {
    // Monitor Core Web Vitals
    import('web-vitals').then(({ getCLS, getFID, getFCP, getLCP, getTTFB }) => {
      getCLS(console.log)
      getFID(console.log)
      getFCP(console.log)
      getLCP(console.log)
      getTTFB(console.log)
    })
    
    // Custom timing
    const startTime = performance.now()
    
    return () => {
      const endTime = performance.now()
      console.log(`Component render time: ${endTime - startTime}ms`)
    }
  }, [])
  
  return null
}
```

## Production Optimizations

### Next.js Configuration

```javascript
// next.config.js
module.exports = {
  // Enable gzip compression
  compress: true,
  
  // Remove powered-by header
  poweredByHeader: false,
  
  // Enable experimental features
  experimental: {
    optimizeCss: true, // Optimize CSS loading
    optimizePackageImports: ['@mui/material', 'lodash'],
  },
  
  // Compiler optimizations
  compiler: {
    removeConsole: process.env.NODE_ENV === 'production',
    styledComponents: true,
  },
  
  // Image optimization
  images: {
    formats: ['image/webp', 'image/avif'],
    minimumCacheTTL: 31536000,
  },
}
```

### Environment-Specific Optimizations

```tsx
// lib/analytics.ts
const isDevelopment = process.env.NODE_ENV === 'development'

export const analytics = {
  track: isDevelopment 
    ? (event: string, properties?: any) => console.log('Track:', event, properties)
    : (event: string, properties?: any) => realAnalytics.track(event, properties),
    
  page: isDevelopment
    ? (page: string) => console.log('Page:', page)
    : (page: string) => realAnalytics.page(page),
}
```

## Performance Checklist

- [ ] Images optimized with `next/image`
- [ ] Fonts preloaded and optimized
- [ ] Critical CSS inlined
- [ ] JavaScript bundles analyzed and optimized
- [ ] Database queries optimized
- [ ] Caching strategies implemented
- [ ] Core Web Vitals measured
- [ ] Third-party scripts optimized
- [ ] Compression enabled
- [ ] CDN configured
- [ ] Performance monitoring in place

This comprehensive guide provides the essential techniques for optimizing Next.js applications for maximum performance and excellent user experience.