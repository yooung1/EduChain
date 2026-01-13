import pytest
from sqlmodel import SQLModel, create_engine, Session, StaticPool
from fastapi.testclient import TestClient
from app.main import app
from app.db.database import get_db
from app.models.user_model import User
from app.user.schemas import UserRole
from app.auth.service import get_password_hash
from fastapi import status


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
    admin_user = User(
        first_name="super_admin",
        last_name="super_admin",
        username="super_admin",
        email="teste_teste@gmail.com",
        hashed_password=get_password_hash("senha_super_admin"),
        role=UserRole.ADMIN
    )
    session.add(admin_user)
    session.commit()
    session.refresh(admin_user)

    # CREATING STUDENT USER
    student_user = User(
        first_name="student",
        last_name="student",
        username="student",
        email="student@gmail.com",
        hashed_password=get_password_hash("senha_student"),
        role=UserRole.STUDENT
    )
    session.add(student_user)
    session.commit()
    session.refresh(student_user)


    # CREATING TEACHER USER
    teacher_user = User(
        first_name="teacher",
        last_name="teacher",
        username="teacher",
        email="teacher@gmail.com",
        hashed_password=get_password_hash("senha_teacher"),
        role=UserRole.TEACHER
    )
    session.add(teacher_user)
    session.commit()
    session.refresh(teacher_user)


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
        "username": "super_admin",
        "password": "senha_super_admin",
    }
    response = client.post("/api/v1/auth/login", data=user_data)
    assert response.status_code == status.HTTP_202_ACCEPTED
    return response.json()["access_token"]


@pytest.fixture(name="login_as_student")
def login_as_student_fixture(client):
    user_data = {
        "username": "student",
        "password": "senha_student",
    }
    response = client.post("/api/v1/auth/login", data=user_data)
    assert response.status_code == status.HTTP_202_ACCEPTED
    return response.json()["access_token"]


@pytest.fixture(name="login_as_teacher")
def login_as_teacher_fixture(client):
    user_data = {
        "username": "teacher",
        "password": "senha_teacher",
    }
    response = client.post("/api/v1/auth/login", data=user_data)
    assert response.status_code == status.HTTP_202_ACCEPTED
    return response.json()["access_token"]