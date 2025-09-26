import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_crud_item():
    # create
    payload = {"name": "Book", "description": "About testing"}
    r = client.post("/api/v1/items/", json=payload)
    assert r.status_code == 201
    data = r.json()
    assert data["name"] == payload["name"]
    item_id = data["id"]

    # get
    r = client.get(f"/api/v1/items/{item_id}")
    assert r.status_code == 200

    # list
    r = client.get("/api/v1/items/?skip=0&limit=10")
    assert r.status_code == 200
    assert isinstance(r.json(), list)

    # update
    upd = {"description": "Updated"}
    r = client.patch(f"/api/v1/items/{item_id}", json=upd)
    assert r.status_code == 200
    assert r.json()["description"] == "Updated"

    # delete
    r = client.delete(f"/api/v1/items/{item_id}")
    assert r.status_code == 204

    # not found
    r = client.get(f"/api/v1/items/{item_id}")
    assert r.status_code == 404
