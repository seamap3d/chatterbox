# Use PyTorch base image that we know works with GPU access
FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-devel

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    wget \
    curl \
    build-essential \
    libsndfile1 \
    libsndfile1-dev \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Set working directory
WORKDIR /app

# Copy local files and install dependencies manually to avoid pkuseg issues
COPY . .

# Install core dependencies first
RUN pip install numpy torch torchaudio transformers diffusers safetensors gradio librosa

# Install the local package without dependencies to avoid pkuseg
RUN pip install -e . --no-deps

# Create directory for generated audio files
RUN mkdir -p /app/outputs

# Expose port for Gradio interface
EXPOSE 7860

# Set default command to run the Gradio TTS app
CMD ["python", "gradio_tts_app.py"]