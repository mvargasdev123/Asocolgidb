from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from database import get_session
from models.usuario import Usuario
from utils.seguridad import verificar_password, crear_token_acceso

router = APIRouter(tags=["Autenticación"])

@router.post("/token")
def iniciar_sesion(
    # El frontend enviará los datos como formulario, no como JSON
    form_data: OAuth2PasswordRequestForm = Depends(), 
    session: Session = Depends(get_session)
):
    # 1. Buscamos al usuario. 
    # OJO: El estándar OAuth2 siempre llama a la variable 'username', 
    # así que el frontend debe mandar el correo dentro del campo 'username'.
    usuario_db = session.exec(select(Usuario).where(Usuario.email == form_data.username)).first()
    
    # 2. Verificamos que exista y no sea un fantasma (Soft Delete)
    if not usuario_db or not usuario_db.activo:
        # Usamos el mismo mensaje de error para correo y contraseña
        # para que los hackers no sepan qué parte adivinaron bien.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos.",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    # 3. Chocamos la contraseña contra el hash de SQLite
    if not verificar_password(form_data.password, usuario_db.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos.",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    # 4. Fabricamos el Token de Acceso
    # Metemos el ID del usuario en el campo 'sub' (Subject, un estándar de JWT)
    datos_token = {"sub": str(usuario_db.id), "es_admin": usuario_db.es_admin}
    token = crear_token_acceso(datos_token)
    
    # Este formato exacto es el que exige FastAPI y el estándar OAuth2
    return {"access_token": token, "token_type": "bearer"}