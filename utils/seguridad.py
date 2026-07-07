import os
from dotenv import load_dotenv
import bcrypt
import jwt # <-- Importación de PyJWT
from datetime import datetime, timedelta, timezone # <-- Para manejar el tiempo

# 1. Cargamos el archivo .env en la memoria de Python
load_dotenv()

# 2. Leemos las variables. Si por algún motivo el .env no existe, 
# ponemos un valor por defecto (fallback) o hacemos que el programa explote.
SECRET_KEY = os.getenv("SECRET_KEY", "clave_por_defecto_insegura")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = 60


# --- CONFIGURACIÓN DEL TOKEN ---
# LA FIRMA DEL DICTADOR: Esta es la clave maestra. Si alguien la descubre, 
# puede falsificar tokens y entrar como admin. ¡NUNCA se sube a GitHub en la vida real!
# (Por ahora la dejamos en texto plano por practicidad en local).
SECRET_KEY = "la_clave_super_secreta_de_asocolgi_que_nadie_sabe" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 # El token durará 1 hora exacta
RESET_TOKEN_EXPIRE_MINUTES = 15 # El token de recuperación durará solo 15 minutos

def obtener_hash_password(password: str) -> str:
    """
    Toma la contraseña en texto plano, genera un poco de 'sal' matemática (salt)
    y devuelve la cadena hasheada lista para la base de datos.
    """
    # bcrypt requiere que los textos se conviertan a bytes (utf-8) antes de encriptar
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    
    hashed_password = bcrypt.hashpw(pwd_bytes, salt)
    
    # Lo devolvemos como un string normal para que SQLite lo guarde feliz
    return hashed_password.decode('utf-8')

def verificar_password(password_plana: str, password_hasheada: str) -> bool:
    """
    Toma la contraseña del login y la compara con el hash guardado.
    """
    pwd_bytes = password_plana.encode('utf-8')
    hash_bytes = password_hasheada.encode('utf-8')
    
    return bcrypt.checkpw(pwd_bytes, hash_bytes)

def crear_token_acceso(data: dict) -> str:
    """Fabrica la pulsera VIP para el usuario."""
    datos_a_codificar = data.copy()
    
    # Le decimos al token a qué hora tiene que autodestruirse (caducar)
    fecha_expiracion = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    datos_a_codificar.update({"exp": fecha_expiracion})
    
    # Sellamos el token con nuestra firma secreta
    token_jwt = jwt.encode(datos_a_codificar, SECRET_KEY, algorithm=ALGORITHM)
    
    return token_jwt

def crear_token_recuperacion(email: str) -> str:
    """Fabrica el token temporal de 15 minutos exclusivo para resetear contraseña."""
    fecha_expiracion = datetime.now(timezone.utc) + timedelta(minutes=RESET_TOKEN_EXPIRE_MINUTES)
    # Incluimos un campo "tipo" para asegurar que no usen un token de login para resetear
    datos_a_codificar = {"sub": email, "tipo": "recuperacion", "exp": fecha_expiracion}
    
    return jwt.encode(datos_a_codificar, SECRET_KEY, algorithm=ALGORITHM)

def validar_token_recuperacion(token: str) -> str:
    """Valida el token temporal y devuelve el correo electrónico al que pertenece."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Prevenimos que un hacker use un token de acceso normal para cambiar contraseñas
        if payload.get("tipo") != "recuperacion":
            raise ValueError("El token provisto no es válido para esta operación.")
            
        email = payload.get("sub")
        if email is None:
            raise ValueError("Token inválido.")
            
        return email
    except jwt.ExpiredSignatureError:
        raise ValueError("El token de recuperación ha caducado. Por favor, solicita uno nuevo.")
    except jwt.PyJWTError:
        raise ValueError("El token es falso o ha sido alterado.")