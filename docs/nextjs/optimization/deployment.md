# Deployment Guide

Comprehensive guide for deploying Next.js applications to various platforms.

## Vercel (Recommended)

Vercel is the easiest way to deploy Next.js applications with zero configuration.

### Basic Deployment

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Or connect GitHub and auto-deploy
```

### Configuration

```json
// vercel.json
{
  "framework": "nextjs",
  "buildCommand": "npm run build",
  "outputDirectory": ".next",
  "installCommand": "npm install",
  "devCommand": "npm run dev",
  "env": {
    "DATABASE_URL": "@database-url",
    "NEXTAUTH_SECRET": "@nextauth-secret"
  },
  "build": {
    "env": {
      "NEXT_PUBLIC_API_URL": "https://api.example.com"
    }
  },
  "functions": {
    "app/api/**/*.ts": {
      "maxDuration": 30
    }
  },
  "regions": ["iad1", "sfo1"],
  "redirects": [
    {
      "source": "/old-path",
      "destination": "/new-path",
      "permanent": true
    }
  ],
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "X-Frame-Options",
          "value": "DENY"
        }
      ]
    }
  ]
}
```

### Environment Variables

```bash
# Set environment variables
vercel env add DATABASE_URL production
vercel env add NEXTAUTH_SECRET production
vercel env add NEXT_PUBLIC_API_URL production

# Pull environment variables locally
vercel env pull .env.local
```

## Self-Hosted Deployment

### Docker

```dockerfile
# Dockerfile
FROM node:18-alpine AS base

# Install dependencies only when needed
FROM base AS deps
RUN apk add --no-cache libc6-compat
WORKDIR /app

COPY package.json package-lock.json* ./
RUN \
  if [ -f package-lock.json ]; then npm ci --only=production; \
  else echo "Lockfile not found." && exit 1; \
  fi

# Rebuild the source code only when needed
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .

ENV NEXT_TELEMETRY_DISABLED 1

RUN npm run build

# Production image, copy all the files and run next
FROM base AS runner
WORKDIR /app

ENV NODE_ENV production
ENV NEXT_TELEMETRY_DISABLED 1

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public

# Set the correct permission for prerender cache
RUN mkdir .next
RUN chown nextjs:nodejs .next

# Automatically leverage output traces to reduce image size
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT 3000
ENV HOSTNAME "0.0.0.0"

