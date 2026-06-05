from sqlmodel import Session, select
from models.persona import Persona

class RepositorioPersona:
    def __init__(self, session: Session):
        # Al inyectar la sesión aquí, el repositorio no necesita saber cómo conectarse a la BD, 
        # solo sabe cómo usar la conexión que le den.
        self.session = session

    def crear_persona(self, persona: Persona) -> Persona:
        self.session.add(persona)
        self.session.commit()
        self.session.refresh(persona) # Refresca para obtener el ID recién generado por la base de datos
        return persona

    def obtener_por_id(self, id_persona: int) -> Persona | None:
        # get() busca directamente por la Llave Primaria. Rápido y limpio.
        return self.session.get(Persona, id_persona)

    def obtener_todas(self) -> list[Persona]:
        # Equivalente a SELECT * FROM persona;
        statement = select(Persona)
        return self.session.exec(statement).all()