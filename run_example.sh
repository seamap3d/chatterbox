#!/bin/bash

# Run example scripts with GPU support
# This script builds the Docker image and runs the example TTS script

echo "Building Chatterbox TTS Docker image..."
docker-compose build

echo "Running TTS example with GPU support..."
docker-compose --profile example up chatterbox-example