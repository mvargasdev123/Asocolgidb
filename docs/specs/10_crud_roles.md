# Especificación: 09_listado_y_navegacion

## 1. Contexto y Usuario
Vamos a separar la parte de persona de los roles para su facilidad de manejo y como mejora de la api va a ser de lado del programador 

## 2. Historia de Usuario
En este momento el post de persona se ve tal que así

{
  "identificacion": {
    "tipo_documento": "string",
    "numero_identificacion": "string",
    "nacionalidad": "string"
  },
  "datos_personales": {
    "nombre_completo": "string",
    "fecha_nacimiento": "2026-09-06",
    "genero": "string",
    "correo_electronico": "string",
    "direccion_residencia": "string",
    "codigo_postal": "string",
    "ciudad": "string"
  },
  "situacion_social": {
    "situacion_admin": "string",
    "unidad_familiar": 0,
    "madre_soltera": "string",
    "violencia_genero": "string",
    "nivel_educativo": "string"
  },
  "legal_acogida": {
    "tiene_padron": true,
    "fecha_padron": "2026-09-06",
    "motivo_consulta": "string",
    "derivacion": "string",
    "tecnica_acogida": "string",
    "autoriza_datos": true,
    "autoriza_imagen": true
  },
  "contacto_emergencia": {
    "nombre": "string",
    "parentesco": "string",
    "telefono": "string"
  },
  "es_asociado": false,
  "datos_asociado": {
    "metodo_pago": "string",
    "estado_membresia": "string",
    "estado_pago": "string",
    "autoriza_whatsapp": true
  },
  "es_voluntario": false,
  "datos_voluntario": {
    "cargo": "string",
    "campo_accion": "string",
    "tipo": "string",
    "horas_semana": 0,
    "url_doc": "string",
    "url_cv": "string",
    "carta_compromiso_firmada": true,
    "formulario_inscripcion": true
  }
}

La idea es hacer un crud para Voluntario y un crud de Asociado 
- Y hagregar en asocociado el dato opcional "fecha vinculacion" para desde ahi en su get calcular su antiguedad 


