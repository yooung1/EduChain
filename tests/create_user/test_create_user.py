from fastapi.testclient import TestClient
from app.api.main import app
from app.constants.user_registration_model_constants import UserRole



client = TestClient(app)



#TODO: MOCKAR OS TESTES PARA NAO CRIAR NADA NO BANCO DE DADOS
def test_create_user():
    username = "testenovo001"
    email = "testenovo001@gmail.com"
    password = "password"
    user_type = UserRole.STUDENT

    payload = {
        "username": username,
        "email": email,
        "password": password,
        "user_type": user_type
    }
    response = client.post("/create/user", json=payload)
    assert response.status_code == 200
    assert response.json()["username"] == username


def test_read_users():
    response = client.get("/users")
    
    assert response.status_code == 200
    assert isinstance(response.json(), list)
