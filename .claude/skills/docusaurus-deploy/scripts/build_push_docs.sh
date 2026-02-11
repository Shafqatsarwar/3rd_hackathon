#!/bin/bash
# Docusaurus Build and Push Script

if [ $# -eq 0 ]; then
    echo "Usage: $0 <site-name> [namespace]"
    exit 1
fi

SITE_NAME=$1
NAMESPACE=${2:-default}
SOURCE_DIR=${3:-"src/docs"}

if [ ! -d "$SOURCE_DIR" ]; then
    if [ -d "website" ]; then
        SOURCE_DIR="website"
    elif [ -d "docs" ]; then
        SOURCE_DIR="docs"
    else
        echo "✗ Source directory not found: $SOURCE_DIR"
        exit 1
    fi
fi

echo "Building and pushing Docusaurus site: $SITE_NAME from $SOURCE_DIR"

# Build the Docker image
echo "Building Docker image for $SITE_NAME..."
docker build -t $SITE_NAME:latest "$SOURCE_DIR"

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