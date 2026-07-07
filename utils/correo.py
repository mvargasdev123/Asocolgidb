import os
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr
from dotenv import load_dotenv

load_dotenv()

# Configuración leída desde tu .env seguro
conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM", os.getenv("MAIL_USERNAME")),
    MAIL_PORT=int(os.getenv("MAIL_PORT", 587)),
    MAIL_SERVER=os.getenv("MAIL_SERVER", "smtp.gmail.com"),
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

fastmail_client = FastMail(conf)

async def enviar_correo_recuperacion(email_destino: EmailStr, token: str):
    """
    Envía el correo de recuperación al administrador con el token especial de reseteo.
    """
    # Aquí podríamos mandar un enlace a tu Frontend en Flutter, 
    # pero por ahora le enviaremos el Token directamente (o una simulación de URL).
    # Ejemplo de URL si Flutter corriera en localhost:3000
    link_recuperacion = f"http://localhost:3000/reset-password?token={token}"
    
    html_cuerpo = f"""
    <h2>Recuperación de Contraseña - Asocolgi</h2>
    <p>Hemos recibido una solicitud para restablecer tu contraseña.</p>
    <p>Este enlace es válido únicamente por <b>15 minutos</b>.</p>
    <p>Tu Token de Recuperación es:</p>
    <code>{token}</code>
    <br><br>
    <p>Si estuvieras en el frontend, harías clic aquí (simulación):</p>
    <a href="{link_recuperacion}">Restablecer Contraseña</a>
    <br><br>
    <p>Si no solicitaste este cambio, simplemente ignora este correo.</p>
    """

    mensaje = MessageSchema(
        subject="Recuperación de Contraseña - Asocolgi",
        recipients=[email_destino],
        body=html_cuerpo,
        subtype=MessageType.html
    )

    await fastmail_client.send_message(mensaje)
