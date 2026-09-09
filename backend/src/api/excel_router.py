import json
from typing import Optional, Dict
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status
from pydantic import BaseModel
from sqlmodel import Session

from infrastructure.database import get_session
from application.excel_service import (
    generar_excel_memoria, 
    analizar_excel_dry_run, 
    ejecutar_importacion_definitiva
)
from application.email_service import enviar_excel_por_correo
from api.dependencies import get_current_user

from fastapi.responses import Response

router = APIRouter(prefix="/excel", tags=["Excel Import / Export"])

class ExportRequest(BaseModel):
    tipo_exportacion: str = "completa" # "completa", "asociados", "voluntarios", "expedientes"


@router.post("/exportar")
def exportar_excel_email(
    req: ExportRequest,
    session: Session = Depends(get_session),
    user: dict = Depends(get_current_user)
):
    tipo = req.tipo_exportacion.lower()
    if tipo not in ["completa", "asociados", "voluntarios", "expedientes"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tipo de exportación no válido. Opciones: 'completa', 'asociados', 'voluntarios', 'expedientes'."
        )

    excel_bytes = generar_excel_memoria(session, tipo_exportacion=tipo)

    filename = f"asocolgi_export_{tipo}.xlsx"
    enviar_excel_por_correo(excel_bytes, filename=filename)

    return {
        "status": "success",
        "message": f"El archivo Excel ('{filename}') ha sido generado en memoria y enviado al correo oficial (asocolgibasededatos@gmail.com)."
    }


@router.post("/descargar-directo", response_class=Response)
def descargar_excel_directo(
    req: ExportRequest,
    session: Session = Depends(get_session),
    user: dict = Depends(get_current_user)
):
    tipo = req.tipo_exportacion.lower()
    if tipo not in ["completa", "asociados", "voluntarios", "expedientes"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tipo de exportación no válido."
        )

    excel_bytes = generar_excel_memoria(session, tipo_exportacion=tipo)
    filename = f"asocolgi_export_{tipo}.xlsx"

    return Response(
        content=excel_bytes,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )


@router.post("/analizar-importacion")
async def analizar_importacion_dry_run(
    file: UploadFile = File(...),
    session: Session = Depends(get_session),
    user: dict = Depends(get_current_user)
):
    if not file.filename.endswith((".xlsx", ".xls")):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El archivo debe tener extensión .xlsx"
        )

    contents = await file.read()
    reporte = analizar_excel_dry_run(contents, session)

    return {
        "status": "success",
        "reporte": reporte
    }


@router.post("/confirmar-importacion")
async def confirmar_importacion_definitiva(
    file: UploadFile = File(...),
    decisiones_json: str = Form("{}"),
    session: Session = Depends(get_session),
    user: dict = Depends(get_current_user)
):
    if not file.filename.endswith((".xlsx", ".xls")):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El archivo debe tener extensión .xlsx"
        )

    try:
        decisiones = json.loads(decisiones_json)
    except Exception:
        decisiones = {}

    contents = await file.read()
    resultado = ejecutar_importacion_definitiva(contents, decisiones, session)

    return resultado
