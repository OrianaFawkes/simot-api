
import pytest
from fastapi.testclient import TestClient

from main import app
from services.items import item_store


client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_item_store():
    # Keep each test independent of items created by other tests.
    item_store.clear()


@pytest.fixture
def item_payload():
    return {
        "name": "Rolled oats",
        "quantity": 2,
        "unit": "pack",
        "category": "grains",
        "min_quantity": 1,
        "is_essential": True,
        "storage_location": "pantry",
        "expiry_date": "2026-11-15",
        "purchase_date": "2026-10-10",
        "opened_at": None,
        "barcode": None,
    }


def test_create_item(item_payload):
    response = client.post("/items", json=item_payload)

    assert response.status_code == 201

    item = response.json()
    assert item["name"] == "Rolled oats"
    assert item["quantity"] == 2
    assert item["unit"] == "pack"
    assert item["category"] == "grains"
    assert item["is_essential"] is True
    assert item["id"]
    assert item["created_at"]
    assert item["updated_at"]


def test_list_items(item_payload):
    client.post("/items", json=item_payload)

    response = client.get("/items")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "Rolled oats"


def test_get_item(item_payload):
    created = client.post("/items", json=item_payload).json()

    response = client.get(f"/items/{created['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


def test_get_missing_item():
    response = client.get("/items/nonexistent")

    assert response.status_code == 404


def test_patch_item(item_payload):
    created = client.post("/items", json=item_payload).json()

    response = client.patch(
        f"/items/{created['id']}",
        json={"quantity": 0.5},
    )

    assert response.status_code == 200
    assert response.json()["quantity"] == 0.5
    assert response.json()["name"] == "Rolled oats"
    assert response.json()["created_at"] == created["created_at"]


def test_patch_can_clear_optional_field(item_payload):
    created = client.post("/items", json=item_payload).json()

    response = client.patch(
        f"/items/{created['id']}",
        json={"expiry_date": None},
    )

    assert response.status_code == 200
    assert response.json()["expiry_date"] is None


def test_patch_rejects_null_name(item_payload):
    created = client.post("/items", json=item_payload).json()

    response = client.patch(
        f"/items/{created['id']}",
        json={"name": None},
    )

    assert response.status_code == 422


def test_create_rejects_negative_quantity(item_payload):
    item_payload["quantity"] = -1

    response = client.post("/items", json=item_payload)

    assert response.status_code == 422


def test_create_rejects_invalid_unit(item_payload):
    item_payload["unit"] = "bucket"

    response = client.post("/items", json=item_payload)

    assert response.status_code == 422


def test_delete_item(item_payload):
    created = client.post("/items", json=item_payload).json()

    response = client.delete(f"/items/{created['id']}")

    assert response.status_code == 204
    assert client.get(f"/items/{created['id']}").status_code == 404


def test_delete_missing_item():
    response = client.delete("/items/nonexistent")

    assert response.status_code == 404