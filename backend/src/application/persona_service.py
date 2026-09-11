from datetime import date, datetime
from fastapi import HTTPException, status
from domain.schemas.persona_schemas import PersonaCreateRequest
from domain.models.persona import Persona
from domain.models.roles import DatosAsociado, DatosVoluntario
from domain.models.catalogos import (
    TipoDocumento, Nacionalidad, Ciudad, NivelEducativo,
    MotivoConsulta, Derivacion, TecnicaAcogida
)
from infrastructure.persona_repository import PersonaRepository

class PersonaService:
    def __init__(self, repository: PersonaRepository):
        self.repository = repository

    def _resolver_catalogo(self, modelo, valor: str | None) -> int | None:
        """Helper para resolver catálogos solo si el valor no es nulo ni vacío."""
        if valor and str(valor).strip():
            return self.repository.get_or_create_catalog(modelo, str(valor).strip())
        return None

    def _obtener_nombre_catalogo(self, modelo, id_val: int | None) -> str | None:
        if id_val is None:
            return None
        item = self.repository.session.get(modelo, id_val)
        return item.nombre if item else None

    def _persona_to_dict(self, persona: Persona) -> dict:
        data = persona.model_dump()
        
        def _fmt_d(d):
            if d is None: return None
            if isinstance(d, datetime): d = d.date()
            if isinstance(d, date): return d.strftime("%m/%d/%Y")
            return str(d)

        data["fecha_nacimiento"] = _fmt_d(persona.fecha_nacimiento)
        data["fecha_atencion"] = _fmt_d(persona.fecha_atencion)
        data["fecha_padron"] = _fmt_d(persona.fecha_padron)
        
        # Resolver nombres de texto de los catálogos dinámicos
        data["tipo_documento"] = self._obtener_nombre_catalogo(TipoDocumento, persona.id_tipo_documento)
        data["nacionalidad"] = self._obtener_nombre_catalogo(Nacionalidad, persona.id_nacionalidad)
        data["ciudad"] = self._obtener_nombre_catalogo(Ciudad, persona.id_ciudad)
        data["nivel_educativo"] = self._obtener_nombre_catalogo(NivelEducativo, persona.id_nivel_educativo)
        data["motivo_consulta"] = self._obtener_nombre_catalogo(MotivoConsulta, persona.id_motivo_consulta)
        data["derivacion"] = self._obtener_nombre_catalogo(Derivacion, persona.id_derivacion)
        data["tecnica_acogida"] = self._obtener_nombre_catalogo(TecnicaAcogida, persona.id_tecnica_acogida)

        es_asoc = persona.datos_asociado is not None and persona.datos_asociado.estado_membresia != "Inactivo"
        es_vol = persona.datos_voluntario is not None
        data["es_asociado"] = es_asoc
        if persona.datos_asociado:
            da_dict = persona.datos_asociado.model_dump()
            da_dict["fecha_vinculacion"] = _fmt_d(persona.datos_asociado.fecha_vinculacion)
            data["datos_asociado"] = da_dict
        else:
            data["datos_asociado"] = None

        data["es_voluntario"] = es_vol
        if persona.datos_voluntario:
            dv_dict = persona.datos_voluntario.model_dump()
            dv_dict["fecha_vinculacion"] = _fmt_d(persona.datos_voluntario.fecha_vinculacion)
            dv_dict["fecha_alta"] = _fmt_d(persona.datos_voluntario.fecha_alta)
            dv_dict["fecha_baja"] = _fmt_d(persona.datos_voluntario.fecha_baja)
            data["datos_voluntario"] = dv_dict
        else:
            data["datos_voluntario"] = None

        return data

    def registrar_persona(self, request: PersonaCreateRequest) -> dict:
        # 1. Validar campos obligatorios de creación (Spec 02)
        if not request.identificacion or not request.identificacion.numero_identificacion or not request.identificacion.numero_identificacion.strip():
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="El Número de Identificación es obligatorio"
            )
        if not request.datos_personales or not request.datos_personales.nombre_completo or not request.datos_personales.nombre_completo.strip():
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="El Nombre Completo es obligatorio"
            )

        num_identificacion = request.identificacion.numero_identificacion.strip()
        if self.repository.existe_numero_identificacion(num_identificacion):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Esta persona ya existe"
            )

        # 2. Mapear JSON anidado a Tabla Aplanada (Persona)
        # 2.1. Resolver catálogos dinámicos (Spec 02, sección 3.2)
        id_tipo_doc = self._resolver_catalogo(TipoDocumento, request.identificacion.tipo_documento)
        id_nacionalidad = self._resolver_catalogo(Nacionalidad, request.identificacion.nacionalidad)
        id_ciudad = self._resolver_catalogo(Ciudad, request.datos_personales.ciudad)
        
        id_nivel_edu = None
        if request.situacion_social:
            id_nivel_edu = self._resolver_catalogo(NivelEducativo, request.situacion_social.nivel_educativo)
            
        id_motivo = None
        id_derivacion = None
        id_tecnica = None
        if request.legal_acogida:
            id_motivo = self._resolver_catalogo(MotivoConsulta, request.legal_acogida.motivo_consulta)
            id_derivacion = self._resolver_catalogo(Derivacion, request.legal_acogida.derivacion)
            id_tecnica = self._resolver_catalogo(TecnicaAcogida, request.legal_acogida.tecnica_acogida)

        # 2.2. Construir la entidad Persona
        nueva_persona = Persona(
            numero_identificacion=num_identificacion,
            nombre_completo=request.datos_personales.nombre_completo,
            fecha_nacimiento=request.datos_personales.fecha_nacimiento,
            fecha_atencion=request.datos_personales.fecha_atencion,
            telefono_principal=request.datos_personales.telefono_principal,
            genero=request.datos_personales.genero,
            correo_electronico=request.datos_personales.correo_electronico,
            direccion_residencia=request.datos_personales.direccion_residencia,
            codigo_postal=request.datos_personales.codigo_postal,
            
            # Catálogos
            id_tipo_documento=id_tipo_doc,
            id_nacionalidad=id_nacionalidad,
            id_ciudad=id_ciudad,
            id_nivel_educativo=id_nivel_edu,
            id_motivo_consulta=id_motivo,
            id_derivacion=id_derivacion,
            id_tecnica_acogida=id_tecnica,
            
            # Situacion Social
            situacion_admin=request.situacion_social.situacion_admin if request.situacion_social else None,
            unidad_familiar=request.situacion_social.unidad_familiar if request.situacion_social else None,
            madre_soltera=request.situacion_social.madre_soltera if request.situacion_social else None,
            violencia_genero=request.situacion_social.violencia_genero if request.situacion_social else None,
            
            # Legal Acogida
            tiene_padron=request.legal_acogida.tiene_padron if request.legal_acogida else None,
            fecha_padron=request.legal_acogida.fecha_padron if request.legal_acogida else None,
            autoriza_datos=request.legal_acogida.autoriza_datos if request.legal_acogida else False,
            autoriza_imagen=request.legal_acogida.autoriza_imagen if request.legal_acogida else False,
            
            # Contacto Emergencia
            contacto_emergencia_nombre=request.contacto_emergencia.nombre if request.contacto_emergencia else None,
            contacto_emergencia_parentesco=request.contacto_emergencia.parentesco if request.contacto_emergencia else None,
            contacto_emergencia_telefono=request.contacto_emergencia.telefono if request.contacto_emergencia else None,
            
            # Inicialización de Visitas Obligatorio (Spec 02, sección 3.2)
            contador_visitas=1
        )

        # 3. Mapear roles adicionales si existen
        asociado = None
        if request.es_asociado and request.datos_asociado:
            asociado = DatosAsociado(
                metodo_pago=request.datos_asociado.metodo_pago,
                estado_membresia=request.datos_asociado.estado_membresia or "Activo",
                estado_pago=request.datos_asociado.estado_pago,
                autoriza_whatsapp=request.datos_asociado.autoriza_whatsapp,
                fecha_vinculacion=request.datos_asociado.fecha_vinculacion
            )
            
        voluntario = None
        if request.es_voluntario:
            vd = request.datos_voluntario
            voluntario = DatosVoluntario(
                cargo=vd.cargo if vd else None,
                campo_accion=vd.campo_accion if vd else None,
                tipo=vd.tipo if vd else None,
                horas_semana=vd.horas_semana if vd else None,
                url_doc=vd.url_doc if vd else None,
                url_cv=vd.url_cv if vd else None,
                fecha_vinculacion=vd.fecha_vinculacion if vd else None,
                fecha_alta=vd.fecha_alta if vd else None,
                fecha_baja=vd.fecha_baja if vd else None,
                carta_compromiso_firmada=vd.carta_compromiso_firmada if vd else False,
                formulario_inscripcion=vd.formulario_inscripcion if vd else False,
            )

        # 4. Guardar todo en una transacción
        persona_creada = self.repository.create_persona(nueva_persona, asociado, voluntario)
        
        return self._persona_to_dict(persona_creada)

    def obtener_todas(
        self,
        last_id: int | None = None,
        limit: int = 10,
        search: str | None = None,
        genero: str | None = None,
        rol: str | None = None,
        situacion_admin: str | None = None
    ) -> list[dict]:
        personas = self.repository.get_all_activas(
            last_id=last_id,
            limit=limit,
            search=search,
            genero=genero,
            rol=rol,
            situacion_admin=situacion_admin
        )
        return [self._persona_to_dict(p) for p in personas]

    def obtener_por_id(self, persona_id: int) -> Persona:
        persona = self.repository.get_by_id(persona_id)
        if not persona:
            raise HTTPException(status_code=404, detail="Persona no encontrada")
        return persona

    def obtener_por_id_dict(self, persona_id: int) -> dict:
        persona = self.obtener_por_id(persona_id)
        return self._persona_to_dict(persona)

    def actualizar_persona(self, persona_id: int, request) -> dict:
        persona = self.obtener_por_id(persona_id)

        if request.identificacion:
            if request.identificacion.numero_identificacion:
                num = request.identificacion.numero_identificacion.strip()
                if num != persona.numero_identificacion:
                    if self.repository.existe_numero_identificacion(num):
                        raise HTTPException(status_code=409, detail="Este Número de Documento ya está asignado a otro usuario")
                    persona.numero_identificacion = num
            
            if request.identificacion.tipo_documento is not None:
                persona.id_tipo_documento = self._resolver_catalogo(TipoDocumento, request.identificacion.tipo_documento)
            if request.identificacion.nacionalidad is not None:
                persona.id_nacionalidad = self._resolver_catalogo(Nacionalidad, request.identificacion.nacionalidad)

        if request.datos_personales:
            dp = request.datos_personales
            if dp.nombre_completo is not None: persona.nombre_completo = dp.nombre_completo
            if dp.fecha_nacimiento is not None: persona.fecha_nacimiento = dp.fecha_nacimiento
            if dp.fecha_atencion is not None: persona.fecha_atencion = dp.fecha_atencion
            if dp.telefono_principal is not None: persona.telefono_principal = dp.telefono_principal
            if dp.genero is not None: persona.genero = dp.genero
            if dp.correo_electronico is not None: persona.correo_electronico = dp.correo_electronico
            if dp.direccion_residencia is not None: persona.direccion_residencia = dp.direccion_residencia
            if dp.codigo_postal is not None: persona.codigo_postal = dp.codigo_postal
            if dp.ciudad is not None:
                persona.id_ciudad = self._resolver_catalogo(Ciudad, dp.ciudad)

        if request.situacion_social:
            ss = request.situacion_social
            if ss.situacion_admin is not None: persona.situacion_admin = ss.situacion_admin
            if ss.unidad_familiar is not None: persona.unidad_familiar = ss.unidad_familiar
            if ss.madre_soltera is not None: persona.madre_soltera = ss.madre_soltera
            if ss.violencia_genero is not None: persona.violencia_genero = ss.violencia_genero
            if ss.nivel_educativo is not None:
                persona.id_nivel_educativo = self._resolver_catalogo(NivelEducativo, ss.nivel_educativo)

        if request.legal_acogida:
            la = request.legal_acogida
            if la.tiene_padron is not None: persona.tiene_padron = la.tiene_padron
            if la.fecha_padron is not None: persona.fecha_padron = la.fecha_padron
            if la.autoriza_datos is not None: persona.autoriza_datos = la.autoriza_datos
            if la.autoriza_imagen is not None: persona.autoriza_imagen = la.autoriza_imagen
            if la.motivo_consulta is not None:
                persona.id_motivo_consulta = self._resolver_catalogo(MotivoConsulta, la.motivo_consulta)
            if la.derivacion is not None:
                persona.id_derivacion = self._resolver_catalogo(Derivacion, la.derivacion)
            if la.tecnica_acogida is not None:
                persona.id_tecnica_acogida = self._resolver_catalogo(TecnicaAcogida, la.tecnica_acogida)

        if request.contacto_emergencia:
            ce = request.contacto_emergencia
            if ce.nombre is not None: persona.contacto_emergencia_nombre = ce.nombre
            if ce.parentesco is not None: persona.contacto_emergencia_parentesco = ce.parentesco
            if ce.telefono is not None: persona.contacto_emergencia_telefono = ce.telefono

        # Actualización de Roles (Asociado / Voluntario)
        if request.es_asociado is not None:
            if request.es_asociado == False and persona.datos_asociado:
                persona.datos_asociado.estado_membresia = "Inactivo"
            elif request.es_asociado == True:
                if not persona.datos_asociado:
                    asoc_data = request.datos_asociado
                    persona.datos_asociado = DatosAsociado(
                        id_persona=persona.id,
                        metodo_pago=asoc_data.metodo_pago if asoc_data else 'Efectivo',
                        estado_membresia='Activo',
                        estado_pago=asoc_data.estado_pago if asoc_data else 'Al día',
                        autoriza_whatsapp=asoc_data.autoriza_whatsapp if asoc_data else False,
                        fecha_vinculacion=asoc_data.fecha_vinculacion if asoc_data else None,
                    )
                else:
                    persona.datos_asociado.estado_membresia = "Activo"
                    if request.datos_asociado:
                        ad = request.datos_asociado
                        if ad.metodo_pago: persona.datos_asociado.metodo_pago = ad.metodo_pago
                        if ad.estado_membresia: persona.datos_asociado.estado_membresia = ad.estado_membresia
                        if ad.estado_pago: persona.datos_asociado.estado_pago = ad.estado_pago
                        if ad.autoriza_whatsapp is not None: persona.datos_asociado.autoriza_whatsapp = ad.autoriza_whatsapp
                        if ad.fecha_vinculacion is not None: persona.datos_asociado.fecha_vinculacion = ad.fecha_vinculacion

        if request.es_voluntario is not None:
            if request.es_voluntario == False and persona.datos_voluntario:
                self.repository.session.delete(persona.datos_voluntario)
                persona.datos_voluntario = None
            elif request.es_voluntario == True:
                vd = request.datos_voluntario
                if not persona.datos_voluntario:
                    persona.datos_voluntario = DatosVoluntario(
                        id_persona=persona.id,
                        cargo=vd.cargo if vd else None,
                        campo_accion=vd.campo_accion if vd else None,
                        tipo=vd.tipo if vd else None,
                        horas_semana=vd.horas_semana if vd else None,
                        url_doc=vd.url_doc if vd else None,
                        url_cv=vd.url_cv if vd else None,
                        fecha_vinculacion=vd.fecha_vinculacion if vd else None,
                        fecha_alta=vd.fecha_alta if vd else None,
                        fecha_baja=vd.fecha_baja if vd else None,
                        carta_compromiso_firmada=vd.carta_compromiso_firmada if vd else False,
                        formulario_inscripcion=vd.formulario_inscripcion if vd else False,
                    )
                elif vd:
                    if vd.cargo is not None: persona.datos_voluntario.cargo = vd.cargo
                    if vd.campo_accion is not None: persona.datos_voluntario.campo_accion = vd.campo_accion
                    if vd.tipo is not None: persona.datos_voluntario.tipo = vd.tipo
                    if vd.horas_semana is not None: persona.datos_voluntario.horas_semana = vd.horas_semana
                    if vd.url_doc is not None: persona.datos_voluntario.url_doc = vd.url_doc
                    if vd.url_cv is not None: persona.datos_voluntario.url_cv = vd.url_cv
                    if vd.fecha_vinculacion is not None: persona.datos_voluntario.fecha_vinculacion = vd.fecha_vinculacion
                    if vd.fecha_alta is not None: persona.datos_voluntario.fecha_alta = vd.fecha_alta
                    if vd.fecha_baja is not None: persona.datos_voluntario.fecha_baja = vd.fecha_baja
                    if vd.carta_compromiso_firmada is not None: persona.datos_voluntario.carta_compromiso_firmada = vd.carta_compromiso_firmada
                    if vd.formulario_inscripcion is not None: persona.datos_voluntario.formulario_inscripcion = vd.formulario_inscripcion

        updated = self.repository.update_persona(persona)
        return self._persona_to_dict(updated)

    def eliminar_persona(self, persona_id: int):
        persona = self.obtener_por_id(persona_id)
        self.repository.soft_delete(persona)
