from sqlmodel import Session, select
from models.estado import Estado
from models.persona_estado import PersonaEstado
from models.datos_voluntario import DatosVoluntario
from models.datos_asociado import DatosAsociado
from models.datos_contratado import DatosContratado

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

    def crear_registro_voluntario(self, datos_voluntario: DatosVoluntario):
        """Guarda la ficha técnica del voluntario"""
        self.session.add(datos_voluntario)
        # El Servicio hará el commit general.

    def crear_registro_asociado(self, datos_asociado: DatosAsociado):
        """Guarda la ficha técnica del asociado"""
        self.session.add(datos_asociado)

    def crear_registro_contratado(self, datos_contratado: DatosContratado):
        """Guarda la ficha técnica del contratado"""
        self.session.add(datos_contratado)