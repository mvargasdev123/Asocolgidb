import pytest
from sqlmodel import Session, select
from domain.models.persona import Persona
from domain.models.catalogos import Ciudad, Nacionalidad
from domain.models.roles import DatosAsociado, DatosVoluntario
from domain.schemas.persona_schemas import PersonaCreateRequest

def get_auth_headers(client, usuario_prueba):
    login_res = client.post("/auth/login", data={"username": "test@asocolgi.org", "password": "password123"})
    token = login_res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_guardar_usuario_exitoso_y_catalogos(client, usuario_prueba, session: Session):
    headers = get_auth_headers(client, usuario_prueba)
    payload = {
        "identificacion": {
            "tipo_documento": "DNI",
            "numero_identificacion": "12345678A",
            "nacionalidad": "Colombia"
        },
        "datos_personales": {
            "nombre_completo": "Juan Perez",
            "ciudad": "Cali"
        },
        "es_asociado": False,
        "es_voluntario": False
    }

    response = client.post("/personas/", json=payload, headers=headers)
    assert response.status_code == 201
    
    # 1. Validar que la persona existe
    persona_db = session.exec(select(Persona).where(Persona.numero_identificacion == "12345678A")).first()
    assert persona_db is not None
    assert persona_db.nombre_completo == "Juan Perez"
    
    # 2. Validar que el contador se inicializó en 1
    assert persona_db.contador_visitas == 1

    # 3. Validar Catálogos Dinámicos (Event-driven logic)
    ciudad_db = session.exec(select(Ciudad).where(Ciudad.nombre == "Cali")).first()
    assert ciudad_db is not None
    assert persona_db.id_ciudad == ciudad_db.id
    
    nacionalidad_db = session.exec(select(Nacionalidad).where(Nacionalidad.nombre == "Colombia")).first()
    assert nacionalidad_db is not None
    assert persona_db.id_nacionalidad == nacionalidad_db.id

def test_guardar_usuario_duplicado_409(client, usuario_prueba, session: Session):
    """Valida Spec 02: Rechazo por Documento Duplicado (409 Conflict)"""
    headers = get_auth_headers(client, usuario_prueba)
    payload = {
        "identificacion": {
            "numero_identificacion": "99999999Z",
        },
        "datos_personales": {
            "nombre_completo": "Maria Lopez",
        }
    }
    
    # Primer registro exitoso
    res1 = client.post("/personas/", json=payload, headers=headers)
    assert res1.status_code == 201
    
    # Segundo registro con el mismo documento
    res2 = client.post("/personas/", json=payload, headers=headers)
    assert res2.status_code == 409
    assert res2.json()["detail"] == "Esta persona ya existe"

def test_falla_por_falta_de_datos_obligatorios(client, usuario_prueba):
    """Asegura que la API rechace payload si faltan campos obligatorios (422)"""
    headers = get_auth_headers(client, usuario_prueba)
    payload = {
        "identificacion": {
            # Falta numero_identificacion
        },
        "datos_personales": {
            # Falta nombre_completo
        }
    }
    
    response = client.post("/personas/", json=payload, headers=headers)
    assert response.status_code == 422 # Error de validación de Pydantic

def test_fechas_invalidas_rechazadas_422(client, usuario_prueba):
    """Verifica que Pydantic rechace strings malformados para fechas."""
    headers = get_auth_headers(client, usuario_prueba)
    payload = {
        "identificacion": {
            "numero_identificacion": "ABC123456",
        },
        "datos_personales": {
            "nombre_completo": "Carlos Perez",
            "fecha_nacimiento": "fecha-invalida-no-soy-iso"
        }
    }
    response = client.post("/personas/", json=payload, headers=headers)
    assert response.status_code == 422

