from fastapi.testclient import TestClient
from app.main import app
from fastapi import status



def test_create_student(client):
    URL =  "/api/v1/users/create/student/"
    first_name = "Ana"
    last_name = "Silva"
    username = "ana.silva1"
    email = "ana.silva1@example.com"
    password = "senha12312312334"

    payload = {
        "first_name": first_name,
        "last_name": last_name,
        "username": username,
        "email": email,
        "password": password
    }

    response = client.post(
        URL,
        json=payload
    )

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["username"] == username
    assert data["first_name"] == first_name
    assert "id" in data


def test_get_users(client):
    CREATE_USER_URL =  "/api/v1/users/create/student/"
    GET_USER_URL =  "/api/v1/users/"
    
    # create first user
    first_name1 = "Ana"
    last_name1 = "Silva"
    username1 = "ana.silva1"
    email1 = "ana.silva1@example.com"
    password1 = "senha12312312334"

    payload = {
        "first_name": first_name1,
        "last_name": last_name1,
        "username": username1,
        "email": email1,
        "password": password1
    }

    response = client.post(CREATE_USER_URL, json=payload)
    assert response.status_code == status.HTTP_201_CREATED

    # create second user
    first_name2 = "Lucas"
    last_name2 = "Silva"
    username2 = "ana.silva21"
    email2 = "lucas.silva21@example.com"
    password2 = "senha12312312334"

    payload = {
        "first_name": first_name2,
        "last_name": last_name2,
        "username": username2,
        "email": email2,
        "password": password2
    }

    response = client.post(CREATE_USER_URL, json=payload)
    assert response.status_code == status.HTTP_201_CREATED

    response = client.get(GET_USER_URL)
    assert response.status_code ==status.HTTP_200_OK
    assert len(response.json()) == 2
    data = response.json()
    assert data[0]["first_name"] == first_name1
    assert data[1]["first_name"] == first_name2