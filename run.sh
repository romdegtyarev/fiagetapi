#!/bin/bash

# === Configuration ===
IMAGE_NAME="racepagebot"
CONTAINER_NAME="racepage-cli"
CONTAINER_WORKDIR="/app"
DATA_DIR="$(pwd)/data"
CACHE_DIR="$(pwd)/fastf1_cache"
DOCKERFILE="Dockerfile"

# === Check if image exists ===
IMAGE_EXISTS=$(docker images -q "$IMAGE_NAME")

if [ -z "$IMAGE_EXISTS" ]; then
  echo "❌ Image '$IMAGE_NAME' not found. Building..."
  if ! docker build -t "$IMAGE_NAME" -f "$DOCKERFILE" . > /dev/null; then
    echo "❌ Build failed!"
    exit 1
  fi
else
  echo "✅ Image '$IMAGE_NAME' exists."
fi

# === Check if image is outdated (based on .py files) ===
NEEDS_REBUILD=$(find . -name "*.py" -newermt "$(docker inspect --format='{{.Created}}' "$IMAGE_NAME" 2>/dev/null)" | wc -l)

if [ "$NEEDS_REBUILD" -gt 0 ]; then
  echo "Detected source changes. Rebuilding image..."
  docker build -t "$IMAGE_NAME" -f "$DOCKERFILE" .
fi

# === Ensure required directories exist ===
[ ! -d "$DATA_DIR" ] && mkdir -p "$DATA_DIR"
[ ! -d "$CACHE_DIR" ] && mkdir -p "$CACHE_DIR"

# === Run container ===
echo "Running CLI container..."
docker run --rm \
  --name "$CONTAINER_NAME" \
  -v "$DATA_DIR":"$CONTAINER_WORKDIR"/data \
  -v "$CACHE_DIR":/root/.cache/fastf1 \
  -w "$CONTAINER_WORKDIR" \
  "$IMAGE_NAME" \
  python bot/cli.py "$@"
