import pytest
from fastapi.testclient import TestClient

def test_metrics_dashboard_y_morosos(client: TestClient, usuario_prueba):
    login_res = client.post("/auth/login", data={"username": "test@asocolgi.org", "password": "password123"})
    assert login_res.status_code == 200
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Crear Asociado Moroso
    asociado_payload = {
        "identificacion": {
            "tipo_documento": "DNI",
            "numero_identificacion": "88888888M",
            "nacionalidad": "Colombiana"
        },
        "datos_personales": {
            "nombre_completo": "Juan Moroso",
            "fecha_nacimiento": "1985-04-12",
            "ciudad": "Madrid"
        },
        "es_asociado": True,
        "datos_asociado": {
            "estado_pago": "Moroso",
            "estado_membresia": "Activo"
        }
    }
    client.post("/personas/", json=asociado_payload, headers=headers)

    # GET /metrics
    res_metrics = client.get("/metrics", headers=headers)
    assert res_metrics.status_code == 200
    data = res_metrics.json()
    assert data["total_personas"] >= 1
    assert data["asociados_morosos_count"] >= 1
    assert "Asociados" in data["distribucion_roles"]
    assert "Regular" in data["situacion_administrativa"]
    assert "Hombres" in data["demografia_genero"]

    # GET /metrics/asociados-morosos-pendientes
    res_split = client.get("/metrics/asociados-morosos-pendientes", headers=headers)
    assert res_split.status_code == 200
    split_data = res_split.json()
    assert "morosos" in split_data
    assert "pendientes" in split_data
    assert len(split_data["morosos"]) >= 1
    assert split_data["morosos"][0]["nombre_completo"] == "Juan Moroso"
