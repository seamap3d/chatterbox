# 🎬 Chatterbox TTS & Script Reader - Extended Version

This is an extended version of [Resemble AI's Chatterbox TTS](https://github.com/resemble-ai/chatterbox) with additional **PDF Script Reader** functionality for film and media production.

## 🆕 What's New - Script Reader Service

In addition to the original TTS and Voice Conversion capabilities, this version adds:

### 🎭 PDF Film Script Processing
- **Automatic Character Extraction**: Upload PDF scripts and automatically identify characters
- **Dialogue Parsing**: Extract and organize dialogue by character
- **Batch TTS Conversion**: Convert entire scripts to speech with character-specific voices
- **Voice Assignment**: Upload reference audio for each character
- **Downloadable Audio**: Get organized audio files for each character's lines

## 🚀 Three Services Available

### 1. 🎤 Text-to-Speech (TTS) Service
- Convert any text to natural-sounding speech
- Upload reference audio for voice cloning
- Adjustable parameters (temperature, exaggeration, etc.)
- **Access:** http://kaizen:7860

### 2. 🔄 Voice Conversion Service  
- Convert existing audio to different voices
- Upload source audio and target voice reference
- Transform voice characteristics while preserving content
- **Access:** http://kaizen:7861

### 3. 🎬 Script Reader Service (NEW!)
- Upload PDF film scripts
- Automatically extract characters and their dialogue
- Assign reference voices to each character
- Convert entire scripts to speech with character-specific voices
- Download audio files for each character
- **Access:** http://kaizen:7862

### 4. 🎬 Script Reader (Tortoise TTS)
- Same script analysis and character assignment flow
- Tortoise TTS backend (quality-focused preset by default)
- Assign characters to voice samples via dropdown
- **Access:** http://kaizen:7863

## 📋 Quick Start

### Prerequisites
- Docker & Docker Compose
- NVIDIA GPU with CUDA support
- nvidia-docker runtime

### 🏃‍♂️ Running All Services

1. **Clone this extended version:**
   ```bash
   git clone https://github.com/seamap3d/chatterbox.git
   cd chatterbox
   ```

2. **Build and start all services:**
   ```bash
   docker-compose build
   docker-compose up -d
   ```

3. **Verify all services are running:**
   ```bash
   python3 test_services.py
   ```

### 🧪 Tortoise Script Reader (optional)
This app is a parallel version that uses Tortoise TTS. Install its deps in the same environment, then run:

```bash
python3 script_reader_tortoise_app.py
```

It listens on port 7863 and requires the `tortoise-tts-fast` package (plus its dependencies).

### 🌐 Access URLs
- **TTS Service:** http://kaizen:7860
- **Voice Conversion:** http://kaizen:7861  
- **Script Reader:** http://kaizen:7862
- **Script Reader (Tortoise):** http://kaizen:7863

## 🎭 Script Reader Detailed Usage

### Step 1: Prepare Your Script
The script reader works best with properly formatted film scripts:

**Good Format:**
```
JOHN
Hello, how are you today?

SARAH  
I'm doing great, thanks for asking!

NARRATOR
The two characters continued their conversation.
```

**Supported Script Elements:**
- Character names in ALL CAPS
- Dialogue following character names
- Stage directions (automatically filtered)
- Scene headers (automatically ignored)

### Step 2: Upload & Process
1. Navigate to http://kaizen:7862
2. Upload your PDF script using the file uploader
3. Click "📖 Process Script" 
4. Review the extracted characters and their dialogue counts

### Step 3: Voice Assignment
For each detected character:
1. Upload a reference audio file (WAV, MP3, etc.)
2. This will be the "voice" for that character
3. The system will clone this voice for all character dialogue

### Step 4: Generate Speech
1. Click "🎤 Convert to Speech" for each character
2. Preview the first line of generated speech
3. Download ZIP file containing all audio files for that character
4. Audio files are named sequentially (e.g., `JOHN_line_001.wav`)

### Use Cases
- **Film Pre-production**: Generate temp voice tracks from scripts
- **Audiobook Creation**: Multi-character narration
- **Game Development**: Character voice generation
- **Content Creation**: Podcast and video production
- **Accessibility**: Convert scripts to audio format

## 🛠️ Technical Implementation

### New Components Added
- **script_parser.py**: PDF parsing and character extraction
- **script_reader_app.py**: Gradio web interface for script processing
- **Enhanced startup script**: Manages all three services

### Docker Configuration
```yaml
services:
  chatterbox:
    ports:
      - "7860:7860"  # TTS Service
      - "7861:7861"  # Voice Conversion Service  
      - "7862:7862"  # Script Reader Service (NEW)
```

### Dependencies Added
- **PyPDF2**: PDF text extraction
- **soundfile**: Audio file handling
- **zipfile**: Batch audio download

## 📊 Performance & Scaling

### Processing Times
- **Script Analysis**: 5-15 seconds for typical scripts
- **Character Extraction**: Automatic, real-time
- **TTS Generation**: ~2-5 seconds per dialogue line
- **Batch Processing**: Depends on script length and character count

### Resource Requirements
- **GPU Memory**: 6GB+ recommended for optimal performance
- **Storage**: Generated audio files stored in `./outputs/` volume
- **Concurrent Users**: Multiple users can process different scripts simultaneously

## 🔧 Configuration Options

### Script Parser Settings
The parser can be tuned for different script formats by modifying `script_parser.py`:

```python
# Character name patterns (customizable)
self.character_patterns = [
    r'^([A-Z][A-Z\s\.\-\']+)$',     # Standard ALL CAPS
    r'^([A-Z][A-Z\s\.\-\']+):',     # With colon
    r'^\s*([A-Z][A-Z\s\.\-\']+)\s*$' # With whitespace
]
```

### TTS Parameters
Default settings optimized for script reading:
- **Exaggeration**: 0.5 (neutral performance)
- **Temperature**: 0.8 (natural variation)
- **CFG Weight**: 0.5 (balanced guidance)

## 🐛 Troubleshooting

### Script Processing Issues

**"No characters found"**
- Ensure character names are in ALL CAPS
- Check that PDF contains selectable text (not scanned images)
- Verify script follows standard formatting

**"Poor character detection"**
- Some script formats may need manual adjustment
- Check for unusual formatting or fonts
- Consider converting script to standard format

**"Audio generation fails"**
- Ensure reference audio files are clear and good quality
- Check that GPU memory is sufficient
- Monitor container logs for detailed error messages

### Service Access Issues
```bash
# Check if all services are running
docker-compose ps

# View logs for debugging
docker-compose logs chatterbox

# Test individual services
curl http://localhost:7860  # TTS
curl http://localhost:7861  # VC  
curl http://localhost:7862  # Script Reader
```

## 📁 Extended File Structure

```
chatterbox/
├── docker-compose.yml              # Container orchestration
├── Dockerfile                      # Extended container definition
├── gradio_tts_app.py               # Original TTS interface
├── gradio_vc_app.py                # Original VC interface  
├── script_reader_app.py            # NEW: Script reader interface
├── script_parser.py                # NEW: PDF parsing logic
├── start_both_services.py          # Multi-service startup (updated)
├── test_services.py                # Service testing utility
├── create_sample_script.py         # Sample script generator
├── README.md                       # This documentation
└── outputs/                        # Generated audio files
```

## 🔄 Original Chatterbox Features

This extended version maintains full compatibility with the original Chatterbox TTS features:

- ✅ Multilingual TTS (23 languages)
- ✅ Zero-shot voice cloning
- ✅ Emotion exaggeration control
- ✅ Voice conversion capabilities
- ✅ Built-in Perth watermarking
- ✅ MIT License

For original documentation and API usage, see the base repository: https://github.com/resemble-ai/chatterbox

## 🎯 Production Considerations

### Scaling for Production
- Consider using external storage for generated audio files
- Implement user authentication for multi-tenant deployments
- Add rate limiting for API endpoints
- Monitor GPU utilization and implement queueing

### Quality Optimization
- Use high-quality reference audio (22kHz+, mono preferred)
- Ensure clean script formatting for best character detection
- Test with various script types to optimize parser patterns

## 🤝 Contributing

This is an extended version of Resemble AI's Chatterbox. Contributions to the script reader functionality are welcome!

### Areas for Enhancement
- Support for more script formats (Final Draft, WriterDuet, etc.)
- Improved character detection algorithms
- Batch processing optimizations
- Advanced voice assignment features

## 📄 License

- **Original Chatterbox TTS**: MIT License (Resemble AI)
- **Script Reader Extensions**: MIT License
- **Dependencies**: Various licenses (see pyproject.toml)

## 🙏 Acknowledgements

- **Resemble AI** for the excellent Chatterbox TTS foundation
- **Original Chatterbox Contributors** for the core TTS and VC functionality
- **Open Source Community** for supporting tools and libraries

---

**Enhanced with ❤️ for film production and content creation workflows**

For support with the original Chatterbox features, visit the [official Discord](https://discord.gg/rJq9cRJBJ6).  
For script reader specific questions, please open an issue in this repository.
