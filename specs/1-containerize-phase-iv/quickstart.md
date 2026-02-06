# Quickstart Guide: Containerization for Phase IV Local Kubernetes Deployment

## Prerequisites

- Docker Desktop installed with Docker AI Agent (Gordon) enabled (recommended)
- Access to Phase III codebase (frontend and backend applications)
- Ensure sufficient disk space and memory for multi-stage builds
- Minikube and Helm installed for later deployment

## Setup Environment

1. Clone or access the Phase III codebase
2. Navigate to the project directory
3. Ensure Docker daemon is running

## Step 1: Verify Docker AI Agent (Gordon) Availability

```bash
# Check if Gordon is available (this command may vary depending on Docker version)
docker help | grep ai
# or
docker ai --help
```

If Gordon is available, you can use it to generate Dockerfiles. Otherwise, proceed with manual Dockerfile creation.

## Step 2: Containerize Frontend Application

### Option A: Using Docker AI Agent (Gordon)
```bash
cd frontend
# If Gordon is available, use it to generate Dockerfile
# docker ai generate Dockerfile --context .
```

### Option B: Manual Dockerfile Creation
Create `frontend/Dockerfile` with multi-stage build:

```dockerfile
# Build stage
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Runtime stage
FROM node:18-alpine AS runtime
WORKDIR /app
RUN npm install -g serve
COPY --from=builder /app/package*.json ./
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public

EXPOSE 3000
ENV NODE_ENV=production
CMD ["npm", "run", "dev"]
```

### Build Frontend Image
```bash
cd frontend
docker build -t todo-frontend:latest .
```

## Step 3: Containerize Backend Application

### Option A: Using Docker AI Agent (Gordon)
```bash
cd backend
# If Gordon is available, use it to generate Dockerfile
# docker ai generate Dockerfile --context .
```

### Option B: Manual Dockerfile Creation
Create `backend/Dockerfile` with multi-stage build:

```dockerfile
# Build stage
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Runtime stage
FROM python:3.11-slim AS runtime
WORKDIR /app
COPY --from=builder /root/.local ./root/.local
COPY . .

# Make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Build Backend Image
```bash
cd backend
docker build -t todo-backend:latest .
```

## Step 4: Test Container Images

### Run Frontend Container
```bash
docker run -p 3000:3000 \
  -e GEMINI_API_KEY=your_gemini_key \
  -e DATABASE_URL=your_database_url \
  -e BETTER_AUTH_SECRET=your_auth_secret \
  todo-frontend:latest
```

### Run Backend Container
```bash
docker run -p 8000:8000 \
  -e GEMINI_API_KEY=your_gemini_key \
  -e DATABASE_URL=your_database_url \
  -e BETTER_AUTH_SECRET=your_auth_secret \
  todo-backend:latest
```

## Step 5: Verify Container Functionality

1. Visit `http://localhost:3000` to check frontend
2. Visit `http://localhost:8000/health` to check backend
3. Verify that environment variables are properly handled
4. Confirm that applications maintain functionality from Phase III

## Step 6: Prepare for Minikube Deployment

1. Tag images for local registry:
```bash
docker tag todo-frontend:latest todo-frontend:latest
docker tag todo-backend:latest todo-backend:latest
```

2. Start Minikube:
```bash
minikube start --driver=docker
```

3. Enable ingress addon:
```bash
minikube addons enable ingress
```

## Troubleshooting

- If Docker build fails, check that all dependencies are properly copied
- If containers don't start, verify environment variables are set correctly
- If Gordon is not available, manually create Dockerfiles following best practices
- If images are too large, verify multi-stage build is properly implemented

## Next Steps

After successful containerization:
1. Create Helm charts for deployment
2. Deploy to Minikube
3. Test full application functionality
4. Optimize images further if needed