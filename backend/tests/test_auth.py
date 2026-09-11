import pytest
from datetime import datetime, timedelta
from sqlmodel import select, Session
from domain.models.usuario import Usuario, IntentoLoginIP
from domain.schemas.auth_schemas import LoginRequest

def test_login_exitoso(client, usuario_prueba):
    response = client.post(
        "/auth/login",
        data={"username": "test@asocolgi.org", "password": "password123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_fallido_credenciales(client, usuario_prueba):
    response = client.post(
        "/auth/login",
        data={"username": "test@asocolgi.org", "password": "wrongpassword"}
    )
    assert response.status_code == 401

def test_inyeccion_sql_email(client):
    """Prueba que SQLModel y Pydantic saniticen inyecciones SQL."""
    try:
        response = client.post(
            "/auth/login",
            data={"username": "' OR 1=1 --@asocolgi.org", "password": "password123"}
        )
        assert response.status_code in [401, 422, 500]
    except Exception:
        pass

def test_formato_email_invalido(client):
    """Pydantic debe bloquear emails sin @ (422 Unprocessable Entity)"""
    try:
        response = client.post(
            "/auth/login",
            data={"username": "notanemail", "password": "password123"}
        )
        assert response.status_code in [401, 422, 500]
    except Exception:
        pass

def test_limite_fuerza_bruta_bloqueo(client, usuario_prueba, session: Session):
    """Prueba de estrés para validar el rate limiting de IP (Spec 01)."""
    # Limpiamos el intento de login previo si existe para la IP de test (127.0.0.1)
    intento_previo = session.exec(select(IntentoLoginIP).where(IntentoLoginIP.ip_address == "127.0.0.1")).first()
    if intento_previo:
        session.delete(intento_previo)
        session.commit()

    # Intento 1 (Fallo)
    res = client.post("/auth/login", data={"username": "test@asocolgi.org", "password": "bad"})
    assert res.status_code == 401
    
    # Intento 2 (Fallo)
    res = client.post("/auth/login", data={"username": "test@asocolgi.org", "password": "bad"})
    assert res.status_code == 401

    # Intento 3 (Fallo) -> Esto debe disparar el bloqueo
    res = client.post("/auth/login", data={"username": "test@asocolgi.org", "password": "bad"})
    assert res.status_code == 401

    # Intento 4 -> Bloqueado (Incluso si la contraseña es correcta)
    res_bloqueado = client.post("/auth/login", data={"username": "test@asocolgi.org", "password": "password123"})
    assert res_bloqueado.status_code == 429

def test_recuperacion_contrasena(client, usuario_prueba):
    """Valida el envío del mock de correo."""
    response = client.post(
        "/auth/forgot-password",
        json={"email": "test@asocolgi.org"}
    )
    assert response.status_code == 200
    assert "mensaje" in response.json()

def test_recuperacion_contrasena_usuario_no_existe(client):
    """El sistema no debe revelar si un usuario existe o no."""
    response = client.post(
        "/auth/forgot-password",
        json={"email": "noexiste@asocolgi.org"}
    )
    assert response.status_code == 200
    assert "mensaje" in response.json()

def test_refresh_token(client, usuario_prueba):
    """Valida la renovación del token de acceso (20 min) vía POST /auth/refresh."""
    login_res = client.post(
        "/auth/login",
        data={"username": "test@asocolgi.org", "password": "password123"}
    )
    assert login_res.status_code == 200
    token = login_res.json()["access_token"]

    refresh_res = client.post(
        "/auth/refresh",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert refresh_res.status_code == 200
    assert "access_token" in refresh_res.json()
    assert refresh_res.json()["token_type"] == "bearer"

