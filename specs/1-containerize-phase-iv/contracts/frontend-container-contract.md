# API Contract: Frontend Container Build Interface

## Build Configuration

**Image Name**: `todo-frontend:latest`
**Build Context**: `./frontend`
**Base Image**: `node:18-alpine`

## Build Arguments
- `NODE_ENV`: Production/development environment (default: production)

## Ports
- `3000`: HTTP port for Next.js application

## Health Check
- **Endpoint**: `GET /`
- **Interval**: 30 seconds
- **Timeout**: 10 seconds
- **Retries**: 3
- **Start Period**: 60 seconds

## Environment Variables
- `GEMINI_API_KEY`: API key for Gemini integration (required)
- `DATABASE_URL`: Connection string for Neon PostgreSQL (required)
- `BETTER_AUTH_SECRET`: Secret for JWT token signing (required)
- `NEXT_PUBLIC_BASE_URL`: Base URL for the application (optional)

## Volumes
- `/app/.next`: Next.js build artifacts (for caching in development)

## Commands
- **Development**: `npm run dev` (exposes port 3000)
- **Production**: `npm start` (exposes port 3000)

## Dependencies
- Node.js 18.x
- npm 8.x or yarn
- Next.js 16+
- All dependencies listed in package.json

## Expected Behavior
- Container starts and serves the Next.js application
- Responds to health checks
- Properly handles environment variables
- Gracefully handles shutdown signals