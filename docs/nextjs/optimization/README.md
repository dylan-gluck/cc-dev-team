# Performance Optimization & Deployment

Next.js performance optimization strategies and deployment guides.

## Contents

- **performance.md** - Core Web Vitals optimization techniques
- **deployment.md** - Deployment strategies and best practices  
- **caching.md** - Advanced caching strategies
- **bundle-optimization.md** - Bundle size and code splitting optimization

## Performance Priorities

1. **Core Web Vitals**
   - Largest Contentful Paint (LCP)
   - First Input Delay (FID) / Interaction to Next Paint (INP)
   - Cumulative Layout Shift (CLS)

2. **Next.js Optimizations**
   - Image optimization
   - Font optimization
   - Code splitting
   - Static generation
   - Edge caching

## Quick Wins

- Use `next/image` for all images
- Implement proper loading states
- Enable compression and caching
- Minimize JavaScript bundles
- Use CDN for static assets