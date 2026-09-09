import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from domain.models.persona import Persona
from domain.models.roles import DatosVoluntario
from application.auth_service import AuthService
from infrastructure.auth_repository import AuthRepository

def test_crud_voluntarios(client: TestClient, session: Session, usuario_prueba):
    auth_service = AuthService(AuthRepository(session))
    token = auth_service.crear_token_acceso({"sub": str(usuario_prueba.id)})
    headers = {"Authorization": f"Bearer {token}"}

    # 1. Crear persona base
    persona = Persona(
        numero_identificacion="VOL123456",
        nombre_completo="Voluntario Test User",
        correo_electronico="voluntario@test.com",
        activo=True
    )
    session.add(persona)
    session.commit()
    session.refresh(persona)

    # 2. Crear voluntario POST /voluntarios/
    res_post = client.post(
        "/voluntarios/",
        json={
            "id_persona": persona.id,
            "cargo": "Coordinador Legal",
            "campo_accion": "Derechos Humanos",
            "tipo": "Presencial",
            "horas_semana": 10,
            "carta_compromiso_firmada": True
        },
        headers=headers
    )
    assert res_post.status_code == 201
    data_post = res_post.json()
    voluntario_id = data_post["id"]
    assert data_post["id_persona"] == persona.id
    assert data_post["cargo"] == "Coordinador Legal"
    assert data_post["horas_semana"] == 10

    # 3. Intentar duplicar voluntario para la misma persona (debe fallar 400)
    res_dup = client.post(
        "/voluntarios/",
        json={"id_persona": persona.id},
        headers=headers
    )
    assert res_dup.status_code == 400

    # 4. GET /voluntarios/
    res_get_all = client.get("/voluntarios/", headers=headers)
    assert res_get_all.status_code == 200
    assert len(res_get_all.json()) >= 1

    # 5. GET /voluntarios/{id}
    res_get = client.get(f"/voluntarios/{voluntario_id}", headers=headers)
    assert res_get.status_code == 200
    assert res_get.json()["id"] == voluntario_id

    # 6. PATCH /voluntarios/{id}
    res_patch = client.patch(
        f"/voluntarios/{voluntario_id}",
        json={"horas_semana": 15},
        headers=headers
    )
    assert res_patch.status_code == 200
    assert res_patch.json()["horas_semana"] == 15
    assert res_patch.json()["cargo"] == "Coordinador Legal"  # Cero pérdida de datos

    # 7. DELETE /voluntarios/{id}
    res_del = client.delete(f"/voluntarios/{voluntario_id}", headers=headers)
    assert res_del.status_code == 204
