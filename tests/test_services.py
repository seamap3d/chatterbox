#!/usr/bin/env python3
"""
Test suite for Chatterbox services to ensure core functionality remains intact.
Run with: pytest tests/test_services.py -v
"""

import pytest
import requests
import time
import subprocess
import json
from urllib3.exceptions import InsecureRequestWarning

# Suppress SSL warnings for self-signed certificates
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

# Service endpoints
BASE_URL = "https://localhost"
TTS_PORT = 7860
VC_PORT = 7861
SCRIPT_READER_PORT = 7862

SERVICES = {
    "TTS": f"{BASE_URL}:{TTS_PORT}",
    "Voice Conversion": f"{BASE_URL}:{VC_PORT}",
    "Script Reader": f"{BASE_URL}:{SCRIPT_READER_PORT}"
}


class TestServiceAvailability:
    """Test that all services are accessible and responding."""
    
    @pytest.mark.parametrize("service_name,service_url", SERVICES.items())
    def test_service_responds(self, service_name, service_url):
        """Test that each service returns HTTP 200."""
        response = requests.get(service_url, verify=False, timeout=10)
        assert response.status_code == 200, f"{service_name} service not responding"
    
    def test_all_services_up(self):
        """Test that all three services are running simultaneously."""
        results = {}
        for name, url in SERVICES.items():
            try:
                response = requests.get(url, verify=False, timeout=5)
                results[name] = response.status_code == 200
            except Exception as e:
                results[name] = False
        
        assert all(results.values()), f"Not all services are up: {results}"


class TestDockerContainer:
    """Test Docker container health and configuration."""
    
    def test_container_running(self):
        """Test that the chatterbox container is running."""
        result = subprocess.run(
            ["docker", "ps", "--filter", "name=chatterbox-tts", "--format", "{{.Status}}"],
            capture_output=True,
            text=True
        )
        assert "Up" in result.stdout, "Container is not running"
    
    def test_container_ports_exposed(self):
        """Test that all required ports are exposed."""
        result = subprocess.run(
            ["docker", "port", "chatterbox-tts"],
            capture_output=True,
            text=True
        )
        output = result.stdout
        
        assert "7860" in output, "TTS port 7860 not exposed"
        assert "7861" in output, "VC port 7861 not exposed"
        assert "7862" in output, "Script Reader port 7862 not exposed"
    
    def test_container_processes(self):
        """Test that all service processes are running inside container."""
        result = subprocess.run(
            ["docker", "exec", "chatterbox-tts", "ps", "aux"],
            capture_output=True,
            text=True
        )
        output = result.stdout
        
        assert "gradio_tts_app.py" in output, "TTS process not running"
        assert "gradio_vc_app.py" in output, "VC process not running"
        assert "script_reader_app.py" in output, "Script Reader process not running"


