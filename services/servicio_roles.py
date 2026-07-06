from sqlmodel import Session
from fastapi import HTTPException
from datetime import date
from repositories.repositorio_roles import RepositorioRoles
from repositories.repositorio_persona import RepositorioPersona
from models.datos_voluntario import DatosVoluntario
from models.datos_asociado import DatosAsociado, EstadoAsociadoEnum
from schemas.roles_schema import VoluntarioCreate, VoluntarioUpdate, AsociadoCreate

class ServicioRoles:
    def __init__(self, session: Session):
        self.session = session
        self.repo_roles = RepositorioRoles(session)
        self.repo_persona = RepositorioPersona(session)

    # --- EL MOTOR CENTRAL DE TRANSICIONES (PRIVADO) ---
    def _transicion_estado_base(self, id_persona: int, nombre_nuevo_estado: str) -> str:
        """
        Hace el trabajo sucio genérico: Verifica la persona, retira la etiqueta 
        de Externo y pone la nueva etiqueta en la tabla pivote. 
        Devuelve el nombre de la persona para usarlo en los mensajes de éxito.
        """
        persona = self.repo_persona.obtener_por_id(id_persona)
        if not persona:
            raise HTTPException(status_code=404, detail="Persona no encontrada.")

        estado_externo = self.repo_roles.obtener_estado_por_nombre("Externo")
        nuevo_estado = self.repo_roles.obtener_estado_por_nombre(nombre_nuevo_estado)

        if not estado_externo or not nuevo_estado:
            raise HTTPException(status_code=500, detail="Estados base no configurados.")

        # Si ya tiene el rol, bloqueamos para no duplicar llaves en la base de datos
        if self.repo_roles.verificar_estado_persona(id_persona, nuevo_estado.id):
            raise HTTPException(status_code=400, detail=f"Ya posee el rol de {nombre_nuevo_estado}.")

        # Ejecutamos los cambios en la pivote (sin hacer commit todavía)
        self.repo_roles.remover_estado_en_pivote(id_persona, estado_externo.id)
        self.repo_roles.asignar_estado_en_pivote(id_persona, nuevo_estado.id)
        
        return persona.nombre

    # --- LOS MÉTODOS PÚBLICOS LIMPIOS ---
    
    def ascender_a_voluntario(self, id_persona: int, datos: VoluntarioCreate):
        try:
            nombre = self._transicion_estado_base(id_persona, "Voluntario")
            
            nuevo_registro = DatosVoluntario(
                id_persona=id_persona,
                cargo=datos.cargo,
                campo_accion=datos.campo_accion,
                tipo_voluntariado=datos.tipo_voluntariado,
                horas_disponibles=datos.horas_disponibles,
                carta_compromiso_entregada=datos.carta_compromiso_entregada,
                formulario_inscripcion_entregado=datos.formulario_inscripcion_entregado,
                copia_documento_url=datos.copia_documento_url,
                curriculum_url=datos.curriculum_url
            )
            
            # Tu repositorio debe tener esta función (igualita a la de asociado pero con un session.add)
            self.repo_roles.crear_registro_voluntario(nuevo_registro) 
            self.session.commit()
            
            return {"mensaje": f"Éxito: {nombre} ha sido condenado a trabajo no remunerado como Voluntario."}
        
        except HTTPException:
            raise
        except Exception as e:
            self.session.rollback()
            raise HTTPException(status_code=500, detail=f"Fallo al guardar voluntario: {str(e)}")

    def actualizar_datos_voluntario(self, id_persona: int, datos: VoluntarioUpdate) -> DatosVoluntario:
        datos_voluntario = self.repo_roles.obtener_datos_voluntario_por_persona(id_persona)
        if not datos_voluntario:
            raise HTTPException(status_code=404, detail="La persona no es voluntario o no se encontraron sus datos.")
            
        datos_diccionario = datos.model_dump(exclude_unset=True)
        
        for clave, valor in datos_diccionario.items():
            setattr(datos_voluntario, clave, valor)
            
        try:
            self.session.add(datos_voluntario)
            self.session.commit()
            self.session.refresh(datos_voluntario)
            return datos_voluntario
        except Exception as e:
            self.session.rollback()
            raise HTTPException(status_code=500, detail=f"Error al actualizar voluntario: {str(e)}")

    def obtener_todos_los_voluntarios(self):
        return self.repo_roles.obtener_todas_las_personas_voluntarias()

    def ascender_a_asociado(self, id_persona: int, datos: AsociadoCreate):
        try:
            # Tu función mágica que ya pone la etiqueta en la tabla pivote de forma segura
            nombre = self._transicion_estado_base(id_persona, "Asociado")
            
            # Inyectamos los NUEVOS campos financieros 
            nuevo_registro = DatosAsociado(
                id_persona=id_persona,
                numero_registro_asociado=datos.numero_registro_asociado,
                metodo_pago=datos.metodo_pago,
                autoriza_whatsapp=datos.autoriza_whatsapp,
                estado_membresia=datos.estado_membresia,
                estado_pago=datos.estado_pago
            )
            
            self.repo_roles.crear_registro_asociado(nuevo_registro)
            self.session.commit()
            return {"mensaje": f"Éxito: {nombre} ahora es un honorable Asociado (que paga) en Asocolgi."}
        
        except HTTPException:
            raise
        except Exception as e:
            self.session.rollback()
            raise HTTPException(status_code=500, detail=f"Fallo en transacción financiera: {str(e)}")

    def remover_rol(self, id_persona: int, nombre_rol_a_quitar: str):
        try:
            persona = self.repo_persona.obtener_por_id(id_persona)
            if not persona:
                raise HTTPException(status_code=404, detail="Persona no encontrada.")

            estado_a_quitar = self.repo_roles.obtener_estado_por_nombre(nombre_rol_a_quitar)
            if not estado_a_quitar:
                raise HTTPException(status_code=404, detail="El rol especificado no existe.")

            # 1. Verificamos si realmente tiene el rol
            if not self.repo_roles.verificar_estado_persona(id_persona, estado_a_quitar.id):
                raise HTTPException(status_code=400, detail=f"La persona no tiene el rol de {nombre_rol_a_quitar}.")

            # 2. Le quitamos la etiqueta en la tabla pivote
            self.repo_roles.remover_estado_en_pivote(id_persona, estado_a_quitar.id)

            # --- LA MAGIA DEL SOFT DELETE (Resolviendo tu #OJO) ---
            if nombre_rol_a_quitar == "Asociado":
                # Necesitas que tu repo_roles tenga esta pequeña función para buscar el perfil
                datos_asoc = self.repo_roles.obtener_datos_asociado_por_persona(id_persona)
                if datos_asoc:
                    datos_asoc.estado_membresia = EstadoAsociadoEnum.INACTIVO
                    datos_asoc.fecha_baja = date.today()
                    # Nota: SQLAlchemy detecta el cambio en el objeto y lo guarda en el commit final
            elif nombre_rol_a_quitar == "Voluntario":
                datos_vol = self.repo_roles.obtener_datos_voluntario_por_persona(id_persona)
                if datos_vol:
                    datos_vol.activo = False
                    datos_vol.fecha_baja = date.today()

            # 3. LA REGLA DE ORO: Verificamos si se quedó sin roles
            roles_restantes = [est for est in persona.estados if est.nombre_estado != nombre_rol_a_quitar]
            
            if len(roles_restantes) == 0:
                estado_externo = self.repo_roles.obtener_estado_por_nombre("Externo")
                self.repo_roles.asignar_estado_en_pivote(id_persona, estado_externo.id)

            self.session.commit()
            return {"mensaje": f"Éxito: Se ha removido el rol de {nombre_rol_a_quitar} a {persona.nombre}."}

        except HTTPException:
            raise
        except Exception as e:
            self.session.rollback()
            raise HTTPException(status_code=500, detail=f"Fallo al remover rol: {str(e)}")