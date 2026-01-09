#!/usr/bin/env python3
"""
Deployment Compatibility Test
Tests Docker and system requirements for running the application
For all team members (not model development specific)

Usage: python test_compability.py
"""

import os
import sys
import subprocess
import shutil
from datetime import datetime
from pathlib import Path


def create_log_folder():
    """Create log folder if it doesn't exist"""
    log_dir = Path(__file__).parent / "logs"
    log_dir.mkdir(exist_ok=True)
    return log_dir


def get_log_filename():
    """Generate log filename with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return f"deployment_test_{timestamp}.log"


class Logger:
    """Logger for console and file output"""
    def __init__(self, log_file):
        self.log_file = log_file
        self.file_handle = open(log_file, 'w')
    
    def log(self, message):
        """Write to console and file"""
        print(message)
        self.file_handle.write(message + '\n')
        self.file_handle.flush()
    
    def close(self):
        """Close log file"""
        self.file_handle.close()


def test_docker(logger):
    """Test Docker availability and daemon status"""
    logger.log("\nDOCKER TEST")
    
    try:
        result = subprocess.run(['docker', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.strip()
            logger.log(f"Docker: {version}")
            
            # Test Docker daemon
            daemon_test = subprocess.run(['docker', 'info'], capture_output=True, text=True, timeout=5)
            if daemon_test.returncode == 0:
                logger.log("Docker daemon: Running")
                logger.log("Docker test passed")
                return True
            else:
                logger.log("Docker daemon: Not running or no permissions")
                logger.log("Hint: Start Docker or add user to docker group")
                return False
        else:
            logger.log("Docker not found")
            logger.log("Install: https://docs.docker.com/engine/install/")
            return False
    except subprocess.TimeoutExpired:
        logger.log("Docker daemon: Timeout (not responding)")
        return False
    except Exception as e:
        logger.log(f"Docker test failed: {str(e)}")
        return False


def test_docker_compose(logger):
    """Test Docker Compose availability"""
    logger.log("\nDOCKER COMPOSE TEST")
    
    try:
        # Try docker compose (v2)
        result = subprocess.run(['docker', 'compose', 'version'], capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.strip()
            logger.log(f"Docker Compose: {version}")
            logger.log("Docker Compose test passed")
            return True
        
        # Try docker-compose (v1)
        result = subprocess.run(['docker-compose', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.strip()
            logger.log(f"Docker Compose (legacy): {version}")
            logger.log("Docker Compose test passed")
            return True
        
        logger.log("Docker Compose not found")
        logger.log("Included with Docker Desktop or install separately")
        return False
    except Exception as e:
        logger.log(f"Docker Compose test failed: {str(e)}")
        return False


def test_git(logger):
    """Test Git availability"""
    logger.log("\nGIT TEST")
    
    try:
        result = subprocess.run(['git', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.strip()
            logger.log(f"Git: {version}")
            logger.log("Git test passed")
            return True
        else:
            logger.log("Git not found")
            return False
    except Exception as e:
        logger.log(f"Git test failed: {str(e)}")
        return False


def test_curl(logger):
    """Test curl for API testing"""
    logger.log("\nCURL TEST")
    
    try:
        result = subprocess.run(['curl', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.split('\n')[0]
            logger.log(f"curl: {version}")
            logger.log("curl test passed")
            return True
        else:
            logger.log("curl not found")
            logger.log("curl is optional but useful for API testing")
            return False
    except Exception as e:
        logger.log(f"curl test failed: {str(e)}")
        return False


def test_port_availability(logger):
    """Test if required ports are available"""
    logger.log("\nPORT AVAILABILITY TEST")
    
    try:
        import socket
        
        ports_to_check = {
            11434: "Ollama API",
            3000: "Frontend (Next.js)",
        }
        
        ports_in_use = []
        
        for port, service in ports_to_check.items():
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(('localhost', port))
            sock.close()
            
            if result == 0:
                logger.log(f"Port {port} ({service}): IN USE (service may be running)")
                ports_in_use.append(port)
            else:
                logger.log(f"Port {port} ({service}): Available")
        
        if not ports_in_use:
            logger.log("Port availability test passed")
            return True
        else:
            logger.log("Port status: UNDETERMINED (services may already be running)")
            return "undetermined"
    except Exception as e:
        logger.log(f"Port test failed: {str(e)}")
        return False


def test_disk_space(logger):
    """Test available disk space"""
    logger.log("\nDISK SPACE TEST")
    
    try:
        stat = shutil.disk_usage(Path(__file__).parent)
        free_gb = stat.free / (1024**3)
        total_gb = stat.total / (1024**3)
        
        logger.log(f"Free space: {free_gb:.2f} GB / {total_gb:.2f} GB")
        
        required_gb = 10  # Minimum for Docker images and models
        if free_gb >= required_gb:
            logger.log(f"Sufficient space (>= {required_gb} GB required)")
            logger.log("Disk space test passed")
            return True
        else:
            logger.log(f"WARNING: Low disk space (< {required_gb} GB free)")
            logger.log("Disk space test passed with warning")
            return True
    except Exception as e:
        logger.log(f"Disk space test failed: {str(e)}")
        return False


def test_project_structure(logger):
    """Test if project structure is correct"""
    logger.log("\nPROJECT STRUCTURE TEST")
    
    project_root = Path(__file__).parent
    
    required_paths = {
        "docker-compose.yml": "Docker orchestration file",
        "backend/models": "Model deployment directory",
        "backend/models/Dockerfile": "Model container definition",
        "frontend": "Frontend application directory",
    }
    
    all_exist = True
    
    for path, description in required_paths.items():
        full_path = project_root / path
        if full_path.exists():
            logger.log(f"{path}: Found")
        else:
            logger.log(f"{path}: MISSING ({description})")
            all_exist = False
    
    if all_exist:
        logger.log("Project structure test passed")
    else:
        logger.log("Project structure test failed")
    
    return all_exist


def main():
    """Main test execution"""
    
    # Setup logging
    log_dir = create_log_folder()
    log_filename = get_log_filename()
    log_path = log_dir / log_filename
    
    logger = Logger(log_path)
    
    # Header
    logger.log("=" * 80)
    logger.log("DEPLOYMENT COMPATIBILITY TEST")
    logger.log("=" * 80)
    logger.log(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.log(f"Python: {sys.version.split()[0]}")
    logger.log(f"Platform: {sys.platform}")
    logger.log("")
    
    logger.log("=" * 80)
    logger.log("SYSTEM REQUIREMENTS")
    logger.log("=" * 80)
    
    # Run tests
    test_results = {
        'Docker': test_docker(logger),
        'Docker Compose': test_docker_compose(logger),
        'Git': test_git(logger),
        'curl': test_curl(logger),
        'Port Availability': test_port_availability(logger),
        'Disk Space': test_disk_space(logger),
        'Project Structure': test_project_structure(logger),
    }
    
    # Summary
    logger.log("\n" + "=" * 80)
    logger.log("TEST SUMMARY")
    logger.log("=" * 80)
    
    for test_name, result in test_results.items():
        if result == "undetermined":
            status = "UNDETERMINED"
        elif result:
            status = "PASSED"
        else:
            status = "FAILED"
        logger.log(f"  {test_name}: {status}")
    
    total_passed = sum(1 for r in test_results.values() if r is True)
    total_undetermined = sum(1 for r in test_results.values() if r == "undetermined")
    total_tests = len(test_results)
    logger.log(f"\nTotal: {total_passed} passed, {total_undetermined} undetermined, {total_tests - total_passed - total_undetermined} failed")
    
    # Critical tests (must pass to deploy)
    critical_tests = ['Docker', 'Docker Compose', 'Project Structure']
    critical_passed = all(test_results.get(test, False) for test in critical_tests)
    
    if critical_passed and total_passed >= total_tests - 1:  # Allow curl to fail
        logger.log("\n[SUCCESS] System ready for deployment")
        logger.log("\nNext steps:")
        logger.log("  1. docker compose build ollama")
        logger.log("  2. docker compose up -d ollama")
        logger.log("  3. curl http://localhost:11434/api/tags")
    elif critical_passed:
        logger.log("\n[WARNING] System ready but with minor issues")
    else:
        logger.log("\n[FAILED] Critical requirements missing")
        logger.log("Fix failed tests before deployment")
    
    logger.log(f"\nCompleted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.log("=" * 80)
    
    logger.close()
    
    print(f"\nLog saved: {log_path}")
    
    # Exit code
    sys.exit(0 if critical_passed else 1)


if __name__ == "__main__":
    main()
