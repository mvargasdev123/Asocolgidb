from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
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
        # Usamos selectinload para cargar relaciones automáticamente en un solo viaje
        consulta = select(Persona).where(Persona.id == id_persona).options(
            selectinload(Persona.comentarios),
            selectinload(Persona.estados),
            selectinload(Persona.expedientes)
        )
        return self.session.exec(consulta).first()

    def obtener_todas(self, skip: int = 0, limit: int = 50, busqueda_nombre: str = None) -> list[Persona]:
        """
        Trae a las personas activas. 
        skip = Cuántas me salto.
        limit = Cuántas traigo como máximo.
        """
        # Empezamos con la consulta base y pre-cargamos relaciones para evitar N+1 queries
        consulta = select(Persona).where(Persona.activo == True).options(
            selectinload(Persona.comentarios),
            selectinload(Persona.estados),
            selectinload(Persona.expedientes)
        )

        # Si el frontend nos mandó algo en 'busqueda_nombre', le inyectamos el filtro
        if busqueda_nombre:
            # Convierte "Carlos" en "%Carlos%", buscando coincidencias en cualquier parte del nombre
            consulta = consulta.where(Persona.nombre.like(f"%{busqueda_nombre}%"))

        # Aplicamos la paginación al final de todo
        consulta = consulta.offset(skip).limit(limit)
        
        return self.session.exec(consulta).all()