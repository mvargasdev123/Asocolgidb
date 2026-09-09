import pytest
from fastapi.testclient import TestClient

def test_expedientes_reglas_negocio(client: TestClient, usuario_prueba):
    # Login
    login_res = client.post("/auth/login", data={"username": "test@asocolgi.org", "password": "password123"})
    assert login_res.status_code == 200
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 1. Crear persona NO voluntaria (solo asociado o externo)
    p_externo = {
        "identificacion": {
            "tipo_documento": "DNI",
            "numero_identificacion": "11111111A",
            "nacionalidad": "Colombiana"
        },
        "datos_personales": {
            "nombre_completo": "Carlos Externo",
            "fecha_nacimiento": "1995-05-05",
            "ciudad": "Madrid"
        },
        "es_voluntario": False
    }
    res_ext = client.post("/personas/", json=p_externo, headers=headers)
    assert res_ext.status_code == 201
    id_externo = res_ext.json()["id"]

    # Crear expediente a persona (se autogenera rol voluntario si es necesario) -> 201 Created
    exp_payload = {
        "tipo_tramite": "Arraigo Social",
        "fecha_presentacion": "2026-09-01"
    }
    res_bad = client.post(f"/personas/{id_externo}/expedientes", json=exp_payload, headers=headers)
    assert res_bad.status_code == 201

    # 2. Crear persona Voluntaria
    p_voluntario = {
        "identificacion": {
            "tipo_documento": "NIE",
            "numero_identificacion": "Y1234567Z",
            "nacionalidad": "Venezolana"
        },
        "datos_personales": {
            "nombre_completo": "Ana Voluntaria",
            "fecha_nacimiento": "1992-02-02",
            "ciudad": "Barcelona"
        },
        "es_voluntario": True,
        "datos_voluntario": {
            "cargo": "Asesora Legal",
            "campo_accion": "Derechos Humanos",
            "tipo": "Interno",
            "horas_semana": 10
        }
    }
    res_vol = client.post("/personas/", json=p_voluntario, headers=headers)
    assert res_vol.status_code == 201
    id_voluntario = res_vol.json()["id"]

    # Crear 1er Expediente para la voluntaria -> 201 Created
    res_exp1 = client.post(f"/personas/{id_voluntario}/expedientes", json=exp_payload, headers=headers)
    assert res_exp1.status_code == 201
    data_exp1 = res_exp1.json()
    assert data_exp1["id_persona"] == id_voluntario
    assert data_exp1["estado"] == "En tramite"
    assert data_exp1["numero_registro"] == "EXP-2026-0002"
    assert data_exp1["persona"]["nombre_completo"] == "Ana Voluntaria"
    id_exp1 = data_exp1["id"]

    # Intentar crear un 2do expediente con el 1ro en "En tramite" -> 400 Bad Request
    exp_payload2 = {
        "tipo_tramite": "Renovación Asilo",
        "fecha_presentacion": "2026-09-05"
    }
    res_exp_dup = client.post(f"/personas/{id_voluntario}/expedientes", json=exp_payload2, headers=headers)
    assert res_exp_dup.status_code == 400
    assert "expediente en trámite" in res_exp_dup.json()["detail"]

    # 3. Cambiar estado del 1er expediente a "Favorable" (inactivo)
    patch_payload = {"estado": "Favorable"}
    res_patch = client.patch(f"/expedientes/{id_exp1}", json=patch_payload, headers=headers)
    assert res_patch.status_code == 200
    assert res_patch.json()["estado"] == "Favorable"

    # 4. Ahora SÍ debe permitir crear un 2do expediente
    res_exp2 = client.post(f"/personas/{id_voluntario}/expedientes", json=exp_payload2, headers=headers)
    assert res_exp2.status_code == 201
    data_exp2 = res_exp2.json()
    assert data_exp2["estado"] == "En tramite"
    assert data_exp2["numero_registro"] == "EXP-2026-0003"
    id_exp2 = data_exp2["id"]

    # 5. Probar endpoints de consulta
    # GET /expedientes/
    res_all = client.get("/expedientes/", headers=headers)
    assert res_all.status_code == 200
    assert len(res_all.json()) == 3

    # GET /expedientes/?estado=Favorable
    res_fav = client.get("/expedientes/?estado=Favorable", headers=headers)
    assert res_fav.status_code == 200
    assert len(res_fav.json()) == 1
    assert res_fav.json()[0]["id"] == id_exp1

    # GET /expedientes/{id_expediente}
    res_get_by_id = client.get(f"/expedientes/{id_exp2}", headers=headers)
    assert res_get_by_id.status_code == 200
    assert res_get_by_id.json()["numero_registro"] == "EXP-2026-0003"

    # DELETE /expedientes/{id_expediente}
    res_del = client.delete(f"/expedientes/{id_exp1}", headers=headers)
    assert res_del.status_code == 204
