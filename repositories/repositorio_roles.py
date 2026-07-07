from sqlmodel import Session, select
from models.estado import Estado
from models.persona_estado import PersonaEstado
from models.datos_voluntario import DatosVoluntario
from models.datos_asociado import DatosAsociado
from models.persona import Persona

class RepositorioRoles:
    def __init__(self, session: Session):
        self.session = session

    def obtener_estado_por_nombre(self, nombre_estado: str) -> Estado | None:
        """Busca el ID de un estado sabiendo su nombre (ej. 'Voluntario')"""
        statement = select(Estado).where(Estado.nombre_estado == nombre_estado)
        return self.session.exec(statement).first()

    def verificar_estado_persona(self, id_persona: int, id_estado: int) -> PersonaEstado | None:
        """Revisa si la persona ya tiene ese estado exacto en la tabla pivote"""
        statement = select(PersonaEstado).where(
            PersonaEstado.id_persona == id_persona,
            PersonaEstado.id_estado == id_estado
        )
        return self.session.exec(statement).first()

    def asignar_estado_en_pivote(self, id_persona: int, id_estado: int):
        """Inserta el registro N:M en la tabla persona_estado"""
        nuevo_pivote = PersonaEstado(id_persona=id_persona, id_estado=id_estado)
        self.session.add(nuevo_pivote)
        # OJO: No hacemos commit aquí. El commit lo hará el Servicio al final 
        # para asegurar que todo se guarde junto (Transacción SQL).

    def remover_estado_en_pivote(self, id_persona: int, id_estado: int):
        """Elimina un estado de la persona (ej. quitarle el 'Externo')"""
        pivote = self.verificar_estado_persona(id_persona, id_estado)
        if pivote:
            self.session.delete(pivote)
            # Igual que arriba, sin commit todavía.

    def crear_registro_voluntario(self, registro: DatosVoluntario) -> DatosVoluntario:
        """Inyecta el nuevo voluntario en la base de datos"""
        self.session.add(registro)
        # Nota: El commit lo hacemos en la capa de servicio, así que aquí solo añadimos
        return registro

    def crear_registro_asociado(self, datos_asociado: DatosAsociado):
        """Guarda la ficha técnica del asociado"""
        self.session.add(datos_asociado)

    def obtener_datos_asociado_por_persona(self, id_persona: int) -> DatosAsociado | None:
        statement = select(DatosAsociado).where(DatosAsociado.id_persona == id_persona)
        return self.session.exec(statement).first()
    
    def obtener_datos_voluntario_por_persona(self, id_persona: int) -> DatosVoluntario | None:
        """Busca el contrato de esclavitud (voluntariado) de una persona en la BD"""
        statement = select(DatosVoluntario).where(DatosVoluntario.id_persona == id_persona)
        return self.session.exec(statement).first()

    def obtener_todas_las_personas_voluntarias(self, skip: int = 0, limit: int = 50) -> list[Persona]:
        statement = (
            select(Persona)
            .join(PersonaEstado)
            .join(Estado)
            .where(Estado.nombre_estado == "Voluntario")
            .offset(skip).limit(limit)
        )
        return self.session.exec(statement).all()

    def obtener_datos_asociado_por_persona(self, id_persona: int) -> DatosAsociado | None:
        statement = select(DatosAsociado).where(DatosAsociado.id_persona == id_persona)
        return self.session.exec(statement).first()

    def obtener_todas_las_personas_asociadas(self, skip: int = 0, limit: int = 50) -> list[Persona]:
        statement = (
            select(Persona)
            .join(PersonaEstado)
            .join(Estado)
            .where(Estado.nombre_estado == "Asociado")
            .offset(skip).limit(limit)
        )
        return self.session.exec(statement).all()