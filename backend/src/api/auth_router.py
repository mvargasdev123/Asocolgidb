from fastapi import APIRouter, Depends, Request, HTTPException, status
from sqlmodel import Session
from fastapi.security import OAuth2PasswordRequestForm
from domain.schemas.auth_schemas import LoginResponse, ErrorResponse
from infrastructure.database import get_session
from infrastructure.auth_repository import AuthRepository
from application.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Autenticación"])

def get_auth_service(session: Session = Depends(get_session)) -> AuthService:
    repository = AuthRepository(session)
    return AuthService(repository)

@router.post("/login", response_model=LoginResponse)
async def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Inicia sesión con correo y contraseña. Implementa bloqueo progresivo por IP.
    """
    # Extraemos la IP del cliente (si está detrás de un proxy, miramos X-Forwarded-For, sino origin)
    forwarded = request.headers.get("X-Forwarded-For")
    ip_address = forwarded.split(",")[0] if forwarded else request.client.host
    
    # Simulamos el objeto LoginRequest que espera el servicio, o le pasamos los datos
    from domain.schemas.auth_schemas import LoginRequest
    request_data = LoginRequest(email=form_data.username, password=form_data.password)
    
    return await auth_service.login(request_data, ip_address)

from api.dependencies import get_current_user
from domain.models.usuario import Usuario

@router.post("/refresh", response_model=LoginResponse)
async def refresh_token(
    current_user: Usuario = Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Renueva el token de acceso JWT por otros 20 minutos si el usuario está autenticado y activo.
    """
    return auth_service.refrescar_token(current_user)

@router.post("/forgot-password")
async def forgot_password(auth_service: AuthService = Depends(get_auth_service)):
    """
    Genera un token de recuperación y lo envía al correo administrativo predefinido.
    """
    return await auth_service.forgot_password()
