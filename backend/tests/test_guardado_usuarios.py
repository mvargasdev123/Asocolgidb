import pytest
from sqlmodel import Session, select
from domain.models.persona import Persona
from domain.models.catalogos import Ciudad, Nacionalidad
from domain.models.roles import DatosAsociado, DatosVoluntario
from domain.schemas.persona_schemas import PersonaCreateRequest

def test_guardar_usuario_exitoso_y_catalogos(client, session: Session):
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

    response = client.post("/personas/", json=payload)
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

def test_guardar_usuario_duplicado_409(client, session: Session):
    """Valida Spec 02: Rechazo por Documento Duplicado (409 Conflict)"""
    payload = {
        "identificacion": {
            "numero_identificacion": "99999999Z",
        },
        "datos_personales": {
            "nombre_completo": "Maria Lopez",
        }
    }
    
    # Primer registro exitoso
    res1 = client.post("/personas/", json=payload)
    assert res1.status_code == 201
    
    # Segundo registro con el mismo documento
    res2 = client.post("/personas/", json=payload)
    assert res2.status_code == 409
    assert res2.json()["detail"] == "Esta persona ya existe"

def test_falla_por_falta_de_datos_obligatorios(client):
    """Asegura que la API rechace payload si faltan campos obligatorios (422)"""
    payload = {
        "identificacion": {
            # Falta numero_identificacion
        },
        "datos_personales": {
            # Falta nombre_completo
        }
    }
    
    response = client.post("/personas/", json=payload)
    assert response.status_code == 422 # Error de validación de Pydantic

def test_fechas_invalidas_rechazadas_422(client):
    """Verifica que Pydantic rechace strings malformados para fechas."""
    payload = {
        "identificacion": {
            "numero_identificacion": "ABC123456",
        },
        "datos_personales": {
            "nombre_completo": "Carlos Perez",
            "fecha_nacimiento": "fecha-invalida-no-soy-iso"
        }
    }
    response = client.post("/personas/", json=payload)
    assert response.status_code == 422

def test_catalogo_espacios_blanco_ignorados(client, session: Session):
    """Verifica que strings vacíos o con espacios no generen basura en catálogos."""
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
    
    response = client.post("/personas/", json=payload)
    assert response.status_code == 201
    
    persona_db = session.exec(select(Persona).where(Persona.numero_identificacion == "X888888")).first()
    
    # Debe ser nulo en base de datos, no un id apuntando a "  "
    assert persona_db.id_nacionalidad is None
    assert persona_db.id_ciudad is None

def test_maximo_viable_roles_multiples(client, session: Session):
    """Prueba de estrés relacional: Un usuario que es Asociado y Voluntario al mismo tiempo."""
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
    
    response = client.post("/personas/", json=payload)
    assert response.status_code == 201
    
    # Validar transaccionalidad de roles 1:1
    persona_db = session.exec(select(Persona).where(Persona.numero_identificacion == "MULTI999")).first()
    assert persona_db is not None
    
    asociado_db = session.exec(select(DatosAsociado).where(DatosAsociado.id_persona == persona_db.id)).first()
    assert asociado_db is not None
    assert asociado_db.metodo_pago == "Banco"
    
    voluntario_db = session.exec(select(DatosVoluntario).where(DatosVoluntario.id_persona == persona_db.id)).first()
    assert voluntario_db is not None
