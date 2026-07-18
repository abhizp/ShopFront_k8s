import os
import requests
from fastapi import FastAPI

app = FastAPI(title="Shopfront Web Frontend")

# Looks for the API on the internal network, defaults to localhost for testing
API_URL = os.getenv("API_URL", "http://localhost:8000")


@app.get("/healthz")
def healthz():
    return {"status": "frontend-operational"}


@app.get("/")
def home_page(q: str = "waterproof jacket"):
    try:
        backend_response = requests.get(f"{API_URL}/api/v1/search?q={q}", timeout=3)
        return {
            "tier": "frontend-ui",
            "api_status": "connected",
            "payload": backend_response.json()
        }
    except Exception as e:
        return {
            "tier": "frontend-ui",
            "api_status": "disconnected/error",
            "details": str(e)
        }
