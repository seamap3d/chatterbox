"""
Test script to verify all Chatterbox services are working
"""
import requests
import time

def test_service(port, name):
    """Test if a service is responding"""
    try:
        response = requests.get(f"http://localhost:{port}", timeout=5)
        if response.status_code == 200:
            print(f"✅ {name} (port {port}): Working")
            return True
        else:
            print(f"❌ {name} (port {port}): HTTP {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ {name} (port {port}): Connection error - {e}")
        return False

def main():
    print("🧪 Testing Chatterbox Services...")
    print("=" * 50)
    
    services = [
        (7860, "TTS Service"),
        (7861, "Voice Conversion Service"), 
        (7862, "Script Reader Service")
    ]
    
    all_working = True
    for port, name in services:
        working = test_service(port, name)
        all_working = all_working and working
        time.sleep(1)
    
    print("=" * 50)
    if all_working:
        print("🎉 All services are working!")
        print("\n📋 Access URLs:")
        print("🎤 TTS Service:          http://kaizen:7860")
        print("🔄 Voice Conversion:     http://kaizen:7861")
        print("🎬 Script Reader:        http://kaizen:7862")
    else:
        print("⚠️  Some services are not responding")

if __name__ == "__main__":
    main()