from sqlmodel import Session
from fastapi import HTTPException
from repositories.repositorio_roles import RepositorioRoles
from repositories.repositorio_persona import RepositorioPersona
from models.datos_voluntario import DatosVoluntario
from models.datos_asociado import DatosAsociado
from models.datos_contratado import DatosContratado
from schemas.roles_schema import VoluntarioCreate, AsociadoCreate, ContratadoCreate

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
            # 1. Llamamos a la función genérica
            nombre = self._transicion_estado_base(id_persona, "Voluntario")
            
            # 2. Hacemos lo específico de este rol
            nuevo_registro = DatosVoluntario(
                id_persona=id_persona,
                area_voluntariado=datos.area_voluntariado,
                horas_disponibles=datos.horas_disponibles,
                fecha_inicio=datos.fecha_inicio
            )
            self.repo_roles.crear_registro_voluntario(nuevo_registro)
            
            # 3. Confirmamos transacción global
            self.session.commit()
            return {"mensaje": f"Éxito: {nombre} ahora es Voluntario en Asocolgi."}
            
        # Si falló una validación arriba (ej. HTTPException de NotFound), la dejamos pasar
        except HTTPException:
            raise
        except Exception as e:
            self.session.rollback()
            raise HTTPException(status_code=500, detail=f"Fallo en transacción: {str(e)}")

    def ascender_a_asociado(self, id_persona: int, datos: AsociadoCreate):
        try:
            nombre = self._transicion_estado_base(id_persona, "Asociado")
            nuevo_registro = DatosAsociado(
                id_persona=id_persona,
                tramites=datos.tramites, # O como lo hayas definido en tu Pydantic
                fecha_inicio=datos.fecha_inicio
            )
            self.repo_roles.crear_registro_asociado(nuevo_registro)
            self.session.commit()
            return {"mensaje": f"Éxito: {nombre} ahora es Asociado de Asocolgi."}
        except HTTPException:
            raise
        except Exception as e:
            self.session.rollback()
            raise HTTPException(status_code=500, detail=f"Fallo en transacción: {str(e)}")

    def ascender_a_contratado(self, id_persona: int, datos: ContratadoCreate):
        try:
            nombre = self._transicion_estado_base(id_persona, "Contratado")
            nuevo_registro = DatosContratado(
                id_persona=id_persona,
                funcion=datos.funcion,
                horas_contratadas=datos.horas_contratadas,
                fecha_inicio=datos.fecha_inicio,
                fecha_termino=datos.fecha_termino # Puede ser None
            )
            self.repo_roles.crear_registro_contratado(nuevo_registro)
            self.session.commit()
            return {"mensaje": f"Éxito: {nombre} ahora es personal Contratado."}
        except HTTPException:
            raise
        except Exception as e:
            self.session.rollback()
            raise HTTPException(status_code=500, detail=f"Fallo en transacción: {str(e)}")

    def remover_rol(self, id_persona: int, nombre_rol_a_quitar: str):
        try:
            persona = self.repo_persona.obtener_por_id(id_persona)
            if not persona:
                raise HTTPException(status_code=404, detail="Persona no encontrada.")

            estado_a_quitar = self.repo_roles.obtener_estado_por_nombre(nombre_rol_a_quitar)
            if not estado_a_quitar:
                raise HTTPException(status_code=404, detail="El rol especificado no existe.")

            # 1. Verificamos si realmente tiene el rol que queremos quitar
            if not self.repo_roles.verificar_estado_persona(id_persona, estado_a_quitar.id):
                raise HTTPException(status_code=400, detail=f"La persona no tiene el rol de {nombre_rol_a_quitar}.")

            # 2. Le quitamos la etiqueta en la tabla pivote
            self.repo_roles.remover_estado_en_pivote(id_persona, estado_a_quitar.id)

            # 3. LA REGLA DE ORO: Verificamos si se quedó sin roles
            # Para esto, refrescamos a la persona (aunque en memoria SQLModel ya debería saberlo)
            # Si su lista de estados quedó vacía, le devolvemos el estado "Externo"
            roles_restantes = [est for est in persona.estados if est.nombre_estado != nombre_rol_a_quitar]
            
            if len(roles_restantes) == 0:
                estado_externo = self.repo_roles.obtener_estado_por_nombre("Externo")
                self.repo_roles.asignar_estado_en_pivote(id_persona, estado_externo.id)

            # OJO: Aquí deberíamos añadir lógica para "cerrar" o "eliminar" 
            # el registro en la tabla hija (ej. datos_voluntario), pero lo haremos 
            # más adelante o le pondremos una "fecha_termino".

            self.session.commit()
            return {"mensaje": f"Éxito: Se ha removido el rol de {nombre_rol_a_quitar} a {persona.nombre}."}

        except HTTPException:
            raise
        except Exception as e:
            self.session.rollback()
            raise HTTPException(status_code=500, detail=f"Fallo al remover rol: {str(e)}")