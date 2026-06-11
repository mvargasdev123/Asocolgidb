# IMPORTACIONES DE ERRAMIENTAS
from sqlmodel import Session
from datetime import date
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
# IMPORTACIONES DE REPOSITORIES
from repositories.repositorio_persona import RepositorioPersona
from repositories.repositorio_roles import RepositorioRoles
# IMPORTACIONES DE SCHEMAS
from schemas.persona_schema import PersonaCreate
# IMPORTACIONES DE MODELS
from models.persona import Persona

class ServicioPersona:
    def __init__(self, session: Session):
        self.session = session
        # El servicio instancia el repositorio pasándole la sesión de la base de datos
        self.repo = RepositorioPersona(session)
        self.repo_roles = RepositorioRoles(session)

    def registrar_nueva_persona(self, datos: PersonaCreate) -> Persona:
        try:
            # 1. Preparamos el modelo Persona
            nueva_persona = Persona(
                nombre=datos.nombre,
                correo=datos.correo,
                fecha_nacimiento=datos.fecha_nacimiento,
                direccion=datos.direccion,
                proteccion_datos=datos.proteccion_datos,
                id_tipo_documento=datos.id_tipo_documento,
                id_nacionalidad=datos.id_nacionalidad,
                fecha_ingreso=date.today()
            )
            
            # 2. Guardamos la persona para que la BD le asigne un ID
            persona_guardada = self.repo.crear_persona(nueva_persona)
            
            # 3. Buscamos el ID del estado "Externo"
            estado_externo = self.repo_roles.obtener_estado_por_nombre("Externo")
            if not estado_externo:
                raise ValueError("El estado 'Externo' no existe en la base de datos.")
                
            # 4. Le asignamos la etiqueta de Externo en la tabla pivote
            self.repo_roles.asignar_estado_en_pivote(persona_guardada.id, estado_externo.id)
            
            # 5. Confirmamos TODO. Si falla el rol, no se crea la persona. Transacción limpia.
            self.session.commit()
            self.session.refresh(persona_guardada)
            
            return persona_guardada
            
        except IntegrityError as e:
            # CAPTURA 1: Si la base de datos rechaza la inserción por una restricción (como el correo UNIQUE)
            self.session.rollback()
            
            # Validamos si la violación de unicidad corresponde al campo correo
            if "persona.correo" in str(e):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El correo electrónico ya se encuentra registrado."
                )
            
            # Por si falla otra restricción UNIQUE o FOREIGN KEY que no sea el correo
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error de integridad en los datos enviados."
            )
            
        except Exception as e:
            # CAPTURA 2: Cualquier otro error inesperado (fallos de conexión, bugs de lógica, etc.)
            self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Fallo al registrar la persona: {str(e)}"
            )
        
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