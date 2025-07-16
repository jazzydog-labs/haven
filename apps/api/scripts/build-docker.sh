#!/bin/bash
# Docker build script for Haven

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
IMAGE_NAME="${IMAGE_NAME:-haven}"
IMAGE_TAG="${IMAGE_TAG:-latest}"
REGISTRY="${REGISTRY:-}"
BUILD_ARGS="${BUILD_ARGS:-}"
PLATFORMS="${PLATFORMS:-linux/amd64}"

# Functions
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
    exit 1
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --push)
            PUSH=true
            shift
            ;;
        --multi-arch)
            PLATFORMS="linux/amd64,linux/arm64"
            shift
            ;;
        --tag)
            IMAGE_TAG="$2"
            shift 2
            ;;
        --registry)
            REGISTRY="$2"
            shift 2
            ;;
        *)
            error "Unknown option: $1"
            ;;
    esac
done

# Main build process
main() {
    log "Starting Docker build for Haven"
    
    # Check Docker is available
    if ! command -v docker &> /dev/null; then
        error "Docker is not installed or not in PATH"
    fi
    
    # Build full image name
    if [[ -n "$REGISTRY" ]]; then
        FULL_IMAGE_NAME="${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}"
    else
        FULL_IMAGE_NAME="${IMAGE_NAME}:${IMAGE_TAG}"
    fi
    
    log "Building image: ${FULL_IMAGE_NAME}"
    log "Platforms: ${PLATFORMS}"
    
    # Check for multi-arch build
    if [[ "$PLATFORMS" == *","* ]]; then
        log "Setting up Docker buildx for multi-architecture build"
        
        # Ensure buildx is available
        docker buildx create --use --name haven-builder 2>/dev/null || true
        docker buildx inspect haven-builder --bootstrap
        
        BUILD_CMD="docker buildx build --platform=${PLATFORMS}"
        
        if [[ "${PUSH:-false}" == "true" ]]; then
            BUILD_CMD="${BUILD_CMD} --push"
        else
            BUILD_CMD="${BUILD_CMD} --load"
            warning "Multi-arch build without push only loads the current platform"
        fi
    else
        BUILD_CMD="docker build"
    fi
    
    # Add build arguments
    if [[ -n "$BUILD_ARGS" ]]; then
        BUILD_CMD="${BUILD_CMD} ${BUILD_ARGS}"
    fi
    
    # Add labels
    BUILD_CMD="${BUILD_CMD} \
        --label org.opencontainers.image.created=$(date -u +'%Y-%m-%dT%H:%M:%SZ') \
        --label org.opencontainers.image.revision=$(git rev-parse HEAD) \
        --label org.opencontainers.image.version=${IMAGE_TAG}"
    
    # Build the image
    log "Executing build command..."
    ${BUILD_CMD} -t "${FULL_IMAGE_NAME}" -f Dockerfile .
    
    if [[ $? -eq 0 ]]; then
        log "Build completed successfully!"
        
        # Show image info if single platform build
        if [[ "$PLATFORMS" != *","* ]]; then
            log "Image details:"
            docker images "${FULL_IMAGE_NAME}"
            
            # Show image size
            SIZE=$(docker image inspect "${FULL_IMAGE_NAME}" --format='{{.Size}}' | numfmt --to=si)
            log "Image size: ${SIZE}B"
        fi
        
        # Push if requested
        if [[ "${PUSH:-false}" == "true" ]] && [[ "$PLATFORMS" != *","* ]]; then
            log "Pushing image to registry..."
            docker push "${FULL_IMAGE_NAME}"
        fi
    else
        error "Build failed!"
    fi
}

# Show usage
usage() {
    cat << EOF
Usage: $0 [OPTIONS]

Options:
    --push          Push image to registry after build
    --multi-arch    Build for multiple architectures (amd64 and arm64)
    --tag TAG       Image tag (default: latest)
    --registry REG  Registry URL (e.g., ghcr.io/username)

Examples:
    # Build local image
    $0

    # Build and push to registry
    $0 --push --registry ghcr.io/jazzydog-labs

    # Build multi-arch image
    $0 --multi-arch --push --registry ghcr.io/jazzydog-labs

    # Build with specific tag
    $0 --tag v1.0.0
EOF
}

# Show usage if --help
if [[ "${1:-}" == "--help" ]] || [[ "${1:-}" == "-h" ]]; then
    usage
    exit 0
fi

# Run main function
main