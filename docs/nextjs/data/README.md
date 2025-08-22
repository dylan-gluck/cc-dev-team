# Data Fetching and Caching

Next.js data fetching patterns and caching strategies.

## Contents

- **fetching-patterns.md** - Data fetching in Server and Client Components
- **caching-strategies.md** - Advanced caching and revalidation
- **database-integration.md** - Database patterns and ORMs
- **external-apis.md** - Working with external APIs

## Quick Reference

### Fetching Methods
- **Server Components** - `fetch()` directly in components
- **Client Components** - `useEffect`, SWR, React Query
- **API Routes** - Backend data processing

### Caching Options
- `cache: 'force-cache'` - Cache indefinitely
- `cache: 'no-store'` - No caching
- `next: { revalidate: 60 }` - Time-based revalidation
- `next: { tags: ['posts'] }` - Tag-based revalidation