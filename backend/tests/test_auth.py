import pytest
from datetime import datetime, timedelta
from sqlmodel import select, Session
from domain.models.usuario import Usuario, IntentoLoginIP
from domain.schemas.auth_schemas import LoginRequest

def test_login_exitoso(client, usuario_prueba):
    response = client.post(
        "/auth/login",
        json={"email": "test@asocolgi.org", "password": "password123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_fallido_credenciales(client, usuario_prueba):
    response = client.post(
        "/auth/login",
        json={"email": "test@asocolgi.org", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Correo o contraseña incorrectos"

def test_inyeccion_sql_email(client):
    """Prueba que SQLModel y Pydantic saniticen inyecciones SQL."""
    response = client.post(
        "/auth/login",
        json={"email": "' OR 1=1 --@asocolgi.org", "password": "password123"}
    )
    # Como es un correo inválido estructuralmente según Pydantic (debido a espacios o no encontrarlo en DB)
    # Debería devolver 401 o 422
    assert response.status_code in [401, 422]

def test_formato_email_invalido(client):
    """Pydantic debe bloquear emails sin @ (422 Unprocessable Entity)"""
    response = client.post(
        "/auth/login",
        json={"email": "notanemail", "password": "password123"}
    )
    assert response.status_code == 422

def test_limite_fuerza_bruta_bloqueo(client, usuario_prueba, session: Session):
    """Prueba de estrés para validar el rate limiting de IP (Spec 01)."""
    # Limpiamos el intento de login previo si existe para la IP de test (127.0.0.1)
    intento_previo = session.exec(select(IntentoLoginIP).where(IntentoLoginIP.ip_address == "127.0.0.1")).first()
    if intento_previo:
        session.delete(intento_previo)
        session.commit()

    # Intento 1 (Fallo)
    res = client.post("/auth/login", json={"email": "test@asocolgi.org", "password": "bad"})
    assert res.status_code == 401
    
    # Intento 2 (Fallo)
    res = client.post("/auth/login", json={"email": "test@asocolgi.org", "password": "bad"})
    assert res.status_code == 401

    # Intento 3 (Fallo) -> Esto debe disparar el bloqueo
    res = client.post("/auth/login", json={"email": "test@asocolgi.org", "password": "bad"})
    assert res.status_code == 401

    # Intento 4 -> Bloqueado (Incluso si la contraseña es correcta)
    res_bloqueado = client.post("/auth/login", json={"email": "test@asocolgi.org", "password": "password123"})
    assert res_bloqueado.status_code == 429
    assert "Demasiados intentos fallidos" in res_bloqueado.json()["detail"]

def test_recuperacion_contrasena(client, usuario_prueba):
    """Valida el envío del mock de correo."""
    response = client.post(
        "/auth/forgot-password",
        json={"email": "test@asocolgi.org"}
    )
    assert response.status_code == 200
    # Validar la regla de Spec 01: El correo debe enviarse al central, no al usuario
    assert response.json()["message"] == "Se ha enviado un correo con instrucciones a asocolgibasededatos@gmail.com"

def test_recuperacion_contrasena_usuario_no_existe(client):
    """El sistema no debe revelar si un usuario existe o no."""
    response = client.post(
        "/auth/forgot-password",
        json={"email": "noexiste@asocolgi.org"}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Se ha enviado un correo con instrucciones a asocolgibasededatos@gmail.com"
