import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from domain.models.persona import Persona
from domain.models.roles import DatosAsociado
from application.auth_service import AuthService
from infrastructure.auth_repository import AuthRepository

def test_crud_asociados(client: TestClient, session: Session, usuario_prueba):
    auth_service = AuthService(AuthRepository(session))
    token = auth_service.crear_token_acceso({"sub": str(usuario_prueba.id)})
    headers = {"Authorization": f"Bearer {token}"}

    # 1. Crear persona base
    persona = Persona(
        numero_identificacion="ASOC123456",
        nombre_completo="Asociado Test User",
        correo_electronico="asociado@test.com",
        activo=True
    )
    session.add(persona)
    session.commit()
    session.refresh(persona)

    # 2. Crear asociado POST /asociados/
    res_post = client.post(
        "/asociados/",
        json={
            "id_persona": persona.id,
            "metodo_pago": "Transferencia",
            "estado_membresia": "Activo",
            "estado_pago": "Al dia",
            "autoriza_whatsapp": True
        },
        headers=headers
    )
    assert res_post.status_code == 201
    data_post = res_post.json()
    asociado_id = data_post["id"]
    assert data_post["id_persona"] == persona.id
    assert data_post["metodo_pago"] == "Transferencia"
    assert data_post["autoriza_whatsapp"] is True

    # 3. Intentar duplicar asociado para la misma persona (debe fallar 400)
    res_dup = client.post(
        "/asociados/",
        json={"id_persona": persona.id},
        headers=headers
    )
    assert res_dup.status_code == 400

    # 4. GET /asociados/
    res_get_all = client.get("/asociados/", headers=headers)
    assert res_get_all.status_code == 200
    assert len(res_get_all.json()) >= 1

    # 5. GET /asociados/{id}
    res_get = client.get(f"/asociados/{asociado_id}", headers=headers)
    assert res_get.status_code == 200
    assert res_get.json()["id"] == asociado_id

    # 6. PATCH /asociados/{id}
    res_patch = client.patch(
        f"/asociados/{asociado_id}",
        json={"estado_pago": "Moroso"},
        headers=headers
    )
    assert res_patch.status_code == 200
    assert res_patch.json()["estado_pago"] == "Moroso"
    assert res_patch.json()["metodo_pago"] == "Transferencia"  # Cero pérdida de datos

    # 7. DELETE /asociados/{id}
    res_del = client.delete(f"/asociados/{asociado_id}", headers=headers)
    assert res_del.status_code == 204
