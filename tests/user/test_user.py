from fastapi import status
from app.user.schemas import UserRole


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
        json=payload,
    )

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["username"] == username
    assert data["first_name"] == first_name
    assert "id" in data


def test_get_users(client, login_as_admin):
    headers = {"Authorization": f"Bearer {login_as_admin}"}
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

    response = client.post(
        CREATE_USER_URL,
        json=payload,
        headers=headers)
    

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



def test_login(client):
    URL =  "/api/v1/users/create/student/"
    LOGIN_URL =  "/api/v1/auth/login"
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


    login_payload = {
        "username": username,
        "password": password
    }

    response = client.post(LOGIN_URL, data=login_payload)
    assert response.status_code == status.HTTP_202_ACCEPTED
    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"



def test_create_teacher(client, login_as_admin):
    headers = {"Authorization": f"Bearer {login_as_admin}"}
    URL = "/api/v1/users/create/teacher"
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

    response = client.post(url=URL, json=payload, headers=headers)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    
    assert data["role"] == UserRole.TEACHER


def test_create_teacher_with_no_authorization(client, login_as_teacher, login_as_student):
    teacher_login = {"Authorization": f"Bearer {login_as_teacher}"}
    student_login = {"Authorization": f"Bearer {login_as_student}"}
    URL = "/api/v1/users/create/teacher"
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

    response = client.post(url=URL, json=payload, headers=teacher_login)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    response = client.post(url=URL, json=payload, headers=student_login)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    response = client.post(url=URL, json=payload)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED



def test_create_admin(client, login_as_admin):
    headers = {"Authorization": f"Bearer {login_as_admin}"}

    URL = "/api/v1/users/create/admin"
    first_name = "ADmin"
    last_name = "Admin"
    username = "admin_222"
    email = "adiadimin@example.com"
    password = "senha12312312334"

    payload = {
        "first_name": first_name,
        "last_name": last_name,
        "username": username,
        "email": email,
        "password": password
    }

    response = client.post(url=URL, json=payload, headers=headers)
    assert response.status_code == status.HTTP_201_CREATED



def test_create_teacher_with_no_authorization(client, login_as_student, login_as_teacher):
    student_login = {"Authorization": f"Bearer {login_as_student}"}
    teacher_login = {"Authorization": f"Bearer {login_as_teacher}"}

    URL = "/api/v1/users/create/admin"
    first_name = "ADmin"
    last_name = "Admin"
    username = "admin_222"
    email = "adiadimin@example.com"
    password = "senha12312312334"

    payload = {
        "first_name": first_name,
        "last_name": last_name,
        "username": username,
        "email": email,
        "password": password
    }

    response = client.post(url=URL, json=payload, headers=student_login)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    response = client.post(url=URL, json=payload, headers=teacher_login)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    response = client.post(url=URL, json=payload)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_delete_user(client, login_as_admin):
    headers = {"Authorization": f"Bearer {login_as_admin}"}

    URL = "/api/v1/users/create/student"
    DELETE_URL = "/api/v1/users/delete/"
    first_name = "student"
    last_name = "student"
    username = "student_222"
    email = "student@example.com"
    password = "senha12312312334"

    payload = {
        "first_name": first_name,
        "last_name": last_name,
        "username": username,
        "email": email,
        "password": password
    }

    response = client.post(url=URL, json=payload, headers=headers)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()

    user_id = str(data["id"])

    # delete user
    response = client.delete(url=DELETE_URL+user_id, headers=headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_user_with_no_authorization(client, login_as_student, login_as_admin, login_as_teacher):
    student_auth = {"Authorization": f"Bearer {login_as_student}"}
    teacher_auth = {"Authorization": f"Bearer {login_as_teacher}"}
    admin_auth = {"Authorization": f"Bearer {login_as_admin}"}

    URL = "/api/v1/users/create/student"
    DELETE_URL = "/api/v1/users/delete/"
    first_name = "student"
    last_name = "student"
    username = "student_222"
    email = "student@example.com"
    password = "senha12312312334"

    payload = {
        "first_name": first_name,
        "last_name": last_name,
        "username": username,
        "email": email,
        "password": password
    }

    response = client.post(url=URL, json=payload, headers=admin_auth)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    user_id = str(data["id"])

    # delete user as a student
    response = client.delete(url=DELETE_URL+user_id, headers=student_auth)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


    # delete user as a teacher
    response = client.delete(url=DELETE_URL+user_id, headers=teacher_auth)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED



def test_patch_user(client, login_as_admin):
    headers = {"Authorization": f"Bearer {login_as_admin}"}

    URL = "/api/v1/users/create/student"
    PATCH_URL = "/api/v1/users/edit/"
    first_name = "student"
    last_name = "student"
    username = "student_222"
    email = "student@example.com"
    password = "senha12312312334"

    payload = {
        "first_name": first_name,
        "last_name": last_name,
        "username": username,
        "email": email,
        "password": password
    }

    response = client.post(url=URL, json=payload, headers=headers)
    assert response.status_code == status.HTTP_201_CREATED
    user_id = str(response.json()["id"])

    # edit data
    new_username = "new_username1001"
    new_payload = {
        "username": new_username
    }

    response = client.patch(url=PATCH_URL+user_id, headers=headers, json=new_payload)
    
    assert response.status_code == status.HTTP_202_ACCEPTED

    data = response.json()

    assert data["username"] == new_username


def test_patch_user_with_no_authorization(client, login_as_admin, login_as_student):
    admin_auth = {"Authorization": f"Bearer {login_as_admin}"}
    student_auth = {"Authorization": f"Bearer {login_as_student}"}

    URL = "/api/v1/users/create/student"
    PATCH_URL = "/api/v1/users/edit/"
    first_name = "student"
    last_name = "student"
    username = "student_222"
    email = "student@example.com"
    password = "senha12312312334"

    payload = {
        "first_name": first_name,
        "last_name": last_name,
        "username": username,
        "email": email,
        "password": password
    }

    response = client.post(url=URL, json=payload, headers=admin_auth)
    assert response.status_code == status.HTTP_201_CREATED
    user_id = str(response.json()["id"])

    
    new_username = "new_username1001"
    new_payload = {
        "username": new_username
    }

    # edit data as a student
    response = client.patch(url=PATCH_URL+user_id, headers=student_auth, json=new_payload)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


    # edit data with no login
    response = client.patch(url=PATCH_URL+user_id, json=new_payload)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED