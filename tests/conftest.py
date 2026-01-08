import pytest
from sqlmodel import SQLModel, create_engine, Session, StaticPool
from fastapi.testclient import TestClient
from app.main import app
from app.db.database import get_db
from app.db.database import Base




@pytest.fixture(name="session")
def session_fixture():
    # O StaticPool garante que todos os fios (threads) usem a mesma conexão na memória
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    Base.metadata.create_all(bind=engine)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

@pytest.fixture(name="client")
def client_fixture(session):
    # Sobrescrevemos a dependência do banco real pela sessão de teste
    def get_session_override():
        return session
    
    app.dependency_overrides[get_db] = get_session_override
    client = TestClient(app)
    yield client
    # Limpa as sobrescrições após o teste
    app.dependency_overrides.clear()