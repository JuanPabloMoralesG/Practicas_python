from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient
import httpx
from main import app

client = TestClient(app)


def test_read_users():
    response = client.get("/users")
    assert response.status_code == 200


def test_delete_user():
    response = client.delete("/user/test@test.com",auth=client.post("/token",json={"username":"pablo1","password":"12345"}))
    assert response.status_code == 204
