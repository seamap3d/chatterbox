#!/bin/bash

# Build and run Chatterbox TTS with GPU support
# This script builds the Docker image and runs the Gradio web interface

echo "Building Chatterbox TTS Docker image..."
docker-compose build

echo "Starting Chatterbox TTS with GPU support..."
echo "The Gradio interface will be available at http://localhost:7860"
echo "Press Ctrl+C to stop the container"

docker-compose up chatterbox