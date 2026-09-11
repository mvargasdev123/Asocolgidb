import io
import openpyxl
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select

from domain.models.persona import Persona
from application.excel_service import analizar_excel_dry_run, ejecutar_importacion_definitiva
from application.auth_service import AuthService
from infrastructure.auth_repository import AuthRepository

def _crear_excel_dummy(rows_bd: list) -> bytes:
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    ws = wb.create_sheet("BD")
    for r in rows_bd:
        ws.append(r)
    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    return output.read()

def test_dry_run_y_resolucion_duplicados(session: Session, client: TestClient, usuario_prueba):
    auth_service = AuthService(AuthRepository(session))
    token = auth_service.crear_token_acceso({"sub": usuario_prueba.email})
    # 1. Crear persona en DB
    p_exist = Persona(
        numero_identificacion="X9999999Z",
        nombre_completo="Juan Existente",
        activo=True
    )
    session.add(p_exist)
    session.commit()

    # 2. Crear Excel con 1 nuevo y 1 duplicado
    headers = [
        "FECHA ATENCIÓN", "TIPO IDENTIFICACION", "NÚMERO IDENTIFICACION", "NOMBRE COMPLETO",
        "TELEFONO", "E-MAIL", "MOTIVO CONSULTA", "No. REGISTRO ASOCIADO"
    ]
    row1 = ["01/01/2026", "NIE", "X9999999Z", "Juan Actualizado", "123", "juan@test.com", "Consulta", "N/A"]
    row2 = ["01/01/2026", "DNI", "Y8888888W", "Nuevo Usuario", "456", "nuevo@test.com", "Consulta", "N/A"]

    excel_bytes = _crear_excel_dummy([headers, row1, row2])

    # Test Dry-run
    reporte = analizar_excel_dry_run(excel_bytes, session)
    assert reporte["total_filas"] == 2
    assert reporte["nuevos_listos_para_guardar"] == 1
    assert len(reporte["duplicados"]) == 1
    assert reporte["duplicados"][0]["identificacion"] == "X9999999Z"

    # Test Importación Definitiva con decisión 'omitir' para el duplicado
    decisiones = {"X9999999Z": "omitir"}
    res = ejecutar_importacion_definitiva(excel_bytes, decisiones, session)
    assert res["registros_creados"] == 1
    assert res["registros_omitidos"] == 1

    # Verificar DB: el existente no fue alterado
    p_check = session.exec(select(Persona).where(Persona.numero_identificacion == "X9999999Z")).first()
    assert p_check.nombre_completo == "Juan Existente"

    # Verificar que el nuevo sí fue creado
    p_nuevo = session.exec(select(Persona).where(Persona.numero_identificacion == "Y8888888W")).first()
    assert p_nuevo is not None
    assert p_nuevo.nombre_completo == "Nuevo Usuario"


def test_importacion_definitiva_sobreescribir(session: Session):
    p_exist = Persona(
        numero_identificacion="X7777777Y",
        nombre_completo="Maria Vieja",
        activo=True
    )
    session.add(p_exist)
    session.commit()

    headers = ["FECHA ATENCIÓN", "TIPO IDENTIFICACION", "NÚMERO IDENTIFICACION", "NOMBRE COMPLETO"]
    row1 = ["01/01/2026", "NIE", "X7777777Y", "Maria Sobreescrita"]
    excel_bytes = _crear_excel_dummy([headers, row1])

    decisiones = {"X7777777Y": "sobreescribir"}
    res = ejecutar_importacion_definitiva(excel_bytes, decisiones, session)
    assert res["registros_actualizados"] == 1

    p_check = session.exec(select(Persona).where(Persona.numero_identificacion == "X7777777Y")).first()
    assert p_check.nombre_completo == "Maria Sobreescrita"


def test_import_mm_dd_yyyy_dates(session: Session):
    headers = [
        "FECHA ATENCIÓN", "TIPO IDENTIFICACION", "NÚMERO IDENTIFICACION", "NOMBRE COMPLETO",
        "FECHA NACIMIENTO", "FECHA PADRON"
    ]
    # 11/13/1955 -> Nov 13, 1955. 01/29/1981 -> Jan 29, 1981
    row1 = ["09/06/2026", "NIE", "X11223344M", "Fecha Test MM DD YYYY", "11/13/1955", "01/29/1981"]
    excel_bytes = _crear_excel_dummy([headers, row1])

    res = ejecutar_importacion_definitiva(excel_bytes, {}, session)
    assert res["status"] == "success"

    p = session.exec(select(Persona).where(Persona.numero_identificacion == "X11223344M")).first()
    assert p is not None
    assert p.fecha_nacimiento.year == 1955
    assert p.fecha_nacimiento.month == 11
    assert p.fecha_nacimiento.day == 13
    assert p.fecha_padron.year == 1981
    assert p.fecha_padron.month == 1
    assert p.fecha_padron.day == 29


