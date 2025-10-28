#!/bin/bash
echo "Installing CUDA-compatible PyTorch..."
pip install torch==2.0.1+cu117 torchaudio==2.0.2+cu117 --index-url https://download.pytorch.org/whl/cu117 --force-reinstall

echo "Restarting Python services..."
pkill -f gradio_tts_app.py
pkill -f gradio_vc_app.py  
pkill -f script_reader_app.py

# Wait a moment for processes to die
sleep 2

# Restart the main service launcher which will restart all services
python /app/start_both_services.py &

echo "Services restarted with CUDA-compatible PyTorch!"