"""
Pytest configuration and shared fixtures for the LLM Evaluation System tests.
Supports multi-provider testing (Groq, OpenAI, Anthropic).
"""

import os
import sys
import pytest

# Load environment variables FIRST, before anything else imports
try:
    from dotenv import load_dotenv
    # Explicitly load from .env in project root
    env_file = os.path.join(os.path.dirname(__file__), '.env')
    load_dotenv(dotenv_path=env_file, override=True)
except ImportError:
    pass  # dotenv optional


@pytest.fixture(scope="session", autouse=True)
def setup_env():
    """Ensure environment is loaded before tests run."""
    apis = {
        "GROQ": os.getenv("GROQ_API_KEY"),
        "OPENAI": os.getenv("OPENAI_API_KEY"),
        "ANTHROPIC": os.getenv("ANTHROPIC_API_KEY"),
    }
    
    available = [k for k, v in apis.items() if v]
    if available:
        print(f"\n✓ Available API keys: {', '.join(available)}")
    else:
        print("\n⚠ No API keys found in environment")
    
    return apis


@pytest.fixture
def test_cases():
    """Fixture providing sample test cases."""
    return [
        {"task": "What is 2+2?"},
        {"task": "What is the capital of France?"},
        {"task": "Explain photosynthesis."},
    ]


@pytest.fixture
def system_prompt():
    """Fixture providing a sample system prompt."""
    return "You are a helpful and accurate assistant. Provide clear and concise answers."


@pytest.fixture
def evaluation_goal():
    """Fixture providing a sample evaluation goal."""
    return "Evaluate the assistant's ability to provide accurate and helpful information"


@pytest.fixture
def groq_api_key():
    """Fixture providing Groq API key from environment."""
    return os.getenv("GROQ_API_KEY")


@pytest.fixture
def openai_api_key():
    """Fixture providing OpenAI API key from environment."""
    return os.getenv("OPENAI_API_KEY")


@pytest.fixture
def anthropic_api_key():
    """Fixture providing Anthropic API key from environment."""
    return os.getenv("ANTHROPIC_API_KEY")


@pytest.fixture
def fastapi_client():
    """Fixture providing a FastAPI test client."""
    from fastapi.testclient import TestClient
    from main import app
    
    return TestClient(app)


def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "api: marks tests as API endpoint tests"
    )
    config.addinivalue_line(
        "markers", "requires_api_key: marks tests requiring valid GROQ_API_KEY"
    )
