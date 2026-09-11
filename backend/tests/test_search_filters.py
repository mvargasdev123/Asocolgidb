import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session
from domain.models.persona import Persona
from domain.models.roles import DatosAsociado, DatosVoluntario
from application.auth_service import AuthService
from infrastructure.auth_repository import AuthRepository

def test_busqueda_y_filtros_personas(client: TestClient, session: Session, usuario_prueba):
    auth_service = AuthService(AuthRepository(session))
    token = auth_service.crear_token_acceso({"sub": str(usuario_prueba.id)})
    headers = {"Authorization": f"Bearer {token}"}

    # 1. Crear personas de prueba
    p1 = Persona(
        numero_identificacion="11111111A",
        nombre_completo="Carlos Rodriguez",
        genero="Hombre",
        situacion_admin="Regular",
        activo=True
    )
    p2 = Persona(
        numero_identificacion="22222222B",
        nombre_completo="Maria Fernandez",
        genero="Mujer",
        situacion_admin="Irregular",
        activo=True
    )
    p3 = Persona(
        numero_identificacion="33333333C",
        nombre_completo="Juan Perez",
        genero="Hombre",
        situacion_admin="En tramite",
        activo=True
    )

    session.add_all([p1, p2, p3])
    session.commit()

    # Asociar p1 como Asociado y p2 como Voluntario
    aso1 = DatosAsociado(id_persona=p1.id, estado_membresia="Activo")
    vol2 = DatosVoluntario(id_persona=p2.id, cargo="Coordinador")
    p4 = Persona(
        numero_identificacion="44444444D",
        nombre_completo="Alex Rivera",
        genero="LGBTI",
        situacion_admin="Regular",
        activo=True
    )

    session.add_all([p1, p2, p3, p4])
    session.add_all([aso1, vol2])
    session.commit()

    # 2. Prueba Búsqueda por texto (nombre / doc)
    res = client.get("/personas/?q=Carlos", headers=headers)
    assert res.status_code == 200
    items = res.json()
    assert len(items) == 1
    assert items[0]["nombre_completo"] == "Carlos Rodriguez"

    res_doc = client.get("/personas/?q=22222222B", headers=headers)
    assert res_doc.status_code == 200
    assert len(res_doc.json()) == 1
    assert res_doc.json()[0]["nombre_completo"] == "Maria Fernandez"

    # 3. Prueba Filtro por Género (Hombres vs Mujeres vs LGBTI)
    res_hombres = client.get("/personas/?genero=Hombres", headers=headers)
    assert res_hombres.status_code == 200
    nombres_h = [p["nombre_completo"] for p in res_hombres.json()]
    assert "Carlos Rodriguez" in nombres_h
    assert "Juan Perez" in nombres_h
    assert "Maria Fernandez" not in nombres_h

    res_mujeres = client.get("/personas/?genero=Mujeres", headers=headers)
    assert res_mujeres.status_code == 200
    nombres_m = [p["nombre_completo"] for p in res_mujeres.json()]
    assert "Maria Fernandez" in nombres_m
    assert "Carlos Rodriguez" not in nombres_m

    res_lgbti = client.get("/personas/?genero=LGBTI", headers=headers)
    assert res_lgbti.status_code == 200
    nombres_lgbt = [p["nombre_completo"] for p in res_lgbti.json()]
    assert "Alex Rivera" in nombres_lgbt
    assert "Carlos Rodriguez" not in nombres_lgbt

    # 4. Prueba Filtro por Rol (Asociados, Voluntarios, Externos)
    res_asoc = client.get("/personas/?rol=Asociados", headers=headers)
    assert res_asoc.status_code == 200
    assert len(res_asoc.json()) == 1
    assert res_asoc.json()[0]["nombre_completo"] == "Carlos Rodriguez"

    res_vol = client.get("/personas/?rol=Voluntarios", headers=headers)
    assert res_vol.status_code == 200
    assert len(res_vol.json()) == 1
    assert res_vol.json()[0]["nombre_completo"] == "Maria Fernandez"

    res_ext = client.get("/personas/?rol=Externos", headers=headers)
    assert res_ext.status_code == 200
    nombres_ext = [p["nombre_completo"] for p in res_ext.json()]
    assert "Juan Perez" in nombres_ext
    assert "Alex Rivera" in nombres_ext

    # 5. Prueba Filtro por Situación Administrativa (Regulares, Irregulares, En trámite)
    res_reg = client.get("/personas/?situacion_admin=Regulares", headers=headers)
    assert res_reg.status_code == 200
    assert any(p["nombre_completo"] == "Carlos Rodriguez" for p in res_reg.json())

    res_irreg = client.get("/personas/?situacion_admin=Irregulares", headers=headers)
    assert res_irreg.status_code == 200
    assert any(p["nombre_completo"] == "Maria Fernandez" for p in res_irreg.json())

    res_tramite = client.get("/personas/?situacion_admin=En trámite", headers=headers)
    assert res_tramite.status_code == 200
    assert any(p["nombre_completo"] == "Juan Perez" for p in res_tramite.json())

    # 6. Prueba Filtros Combinados (Asociados + Regular)
    res_combo = client.get("/personas/?rol=Asociados&situacion_admin=Regulares", headers=headers)
    assert res_combo.status_code == 200
    assert len(res_combo.json()) == 1
    assert res_combo.json()[0]["nombre_completo"] == "Carlos Rodriguez"

