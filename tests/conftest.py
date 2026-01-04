import pytest
from sqlmodel import SQLModel, create_engine, Session
from app.api.main import app
from app.database.database import get_db
from fastapi.testclient import TestClient

from app.models.user_registration_model import User 


# TODO: tem alguns erros q precisam ser ajustados
@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

@pytest.fixture
def client(session):
    app.dependency_overrides[get_db] = lambda: session
    yield TestClient(app)
    app.dependency_overrides.clear()