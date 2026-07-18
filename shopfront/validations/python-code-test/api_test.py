import sys
from fastapi.testclient import TestClient

# Add app directory to Python path so test runner can locate app.py from anywhere
sys.path.append("apps/api")
from app import app  # noqa: E402

client = TestClient(app)


def test_liveness_probe():
    """Test that the /healthz probe always returns 200 OK for Kubernetes."""
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "alive"}


def test_readiness_probe_structure():
    """Test that /readyz returns a valid status payload."""
    response = client.get("/readyz")
    assert response.status_code in [200, 503]
    data = response.json()
    assert "status" in data


def test_search_endpoint_with_query():
    """Test searching for an item (e.g., 'laptop') handles data correctly."""
    response = client.get("/api/v1/search?q=laptop")
    assert response.status_code == 200
    data = response.json()

    assert data["query"] == "laptop"
    assert "engine" in data
    assert "products" in data
    assert len(data["products"]) > 0

    # Verify the product data structure
    first_product = data["products"][0]
    assert "id" in first_product
    assert "name" in first_product
    assert "score" in first_product


def test_search_endpoint_empty_query():
    """Test searching with an empty query string works without breaking."""
    response = client.get("/api/v1/search")
    assert response.status_code == 200
    assert len(response.json()["products"]) > 0
