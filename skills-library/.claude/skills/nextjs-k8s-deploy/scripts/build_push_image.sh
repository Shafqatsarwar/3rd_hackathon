#!/bin/bash
# Build and Push Next.js Docker Image
# Builds a production-ready Next.js image and pushes to registry

set -e

APP_NAME=${1:-"learnflow-frontend"}
REGISTRY=${2:-"localhost:5000"}
TAG=${3:-"latest"}

echo "Building Next.js Docker image: $APP_NAME"

# Navigate to app directory
APP_DIR="src/frontend"
if [ ! -d "$APP_DIR" ]; then
    echo "✗ App directory not found: $APP_DIR"
    exit 1
fi

cd "$APP_DIR"

# Check for Dockerfile
if [ ! -f "Dockerfile" ]; then
    echo "Creating Dockerfile for Next.js..."
    cat > Dockerfile << 'EOF'
# Multi-stage build for Next.js
FROM node:20-alpine AS deps
RUN apk add --no-cache libc6-compat
WORKDIR /app
COPY package*.json ./
RUN npm ci --legacy-peer-deps

FROM node:20-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
ENV NEXT_TELEMETRY_DISABLED 1
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV production
ENV NEXT_TELEMETRY_DISABLED 1

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

USER nextjs
EXPOSE 3000
ENV PORT 3000
CMD ["node", "server.js"]
EOF
    echo "✓ Dockerfile created"
fi

# Build the Docker image
IMAGE_NAME="$REGISTRY/$APP_NAME:$TAG"
echo "Building image: $IMAGE_NAME"

docker build -t "$IMAGE_NAME" .

if [ $? -eq 0 ]; then
    echo "✓ Image built: $IMAGE_NAME"
else
    echo "✗ Build failed"
    exit 1
fi

# Push to registry (if not localhost without registry)
if [[ "$REGISTRY" != "localhost" && "$REGISTRY" != "localhost:5000" ]]; then
    echo "Pushing image to registry..."
    docker push "$IMAGE_NAME"
    if [ $? -eq 0 ]; then
        echo "✓ Image pushed: $IMAGE_NAME"
    else
        echo "✗ Push failed"
        exit 1
    fi
else
    # For local Minikube, load into Minikube's Docker daemon
    echo "Loading image into Minikube..."
    minikube image load "$IMAGE_NAME" 2>/dev/null || true
    echo "✓ Image available in Minikube"
fi

echo "✓ Next.js image ready: $IMAGE_NAME"
