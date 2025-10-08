import pytest
import sys
import os

def run_backend_tests():
    """Run backend unit tests"""
    print("Running backend tests...")
    backend_result = pytest.main([
        'tests/backend',
        '-v',
        '--cov=backend',
        '--cov-report=term-missing',
        '--cov-report=html:coverage/backend'
    ])
    return backend_result

def run_integration_tests():
    """Run integration tests"""
    print("Running integration tests...")
    integration_result = pytest.main([
        'tests/integration',
        '-v',
        '--cov=backend',
        '--cov-append',
        '--cov-report=term-missing',
        '--cov-report=html:coverage/integration'
    ])
    return integration_result

if __name__ == '__main__':
    # Ensure we're in the project root directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Create coverage directory if it doesn't exist
    os.makedirs('coverage', exist_ok=True)
    
    # Run tests
    backend_status = run_backend_tests()
    integration_status = run_integration_tests()
    
    # Exit with non-zero status if any test suite failed
    if backend_status != 0 or integration_status != 0:
        sys.exit(1)
    
    print("\nAll tests completed successfully!")
