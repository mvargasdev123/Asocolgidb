from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from sqlmodel import Session, select

from database import get_session
from models.usuario import Usuario
from utils.seguridad import SECRET_KEY, ALGORITHM

# Le decimos a FastAPI dónde se consiguen los tokens (en el endpoint /token que hicimos)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def obtener_usuario_actual(
    token: str = Depends(oauth2_scheme), 
    session: Session = Depends(get_session)
) -> Usuario:
    """
    El guardia de seguridad oficial. Revisa el token en cada petición.
    Si el token es válido, devuelve al Usuario. Si no, lanza un 401 (Lárgate).
    """
    credenciales_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales de acceso.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # 1. Intentamos descifrar el token con nuestra clave secreta
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        usuario_id: str = payload.get("sub")
        
        if usuario_id is None:
            raise credenciales_exception
            
    except jwt.PyJWTError:
        # Si el token expiró, está alterado o es falso, directo a la calle
        raise credenciales_exception

    # 2. Buscamos al dueño del token en la base de datos
    usuario = session.exec(select(Usuario).where(Usuario.id == int(usuario_id))).first()
    
    if usuario is None or not usuario.activo:
        raise credenciales_exception
        
    # 3. El token es legítimo. Devolvemos al usuario con todos sus datos
    return usuario