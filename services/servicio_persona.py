# IMPORTACIONES DE HERRAMIENTAS
from sqlmodel import Session, select
from datetime import date
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

# IMPORTACIONES DE REPOSITORIES
from repositories.repositorio_persona import RepositorioPersona
from repositories.repositorio_roles import RepositorioRoles

# IMPORTACIONES DE SCHEMAS
from schemas.persona_schema import PersonaCreate, PersonaUpdate

# IMPORTACIONES DE MODELS
from models.persona import Persona
from models.nacionalidad import Nacionalidad
from models.tipo_documento import TipoDocumento
# Asumo que tienes un modelo para los datos específicos del voluntario. 
# Si se llama distinto, ajusta esta importación:
from models.datos_voluntario import DatosVoluntario 

class ServicioPersona:
    def __init__(self, session: Session):
        self.session = session
        self.repo = RepositorioPersona(session)
        self.repo_roles = RepositorioRoles(session)

    # --- FUNCIONES AUXILIARES PRIVADAS (MAGIA GET OR CREATE) ---
    def _obtener_o_crear_nacionalidad(self, nombre_pais: str) -> int:
        # Corregido: Nacionalidad.pais en lugar de Nacionalidad.nombre
        nacionalidad_db = self.session.exec(select(Nacionalidad).where(Nacionalidad.pais == nombre_pais)).first()
        if not nacionalidad_db:
            nacionalidad_db = Nacionalidad(pais=nombre_pais)
            self.session.add(nacionalidad_db)
            self.session.commit()
            self.session.refresh(nacionalidad_db)
        return nacionalidad_db.id

    def _obtener_o_crear_tipo_documento(self, nombre_tipo: str) -> int:
        # Corregido: TipoDocumento.tipo en lugar de TipoDocumento.nombre
        tipo_doc_db = self.session.exec(select(TipoDocumento).where(TipoDocumento.tipo == nombre_tipo)).first()
        if not tipo_doc_db:
            tipo_doc_db = TipoDocumento(tipo=nombre_tipo)
            self.session.add(tipo_doc_db)
            self.session.commit()
            self.session.refresh(tipo_doc_db)
        return tipo_doc_db.id
    # -----------------------------------------------------------

    def registrar_nueva_persona(self, datos: PersonaCreate) -> Persona:
        try:
            # 1. Usamos la magia para traducir los textos en IDs reales de Postgres
            id_nac = self._obtener_o_crear_nacionalidad(datos.nacionalidad)
            id_doc = self._obtener_o_crear_tipo_documento(datos.tipo_documento)

            # 2. Preparamos el modelo Persona con los IDs obtenidos
            nueva_persona = Persona(
                nombre=datos.nombre,
                correo=datos.correo,
                fecha_nacimiento=datos.fecha_nacimiento,
                direccion=datos.direccion,
                proteccion_datos=datos.proteccion_datos,
                id_tipo_documento=id_doc,
                id_nacionalidad=id_nac,
                fecha_ingreso=date.today()
            )
            
            persona_guardada = self.repo.crear_persona(nueva_persona)
            
            estado_externo = self.repo_roles.obtener_estado_por_nombre("Externo")
            if not estado_externo:
                raise ValueError("El estado 'Externo' no existe en la base de datos.")
                
            self.repo_roles.asignar_estado_en_pivote(persona_guardada.id, estado_externo.id)
            
            self.session.commit()
            self.session.refresh(persona_guardada)
            return persona_guardada
            
        except IntegrityError as e:
            self.session.rollback()
            if "persona.correo" in str(e):
                raise HTTPException(status_code=400, detail="El correo electrónico ya se encuentra registrado.")
            raise HTTPException(status_code=400, detail="Error de integridad en los datos enviados.")
            
        except Exception as e:
            self.session.rollback()
            raise HTTPException(status_code=500, detail=f"Fallo al registrar la persona: {str(e)}")

    def actualizar_datos_biograficos(self, id_persona: int, datos: PersonaUpdate) -> Persona:
        persona_db = self.repo.obtener_por_id(id_persona)
        if not persona_db:
            raise HTTPException(status_code=404, detail="Persona no encontrada.")

        # Extraemos solo lo que el frontend envió
        datos_diccionario = datos.model_dump(exclude_unset=True)
        
        # Interceptamos los textos y los convertimos en IDs antes de inyectarlos
        if "nacionalidad" in datos_diccionario:
            texto_nac = datos_diccionario.pop("nacionalidad")
            datos_diccionario["id_nacionalidad"] = self._obtener_o_crear_nacionalidad(texto_nac)
            
        if "tipo_documento" in datos_diccionario:
            texto_doc = datos_diccionario.pop("tipo_documento")
            datos_diccionario["id_tipo_documento"] = self._obtener_o_crear_tipo_documento(texto_doc)
        
        for clave, valor in datos_diccionario.items():
            setattr(persona_db, clave, valor)
            
        self.session.add(persona_db)
        self.session.commit()
        self.session.refresh(persona_db)
        return persona_db
        
    def ascender_a_voluntario(self, id_persona: int, horas_disponibles: int, area: str):
        """
        Ejecuta la transición oficial de Externo a Voluntario.
        """
        # 1. Validar que la persona existe y está activa
        persona = self.repo.obtener_por_id(id_persona)
        if not persona or not persona.activo:
            raise HTTPException(status_code=404, detail="Persona no encontrada o inactiva.")

        # 2. Buscar los IDs de los estados implicados
        estado_externo = self.repo_roles.obtener_estado_por_nombre("Externo")
        estado_voluntario = self.repo_roles.obtener_estado_por_nombre("Voluntario")

        # 3. Validar las reglas de negocio de Asocolgi: 
        # Si ya es voluntario, lanzamos error.
        if estado_voluntario in persona.estados:
            raise HTTPException(status_code=400, detail="Esta persona ya es un Voluntario activo.")

        # 4. Transición de Poder: Le quitamos el estado Externo (si lo tiene) y le damos el Voluntario
        if estado_externo in persona.estados:
            persona.estados.remove(estado_externo)
        
        persona.estados.append(estado_voluntario)

        # 5. Crear el registro técnico en la tabla DatosVoluntario
        nuevos_datos_voluntario = DatosVoluntario(
            id_persona=id_persona,
            horas_disponibles=horas_disponibles,
            area=area
        )
        self.session.add(nuevos_datos_voluntario)

        # 6. Guardar la cirugía completa
        try:
            self.session.commit()
            return {"mensaje": f"{persona.nombre} ha sido ascendido a Voluntario exitosamente."}
        except Exception as e:
            self.session.rollback()
            raise HTTPException(status_code=500, detail="Fallo en la base de datos al realizar el ascenso.")

    def obtener_todas_las_personas(self, skip: int = 0, limit: int = 100, busqueda_nombre: str = None) -> list[Persona]:
        # Arreglé este detalle silenciosamente: le pasamos la búsqueda al repositorio
        return self.repo.obtener_todas(skip=skip, limit=limit, busqueda_nombre=busqueda_nombre)

    def obtener_persona_por_id(self, id_persona: int) -> Persona | None:
        return self.repo.obtener_por_id(id_persona)

    def dar_de_baja_persona(self, id_persona: int):
        persona_db = self.repo.obtener_por_id(id_persona)
        if not persona_db:
            raise HTTPException(status_code=404, detail="Persona no encontrada.")
            
        if not persona_db.activo:
            raise HTTPException(status_code=400, detail="Esta persona ya fue dada de baja anteriormente.")

        persona_db.activo = False
        
        self.session.add(persona_db)
        self.session.commit()
        self.session.refresh(persona_db)
        
        return {"mensaje": f"El registro de {persona_db.nombre} ha sido desactivado exitosamente."}
    
    def quitar_rol_a_persona(self, id_persona: int, nombre_rol_a_quitar: str):
        """
        La guillotina. Le quita un rol a la persona. 
        Si se queda sin roles, lo devuelve al estado base 'Externo'.
        """
        # 1. Buscamos a la persona
        persona = self.repo.obtener_por_id(id_persona)
        if not persona or not persona.activo:
            raise HTTPException(status_code=404, detail="Persona no encontrada o inactiva.")

        # 2. Buscamos la etiqueta del rol que queremos destruir
        rol_a_quitar = self.repo_roles.obtener_estado_por_nombre(nombre_rol_a_quitar)
        if not rol_a_quitar:
            raise HTTPException(status_code=404, detail=f"El rol '{nombre_rol_a_quitar}' no existe en el sistema.")

        # 3. Verificamos si realmente tiene ese rol
        if rol_a_quitar not in persona.estados:
            raise HTTPException(status_code=400, detail=f"La persona no tiene el rol '{nombre_rol_a_quitar}'.")

        # 4. LA GUILLOTINA: Le quitamos el rol de su lista
        persona.estados.remove(rol_a_quitar)

        # 5. EL PARACAÍDAS: Si la persona se quedó sin ningún rol, lo volvemos "Externo"
        if len(persona.estados) == 0:
            estado_externo = self.repo_roles.obtener_estado_por_nombre("Externo")
            persona.estados.append(estado_externo)

        # 6. Guardamos los cambios
        try:
            self.session.commit()
            return {"mensaje": f"Se ha quitado el rol '{nombre_rol_a_quitar}' exitosamente. Roles actuales: {[e.nombre_estado for e in persona.estados]}"}
        except Exception as e:
            self.session.rollback()
            raise HTTPException(status_code=500, detail="Fallo en la base de datos al quitar el rol.")