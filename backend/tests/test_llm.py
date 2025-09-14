# backend/tests/test_llm.py
import pytest
from unittest.mock import patch, MagicMock
from backend.llm import generate_response

@pytest.fixture
def sample_email():
    return "Hello, I cannot access my account. Please help."

@pytest.fixture
def sample_context():
    return [
        "Step 1: Reset your password using the link.",
        "Step 2: Contact support if reset fails."
    ]

def test_generate_response(sample_email, sample_context):
    # Mock the client.models.generate_content method
    with patch("backend.llm.client.models.generate_content") as mock_generate:
        # Create a fake response object with .text attribute
        mock_resp = MagicMock()
        mock_resp.text = "Sure, here’s how you can reset your account..."
        mock_generate.return_value = mock_resp

        result = generate_response(sample_email, sample_context)

        # Assertions
        mock_generate.assert_called_once()  # ensure API was "called"
        args, kwargs = mock_generate.call_args
        # Check that our prompt was passed in contents
        assert any("Hello, I cannot access my account" in c for c in kwargs["contents"])
        assert "Step 1: Reset your password" in kwargs["contents"][0]

        assert result == "Sure, here’s how you can reset your account..."
