#!/bin/bash
# Docusaurus Build and Push Script

if [ $# -eq 0 ]; then
    echo "Usage: $0 <site-name> [namespace]"
    exit 1
fi

SITE_NAME=$1
NAMESPACE=${2:-default}

echo "Building and pushing Docusaurus site: $SITE_NAME"

# Build the Docker image
echo "Building Docker image for $SITE_NAME..."
docker build -t $SITE_NAME:latest deployments/$SITE_NAME/

if [ $? -ne 0 ]; then
    echo "✗ Failed to build Docker image"
    exit 1
fi

echo "✓ Docker image built successfully"

# For local Kubernetes (Minikube), we need to load the image
if command -v minikube &> /dev/null; then
    echo "Loading image into Minikube..."
    minikube image load $SITE_NAME:latest
    if [ $? -ne 0 ]; then
        echo "✗ Failed to load image into Minikube"
        exit 1
    fi
    echo "✓ Image loaded into Minikube"
else
    echo "Note: Skipping image load - not running in Minikube environment"
fi

echo "✓ Docusaurus site $SITE_NAME built and prepared for deployment"