# Implementation Plan: Containerization for Phase IV Local Kubernetes Deployment

**Feature Spec**: [spec.md](../spec.md)
**Created**: 2026-01-23
**Status**: Draft
**Author**: Qwen CLI

## Technical Context

This plan outlines the containerization of the Next.js frontend and FastAPI backend applications using Docker for deployment on Minikube. The implementation will leverage Docker AI Agent (Gordon) if available, use multi-stage builds for optimization, and ensure proper tagging of images.

**Architecture Overview**:
- Frontend: Next.js application containerized with Docker
- Backend: FastAPI application containerized with Docker
- Build process: Multi-stage builds to minimize image sizes
- AI assistance: Docker AI Agent (Gordon) if available
- Deployment target: Minikube for local Kubernetes deployment

**Technology Stack**:
- Docker for containerization
- Next.js 16+ for frontend
- FastAPI for backend
- Multi-stage Docker builds
- Docker AI Agent (Gordon) if available

**Key Unknowns**:
- Whether Docker AI Agent (Gordon) is available and enabled in Docker Desktop
- Specific environment variables required for the applications
- Exact directory structure of frontend and backend code

## Constitution Check

This implementation plan adheres to the Phase II Constitution:

- ✅ **Spec-driven**: Based on the feature spec in `/specs/1-containerize-phase-iv/spec.md`
- ✅ **No manual coding**: Will be implemented using AI agents only
- ✅ **Stateless JWT auth**: Containerization preserves existing auth mechanism
- ✅ **Tech stack compliance**: Uses Docker with existing Next.js/FastAPI stack

## Gates

- ✅ **Feature spec exists**: Located at `/specs/1-containerize-phase-iv/spec.md`
- ✅ **Constitution alignment**: Plan follows all constitutional principles
- ✅ **Technology compliance**: Uses approved tech stack
- ✅ **No manual intervention**: Plan specifies AI agent implementation only

## Phase 0: Outline & Research

### Research Tasks

1. **Check Docker AI Agent (Gordon) Availability**
   - Task: Verify if Docker AI Agent (Gordon) is enabled in Docker Desktop
   - Purpose: Determine if we can leverage AI for Dockerfile generation
   - Method: Check Docker Desktop settings or run Gordon command

2. **Analyze Frontend Code Structure**
   - Task: Examine Next.js frontend application structure
   - Purpose: Understand dependencies and build process for Dockerfile creation
   - Method: Review package.json, dependencies, and build scripts

3. **Analyze Backend Code Structure**
   - Task: Examine FastAPI backend application structure
   - Purpose: Understand dependencies and startup process for Dockerfile creation
   - Method: Review requirements.txt, dependencies, and startup commands

4. **Identify Required Environment Variables**
   - Task: Determine environment variables needed for both applications
   - Purpose: Ensure containers can be configured at runtime
   - Method: Review existing .env files and application configurations

### Research Outcomes

#### Decision: Docker AI Agent (Gordon) Usage
- **Rationale**: Using Gordon demonstrates advanced DevOps practices and can optimize Dockerfile creation
- **Alternative**: Standard Dockerfile creation if Gordon is not available
- **Chosen**: Use Gordon if available, otherwise standard Dockerfile approach

#### Decision: Multi-stage Build Approach
- **Rationale**: Multi-stage builds significantly reduce image sizes and improve security
- **Alternative**: Single-stage builds (larger images, more vulnerabilities)
- **Chosen**: Multi-stage builds for both frontend and backend

#### Decision: Environment Variables Handling
- **Rationale**: Applications need runtime configuration without rebuilding images
- **Alternative**: Hardcoded configurations (not flexible)
- **Chosen**: Pass environment variables at runtime via Docker

## Phase 1: Design & Contracts

### Data Model: Container Configuration

**[Frontend Docker Image]**
- Image name: `todo-frontend:latest`
- Base image: Node.js LTS
- Build stage: Dependencies installation and build
- Runtime stage: Serve built application
- Ports: 3000 (Next.js default)
- Environment variables: GEMINI_API_KEY, DATABASE_URL, BETTER_AUTH_SECRET

**[Backend Docker Image]**
- Image name: `todo-backend:latest`
- Base image: Python 3.11
- Build stage: Dependencies installation
- Runtime stage: Run FastAPI application
- Ports: 8000 (FastAPI default)
- Environment variables: GEMINI_API_KEY, DATABASE_URL, BETTER_AUTH_SECRET

### API Contract: Docker Build Interface

**Frontend Build Contract**
```
Build Args: NODE_ENV=production
Ports: 3000
Health Check: HTTP GET /
Environment Variables: GEMINI_API_KEY, DATABASE_URL, BETTER_AUTH_SECRET
```

**Backend Build Contract**
```
Build Args: PYTHON_ENV=production
Ports: 8000
Health Check: HTTP GET /health
Environment Variables: GEMINI_API_KEY, DATABASE_URL, BETTER_AUTH_SECRET
```

### Quickstart Guide

1. **Prerequisites**
   - Docker Desktop installed with Docker AI Agent (Gordon) enabled (optional)
   - Access to Phase III codebase

2. **Build Frontend Container**
   ```bash
   cd frontend
   docker build -t todo-frontend:latest .
   ```

3. **Build Backend Container**
   ```bash
   cd backend
   docker build -t todo-backend:latest .
   ```

4. **Run Containers**
   ```bash
   docker run -p 3000:3000 -e GEMINI_API_KEY=... -e DATABASE_URL=... -e BETTER_AUTH_SECRET=... todo-frontend:latest
   docker run -p 8000:8000 -e GEMINI_API_KEY=... -e DATABASE_URL=... -e BETTER_AUTH_SECRET=... todo-backend:latest
   ```

## Phase 2: Implementation Approach

### Implementation Steps

1. **Verify Docker Environment**
   - Check Docker installation
   - Verify Docker AI Agent (Gordon) availability
   - Ensure sufficient resources for multi-stage builds

2. **Create Frontend Dockerfile**
   - Use multi-stage build pattern
   - Install dependencies in build stage
   - Copy built assets to runtime stage
   - Set appropriate entrypoint/command

3. **Create Backend Dockerfile**
   - Use multi-stage build pattern
   - Install Python dependencies in build stage
   - Copy application code to runtime stage
   - Set appropriate entrypoint/command (uvicorn main:app)

4. **Test Docker Images**
   - Build frontend image
   - Build backend image
   - Run containers locally to verify functionality
   - Confirm environment variables are properly handled

5. **Optimize Images**
   - Verify multi-stage builds are effective
   - Ensure images are appropriately sized
   - Confirm no unnecessary files are included

## Post-Implementation Verification

- [ ] Frontend Docker image builds successfully
- [ ] Backend Docker image builds successfully
- [ ] Both images run correctly with docker run
- [ ] Multi-stage builds reduce image sizes as expected
- [ ] Environment variables are properly handled
- [ ] Applications maintain functionality from Phase III
- [ ] Dockerfiles follow best practices