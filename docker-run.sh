#!/bin/bash
# Helper script to run yt2mp3 in Docker

# Create output directory if it doesn't exist
mkdir -p output

# Run yt2mp3 in Docker
docker run --rm \
  -v "$(pwd)/output:/output" \
  -v "$(pwd)/examples:/config:ro" \
  yt2mp3:latest "$@"

echo ""
echo "✅ Output files are in: $(pwd)/output/"

