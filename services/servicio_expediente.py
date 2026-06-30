from fastapi import HTTPException
from models.expediente import Expediente
# Asumo que tienes tus esquemas Pydantic creados, usaremos un hipotético ExpedienteCreate
# from schemas.expediente_schema import ExpedienteCreate 

class ServicioExpediente:
    # Inyectamos ambos repositorios al servicio
    def __init__(self, repo_expediente, repo_persona):
        self.repo_expediente = repo_expediente
        self.repo_persona = repo_persona

    def crear_nuevo_expediente(self, datos_entrada) -> Expediente:
        # REGLA 1: Verificar que la persona exista y sacar sus roles
        persona = self.repo_persona.obtener_por_id(datos_entrada.id_persona)
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
        expediente_activo = self.repo_expediente.obtener_activo_por_persona(datos_entrada.id_persona)
        if expediente_activo:
            raise HTTPException(
                status_code=400, 
                detail=f"Operación bloqueada. El asociado ya tiene el expediente '{expediente_activo.numero_registro}' en trámite."
            )

        # Si sobrevive a la inquisición, lo guardamos
        nuevo_expediente = Expediente(
            numero_registro=datos_entrada.numero_registro,
            tipo_tramite=datos_entrada.tipo_tramite,
            fecha_presentacion=datos_entrada.fecha_presentacion,
            # ... el resto de campos mapeados desde Pydantic ...
            id_persona=datos_entrada.id_persona
        )
        
        return self.repo_expediente.crear(nuevo_expediente)
    
