# CPU Version 0.1 Release Notes

**Release Date**: October 28, 2025  
**Git Tag**: `cpu-v0.1`

## Overview

This is the first stable release of Chatterbox services running in CPU-only mode. All three services (TTS, Voice Conversion, and Script Reader) are fully operational and have been validated with a comprehensive test suite.

## Status

✅ **All Services Operational**
- 🎤 TTS Service: `https://kaizen:7860`
- 🔄 Voice Conversion: `https://kaizen:7861`
- 🎬 Script Reader: `https://kaizen:7862`

✅ **Test Suite**: 27/27 tests passing

## Features

### Services
- **Text-to-Speech (TTS)**: Convert text to natural-sounding speech
- **Voice Conversion (VC)**: Transform voice characteristics between speakers
- **Script Reader**: Convert PDF film scripts to speech with character voice differentiation

### Infrastructure
- Docker containerized deployment
- HTTPS/SSL secured endpoints
- Multi-service orchestration via `start_both_services.py`
- Self-signed certificates for development

### Testing
- Comprehensive test suite (27 tests across 7 categories)
- Automated testing via `./tests/run_tests.sh`
- GitHub Actions CI/CD pipeline
- Service availability monitoring
- Dependency verification
- PyTorch/CUDA compatibility checks

## Performance Characteristics

**Current Setup**: CPU-only processing
- GPU: 2x Quadro RTX 5000 (available but not utilized)
- NVIDIA Driver: 470.256.02 (CUDA 11.4)
- PyTorch: 2.6.0+cu124 (incompatible with current driver)

**Performance**: Functional but slower than potential GPU-accelerated processing (~10x slower)

**Reason**: PyTorch CUDA 11.8 requirement exceeds driver CUDA 11.4 capability, forcing CPU fallback

## Known Limitations

1. **CPU-Only Processing**: Services work correctly but are slower than they could be with GPU acceleration
2. **Driver Compatibility**: System NVIDIA driver (470.256.02, CUDA 11.4) incompatible with PyTorch 2.6.0 (requires CUDA 11.8)
3. **Self-Signed Certificates**: HTTPS uses self-signed certificates (appropriate for development, not production)

## Upgrade Path

For GPU acceleration (future enhancement):

### Option 1: Driver Update (Recommended)
- Update NVIDIA driver to version 510+ (CUDA 11.8 support)
- Rebuild container (current Dockerfile will work)
- Expected improvement: ~10x faster processing

### Option 2: PyTorch Downgrade
- Modify Dockerfile to use PyTorch 2.0.1+cu117
- Compatible with current driver
- Requires careful dependency management

## Testing

Run the test suite to verify functionality:

```bash
./tests/run_tests.sh
```

Expected result: All 27 tests pass in ~73 seconds

## Technical Details

### System Configuration
- **OS**: Linux
- **GPU**: 2x Quadro RTX 5000 (16GB each)
- **Driver**: NVIDIA 470.256.02
- **CUDA**: 11.4
- **Docker**: Running with nvidia-runtime

### Software Stack
- **Base Image**: `pytorch/pytorch:2.1.0-cuda11.8-cudnn8-devel`
- **PyTorch**: 2.6.0+cu124
- **Python**: 3.10
- **Gradio**: 5.49.1
- **Key Dependencies**: transformers, diffusers, librosa, soundfile

### Docker Configuration
```yaml
version: '3.8'
services:
  chatterbox:
    runtime: nvidia
    ports:
      - "7860:7860"  # TTS
      - "7861:7861"  # VC
      - "7862:7862"  # Script Reader
```

## Files Included

### Core Application
- `gradio_tts_app.py` - TTS web interface
- `gradio_vc_app.py` - Voice conversion interface
- `script_reader_app.py` - Script reader interface
- `start_both_services.py` - Service orchestration
- `script_parser.py` - PDF parsing utilities

### Configuration
- `Dockerfile` - Container definition
- `docker-compose.yml` - Service composition
- `cert.pem`, `key.pem` - SSL certificates

### Testing
- `tests/test_services.py` - Comprehensive test suite (27 tests)
- `tests/run_tests.sh` - Test runner
- `tests/README.md` - Test documentation
- `.github/workflows/test.yml` - CI/CD pipeline

### Documentation
- `README.md` - Main documentation
- `TESTING.md` - Testing quick reference
- `SCRIPT_READER_README.md` - Script reader documentation
- `HTTPS_README.md` - HTTPS setup guide
- `DOCKER_README.md` - Docker usage guide

## Usage

### Start Services
```bash
docker-compose up -d
```

### Access Services
- TTS: `https://kaizen:7860`
- VC: `https://kaizen:7861`
- Script Reader: `https://kaizen:7862`

### Stop Services
```bash
docker-compose down
```

### Run Tests
```bash
./tests/run_tests.sh
```

## Future Enhancements

Planned for future releases:
- [ ] GPU acceleration (pending driver update)
- [ ] End-to-end functional tests
- [ ] Performance benchmarks
- [ ] Production-ready SSL certificates
- [ ] Voice quality validation tests
- [ ] Automated performance monitoring

## Support

For issues or questions:
1. Check test results: `./tests/run_tests.sh`
2. Review logs: `docker logs chatterbox-tts`
3. Verify services: `curl -k https://localhost:7860`

## Changelog

### New in CPU v0.1
- ✅ Stable CPU-only operation
- ✅ Comprehensive test suite (27 tests)
- ✅ CI/CD pipeline via GitHub Actions
- ✅ All three services operational
- ✅ HTTPS/SSL configuration
- ✅ Docker containerization
- ✅ Multi-service orchestration
- ✅ Complete documentation

---

**Git Tag**: `cpu-v0.1`  
**Commit**: `7f813313290f9e10d3945e9e3a84c84c981bb67b`  
**Branch**: `master`  
**Repository**: `seamap3d/chatterbox`
