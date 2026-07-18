import sys
from unittest.mock import patch, Mock
import requests
from fastapi.testclient import TestClient

# Add web directory to Python path so test runner can locate app.py from the project root
sys.path.append("apps/web")
from app import app  # noqa: E402

client = TestClient(app)


def test_healthz():
    """Test that the /healthz probe returns operational status for Kubernetes."""
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "frontend-operational"}


@patch("app.requests.get")
def test_home_page_api_connected(mock_get):
    """Test home page behavior when the backend API successfully responds."""
    # 1. Create a simulated backend response object
    mock_response = Mock()
    mock_response.json.return_value = {
        "query": "waterproof jacket",
        "engine": "mock-test-engine",
        "products": [{"id": 101, "name": "Premium Waterproof Jacket", "score": 0.99}]
    }
    mock_get.return_value = mock_response

    # 2. Call the frontend endpoint using our test client
    response = client.get("/?q=waterproof+jacket")
    assert response.status_code == 200
    data = response.json()

    # 3. Verify the frontend structured the payload correctly
    assert data["tier"] == "frontend-ui"
    assert data["api_status"] == "connected"
    assert data["payload"]["products"][0]["name"] == "Premium Waterproof Jacket"

    # 4. Verify our app actually attempted to call the correct backend URL once
    mock_get.assert_called_once()


@patch("app.requests.get")
def test_home_page_api_disconnected(mock_get):
    """Test home page gracefully handles backend API connection failures or timeouts."""
    # Simulate a network timeout or connection refusal when calling the backend API
    mock_get.side_effect = requests.exceptions.ConnectionError("Backend API is unreachable")

    response = client.get("/")
    assert response.status_code == 200
    data = response.json()

    # Verify our try/except block caught the error and degraded gracefully
    assert data["tier"] == "frontend-ui"
    assert data["api_status"] == "disconnected/error"
    assert "Backend API is unreachable" in data["details"]
