from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_create_evaluation():
    response = client.post(
        "/evaluations",
        json={
            "model_name": "llama3",
            "dataset_name": "customer_support",
            "version": "1.0",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["model_name"] == "llama3"
    assert data["status"] == "PENDING"


def test_unknown_report():
    response = client.get(
        "/evaluations/00000000-0000-0000-0000-000000000000/report"
    )

    assert response.status_code == 404
