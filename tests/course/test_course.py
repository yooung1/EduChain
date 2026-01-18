from fastapi import status

def test_create_course(client, login_as_teacher):
    headers = {"Authorization": f"Bearer {login_as_teacher}"}
    URL = "/api/v1/course/create"

    payload = {
        "name": "COMO CODAR BEM",
        "description": "ESTE CURSO VAI TE ENSINAR A CODAR DA MELHOR MANEIRA QUE EXISTE"
    }

    response = client.post(url=URL, json=payload, headers=headers)

    assert response.status_code == status.HTTP_201_CREATED


def test_create_course_with_no_permission(client, login_as_student):
    student_perm = {"Authorization": f"Bearer {login_as_student}"}

    URL = "/api/v1/course/create"

    payload = {
        "name": "COMO CODAR BEM",
        "description": "ESTE CURSO VAI TE ENSINAR A CODAR DA MELHOR MANEIRA QUE EXISTE"
    }


    response = client.post(url=URL, json=payload, headers=student_perm)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    response = client.post(url=URL, json=payload)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED



def test_get_course(client, login_as_admin, login_as_teacher):
    admin_perm = {"Authorization": f"Bearer {login_as_admin}"}
    teacher_perm = {"Authorization": f"Bearer {login_as_teacher}"}
    URL = "/api/v1/course"

    response = client.get(url=URL, headers=admin_perm)
    assert response.status_code == status.HTTP_200_OK


    response = client.get(url=URL, headers=teacher_perm)
    assert response.status_code == status.HTTP_200_OK



def test_get_course_with_no_permission(client, login_as_student):
    student_perm = {"Authorization": f"Bearer {login_as_student}"}
    URL = "/api/v1/course"

    response = client.get(url=URL, headers=student_perm)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


    response = client.get(url=URL)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_delete_course(client, login_as_admin):
    headers = {"Authorization": f"Bearer {login_as_admin}"}
    URL_CREATE = "/api/v1/course/create"
    URL = "/api/v1/course/delete/1"

    payload = {
        "name": "COMO CODAR BEM",
        "description": "ESTE CURSO VAI TE ENSINAR A CODAR DA MELHOR MANEIRA QUE EXISTE"
    }

    response = client.post(url=URL_CREATE, json=payload, headers=headers)

    assert response.status_code == status.HTTP_201_CREATED

    # Delete course
    response = client.delete(url=URL, headers=headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT

