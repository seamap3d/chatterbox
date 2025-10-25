# Use PyTorch base image that we know works with GPU access
FROM pytorch/pytorch:2.1.0-cuda11.8-cudnn8-devel

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

# Install chatterbox-tts from PyPI - this handles all dependencies automatically
# Install numpy first to help with pkuseg build issues
RUN pip install numpy
# Try installing all dependencies except pkuseg first
RUN pip install librosa==0.11.0 s3tokenizer torch==2.6.0 torchaudio==2.6.0 transformers==4.46.3 diffusers==0.29.0 resemble-perth==1.0.1 conformer==0.3.2 safetensors==0.5.3 gradio
# Then try to install chatterbox-tts without dependencies
RUN pip install chatterbox-tts --no-deps

# Copy only the demo scripts we need
COPY gradio_tts_app.py gradio_vc_app.py example_tts.py ./

# Create directory for generated audio files
RUN mkdir -p /app/outputs

# Expose port for Gradio interface
EXPOSE 7860

# Set default command to run the Gradio TTS app
CMD ["python", "gradio_tts_app.py"]