def test_catalogo_espacios_blanco_ignorados(client, usuario_prueba, session: Session):
    """Verifica que strings vacíos o con espacios no generen basura en catálogos."""
    headers = get_auth_headers(client, usuario_prueba)
    payload = {
        "identificacion": {
            "numero_identificacion": "X888888",
            "nacionalidad": "   " # String vacío/espacios
        },
        "datos_personales": {
            "nombre_completo": "Test Espacios",
            "ciudad": "" # String vacío
        }
    }
    
    response = client.post("/personas/", json=payload, headers=headers)
    assert response.status_code == 201
    
    persona_db = session.exec(select(Persona).where(Persona.numero_identificacion == "X888888")).first()
    
    # Debe ser nulo en base de datos, no un id apuntando a "  "
    assert persona_db.id_nacionalidad is None
    assert persona_db.id_ciudad is None

def test_maximo_viable_roles_multiples(client, usuario_prueba, session: Session):
    """Prueba de estrés relacional: Un usuario que es Asociado y Voluntario al mismo tiempo."""
    headers = get_auth_headers(client, usuario_prueba)
    payload = {
        "identificacion": {
            "numero_identificacion": "MULTI999",
        },
        "datos_personales": {
            "nombre_completo": "Multi Rol User",
        },
        "es_asociado": True,
        "datos_asociado": {
            "metodo_pago": "Banco",
            "estado_membresia": "Activo"
        },
        "es_voluntario": True,
        "datos_voluntario": {}
    }
    
    response = client.post("/personas/", json=payload, headers=headers)
    assert response.status_code == 201
    
    # Validar transaccionalidad de roles 1:1
    persona_db = session.exec(select(Persona).where(Persona.numero_identificacion == "MULTI999")).first()
    assert persona_db is not None
    
    asociado_db = session.exec(select(DatosAsociado).where(DatosAsociado.id_persona == persona_db.id)).first()
    assert asociado_db is not None
    assert asociado_db.metodo_pago == "Banco"
    
    voluntario_db = session.exec(select(DatosVoluntario).where(DatosVoluntario.id_persona == persona_db.id)).first()
    assert voluntario_db is not None

def test_actualizacion_completa_persona(client, usuario_prueba, session: Session):
    """Valida la actualización completa de campos (correo, genero, direccion, catalogos)."""
    headers = get_auth_headers(client, usuario_prueba)
    payload_creacion = {
        "identificacion": {
            "tipo_documento": "NIF/NIE",
            "numero_identificacion": "UPDATE123",
            "nacionalidad": "España"
        },
        "datos_personales": {
            "nombre_completo": "Original Name",
            "correo_electronico": "original@test.com"
        }
    }
    res_crear = client.post("/personas/", json=payload_creacion, headers=headers)
    assert res_crear.status_code == 201
    persona_id = res_crear.json()["id"]

    # Validar que los catálogos devuelven sus nombres
    assert res_crear.json()["tipo_documento"] == "NIF/NIE"
    assert res_crear.json()["nacionalidad"] == "España"

    # Actualización parcial (PATCH)
    payload_patch = {
        "identificacion": {
            "tipo_documento": "DNI",
            "nacionalidad": "Colombia"
        },
        "datos_personales": {
            "nombre_completo": "Updated Name",
            "correo_electronico": "actualizado@test.com",
            "genero": "H",
            "direccion_residencia": "Calle Falsa 123",
            "codigo_postal": "28001"
        },
        "situacion_social": {
            "situacion_admin": "Regular",
            "unidad_familiar": 3
        }
    }
    res_patch = client.patch(f"/personas/{persona_id}", json=payload_patch, headers=headers)
    assert res_patch.status_code == 200
    data_updated = res_patch.json()

    assert data_updated["nombre_completo"] == "Updated Name"
    assert data_updated["correo_electronico"] == "actualizado@test.com"
    assert data_updated["genero"] == "H"
    assert data_updated["direccion_residencia"] == "Calle Falsa 123"
    assert data_updated["codigo_postal"] == "28001"
    assert data_updated["tipo_documento"] == "DNI"
    assert data_updated["nacionalidad"] == "Colombia"
    assert data_updated["situacion_admin"] == "Regular"
    assert data_updated["unidad_familiar"] == 3
