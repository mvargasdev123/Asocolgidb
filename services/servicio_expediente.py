from fastapi import HTTPException
from models.expediente import Expediente
from schemas.expediente_schema import ExpedienteCreate, ExpedienteUpdate 

class ServicioExpediente:
    # Inyectamos ambos repositorios al servicio
    def __init__(self, repo_expediente, repo_persona):
        self.repo_expediente = repo_expediente
        self.repo_persona = repo_persona

    def crear_nuevo_expediente(self, id_persona: int, datos_entrada: ExpedienteCreate) -> Expediente:
        # REGLA 1: Verificar que la persona exista y sacar sus roles
        persona = self.repo_persona.obtener_por_id(id_persona)
        if not persona:
            raise HTTPException(status_code=404, detail="Persona no encontrada en el sistema.")

        # Buscamos en su lista de estados si tiene el rol supremo
        es_asociado = any(estado.nombre_estado == "Asociado" for estado in persona.estados)
        if not es_asociado:
            raise HTTPException(
                status_code=403, 
                detail="¡Acceso Denegado! Solo los miembros con estado 'Asociado' pueden abrir expedientes legales."
            )

        # REGLA 2: No puede tener dos expedientes activos
        expediente_activo = self.repo_expediente.obtener_activo_por_persona(id_persona)
        if expediente_activo:
            raise HTTPException(
                status_code=400, 
                detail=f"Operación bloqueada. El asociado ya tiene el expediente '{expediente_activo.numero_registro}' en trámite."
            )

        # Si sobrevive a la inquisición, lo guardamos
        nuevo_expediente = Expediente(
            id_persona=id_persona,
            numero_registro=datos_entrada.numero_registro,
            tipo_tramite=datos_entrada.tipo_tramite,
            fecha_presentacion=datos_entrada.fecha_presentacion,
            numero_expediente_asignado=datos_entrada.numero_expediente_asignado,
            representante_legal=datos_entrada.representante_legal,
            consultorio_juridico=datos_entrada.consultorio_juridico,
            aporte_social=datos_entrada.aporte_social,
            solicitante_extranjeria=datos_entrada.solicitante_extranjeria,
            antecedentes_traducidos_y_apostillados=datos_entrada.antecedentes_traducidos_y_apostillados,
            fecha_resolucion=datos_entrada.fecha_resolucion
        )
        
        return self.repo_expediente.crear(nuevo_expediente)

    def obtener_expedientes_persona(self, id_persona: int) -> list[Expediente]:
        persona = self.repo_persona.obtener_por_id(id_persona)
        if not persona:
            raise HTTPException(status_code=404, detail="Persona no encontrada.")
        return self.repo_expediente.obtener_por_persona(id_persona)

    def obtener_expediente(self, id_expediente: int) -> Expediente:
        expediente = self.repo_expediente.obtener_por_id(id_expediente)
        if not expediente:
            raise HTTPException(status_code=404, detail="Expediente no encontrado.")
        return expediente

    def actualizar_expediente(self, id_expediente: int, datos_entrada: ExpedienteUpdate) -> Expediente:
        expediente = self.obtener_expediente(id_expediente)
        
        datos_actualizar = datos_entrada.dict(exclude_unset=True)
        for key, value in datos_actualizar.items():
            setattr(expediente, key, value)
            
        self.repo_expediente.session.add(expediente)
        self.repo_expediente.session.commit()
        self.repo_expediente.session.refresh(expediente)
        return expediente

    def borrar_expediente(self, id_expediente: int):
        expediente = self.obtener_expediente(id_expediente)
        self.repo_expediente.eliminar(expediente)
        return {"mensaje": "Expediente eliminado con éxito."}
