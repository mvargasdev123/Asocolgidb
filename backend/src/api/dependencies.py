from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt.exceptions import InvalidTokenError
from sqlmodel import Session, select
from infrastructure.database import get_session
from domain.models.usuario import Usuario
from application.auth_service import SECRET_KEY, ALGORITHM

# Se le dice a Swagger que el endpoint de autenticación es /auth/login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)) -> Usuario:
    credenciales_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credenciales_exception
    except InvalidTokenError:
        raise credenciales_exception
        
    usuario = session.exec(select(Usuario).where(Usuario.id == int(user_id))).first()
    if usuario is None or not usuario.activo:
        raise credenciales_exception
        
    return usuario
