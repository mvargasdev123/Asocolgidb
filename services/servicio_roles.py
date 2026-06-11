from sqlmodel import Session
from fastapi import HTTPException
from repositories.repositorio_roles import RepositorioRoles
from repositories.repositorio_persona import RepositorioPersona
from models.datos_voluntario import DatosVoluntario
from schemas.roles_schema import VoluntarioCreate

class ServicioRoles:
    def __init__(self, session: Session):
        self.session = session
        # Este servicio necesita DOS músculos para trabajar, así que instanciamos ambos repos
        self.repo_roles = RepositorioRoles(session)
        self.repo_persona = RepositorioPersona(session)

    def ascender_a_voluntario(self, id_persona: int, datos: VoluntarioCreate):
        # 1. Verificar que el humano existe en la base de datos
        persona = self.repo_persona.obtener_por_id(id_persona)
        if not persona:
            raise HTTPException(status_code=404, detail="La persona no existe. No podemos mutar fantasmas.")

        # 2. Traer los IDs de los estados clave de nuestra tabla de diccionario
        estado_externo = self.repo_roles.obtener_estado_por_nombre("Externo")
        estado_voluntario = self.repo_roles.obtener_estado_por_nombre("Voluntario")

        # Esto nunca debería pasar si el 'seeding' funcionó, pero un buen backend asume el desastre
        if not estado_externo or not estado_voluntario:
            raise HTTPException(status_code=500, detail="Error crítico: Los estados base no están configurados.")

        # 3. Verificar si ya es voluntario (para no duplicar registros y que explote la relación 1:1)
        es_voluntario = self.repo_roles.verificar_estado_persona(id_persona, estado_voluntario.id)
        if es_voluntario:
            raise HTTPException(status_code=400, detail="Tranquilo, esta persona ya es voluntaria en Asocolgi.")

        try:
            # 4. Quitarle la etiqueta de 'Externo' (si la tiene, el repositorio la borra)
            self.repo_roles.remover_estado_en_pivote(id_persona, estado_externo.id)

            # 5. Colgarle la nueva medalla de 'Voluntario' en la tabla pivote
            self.repo_roles.asignar_estado_en_pivote(id_persona, estado_voluntario.id)

            # 6. Crear su ficha técnica y llenarla con los datos validados del Schema
            nuevo_registro = DatosVoluntario(
                id_persona=id_persona,
                area_voluntariado=datos.area_voluntariado,
                horas_disponibles=datos.horas_disponibles,
                fecha_inicio=datos.fecha_inicio
            )
            self.repo_roles.crear_registro_voluntario(nuevo_registro)

            # 7. EL MOMENTO DE LA VERDAD: Confirmar todos los cambios en bloque
            self.session.commit()
            
            return {"mensaje": f"Éxito: {persona.nombre} ha sido ascendido a Voluntario."}

        except Exception as e:
            # Si CUALQUIER cosa falla arriba, el rollback deshace todo el progreso no guardado
            self.session.rollback()
            raise HTTPException(status_code=500, detail=f"Fallo en la matriz de transición: {str(e)}")