# API Contract: Backend Container Build Interface

## Build Configuration

**Image Name**: `todo-backend:latest`
**Build Context**: `./backend`
**Base Image**: `python:3.11-slim`

## Build Arguments
- `PYTHON_ENV`: Production/development environment (default: production)

## Ports
- `8000`: HTTP port for FastAPI application

## Health Check
- **Endpoint**: `GET /health`
- **Interval**: 30 seconds
- **Timeout**: 10 seconds
- **Retries**: 3
- **Start Period**: 45 seconds

## Environment Variables
- `GEMINI_API_KEY`: API key for Gemini integration (required)
- `DATABASE_URL`: Connection string for Neon PostgreSQL (required)
- `BETTER_AUTH_SECRET`: Secret for JWT token signing (required)
- `UVICORN_HOST`: Host for uvicorn server (default: 0.0.0.0)
- `UVICORN_PORT`: Port for uvicorn server (default: 8000)

## Volumes
- `/app/logs`: Application logs directory

## Commands
- **Start**: `uvicorn main:app --host 0.0.0.0 --port 8000` (exposes port 8000)

## Dependencies
- Python 3.11
- All dependencies listed in requirements.txt
- FastAPI
- Uvicorn ASGI server

## Expected Behavior
- Container starts and serves the FastAPI application
- Responds to health checks at /health endpoint
- Properly handles environment variables
- Gracefully handles shutdown signals
- Logs to stdout/stderr for container logging systems