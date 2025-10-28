# Testing

## Quick Test

Run the complete test suite to verify all services are working:

```bash
./tests/run_tests.sh
```

## What Gets Tested

✅ **All three services** (TTS, Voice Conversion, Script Reader) are accessible  
✅ **Docker container** is running with all processes  
✅ **PyTorch** is installed and working  
✅ **All dependencies** are present  
✅ **HTTPS/SSL** configuration is correct  
✅ **File structure** is intact  

## When to Run Tests

- ✅ Before committing changes
- ✅ After modifying Dockerfile
- ✅ After updating dependencies  
- ✅ Before deploying

See [tests/README.md](tests/README.md) for detailed documentation.

## Test Results

All 27 tests currently pass on the working system:

```
======================== 27 passed in 73.34s ========================
```

This ensures core functionality remains stable during development.
