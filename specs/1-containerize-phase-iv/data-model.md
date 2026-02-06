# Data Model: Containerization for Phase IV Local Kubernetes Deployment

## Container Configuration Entities

### [Frontend Docker Image]
- **Image Name**: `todo-frontend:latest`
- **Base Image**: Node.js LTS (18-alpine or newer)
- **Build Stage**:
  - Dependencies: Install from package-lock.json
  - Build: Run `npm run build`
  - Assets: Copy build artifacts to intermediate stage
- **Runtime Stage**:
  - Dependencies: Only runtime dependencies
  - Assets: Copy from build stage
  - Command: `npm run dev` (for development) or `npm start` (for production)
  - Port: 3000
- **Environment Variables**:
  - `GEMINI_API_KEY`: API key for Gemini integration
  - `DATABASE_URL`: Connection string for Neon PostgreSQL
  - `BETTER_AUTH_SECRET`: Secret for JWT token signing
- **Validation Rules**:
  - Must expose port 3000
  - Must accept environment variables
  - Must run without build dependencies in runtime

### [Backend Docker Image]
- **Image Name**: `todo-backend:latest`
- **Base Image**: Python 3.11 (slim or alpine variant)
- **Build Stage**:
  - Dependencies: Install from requirements.txt
  - Assets: Copy application code
- **Runtime Stage**:
  - Dependencies: Only runtime dependencies
  - Assets: Copy from build stage
  - Command: `uvicorn main:app --host 0.0.0.0 --port 8000`
  - Port: 8000
- **Environment Variables**:
  - `GEMINI_API_KEY`: API key for Gemini integration
  - `DATABASE_URL`: Connection string for Neon PostgreSQL
  - `BETTER_AUTH_SECRET`: Secret for JWT token signing
- **Validation Rules**:
  - Must expose port 8000
  - Must accept environment variables
  - Must run uvicorn with correct host binding

### [Dockerfile]
- **Structure**: Multi-stage build with separate build and runtime stages
- **Layers**: Optimized layer caching for faster builds
- **Security**: Non-root user in runtime stage
- **Size**: Minimized through multi-stage approach
- **Validation Rules**:
  - Must follow Docker best practices
  - Must use specific base image tags (not latest)
  - Must include health check instructions

### [Multi-stage Build]
- **Build Stage**: Contains all dependencies needed for compilation/building
- **Runtime Stage**: Minimal image with only runtime dependencies
- **Artifacts Transfer**: Secure transfer of build artifacts between stages
- **Validation Rules**:
  - Must not include build tools in final image
  - Must optimize layer caching
  - Must minimize final image size

### [Docker AI Agent (Gordon)]
- **Input**: Project structure and dependencies
- **Output**: Optimized Dockerfile
- **Constraints**: Available only in Docker Desktop with AI features enabled
- **Validation Rules**:
  - Generated Dockerfile must meet all requirements
  - Must be reviewed before use in production
  - Must follow security best practices