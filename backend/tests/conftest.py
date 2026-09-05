import pytest
from sqlmodel import SQLModel, Session, create_engine
from fastapi.testclient import TestClient

# Sobreescribimos la URL para asegurar usar memory DB
import os
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from main import app
from infrastructure.database import engine, get_session
from domain.models.usuario import Usuario
from application.auth_service import pwd_context

@pytest.fixture(name="session")
def session_fixture():
    # Reinicia las tablas en cada test
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session
    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

@pytest.fixture(name="usuario_prueba")
def usuario_prueba_fixture(session: Session):
    usuario = Usuario(
        email="admin@test.com",
        hashed_password=pwd_context.hash("password123"),
        activo=True,
        es_admin=True
    )
    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    return usuario
