# 🔒 HTTPS Setup for Chatterbox TTS Services

## Overview

All Chatterbox services now run with HTTPS using self-signed SSL certificates. This enables microphone access in modern browsers like Chrome, which require secure contexts for audio input.

## 🚀 Quick Start

1. **Start all services:**
   ```bash
   docker-compose up -d
   ```

2. **Access the HTTPS services:**
   - **🎤 TTS Service**: https://kaizen:7860
   - **🔄 Voice Conversion**: https://kaizen:7861
   - **🎬 Script Reader**: https://kaizen:7862

3. **Accept the SSL certificate** in your browser when prompted

## 🔧 SSL Certificate Details

- **Certificate Type**: Self-signed SSL certificate
- **Validity**: 365 days
- **Files**: `cert.pem` (certificate) and `key.pem` (private key)
- **Subject**: CN=localhost (valid for localhost access)

## 🌐 Browser Setup

### Chrome/Chromium
1. Navigate to any of the HTTPS URLs above
2. Click "Advanced" when you see the security warning
3. Click "Proceed to kaizen (unsafe)"
4. The microphone will now be accessible in Gradio interfaces

### Firefox
1. Navigate to any of the HTTPS URLs above
2. Click "Advanced"
3. Click "Accept the Risk and Continue"
4. Microphone access will be enabled

### Safari
1. Navigate to any of the HTTPS URLs above
2. Click "Show Details"
3. Click "visit this website"
4. Click "Visit Website" to confirm

## 🎙️ Microphone Access

With HTTPS enabled, you can now:
- **Record voice samples** directly in the browser for TTS reference
- **Upload audio via microphone** in Voice Conversion
- **Record character voices** in Script Reader for film production

## 🔍 Testing Services

Run the test script to verify all services:
```bash
python3 test_https_services.py
```

Expected output:
```
🧪 Testing Chatterbox HTTPS Services...
==================================================
✅ TTS Service (port 7860): Working
✅ Voice Conversion Service (port 7861): Working  
✅ Script Reader Service (port 7862): Working
==================================================
🎉 All services are working!
```

## 🛠️ Regenerating Certificates

If you need to regenerate the SSL certificates:

```bash
# Generate new self-signed certificate (valid for 365 days)
openssl req -x509 -newkey rsa:2048 -nodes -keyout key.pem -out cert.pem -days 365 \
  -subj "/C=US/ST=PA/L=Pittsburgh/O=Chatterbox/OU=TTS/CN=localhost"

# Rebuild container with new certificates
docker-compose down
docker-compose build
docker-compose up -d
```

## 🔐 Security Notes

- These are **self-signed certificates** for development use
- Browsers will show security warnings - this is expected
- For production deployment, use certificates from a trusted CA
- The certificates are valid for `localhost` and the hostname `kaizen`

## 📋 Service Features with HTTPS

### TTS Service (Port 7860)
- Text-to-speech conversion with voice cloning
- **Microphone recording** for reference audio
- Real-time audio generation

### Voice Conversion Service (Port 7861)  
- Convert audio to different voices
- **Microphone input** for source audio
- Upload target voice samples

### Script Reader Service (Port 7862)
- PDF film script processing
- Character dialogue extraction
- **Microphone recording** for character voices
- Batch audio generation for entire scripts

## 🐛 Troubleshooting

### "ERR_CERT_AUTHORITY_INVALID" Error
- This is expected with self-signed certificates
- Click "Advanced" → "Proceed to site" to continue

### Microphone Still Not Working
1. Ensure you're using HTTPS URLs (not HTTP)
2. Check browser permissions for microphone access
3. Verify the certificate was accepted in browser
4. Try refreshing the page after accepting certificate

### Services Not Starting
```bash
# Check container logs
docker-compose logs

# Rebuild if needed
docker-compose down
docker-compose build
docker-compose up -d
```

## 🎬 Complete Film Production Workflow

With HTTPS enabled, you can now use the complete workflow:

1. **Upload PDF script** to Script Reader service
2. **Record character voices** using microphone for each character
3. **Generate all dialogue** automatically with AI voice synthesis
4. **Download audio files** for use in film production

The SSL setup ensures all browser-based audio features work seamlessly!