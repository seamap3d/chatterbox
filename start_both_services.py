#!/usr/bin/env python3
"""
Startup script to run both TTS and Voice Conversion services on different ports
"""
import subprocess
import time
import sys
import signal
import os

def signal_handler(sig, frame):
    print('\nShutting down services...')
    sys.exit(0)

def start_service(script_name, port, service_name):
    """Start a service and return the process"""
    print(f"Starting {service_name} on port {port}...")
    process = subprocess.Popen([
        sys.executable, script_name
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return process

def main():
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    print("🚀 Starting Chatterbox Services...")
    print("=" * 50)
    
    # Start TTS service on port 7860
    tts_process = start_service("gradio_tts_app.py", 7860, "TTS Service")
    
    # Wait a moment before starting the second service
    time.sleep(3)
    
    # Start Voice Conversion service on port 7861
    vc_process = start_service("gradio_vc_app.py", 7861, "Voice Conversion Service")
    
    # Wait a moment before starting the third service
    time.sleep(3)
    
    # Start Script Reader service on port 7862
    script_process = start_service("script_reader_app.py", 7862, "Script Reader Service")
    
    print("✅ All services started!")
    print("=" * 50)
    print("🎤 TTS Service (Text-to-Speech):     https://kaizen:7860")
    print("🔄 VC Service (Voice Conversion):    https://kaizen:7861")
    print("🎬 Script Reader (PDF to Speech):    https://kaizen:7862")
    print("=" * 50)
    print("Press Ctrl+C to stop all services")
    
    try:
        # Keep the script running and monitor processes
        while True:
            # Check if processes are still running
            tts_poll = tts_process.poll()
            vc_poll = vc_process.poll()
            script_poll = script_process.poll()
            
            if tts_poll is not None:
                print(f"⚠️  TTS service exited with code {tts_poll}")
                break
            if vc_poll is not None:
                print(f"⚠️  VC service exited with code {vc_poll}")
                break
            if script_poll is not None:
                print(f"⚠️  Script Reader service exited with code {script_poll}")
                break
                
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Stopping services...")
        
    finally:
        # Clean up processes
        for process, name in [(tts_process, "TTS"), (vc_process, "VC"), (script_process, "Script Reader")]:
            if process.poll() is None:
                print(f"Terminating {name} service...")
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    print(f"Force killing {name} service...")
                    process.kill()

if __name__ == "__main__":
    main()