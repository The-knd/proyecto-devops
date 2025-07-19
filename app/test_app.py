import pytest
from fastapi.testclient import TestClient
from src import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code in (200, 404)  # Puede ser 404 si no hay endpoint raíz

def test_metrics():
    response = client.get("/metrics")
    assert response.status_code == 200
    assert b"http_requests_total" in response.content 