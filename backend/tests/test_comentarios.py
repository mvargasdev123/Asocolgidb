import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

def test_crud_comentarios(client: TestClient, usuario_prueba):
    # 1. Login para obtener token
    login_res = client.post("/auth/login", data={"username": "test@asocolgi.org", "password": "password123"})
    assert login_res.status_code == 200
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Crear persona de prueba
    persona_payload = {
        "identificacion": {
            "tipo_documento": "DNI",
            "numero_identificacion": "99887766A",
            "nacionalidad": "Española"
        },
        "datos_personales": {
            "nombre_completo": "Prueba Comentarios",
            "fecha_nacimiento": "1990-01-01",
            "ciudad": "Madrid"
        }
    }
    res_persona = client.post("/personas/", json=persona_payload, headers=headers)
    assert res_persona.status_code == 201
    id_persona = res_persona.json()["id"]

    # 3. Crear comentario (POST)
    comentario_payload = {
        "texto": "Comentario inicial de bienvenida",
        "tipo": "Persona"
    }
    res_post = client.post(f"/personas/{id_persona}/comentarios", json=comentario_payload, headers=headers)
    assert res_post.status_code == 201
    data_post = res_post.json()
    id_comentario = data_post["id"]
    assert data_post["texto"] == "Comentario inicial de bienvenida"
    assert data_post["tipo"] == "Persona"
    assert data_post["id_persona"] == id_persona
    fecha_original = data_post["fecha_creacion"]

    # 4. Obtener comentarios (GET)
    res_get = client.get(f"/personas/{id_persona}/comentarios", headers=headers)
    assert res_get.status_code == 200
    list_get = res_get.json()
    assert len(list_get) == 1
    assert list_get[0]["id"] == id_comentario

    # 5. Actualizar comentario (PATCH) - Texto y Tipo
    patch_payload = {
        "texto": "Comentario modificado",
        "tipo": "Voluntario"
    }
    res_patch = client.patch(f"/comentarios/{id_comentario}", json=patch_payload, headers=headers)
    assert res_patch.status_code == 200
    data_patch = res_patch.json()
    assert data_patch["texto"] == "Comentario modificado"
    assert data_patch["tipo"] == "Voluntario"
    # Verificar que la fecha_creacion NO haya cambiado
    assert data_patch["fecha_creacion"] == fecha_original

    # 6. Eliminar comentario (DELETE)
    res_del = client.delete(f"/comentarios/{id_comentario}", headers=headers)
    assert res_del.status_code == 204

    # 7. Verificar que ya no existe (GET)
    res_get_empty = client.get(f"/personas/{id_persona}/comentarios", headers=headers)
    assert res_get_empty.status_code == 200
    assert len(res_get_empty.json()) == 0
