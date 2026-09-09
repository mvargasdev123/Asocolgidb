import os
import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

from fastapi import HTTPException, status

ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "asocolgibasededatos@gmail.com")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")

def enviar_excel_por_correo(excel_bytes: bytes, filename: str, destinatario: str = ADMIN_EMAIL) -> bool:
    """
    Envía el archivo Excel generado en memoria como adjunto al correo oficial.
    Si no hay credenciales SMTP en el servidor, notifica claramente el error.
    """
    if not SMTP_USERNAME or not SMTP_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Servidor SMTP no configurado en el backend (faltan SMTP_USERNAME y SMTP_PASSWORD en .env). Por favor utiliza la opción 'Descargar Excel Directo'."
        )

    try:
        msg = MIMEMultipart()
        msg['From'] = SMTP_USERNAME
        msg['To'] = destinatario
        msg['Subject'] = f"Respaldo Base de Datos Asocolgi - {filename}"

        body = (
            f"Hola Administración,\n\n"
            f"Se ha solicitado la exportación de la base de datos de Asocolgi.\n"
            f"Adjunto a este correo se encuentra el archivo generado: {filename}\n\n"
            f"Saludos,\nSistema Asocolgi V2"
        )
        msg.attach(MIMEText(body, 'plain'))

        part = MIMEBase('application', 'vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        part.set_payload(excel_bytes)
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename="{filename}"')
        msg.attach(part)

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()

        logging.info(f"Correo con archivo '{filename}' enviado con éxito a '{destinatario}'.")
        return True

    except Exception as e:
        logging.error(f"Error al enviar correo con archivo Excel: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en servidor SMTP al enviar correo: {str(e)}"
        )