CMD ["node", "server.js"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  nextjs:
    build: .
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - NEXTAUTH_SECRET=${NEXTAUTH_SECRET}
    depends_on:
      - postgres
      - redis

  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

### Next.js Configuration for Docker

```javascript
// next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  experimental: {
    outputFileTracingRoot: path.join(__dirname, '../../'),
  },
}

module.exports = nextConfig
```

## AWS Deployment

### AWS Amplify

```yaml
# amplify.yml
version: 1
frontend:
  phases:
    preBuild:
      commands:
        - npm ci
    build:
      commands:
        - npm run build
  artifacts:
    baseDirectory: .next
    files:
      - '**/*'
  cache:
    paths:
      - node_modules/**/*
      - .next/cache/**/*
```

### AWS Lambda with Serverless

```bash
npm install -g serverless
npm install serverless-nextjs-plugin
```

```yaml
# serverless.yml
service: my-nextjs-app

provider:
  name: aws
  runtime: nodejs18.x
  region: us-east-1

plugins:
  - serverless-nextjs-plugin

custom:
  nextjs:
    nextConfigDir: './'
    routes:
      - src: '/_next/static/*'
        headers:
          cache-control: 'public, max-age=31536000, immutable'

functions:
  nextjs:
    handler: index.handler
    events:
      - http:
          path: /{any+}
          method: ANY
```

### EC2 with PM2

```javascript
// ecosystem.config.js
module.exports = {
  apps: [
    {
      name: 'nextjs-app',
      script: 'node_modules/next/dist/bin/next',
      args: 'start',
      cwd: '/var/www/nextjs-app',
      instances: 'max',
      exec_mode: 'cluster',
      env: {
        NODE_ENV: 'production',
        PORT: 3000,
      },
      error_file: '/var/log/pm2/nextjs-error.log',
      out_file: '/var/log/pm2/nextjs-out.log',
      log_file: '/var/log/pm2/nextjs-combined.log',
    }
  ]
}
```

```bash
# Deployment script
#!/bin/bash
cd /var/www/nextjs-app
git pull origin main
npm ci --only=production
npm run build
pm2 reload ecosystem.config.js
```

## Google Cloud Platform

### Cloud Run

```dockerfile
# Dockerfile for Cloud Run
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

EXPOSE $PORT

CMD ["npm", "start"]
```

```yaml
# cloudbuild.yaml
steps:
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/nextjs-app', '.']
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/nextjs-app']
  - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
    entrypoint: 'gcloud'
    args:
      - 'run'
      - 'deploy'
      - 'nextjs-app'
      - '--image'
      - 'gcr.io/$PROJECT_ID/nextjs-app'
      - '--region'
      - 'us-central1'
      - '--platform'
      - 'managed'
      - '--allow-unauthenticated'
```

## Performance Optimization for Production

### Caching Strategy

```javascript
// next.config.js
module.exports = {
  async headers() {
    return [
      {
        source: '/_next/static/:path*',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=31536000, immutable',
          },
        ],
      },
      {
        source: '/:all*(svg|jpg|png|webp|ico|woff2)',
        locale: false,
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=31536000, must-revalidate',
          },
        ],
      },
    ]
  },
}
```

### CDN Configuration

```javascript
// For custom CDN
module.exports = {
  assetPrefix: process.env.NODE_ENV === 'production' 
    ? 'https://cdn.example.com' 
    : '',
  images: {
    loader: 'custom',
    loaderFile: './lib/image-loader.js',
  },
}
```

### Database Connection Optimization

```typescript
// lib/db.ts - Production connection pool
import { Pool } from 'pg'

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  max: 20, // Maximum number of clients
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
  ssl: process.env.NODE_ENV === 'production' ? { rejectUnauthorized: false } : false,
})

export default pool
```

## Monitoring and Logging

### Error Tracking

```bash
npm install @sentry/nextjs
```

```javascript
// sentry.client.config.js
import * as Sentry from '@sentry/nextjs'

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  tracesSampleRate: 1.0,
  debug: false,
  replaysOnErrorSampleRate: 1.0,
  replaysSessionSampleRate: 0.1,
  integrations: [
    new Sentry.Replay({
      maskAllText: true,
      blockAllMedia: true,
    }),
  ],
})
```

### Performance Monitoring

```tsx
// lib/analytics.ts
export function trackPerformance() {
  if (typeof window !== 'undefined') {
    import('web-vitals').then(({ getCLS, getFID, getFCP, getLCP, getTTFB }) => {
      getCLS(sendToAnalytics)
      getFID(sendToAnalytics)
      getFCP(sendToAnalytics)
      getLCP(sendToAnalytics)
      getTTFB(sendToAnalytics)
    })
  }
}

function sendToAnalytics(metric: any) {
  // Send to your analytics service
  console.log(metric)
}
```

## Health Checks

### API Health Check

```typescript
// app/api/health/route.ts
import { NextResponse } from 'next/server'

export async function GET() {
  try {
    // Check database connection
    const dbHealth = await checkDatabase()
    
    // Check external services
    const servicesHealth = await checkExternalServices()
    
    const health = {
      status: 'healthy',
      timestamp: new Date().toISOString(),
      services: {
        database: dbHealth,
        ...servicesHealth,
      },
      version: process.env.npm_package_version,
    }
    
    return NextResponse.json(health)
  } catch (error) {
    return NextResponse.json(
      {
        status: 'unhealthy',
        error: error.message,
        timestamp: new Date().toISOString(),
      },
      { status: 503 }
    )
  }
}

async function checkDatabase() {
  // Implement database health check
  return { status: 'connected', responseTime: 50 }
}

async function checkExternalServices() {
  // Check external APIs, Redis, etc.
  return {
    redis: { status: 'connected' },
    externalAPI: { status: 'connected' },
  }
}
```

## CI/CD Pipeline

### GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: 18
          cache: 'npm'
      
      - run: npm ci
      - run: npm run lint
      - run: npm run type-check
      - run: npm run test
      - run: npm run build

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v3
      - uses: amondnet/vercel-action@v20
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.ORG_ID}}
          vercel-project-id: ${{ secrets.PROJECT_ID}}
          vercel-args: '--prod'
```

## Security Configuration

### Content Security Policy

```javascript
// next.config.js
const securityHeaders = [
  {
    key: 'X-DNS-Prefetch-Control',
    value: 'on'
  },
  {
    key: 'Strict-Transport-Security',
    value: 'max-age=63072000; includeSubDomains; preload'
  },
  {
    key: 'X-XSS-Protection',
    value: '1; mode=block'
  },
  {
    key: 'X-Frame-Options',
    value: 'SAMEORIGIN'
  },
  {
    key: 'X-Content-Type-Options',
    value: 'nosniff'
  },
  {
    key: 'Referrer-Policy',
    value: 'origin-when-cross-origin'
  },
  {
    key: 'Content-Security-Policy',
    value: `
      default-src 'self';
      script-src 'self' 'unsafe-eval' 'unsafe-inline' *.googleapis.com;
      style-src 'self' 'unsafe-inline' *.googleapis.com;
      img-src * blob: data:;
      media-src 'none';
      connect-src *;
      font-src 'self' data: *.gstatic.com;
    `.replace(/\n/g, ''),
  },
]

module.exports = {
  async headers() {
    return [
      {
        source: '/:path*',
        headers: securityHeaders,
      },
    ]
  },
}
```

## Deployment Checklist

### Pre-deployment
- [ ] All tests passing
- [ ] TypeScript compilation successful
- [ ] ESLint checks passing
- [ ] Performance audit completed
- [ ] Security headers configured
- [ ] Environment variables set
- [ ] Database migrations ready
- [ ] Error tracking configured

### Post-deployment
- [ ] Health checks passing
- [ ] Performance monitoring active
- [ ] Error rates normal
- [ ] Database connections stable
- [ ] CDN functioning
- [ ] SSL certificate valid
- [ ] Monitoring alerts configured

This comprehensive deployment guide covers the most common deployment scenarios and best practices for Next.js applications in production.