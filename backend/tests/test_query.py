from fastapi.testclient import TestClient
from app.main import create_app

app = create_app(testing=True)

def test_health_returns_ok():
    with TestClient(app) as client:
        response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_query_happy_path():
    with TestClient(app) as client:
        response = client.post("/query", json={"question": "What is artificial intelligence?"})
    assert response.status_code == 200
    body = response.json()
    assert body["answer"]
    assert body["sources"] == ["AI.txt — chunk 0"]

def test_query_rejects_invalid_input():
    with TestClient(app) as client:
        response = client.post("/query", json={"question": ""})
    assert response.status_code == 422
