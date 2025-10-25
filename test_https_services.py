#!/usr/bin/env python3
"""
Test script to verify all Chatterbox HTTPS services are working
"""
import requests
import sys
from urllib3.exceptions import InsecureRequestWarning

# Disable SSL warnings for self-signed certificates
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def test_service(port, name):
    """Test if a service is responding on HTTPS"""
    try:
        url = f"https://localhost:{port}"
        response = requests.get(url, verify=False, timeout=10)
        if response.status_code == 200:
            return True, "Working"
        else:
            return False, f"HTTP {response.status_code}"
    except requests.exceptions.RequestException as e:
        return False, str(e)

def main():
    print("🧪 Testing Chatterbox HTTPS Services...")
    print("=" * 50)
    
    services = [
        (7860, "TTS Service (port 7860)"),
        (7861, "Voice Conversion Service (port 7861)"),
        (7862, "Script Reader Service (port 7862)")
    ]
    
    all_working = True
    
    for port, name in services:
        working, status = test_service(port, name)
        status_emoji = "✅" if working else "❌"
        print(f"{status_emoji} {name}: {status}")
        if not working:
            all_working = False
    
    print("=" * 50)
    
    if all_working:
        print("🎉 All services are working!")
        print("\n📋 HTTPS Access URLs:")
        print("🎤 TTS Service:          https://kaizen:7860")
        print("🔄 Voice Conversion:     https://kaizen:7861")
        print("🎬 Script Reader:        https://kaizen:7862")
        print("\n💡 Note: You may need to accept the self-signed SSL certificate in your browser")
        return 0
    else:
        print("❌ Some services are not working!")
        return 1

if __name__ == "__main__":
    sys.exit(main())