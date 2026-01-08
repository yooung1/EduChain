from fastapi.testclient import TestClient
from app.main import app
from fastapi import status



def test_create_student(client):
    payload = {
        "first_name": "Ana",
        "last_name": "Silva",
        "username": "ana.silva1",
        "email": "ana.silva1@example.com",
        "password": "senha12312312334"
    }

    response = client.post(
        "/api/v1/users/create/student/",
        json=payload
    )

    print(response.json())
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["username"] == "ana.silva1"
    assert "id" in data
