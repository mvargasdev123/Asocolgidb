from sqlmodel import Session
from datetime import date
from repositories.repositorio_persona import RepositorioPersona
from schemas.persona_schema import PersonaCreate
from models.persona import Persona

class ServicioPersona:
    def __init__(self, session: Session):
        # El servicio instancia el repositorio pasándole la sesión de la base de datos
        self.repo = RepositorioPersona(session)

    def registrar_nueva_persona(self, datos: PersonaCreate) -> Persona:
        """
        Toma los datos validados del Schema, le añade la lógica de negocio (como la fecha de ingreso)
        y le dice al repositorio que guarde el modelo en la base de datos.
        """
        # 1. Transformamos el esquema (Pydantic) al modelo (SQLModel)
        nueva_persona = Persona(
            nombre=datos.nombre,
            correo=datos.correo,
            fecha_nacimiento=datos.fecha_nacimiento,
            direccion=datos.direccion,
            proteccion_datos=datos.proteccion_datos,
            id_tipo_documento=datos.id_tipo_documento,
            id_nacionalidad=datos.id_nacionalidad,
            fecha_ingreso=date.today() # ¡Lógica de negocio! El sistema asigna la fecha actual automáticamente
        )
        
        # 2. Le decimos al cajero (repositorio) que lo guarde en la bóveda
        persona_guardada = self.repo.crear_persona(nueva_persona)
        
        # OJO: Aquí más adelante llamaremos a otro repositorio (ej. RepositorioEstado)
        # para asignarle a esta nueva persona el estado "Externo" por defecto en la tabla pivote.
        
        return persona_guardada
        
    def ascender_a_voluntario(self, id_persona: int, horas_disponibles: int, area: str):
        """
        Esqueleto de cómo se verá la transición de estados.
        """
        # 1. Buscar a la persona usando el repo.
        # 2. Buscar en la tabla pivote si tiene el estado "Externo".
        # 3. Si lo tiene -> Eliminar registro de "Externo" en la tabla pivote.
        # 4. Añadir el estado "Voluntario" en la tabla pivote.
        # 5. Crear el registro en la tabla datos_voluntario.
        # 6. Guardar cambios.
        pass

    def obtener_todas_las_personas(self) -> list[Persona]:
        """
        Pide al repositorio la lista completa de personas.
        Por ahora no tenemos filtros, así que devolverá todo el batallón.
        """
        return self.repo.obtener_todas()

    def obtener_persona_por_id(self, id_persona: int) -> Persona | None:
        """
        Busca a una persona en específico. 
        Puede devolver la Persona, o un triste 'None' si no existe.
        """
        return self.repo.obtener_por_id(id_persona)