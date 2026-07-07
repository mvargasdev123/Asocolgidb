from pydantic import BaseModel, EmailStr, Field

class RecuperarPassword(BaseModel):
    email: EmailStr = Field(..., description="Correo del administrador registrado en la base de datos")

class ResetearPassword(BaseModel):
    token: str = Field(..., description="El token de recuperación (jwt) enviado al correo")
    nueva_password: str = Field(..., min_length=8, description="La nueva contraseña")
