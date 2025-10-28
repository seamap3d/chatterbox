#!/bin/bash
# Test runner script for Chatterbox services
# This script ensures the services are running and then runs all tests

set -e

echo "=================================================="
echo "Chatterbox Services Test Suite"
echo "=================================================="

# Check if pytest is installed
if ! python3 -m pytest --version &> /dev/null; then
    echo "❌ pytest not found. Installing test dependencies..."
    python3 -m pip install --user -r tests/requirements.txt
fi

# Check if Docker is running
if ! docker ps &> /dev/null; then
    echo "❌ Docker is not running or not accessible"
    exit 1
fi

# Check if container is running
if ! docker ps | grep -q chatterbox-tts; then
    echo "⚠️  Container not running. Starting services..."
    docker-compose up -d
    echo "⏳ Waiting 30 seconds for services to start..."
    sleep 30
fi

echo ""
echo "✅ Prerequisites met. Running tests..."
echo ""

# Run tests with verbose output
python3 -m pytest tests/test_services.py -v --tb=short

TEST_EXIT_CODE=$?

echo ""
if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo "=================================================="
    echo "✅ All tests passed!"
    echo "=================================================="
else
    echo "=================================================="
    echo "❌ Some tests failed. Exit code: $TEST_EXIT_CODE"
    echo "=================================================="
fi

exit $TEST_EXIT_CODE
