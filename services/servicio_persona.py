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
from models.catalogos import MotivoConsulta, NivelEducativo, Derivacion, TecnicaAcogida
from models.telefono_persona import Telefono
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

    def _obtener_o_crear_motivo_consulta(self, nombre: str) -> int:
        motivo_db = self.session.exec(select(MotivoConsulta).where(MotivoConsulta.nombre == nombre)).first()
        if not motivo_db:
            motivo_db = MotivoConsulta(nombre=nombre)
            self.session.add(motivo_db)
            self.session.commit()
            self.session.refresh(motivo_db)
        return motivo_db.id

    def _obtener_o_crear_nivel_educativo(self, nombre: str) -> int:
        nivel_db = self.session.exec(select(NivelEducativo).where(NivelEducativo.nombre == nombre)).first()
        if not nivel_db:
            nivel_db = NivelEducativo(nombre=nombre)
            self.session.add(nivel_db)
            self.session.commit()
            self.session.refresh(nivel_db)
        return nivel_db.id

    def _obtener_o_crear_derivacion(self, nombre: str) -> int:
        derivacion_db = self.session.exec(select(Derivacion).where(Derivacion.nombre == nombre)).first()
        if not derivacion_db:
            derivacion_db = Derivacion(nombre=nombre)
            self.session.add(derivacion_db)
            self.session.commit()
            self.session.refresh(derivacion_db)
        return derivacion_db.id

    def _obtener_o_crear_tecnica_acogida(self, nombre: str) -> int:
        tecnica_db = self.session.exec(select(TecnicaAcogida).where(TecnicaAcogida.nombre == nombre)).first()
        if not tecnica_db:
            tecnica_db = TecnicaAcogida(nombre=nombre)
            self.session.add(tecnica_db)
            self.session.commit()
            self.session.refresh(tecnica_db)
        return tecnica_db.id
    # -----------------------------------------------------------

    def registrar_nueva_persona(self, datos: PersonaCreate) -> Persona:
        try:
            # 1. Usamos la magia para traducir los textos en IDs reales de Postgres
            id_nac = self._obtener_o_crear_nacionalidad(datos.nacionalidad)
            id_doc = self._obtener_o_crear_tipo_documento(datos.tipo_documento)
            
            id_motivo = self._obtener_o_crear_motivo_consulta(datos.motivo_consulta) if datos.motivo_consulta else None
            id_nivel = self._obtener_o_crear_nivel_educativo(datos.nivel_educativo) if datos.nivel_educativo else None
            id_derivacion = self._obtener_o_crear_derivacion(datos.derivacion) if datos.derivacion else None
            id_tecnica = self._obtener_o_crear_tecnica_acogida(datos.tecnica_acogida) if datos.tecnica_acogida else None

            # 2. Preparamos el modelo Persona INYECTANDO ABSOLUTAMENTE TODO
            nueva_persona = Persona(
                # Clásicos
                nombre=datos.nombre,
                correo=datos.correo,
                fecha_nacimiento=datos.fecha_nacimiento,
                direccion=datos.direccion,
                proteccion_datos=datos.proteccion_datos,
                id_tipo_documento=id_doc,
                id_nacionalidad=id_nac,
                fecha_ingreso=datos.fecha_atencion if datos.fecha_atencion else date.today(),
                
                # Los nuevos campos del Excel mapeados desde Pydantic a SQLModel
                numero_identificacion=datos.numero_identificacion,
                genero=datos.genero,
                situacion_administrativa=datos.situacion_administrativa,
                madre_soltera=datos.madre_soltera,
                violencia_genero=datos.violencia_genero,
                tiene_padron=datos.tiene_padron,
                autoriza_uso_imagen=datos.autoriza_uso_imagen,
                codigo_postal=datos.codigo_postal,
                ciudad_residencia=datos.ciudad_residencia,
                
                # Opcionales añadidos del Excel
                unidad_familiar=datos.unidad_familiar,
                contacto_emergencia_nombre=datos.contacto_emergencia_nombre,
                contacto_emergencia_parentesco=datos.contacto_emergencia_parentesco,
                contacto_emergencia_telefono=datos.contacto_emergencia_telefono,
                fecha_padron=datos.fecha_padron,
                id_motivo_consulta=id_motivo,
                id_nivel_educativo=id_nivel,
                id_derivacion=id_derivacion,
                id_tecnica_acogida=id_tecnica
            )
            
            persona_guardada = self.repo.crear_persona(nueva_persona)
            
            estado_externo = self.repo_roles.obtener_estado_por_nombre("Externo")
            if not estado_externo:
                raise ValueError("El estado 'Externo' no existe en la base de datos.")
                
            self.repo_roles.asignar_estado_en_pivote(persona_guardada.id, estado_externo.id)
            
            # Registrar telefono si viene
            if datos.telefono_principal:
                nuevo_telefono = Telefono(
                    numero=datos.telefono_principal,
                    tipo="Principal",
                    id_persona=persona_guardada.id
                )
                self.session.add(nuevo_telefono)
            
            self.session.commit()
            self.session.refresh(persona_guardada)
            return persona_guardada
        except IntegrityError as e:
            self.session.rollback()
            # Identificamos si el error es por correo o por numero de identificacion
            mensaje = str(e.orig)
            if "correo" in mensaje:
                detalle = "Ya existe una persona registrada con este correo electrónico."
            elif "numero_identificacion" in mensaje:
                detalle = "Ya existe una persona registrada con este número de identificación."
            else:
                detalle = "Ya existe un registro con un valor único que intentas duplicar."
            raise HTTPException(status_code=400, detail=detalle)
        except Exception as e:
            self.session.rollback()
            raise HTTPException(status_code=500, detail=f"Error al registrar la persona: {str(e)}")


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
            
        try:
            self.session.add(persona_db)
            self.session.commit()
            self.session.refresh(persona_db)
            return persona_db
        except IntegrityError as e:
            self.session.rollback()
            mensaje = str(e.orig)
            if "correo" in mensaje:
                detalle = "Ya existe otra persona registrada con este correo electrónico."
            elif "numero_identificacion" in mensaje:
                detalle = "Ya existe otra persona registrada con este número de identificación."
            else:
                detalle = f"Error de unicidad: {mensaje}"
            raise HTTPException(status_code=400, detail=detalle)
        except Exception as e:
            self.session.rollback()
            raise HTTPException(status_code=500, detail=f"Error al actualizar la persona: {str(e)}")
        
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

    def obtener_todas_las_personas(self, skip: int = 0, limit: int = 50, busqueda_nombre: str = None) -> list[Persona]:
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