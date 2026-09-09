from typing import Optional, Type, TypeVar
from sqlmodel import Session, select
from sqlalchemy.orm import joinedload
from domain.models.persona import Persona
from domain.models.roles import DatosAsociado, DatosVoluntario

# TypeVar para el catálogo dinámico (debe ser una clase SQLModel)
TCatalog = TypeVar("TCatalog")

class PersonaRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_or_create_catalog(self, catalog_model: Type[TCatalog], name: str) -> int:
        """
        Busca un valor en el catálogo por su nombre.
        Si no existe, lo crea silenciosamente y retorna su ID.
        """
        name = name.strip()
        # Buscar existente
        statement = select(catalog_model).where(catalog_model.nombre == name)
        existing = self.session.exec(statement).first()
        if existing:
            return existing.id
        
        # Crear nuevo
        new_item = catalog_model(nombre=name)
        self.session.add(new_item)
        self.session.commit()
        self.session.refresh(new_item)
        return new_item.id

    def existe_numero_identificacion(self, numero: str) -> bool:
        """Verifica si el número de documento ya está registrado."""
        statement = select(Persona).where(Persona.numero_identificacion == numero)
        result = self.session.exec(statement).first()
        return result is not None

    def create_persona(self, persona: Persona, asociado: Optional[DatosAsociado] = None, voluntario: Optional[DatosVoluntario] = None) -> Persona:
        """
        Guarda la Persona y sus posibles roles (Asociado/Voluntario)
        en una sola transacción para evitar inconsistencias.
        """
        try:
            self.session.add(persona)
            self.session.flush() # Para obtener el ID de persona sin comitear aún
            
            if asociado:
                asociado.id_persona = persona.id
                self.session.add(asociado)
            
            if voluntario:
                voluntario.id_persona = persona.id
                self.session.add(voluntario)
                
            self.session.commit()
            self.session.refresh(persona)
            return persona
        except Exception as e:
            self.session.rollback()
            raise e

    def get_all_activas(
        self,
        last_id: int | None = None,
        limit: int = 10,
        search: str | None = None,
        genero: str | None = None,
        rol: str | None = None,
        situacion_admin: str | None = None
    ) -> list[Persona]:
        statement = (
            select(Persona)
            .options(joinedload(Persona.datos_asociado), joinedload(Persona.datos_voluntario))
            .where(Persona.activo == True)
        )
        
        # Búsqueda por texto (nombre_completo o numero_identificacion)
        if search and search.strip():
            term = f"%{search.strip()}%"
            statement = statement.where(
                (Persona.nombre_completo.ilike(term)) | (Persona.numero_identificacion.ilike(term))
            )
            
        # Filtro por Género
        if genero and genero.strip():
            g_clean = genero.strip().lower()
            if g_clean in ["h", "hombre", "hombres", "masculino", "masculinos"]:
                statement = statement.where(
                    (Persona.genero.ilike("H%")) | (Persona.genero.ilike("Hombre%")) | (Persona.genero.ilike("Masculino%"))
                )
            elif g_clean in ["m", "mujer", "mujeres", "femenino", "femeninas"]:
                statement = statement.where(
                    (Persona.genero.ilike("M%")) | (Persona.genero.ilike("Mujer%")) | (Persona.genero.ilike("Femenino%"))
                )
            else:
                statement = statement.where(Persona.genero.ilike(f"%{genero.strip()}%"))

        # Filtro por Rol (asociado, voluntario, externo)
        if rol and rol.strip():
            r_clean = rol.strip().lower()
            if r_clean in ["asociado", "asociados"]:
                statement = statement.join(DatosAsociado).where(
                    (DatosAsociado.estado_membresia == None) | (DatosAsociado.estado_membresia != "Inactivo")
                )
            elif r_clean in ["voluntario", "voluntarios"]:
                statement = statement.join(DatosVoluntario)
            elif r_clean in ["externo", "externos"]:
                statement = statement.where(
                    ~Persona.id.in_(select(DatosAsociado.id_persona).where((DatosAsociado.estado_membresia == None) | (DatosAsociado.estado_membresia != "Inactivo"))),
                    ~Persona.id.in_(select(DatosVoluntario.id_persona))
                )

        # Filtro por Situación Administrativa
        if situacion_admin and situacion_admin.strip():
            s_clean = situacion_admin.strip().lower()
            if s_clean in ["regular", "regulares"]:
                statement = statement.where(Persona.situacion_admin.ilike("%Regular%"))
            elif s_clean in ["irregular", "irregulares"]:
                statement = statement.where(Persona.situacion_admin.ilike("%Irregular%"))
            elif "tramite" in s_clean or "trámite" in s_clean:
                statement = statement.where(Persona.situacion_admin.ilike("%tramite%"))
            else:
                statement = statement.where(Persona.situacion_admin.ilike(f"%{situacion_admin.strip()}%"))

        statement = statement.order_by(Persona.id)
        if last_id is not None:
            statement = statement.where(Persona.id > last_id)
        statement = statement.limit(limit)
        return self.session.exec(statement).unique().all()
        
    def get_by_id(self, persona_id: int) -> Optional[Persona]:
        statement = (
            select(Persona)
            .options(joinedload(Persona.datos_asociado), joinedload(Persona.datos_voluntario))
            .where(Persona.id == persona_id, Persona.activo == True)
        )
        return self.session.exec(statement).first()

    def update_persona(self, persona: Persona) -> Persona:
        self.session.add(persona)
        self.session.commit()
        self.session.refresh(persona)
        return persona

    def soft_delete(self, persona: Persona):
        persona.activo = False
        self.session.add(persona)
        self.session.commit()

