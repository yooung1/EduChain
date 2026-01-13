import pytest
from sqlmodel import SQLModel, create_engine, Session, StaticPool
from fastapi.testclient import TestClient
from app.main import app
from app.db.database import get_db
from app.models.user_model import User
from app.user.schemas import UserRole
from app.auth.service import get_password_hash
from fastapi import status
from tests.constants import (
    # Admin
    ADMIN_FIRST_NAME,
    ADMIN_LASTNAME,
    ADMIN_USERNAME,
    ADMIN_EMAIL,
    ADMIN_PASSWORD,
    # Student
    STUDENT_FIRST_NAME,
    STUDENT_LASTNAME,
    STUDENT_USERNAME,
    STUDENT_EMAIL,
    STUDENT_PASSWORD,
    # Teacher
    TEACHER_FIRST_NAME,
    TEACHER_LASTNAME,
    TEACHER_USERNAME,
    TEACHER_EMAIL,
    TEACHER_PASSWORD
)



@pytest.fixture(scope="session", name="engine")
def engine_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    
    SQLModel.metadata.create_all(engine)
    
    return engine


@pytest.fixture(name="session")
def session_fixture(engine):
    connection = engine.connect()
    
    transaction = connection.begin()

    session = Session(bind=connection)
    
    # CREATING ADMIN USER
    users_to_create = [
        User(
            first_name=ADMIN_FIRST_NAME,
            last_name=ADMIN_LASTNAME,
            username=ADMIN_USERNAME,
            email=ADMIN_EMAIL,
            hashed_password=get_password_hash(ADMIN_PASSWORD),
            role=UserRole.ADMIN
        ),
        User(
            first_name=STUDENT_FIRST_NAME,
            last_name=STUDENT_LASTNAME,
            username=STUDENT_USERNAME,
            email=STUDENT_EMAIL,
            hashed_password=get_password_hash(STUDENT_PASSWORD),
            role=UserRole.STUDENT
        ),
        User(
            first_name=TEACHER_FIRST_NAME,
            last_name=TEACHER_LASTNAME,
            username=TEACHER_USERNAME,
            email=TEACHER_EMAIL,
            hashed_password=get_password_hash(TEACHER_PASSWORD),
            role=UserRole.TEACHER
        )
    ]

    session.add_all(users_to_create)
    session.commit()

    yield session


    session.close()
    transaction.rollback() 
    connection.close()


@pytest.fixture(name="client")
def client_fixture(session):
    def get_session_override():
        return session
    
    app.dependency_overrides[get_db] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

#TODO: ENVIAR TODAS ESSAS VARIAVEIS NO ARQUIVO DE CONSTANTES.PY -- variaveis de acesso, etc.
@pytest.fixture(name="login_as_admin")
def login_as_admin_fixture(client):
    user_data = {
        "username": ADMIN_USERNAME,
        "password": ADMIN_PASSWORD,
    }
    response = client.post("/api/v1/auth/login", data=user_data)
    assert response.status_code == status.HTTP_202_ACCEPTED
    return response.json()["access_token"]


@pytest.fixture(name="login_as_student")
def login_as_student_fixture(client):
    user_data = {
        "username": STUDENT_USERNAME,
        "password": STUDENT_PASSWORD,
    }
    response = client.post("/api/v1/auth/login", data=user_data)
    assert response.status_code == status.HTTP_202_ACCEPTED
    return response.json()["access_token"]


@pytest.fixture(name="login_as_teacher")
def login_as_teacher_fixture(client):
    user_data = {
        "username": TEACHER_USERNAME,
        "password": TEACHER_PASSWORD,
    }
    response = client.post("/api/v1/auth/login", data=user_data)
    assert response.status_code == status.HTTP_202_ACCEPTED
    return response.json()["access_token"]