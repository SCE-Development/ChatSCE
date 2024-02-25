from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Welcome": "This is the SCE Chatbot API"}


def test_read_item():
    response = client.get("/gpt/Hello")
    assert response.status_code == 200
    assert "response" in response.json()
