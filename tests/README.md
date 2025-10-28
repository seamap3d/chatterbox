# Chatterbox Test Suite

Comprehensive test suite to ensure core functionality remains intact during development.

## Overview

This test suite verifies:
- ✅ **Service Availability**: All three services (TTS, VC, Script Reader) are accessible
- ✅ **Docker Health**: Container and processes are running correctly
- ✅ **PyTorch Setup**: PyTorch is installed and working (with or without CUDA)
- ✅ **Dependencies**: All required packages are installed
- ✅ **SSL Configuration**: HTTPS endpoints are properly configured
- ✅ **Basic Functionality**: Gradio interfaces are responding
- ✅ **File System**: Required files and directories exist

## Quick Start

### Run All Tests

```bash
# From the project root directory
./tests/run_tests.sh
```

### Run Specific Test Categories

```bash
# Test only service availability
pytest tests/test_services.py::TestServiceAvailability -v

# Test only Docker container health
pytest tests/test_services.py::TestDockerContainer -v

# Test only PyTorch setup
pytest tests/test_services.py::TestPyTorchSetup -v

# Test only dependencies
pytest tests/test_services.py::TestDependencies -v
```

### Run a Single Test

```bash
# Test if TTS service responds
pytest tests/test_services.py::TestServiceAvailability::test_service_responds[TTS-https://localhost:7860] -v

# Test CUDA detection
pytest tests/test_services.py::TestPyTorchSetup::test_cuda_detection -v
```

## Prerequisites

1. **Docker** must be installed and running
2. **Python 3.8+** with pip
3. **Chatterbox services** must be running (`docker-compose up -d`)

### Install Test Dependencies

```bash
pip install -r tests/requirements.txt
```

## Test Categories

### 1. Service Availability Tests (`TestServiceAvailability`)

Tests that all three services are accessible and returning HTTP 200:
- TTS Service (port 7860)
- Voice Conversion Service (port 7861)
- Script Reader Service (port 7862)

**Critical for**: Ensuring services start correctly and are accessible.

### 2. Docker Container Tests (`TestDockerContainer`)

Tests Docker container health and configuration:
- Container is running
- All ports are properly exposed
- Service processes are running inside container

**Critical for**: Verifying Docker setup and process management.

### 3. PyTorch Setup Tests (`TestPyTorchSetup`)

Tests PyTorch installation and configuration:
- PyTorch is installed and importable
- CUDA availability can be detected (result may be True or False)
- Basic tensor operations work

**Critical for**: Ensuring ML framework is properly configured.

### 4. Dependencies Tests (`TestDependencies`)

Tests that all required packages are installed:
- Core packages: torch, torchaudio, transformers, diffusers
- Audio processing: librosa, soundfile
- Web interface: gradio
- Utilities: numpy, PyPDF2
- Main package: chatterbox-tts

**Critical for**: Preventing import errors and missing dependencies.

### 5. SSL Configuration Tests (`TestSSLConfiguration`)

Tests HTTPS/SSL setup:
- SSL certificates exist in container
- Services are accessible via HTTPS

**Critical for**: Ensuring secure connections.

### 6. Functional Basics Tests (`TestFunctionalBasics`)

Tests basic functionality of services:
- Gradio config endpoints are accessible
- Services expose their interfaces correctly

**Critical for**: Verifying services are not just running but functional.

### 7. File System Tests (`TestFileSystem`)

Tests filesystem setup:
- Output directory exists
- All required application scripts are present

**Critical for**: Ensuring proper deployment of application files.

## Understanding Test Results

### All Tests Pass ✅

```
======================== 35 passed in 5.23s =========================
✅ All tests passed!
```

**Meaning**: System is healthy and all components are working correctly.

### Some Tests Fail ❌

```
======================== 2 failed, 33 passed in 5.45s =========================
```

**Action**: Check which tests failed:
- **Service availability failures**: Services may not have fully started (wait longer)
- **PyTorch/CUDA failures**: Check GPU driver compatibility
- **Dependency failures**: Package may be missing or incompatible
- **Container failures**: Docker issue or container not running

## Integration with Development Workflow

### Before Making Changes

```bash
# Baseline test - ensure everything works
./tests/run_tests.sh
```

### After Making Changes

```bash
# Rebuild and test
docker-compose down
docker-compose build
docker-compose up -d
sleep 30  # Wait for services to start
./tests/run_tests.sh
```

### Continuous Integration (CI)

Add this to your CI pipeline:

```yaml
# Example GitHub Actions workflow
- name: Run Chatterbox Tests
  run: |
    docker-compose up -d
    sleep 30
    pip install -r tests/requirements.txt
    pytest tests/test_services.py -v
```

## Common Issues and Solutions

### Issue: Tests fail with connection errors

**Solution**: Services may still be starting. Wait 30-60 seconds after `docker-compose up` before running tests.

```bash
docker-compose up -d
sleep 60
./tests/run_tests.sh
```

### Issue: CUDA tests show "False"

**Explanation**: This is expected on systems without compatible GPU drivers. The test verifies CUDA *detection* works, not that CUDA is available.

**Solution**: No action needed if services work on CPU. For GPU acceleration, update drivers as per system admin.

### Issue: SSL certificate warnings

**Explanation**: Tests use self-signed certificates, which generate warnings.

**Solution**: Tests automatically suppress these warnings. This is expected behavior.

### Issue: Container not found

**Solution**: Start the container first:

```bash
docker-compose up -d
```

## Test Coverage

Current test coverage includes:

- ✅ **HTTP endpoints** - All services respond correctly
- ✅ **Container processes** - All required processes running
- ✅ **Python imports** - All packages importable
- ✅ **PyTorch operations** - Basic tensor operations work
- ✅ **SSL/HTTPS** - Secure connections configured
- ✅ **File structure** - All required files present

**Not yet covered** (future additions):
- ⏳ End-to-end TTS generation
- ⏳ Voice conversion functionality
- ⏳ PDF parsing in Script Reader
- ⏳ Audio output quality validation
- ⏳ Performance benchmarks

## Adding New Tests

### Example: Add a test for a new service

```python
def test_new_service_responds(self):
    """Test that new service returns HTTP 200."""
    response = requests.get("https://localhost:7863", verify=False, timeout=10)
    assert response.status_code == 200, "New service not responding"
```

### Example: Test a specific dependency

```python
def test_new_package_installed(self):
    """Test that new package is installed."""
    result = subprocess.run(
        ["docker", "exec", "chatterbox-tts", "python", "-c", "import new_package"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, "Package new_package not installed"
```

## Maintenance

### Regular Test Runs

Run tests:
- ✅ Before committing changes
- ✅ After pulling updates
- ✅ After modifying Dockerfile
- ✅ After updating dependencies
- ✅ Before deploying to production

### Updating Tests

When adding new features:
1. Add corresponding tests to appropriate test class
2. Update this README with new test descriptions
3. Run full test suite to ensure no regressions

## Support

If tests fail unexpectedly:
1. Check Docker container logs: `docker logs chatterbox-tts`
2. Verify services manually: `curl -k https://localhost:7860`
3. Check container status: `docker ps -a`
4. Review test output for specific error messages

## License

Same as main project (see root LICENSE file).
