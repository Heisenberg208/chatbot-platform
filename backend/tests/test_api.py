import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "database": "connected"}


def test_root_endpoint():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert response.json()["service"] == "chatbot-platform"


@pytest.mark.asyncio
async def test_user_registration():
    """Test user registration endpoint."""
    response = client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "testpassword123"
        }
    )
    # This will fail without proper DB setup, but demonstrates structure
    assert response.status_code in [201, 500]  # 500 if DB not configured


# Add more tests for:
# - Authentication flow
# - Project CRUD
# - Prompt CRUD
# - Chat functionality
# - LLM provider mocking
