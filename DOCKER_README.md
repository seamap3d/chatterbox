# Chatterbox TTS Docker Setup

This Docker setup allows you to run Chatterbox TTS with GPU acceleration in a containerized environment.

## Prerequisites

- Docker Engine 20.10 or higher
- Docker Compose v2
- NVIDIA Container Toolkit (nvidia-docker2)
- NVIDIA GPU with CUDA support

## Host System Information

This setup is configured for:
- CUDA Version: 11.4
- NVIDIA Driver: 470.256.02  
- GPUs: 2x Quadro RTX 5000

## Quick Start

### 1. Run Gradio Web Interface

```bash
./run_gradio.sh
```

This will:
- Build the Docker image with GPU support
- Start the Gradio web interface on http://localhost:7860
- Make both GPUs available to the container

### 2. Run Example Script

```bash
./run_example.sh
```

This will:
- Build the Docker image
- Run the example TTS script (example_tts.py)
- Generate test audio files in the outputs directory

### 3. Manual Docker Commands

#### Build the image:
```bash
docker-compose build
```

#### Run Gradio interface:
```bash
docker-compose up chatterbox
```

#### Run example script:
```bash
docker-compose --profile example up chatterbox-example
```

#### Run interactive container:
```bash
docker-compose run --rm chatterbox bash
```

## Configuration

### GPU Configuration

The setup uses all available GPUs by default. To use specific GPUs, modify the `CUDA_VISIBLE_DEVICES` environment variable in `docker-compose.yml`:

```yaml
environment:
  - CUDA_VISIBLE_DEVICES=0  # Use only GPU 0
  # or
  - CUDA_VISIBLE_DEVICES=0,1  # Use both GPUs
```

### Port Configuration

The Gradio interface runs on port 7860 by default. To change this, modify the port mapping in `docker-compose.yml`:

```yaml
ports:
  - "8080:7860"  # Access via http://localhost:8080
```

## Volumes

- `./outputs:/app/outputs` - Generated audio files
- `./examples:/app/examples` - Example audio files for voice cloning

## Troubleshooting

### GPU not detected

1. Verify NVIDIA Container Toolkit is installed:
```bash
docker run --rm --gpus all nvidia/cuda:11.8-base-ubuntu22.04 nvidia-smi
```

2. Check if Docker can access GPUs:
```bash
docker run --rm --gpus all chatterbox-tts nvidia-smi
```

### Memory issues

If you encounter CUDA out of memory errors:
1. Reduce batch size in the application
2. Use fewer GPUs by modifying `CUDA_VISIBLE_DEVICES`
3. Close other GPU-intensive applications

### Build issues

If the build fails:
1. Ensure you have sufficient disk space
2. Check internet connection for downloading dependencies
3. Try building with `--no-cache` flag:
```bash
docker-compose build --no-cache
```

## File Structure

```
chatterbox/
├── Dockerfile              # Main Docker image definition
├── docker-compose.yml      # Container orchestration
├── .dockerignore           # Files to exclude from build
├── run_gradio.sh          # Quick start script for Gradio
├── run_example.sh         # Quick start script for examples
├── DOCKER_README.md       # This file
└── outputs/               # Generated audio files (created automatically)
```