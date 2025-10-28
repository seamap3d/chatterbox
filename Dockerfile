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
# Install dependencies (excluding torch/torchaudio since they come with base image)
RUN pip install librosa==0.11.0 s3tokenizer transformers==4.46.3 diffusers==0.29.0 resemble-perth==1.0.1 conformer==0.3.2 safetensors==0.5.3 gradio PyPDF2 soundfile
# Then try to install chatterbox-tts without dependencies
RUN pip install chatterbox-tts --no-deps

# Copy only the demo scripts we need
COPY gradio_tts_app.py gradio_vc_app.py example_tts.py start_both_services.py script_parser.py script_reader_app.py ./

# Copy SSL certificates for HTTPS support
COPY cert.pem key.pem ./

# Create directory for generated audio files
RUN mkdir -p /app/outputs

# Expose ports for all Gradio interfaces
EXPOSE 7860 7861 7862

# Set default command to run both services
CMD ["python", "start_both_services.py"]