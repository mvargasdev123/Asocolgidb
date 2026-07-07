from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from database import get_session
from models.usuario import Usuario
from utils.seguridad import verificar_password, crear_token_acceso, crear_token_recuperacion, validar_token_recuperacion, obtener_hash_password
from api.dependencias import obtener_usuario_actual
from schemas.auth_schema import RecuperarPassword, ResetearPassword
from utils.correo import enviar_correo_recuperacion

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

@router.post("/refresh")
def refrescar_token(usuario_actual: Usuario = Depends(obtener_usuario_actual)):
    """
    Ruta para la sesión deslizante (Sliding Session). 
    Requiere un token válido (que aún no haya caducado).
    Devuelve un nuevo token con otros 60 minutos de vida.
    """
    datos_token = {"sub": str(usuario_actual.id), "es_admin": usuario_actual.es_admin}
    nuevo_token = crear_token_acceso(datos_token)
    return {"access_token": nuevo_token, "token_type": "bearer"}

@router.post("/forgot-password")
async def forgot_password(datos: RecuperarPassword, session: Session = Depends(get_session)):
    # 1. Buscamos el usuario por su correo
    usuario_db = session.exec(select(Usuario).where(Usuario.email == datos.email)).first()
    
    if not usuario_db or not usuario_db.activo:
        # Por seguridad no revelamos si el correo existe o no a un posible atacante.
        # Siempre respondemos lo mismo.
        return {"mensaje": "Si el correo existe en nuestro sistema, hemos enviado un enlace de recuperación."}
    
    # 2. Fabricamos el Token de Reseteo (15 mins)
    token = crear_token_recuperacion(datos.email)
    
    # 3. Disparamos el correo
    await enviar_correo_recuperacion(datos.email, token)
    
    return {"mensaje": "Si el correo existe en nuestro sistema, hemos enviado un enlace de recuperación."}

@router.post("/reset-password")
def reset_password(datos: ResetearPassword, session: Session = Depends(get_session)):
    try:
        # 1. Decodificamos el token para extraer el correo. 
        # Si expiró o es trampa, 'validar_token_recuperacion' explotará lanzando un ValueError
        email = validar_token_recuperacion(datos.token)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
        
    # 2. Buscamos al usuario 
    usuario_db = session.exec(select(Usuario).where(Usuario.email == email)).first()
    if not usuario_db or not usuario_db.activo:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
        
    # 3. Hasheamos la nueva contraseña y la guardamos
    usuario_db.hashed_password = obtener_hash_password(datos.nueva_password)
    session.add(usuario_db)
    session.commit()
    
    return {"mensaje": "Tu contraseña ha sido actualizada exitosamente. Ya puedes iniciar sesión con ella."}