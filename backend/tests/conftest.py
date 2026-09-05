import os
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

import pytest
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool
from fastapi.testclient import TestClient

from domain.models import *
import domain.models as models
from main import app
from infrastructure.database import get_session
from domain.models.usuario import Usuario
import bcrypt

test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

@pytest.fixture(name="session")
def session_fixture():
    SQLModel.metadata.drop_all(test_engine)
    SQLModel.metadata.create_all(test_engine)
    with Session(test_engine) as session:
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
    hashed = bcrypt.hashpw("password123".encode('utf-8'), bcrypt.gensalt(12)).decode('utf-8')
    usuario = Usuario(
        email="test@asocolgi.org",
        hashed_password=hashed,
        activo=True,
        es_admin=True
    )
    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    return usuario
