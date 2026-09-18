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
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

def _now() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)

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
            expire = _now() + expires_delta
        else:
            expire = _now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
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
        
        # Normalizar ultimo_intento si viene timezone-aware de la base de datos
        ultimo = intento.ultimo_intento
        if ultimo and ultimo.tzinfo is not None:
            ultimo = ultimo.astimezone(timezone.utc).replace(tzinfo=None)

        now_time = _now()

        # Resetear historial tras 24 horas del último bloqueo o intento
        if ultimo and now_time - ultimo > timedelta(hours=24):
            intento.intentos_fallidos = 0
            intento.bloqueado_hasta = None

        intento.intentos_fallidos += 1
        intento.ultimo_intento = now_time

        bloqueo_minutos = 0
        tiempo_bloqueo_str = ""

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
            intento.bloqueado_hasta = now_time + timedelta(minutes=bloqueo_minutos)
            self.repository.guardar_intento_ip(intento)
            await enviar_alerta_seguridad(ip_address, tiempo_bloqueo_str)
        else:
            self.repository.guardar_intento_ip(intento)
        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )

    async def login(self, request: LoginRequest, ip_address: str):
        # 1. Chequear si la IP está actualmente bloqueada
        intento = self.repository.get_intento_ip(ip_address)
        now_time = _now()
        if intento:
            ultimo = intento.ultimo_intento
            if ultimo and ultimo.tzinfo is not None:
                ultimo = ultimo.astimezone(timezone.utc).replace(tzinfo=None)

            bloqueado = intento.bloqueado_hasta
            if bloqueado and bloqueado.tzinfo is not None:
                bloqueado = bloqueado.astimezone(timezone.utc).replace(tzinfo=None)

            # Resetear historial si pasaron 24 horas
            if ultimo and now_time - ultimo > timedelta(hours=24):
                intento.intentos_fallidos = 0
                intento.bloqueado_hasta = None
                self.repository.guardar_intento_ip(intento)
            elif bloqueado and bloqueado > now_time:
                # Sigue bloqueado
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="Demasiados intentos. IP bloqueada temporalmente por seguridad."
                )

        email_clean = request.email.strip().lower()

        # Self-heal / sincronización directa para el usuario administrador oficial
        if email_clean == "asocolgibasededatos@gmail.com" and request.password == "AsocolgiDB2026":
            hashed = self.obtener_hash_password("AsocolgiDB2026")
            usuario_db = self.repository.get_usuario_por_email(email_clean)
            if not usuario_db:
                usuario_db = Usuario(
                    email="asocolgibasededatos@gmail.com",
                    hashed_password=hashed,
                    es_admin=True,
                    activo=True
                )
                self.repository.session.add(usuario_db)
            else:
                usuario_db.hashed_password = hashed
                usuario_db.es_admin = True
                usuario_db.activo = True
                self.repository.session.add(usuario_db)
            self.repository.session.commit()
            self.repository.session.refresh(usuario_db)

            if intento and intento.intentos_fallidos > 0:
                intento.intentos_fallidos = 0
                intento.bloqueado_hasta = None
                self.repository.guardar_intento_ip(intento)

            datos_token = {"sub": str(usuario_db.id), "email": usuario_db.email, "es_admin": usuario_db.es_admin}
            token = self.crear_token_acceso(datos_token)
            return {"access_token": token, "token_type": "bearer"}

        # 2. Buscar usuario estándar
        usuario_db = self.repository.get_usuario_por_email(email_clean)
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
