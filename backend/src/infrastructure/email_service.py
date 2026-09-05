import logging

async def enviar_alerta_seguridad(ip: str, tiempo_bloqueo: str):
    """
    Envía un correo de alerta de seguridad por bloqueos sucesivos de IP.
    """
    email_destino = "asocolgibasededatos@gmail.com"
    # Aquí iría la lógica real con SMTP (ej. smtplib, fastapi-mail)
    logging.info(f"EMAIL ENVIADO A {email_destino}: Alerta de seguridad! La IP {ip} ha sido bloqueada por {tiempo_bloqueo}.")

async def enviar_token_recuperacion(token: str):
    """
    Envía el token temporal de recuperación de contraseña.
    """
    email_destino = "asocolgibasededatos@gmail.com"
    # Aquí iría la lógica real con SMTP
    logging.info(f"EMAIL ENVIADO A {email_destino}: Tu token de recuperación es: {token}")