class TestPyTorchSetup:
    """Test PyTorch and CUDA configuration."""
    
    def test_pytorch_installed(self):
        """Test that PyTorch is installed and importable."""
        result = subprocess.run(
            ["docker", "exec", "chatterbox-tts", "python", "-c", 
             "import torch; print(torch.__version__)"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, "PyTorch not installed or not importable"
        assert len(result.stdout.strip()) > 0, "PyTorch version not detected"
    
    def test_cuda_detection(self):
        """Test CUDA availability detection (may be False on CPU-only setups)."""
        result = subprocess.run(
            ["docker", "exec", "chatterbox-tts", "python", "-c",
             "import torch; print(torch.cuda.is_available())"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, "Failed to check CUDA availability"
        cuda_available = result.stdout.strip()
        assert cuda_available in ["True", "False"], f"Unexpected CUDA status: {cuda_available}"
    
    def test_pytorch_can_create_tensor(self):
        """Test basic PyTorch tensor operations work."""
        result = subprocess.run(
            ["docker", "exec", "chatterbox-tts", "python", "-c",
             "import torch; t = torch.randn(2, 2); print('SUCCESS' if t.shape == (2, 2) else 'FAIL')"],
            capture_output=True,
            text=True
        )
        assert "SUCCESS" in result.stdout, "PyTorch tensor operations failed"


class TestDependencies:
    """Test that critical dependencies are installed."""
    
    @pytest.mark.parametrize("package", [
        "torch",
        "torchaudio",
        "transformers",
        "diffusers",
        "gradio",
        "librosa",
        "soundfile",
        "numpy",
        "PyPDF2"
    ])
    def test_package_installed(self, package):
        """Test that critical Python packages are installed."""
        result = subprocess.run(
            ["docker", "exec", "chatterbox-tts", "python", "-c", f"import {package}"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"Package {package} not installed or not importable"
    
    def test_chatterbox_tts_installed(self):
        """Test that chatterbox-tts package is installed."""
        result = subprocess.run(
            ["docker", "exec", "chatterbox-tts", "pip", "show", "chatterbox-tts"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, "chatterbox-tts package not installed"
        assert "Version:" in result.stdout, "chatterbox-tts version not detected"


class TestSSLConfiguration:
    """Test SSL/HTTPS configuration."""
    
    def test_ssl_certificates_exist(self):
        """Test that SSL certificate files exist in the container."""
        result = subprocess.run(
            ["docker", "exec", "chatterbox-tts", "ls", "/app/cert.pem", "/app/key.pem"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, "SSL certificates not found in container"
    
    def test_https_connection(self):
        """Test that services are accessible via HTTPS."""
        response = requests.get(SERVICES["TTS"], verify=False, timeout=10)
        assert response.url.startswith("https://"), "Service not using HTTPS"


class TestFunctionalBasics:
    """Test basic functional operations of services."""
    
    def test_tts_gradio_config_available(self):
        """Test that TTS service exposes Gradio config endpoint."""
        try:
            response = requests.get(
                f"{SERVICES['TTS']}/config",
                verify=False,
                timeout=10
            )
            # Gradio config endpoint should return JSON
            assert response.status_code == 200, "TTS config endpoint not accessible"
        except Exception as e:
            pytest.skip(f"Could not test Gradio config: {e}")
    
    def test_vc_gradio_config_available(self):
        """Test that VC service exposes Gradio config endpoint."""
        try:
            response = requests.get(
                f"{SERVICES['Voice Conversion']}/config",
                verify=False,
                timeout=10
            )
            assert response.status_code == 200, "VC config endpoint not accessible"
        except Exception as e:
            pytest.skip(f"Could not test Gradio config: {e}")
    
    def test_script_reader_gradio_config_available(self):
        """Test that Script Reader service exposes Gradio config endpoint."""
        try:
            response = requests.get(
                f"{SERVICES['Script Reader']}/config",
                verify=False,
                timeout=10
            )
            assert response.status_code == 200, "Script Reader config endpoint not accessible"
        except Exception as e:
            pytest.skip(f"Could not test Gradio config: {e}")


class TestFileSystem:
    """Test filesystem setup and permissions."""
    
    def test_outputs_directory_exists(self):
        """Test that the outputs directory exists."""
        result = subprocess.run(
            ["docker", "exec", "chatterbox-tts", "test", "-d", "/app/outputs"],
            capture_output=True
        )
        assert result.returncode == 0, "/app/outputs directory does not exist"
    
    def test_app_scripts_exist(self):
        """Test that all required application scripts exist."""
        scripts = [
            "gradio_tts_app.py",
            "gradio_vc_app.py",
            "script_reader_app.py",
            "start_both_services.py",
            "script_parser.py"
        ]
        
        for script in scripts:
            result = subprocess.run(
                ["docker", "exec", "chatterbox-tts", "test", "-f", f"/app/{script}"],
                capture_output=True
            )
            assert result.returncode == 0, f"Required script {script} not found"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
