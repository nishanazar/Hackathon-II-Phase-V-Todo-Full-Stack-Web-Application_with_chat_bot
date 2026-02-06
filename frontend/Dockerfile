# Build stage
FROM node:18-bullseye AS builder
WORKDIR /app
# Copy package files first to leverage Docker layer caching
COPY package*.json ./
RUN npm ci
# Copy source code and build
COPY . .
# Copy environment variables for build time
COPY .env* ./
RUN npm run build

# Runtime stage
FROM node:18-bullseye AS runtime
WORKDIR /app
# Copy only necessary files from builder stage
COPY --from=builder /app/package*.json ./
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/next.config.js ./next.config.js
# Copy environment variables for runtime
COPY --from=builder /app/.env* ./

EXPOSE 3000
ENV NODE_ENV=production
CMD ["npm", "start"]