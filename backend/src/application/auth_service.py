import os
from datetime import datetime, timedelta, timezone
import jwt
import bcrypt
from fastapi import HTTPException, status
from domain.schemas.auth_schemas import LoginRequest
from domain.models.usuario import Usuario, IntentoLoginIP
from infrastructure.auth_repository import AuthRepository
from infrastructure.email_service import enviar_alerta_seguridad, enviar_token_recuperacion


SECRET_KEY = os.getenv("JWT_SECRET_KEY", "un_secreto_super_seguro_para_desarrollo")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 20

class AuthService:
    def __init__(self, repository: AuthRepository):
        self.repository = repository

    def verificar_password(self, plain_password, hashed_password):
        try:
            return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
        except Exception:
            return False

    def obtener_hash_password(self, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(12)).decode('utf-8')

    def crear_token_acceso(self, data: dict, expires_delta: timedelta = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def refrescar_token(self, usuario: Usuario) -> dict:
        datos_token = {"sub": str(usuario.id), "email": usuario.email, "es_admin": usuario.es_admin}
        nuevo_token = self.crear_token_acceso(datos_token, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        return {"access_token": nuevo_token, "token_type": "bearer"}

    async def _manejar_intento_fallido(self, ip_address: str):
        intento = self.repository.get_intento_ip(ip_address)
        if not intento:
            intento = IntentoLoginIP(ip_address=ip_address)
        
        # Resetear historial tras 24 horas del último bloqueo o intento
        if intento.ultimo_intento and datetime.utcnow() - intento.ultimo_intento > timedelta(hours=24):
            intento.intentos_fallidos = 0
            intento.bloqueado_hasta = None

        intento.intentos_fallidos += 1
        intento.ultimo_intento = datetime.utcnow()

        bloqueo_minutos = 0
        tiempo_bloqueo_str = ""

        # Lógica de bloqueos:
        # - Si falla 3 intentos consecutivos -> bloqueo de 15 segundos
        # - Si falla 4 intentos -> bloqueo de 30 segundos
        # - Si falla 5 intentos -> bloqueo de 5 minutos
        # - Si falla 6 o más intentos -> bloqueo recurrente de 10 minutos
        if intento.intentos_fallidos == 3:
            bloqueo_minutos = 15 / 60.0 # 15 seg
            tiempo_bloqueo_str = "15 segundos"
        elif intento.intentos_fallidos == 4:
            bloqueo_minutos = 30 / 60.0 # 30 seg
            tiempo_bloqueo_str = "30 segundos"
        elif intento.intentos_fallidos == 5:
            bloqueo_minutos = 5.0 # 5 min
            tiempo_bloqueo_str = "5 minutos"
        elif intento.intentos_fallidos >= 6:
            bloqueo_minutos = 10.0 # 10 min
            tiempo_bloqueo_str = "10 minutos"

        if bloqueo_minutos > 0:
            intento.bloqueado_hasta = datetime.utcnow() + timedelta(minutes=bloqueo_minutos)
            self.repository.guardar_intento_ip(intento)
            await enviar_alerta_seguridad(ip_address, tiempo_bloqueo_str)
            # Para el 3er fallo bloqueamos 15s, etc. La excepción la lanzamos para que se aplique.
        else:
            self.repository.guardar_intento_ip(intento)
        
        # Siempre respondemos el mismo error genérico para no dar pistas
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )

    async def login(self, request: LoginRequest, ip_address: str):
        # 1. Chequear si la IP está actualmente bloqueada
        intento = self.repository.get_intento_ip(ip_address)
        if intento:
            # Resetear historial si pasaron 24 horas
            if intento.ultimo_intento and datetime.utcnow() - intento.ultimo_intento > timedelta(hours=24):
                intento.intentos_fallidos = 0
                intento.bloqueado_hasta = None
                self.repository.guardar_intento_ip(intento)
            elif intento.bloqueado_hasta and intento.bloqueado_hasta > datetime.utcnow():
                # Sigue bloqueado
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="Demasiados intentos. IP bloqueada temporalmente por seguridad."
                )

        # 2. Buscar usuario
        usuario_db = self.repository.get_usuario_por_email(request.email)
        if not usuario_db or not usuario_db.activo:
            await self._manejar_intento_fallido(ip_address)

        # 3. Validar contraseña
        if not self.verificar_password(request.password, usuario_db.hashed_password):
            await self._manejar_intento_fallido(ip_address)

        # 4. Si es correcto, resetear intentos fallidos
        if intento and intento.intentos_fallidos > 0:
            intento.intentos_fallidos = 0
            intento.bloqueado_hasta = None
            self.repository.guardar_intento_ip(intento)

        # 5. Generar token
        datos_token = {"sub": str(usuario_db.id), "email": usuario_db.email, "es_admin": usuario_db.es_admin}
        token = self.crear_token_acceso(datos_token)

        return {"access_token": token, "token_type": "bearer"}

    async def forgot_password(self):
        # 1. Según la Spec 01 (Sección 3.3), se omite pedir el correo.
        # Siempre se envía el token a la cuenta predefinida:
        email_admin = "asocolgibasededatos@gmail.com"
        
        # 2. Fabricar Token (ej. 15 minutos)
        datos_token = {"sub": email_admin, "tipo": "recuperacion"}
        token = self.crear_token_acceso(datos_token, expires_delta=timedelta(minutes=15))
        
        # 3. Enviar correo
        await enviar_token_recuperacion(token)
        
        return {"mensaje": "Hemos enviado un enlace de recuperación al correo administrativo."}
