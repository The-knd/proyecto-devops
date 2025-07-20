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

def test_create_and_list_clients():
    # Crear cliente
    response = client.post("/clients", json={"name": "Juan Pérez"})
    assert response.status_code == 200
    data = response.json()
    assert "client_id" in data
    # Listar clientes
    response = client.get("/clients")
    assert response.status_code == 200
    clients = response.json()
    assert any(c["name"] == "Juan Pérez" for c in clients)

def test_create_and_list_products():
    # Crear producto
    response = client.post("/products", json={"name": "Laptop", "price": 999.99})
    assert response.status_code == 200
    data = response.json()
    assert "product_id" in data
    # Listar productos
    response = client.get("/products")
    assert response.status_code == 200
    products = response.json()
    assert any(p["name"] == "Laptop" for p in products)

def test_create_and_list_sales():
    # Crear cliente y producto
    client_resp = client.post("/clients", json={"name": "Cliente Venta"})
    product_resp = client.post("/products", json={"name": "Mouse", "price": 25.0})
    client_id = client_resp.json()["client_id"]
    product_id = product_resp.json()["product_id"]
    # Registrar venta
    sale_resp = client.post("/sales", json={"client_id": client_id, "product_id": product_id, "quantity": 3})
    assert sale_resp.status_code == 200
    assert sale_resp.json()["message"] == "Sale recorded"
    # Listar ventas
    response = client.get("/sales")
    assert response.status_code == 200
    sales = response.json()
    assert any(s["client_id"] == client_id and s["product_id"] == product_id for s in sales)

def test_sale_with_invalid_ids():
    # Intentar registrar venta con IDs inválidos
    sale_resp = client.post("/sales", json={"client_id": "no-existe", "product_id": "no-existe", "quantity": 1})
    assert sale_resp.status_code == 400
    assert sale_resp.json()["detail"] == "Invalid client or product ID" 