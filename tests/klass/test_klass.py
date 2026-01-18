from fastapi import status


def test_create_klass(client, login_as_teacher):
    teacher_auth = {"Authorization": f"Bearer {login_as_teacher}"}

    URL = "/api/v1/klass/create"
    name = "Course number 32"
    video = "url.com"
    description = "this is the description"

    payload = [{
        "name": name,
        "video": video,
        "description": description,
        "course_id": 0
    }]

    response = client.post(
        URL,
        json=payload,
        headers=teacher_auth
    )

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()

    assert data[0]["name"] == name


def test_create_klass_with_no_authorization(client, login_as_student):
    student_auth = {"Authorization": f"Bearer {login_as_student}"}

    URL = "/api/v1/klass/create"
    name = "Course number 32"
    video = "url.com"
    description = "this is the description"

    payload = [{
        "name": name,
        "video": video,
        "description": description,
        "course_id": 0
    }]

    response = client.post(
        URL,
        json=payload,
        headers=student_auth
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


    # test with no login
    response = client.post(
        URL,
        json=payload
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_klass(client, login_as_teacher):
    teacher_auth = {"Authorization": f"Bearer {login_as_teacher}"}
    CREATE_KLASSES_URL = "/api/v1/klass/create"
    URL = "/api/v1/klass"

    payload = [
        {"name": "Aula 1", "video": "url1111111111111111111111", "description": "desc111111111111111111111111111", "course_id": 0},
        {"name": "Aula 2", "video": "url211111111111111111111", "description": "desc1111111111111111111111111111111111111", "course_id": 0},
        {"name": "Aula 3", "video": "url31111111111111111111", "description": "desc311111111111111111111111111", "course_id": 0},
        {"name": "Aula 4", "video": "url31111111111111111111", "description": "desc311111111111111111111111111", "course_id": 0},
    ]

    response = client.post(
        CREATE_KLASSES_URL,
        json=payload,
        headers=teacher_auth
    )


    assert response.status_code == status.HTTP_201_CREATED

    response = client.get(url=URL, headers=teacher_auth)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert len(data) == len(payload)