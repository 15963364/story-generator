import pytest
import os

@pytest.fixture(autouse=True)
def setup_test_environment():
    """Setup test environment variables"""
    os.environ['ANTHROPIC_API_KEY'] = 'test-key-123'
    yield
    # Cleanup after tests
    if 'ANTHROPIC_API_KEY' in os.environ:
        del os.environ['ANTHROPIC_API_KEY']