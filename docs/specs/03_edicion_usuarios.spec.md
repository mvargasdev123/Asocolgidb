# Especificación: 03_edicion_usuarios

## 1. Contexto y Usuario
El módulo de Edición de Miembros permite a los gestores modificar la información de una persona ya registrada en Asocolgi.
**Nota Arquitectónica:** A diferencia de la creación, la edición trae retos de integridad de datos (ej. qué hacer con la información si un miembro pierde su rol de Asociado o Voluntario). El sistema debe ser precavido para evitar la pérdida de datos históricos accidentales.

## 2. Historia de Usuario
* **Como** gestor de la base de datos,
* **Quiero** poder abrir el perfil de cualquier persona y modificar su información o cambiar sus roles (ej. pasarlo de Externo a Voluntario).
* **Para** mantener la base de datos actualizada y reflejar la realidad de la fundación.

## 3. Requisitos Funcionales (E.A.R.S)

### 3.1 Carga de Datos y Formulario (Ubiquitous)
* **El sistema deberá** utilizar exactamente el mismo componente de formulario (Drawer de 7 secciones) usado en la creación, pero con todos los campos pre-llenados con la información actual de la base de datos.
* **El sistema deberá** marcar las casillas de "Asociado" o "Voluntario" automáticamente si la persona posee esos roles activos.

### 3.2 Modificación de Datos y Registro de Visitas (Event-driven)
* **Cuando** el usuario envíe el formulario de edición, **el sistema deberá** actualizar únicamente los campos que sufrieron cambios respecto a la versión original.
* **Cuando** el gestor marque una casilla de rol que antes no estaba marcada (Ej. hacer Voluntario a alguien que era Externo), **el sistema deberá** crear el registro correspondiente en la tabla de roles y enlazarlo a la Persona.
* **Cuando** la persona asista nuevamente a la asociación y el gestor registre su asistencia, **el sistema deberá** incrementar su "Contador de Visitas" en +1.

### 3.3 Protección de Datos y Pérdida de Roles (Unwanted Behavior / State-driven)
* **Si** el gestor desmarca la casilla de un rol que la persona ya tenía (Ej. quitarle el rol de "Asociado"), **entonces el sistema deberá** cambiar su estado a `es_asociado = false`, pero **TIENE ESTRICTAMENTE PROHIBIDO** borrar los datos financieros o históricos asociados a esa persona en la base de datos. Los datos quedarán "hibernados" u ocultos por si se reactiva en el futuro.
* **Si** el gestor modifica el campo "Número de Identificación" a uno que ya pertenece a otra persona distinta, **entonces el sistema deberá** bloquear el guardado, retornar un error `409 Conflict` y mostrar la alerta: "Este Número de Documento ya está asignado a otro usuario".

## 4. Contratos y Tipos (Pydantic / Dart Classes)

**Request Estándar PATCH (Frontend -> Backend):**
*(Nota: Al ser una edición, se espera recibir el ID interno de la persona en la URL `PATCH /usuarios/{id}` y en el cuerpo del JSON solo la información modificada o la información completa actualizada).*

```json
{
  "persona_id": 142,
  "identificacion": {
    "tipo_documento": "NIF/NIE",
    "numero_identificacion": "Y1234567X", 
    "nacionalidad": "Colombia" 
  },
  "es_asociado": false, 
  "es_voluntario": true,
  "datos_voluntario": {
    "cargo": "Organizador",
    "horas_semana": 5
  }
}
```

## 5. Criterios de Aceptación (Gherkin)

```gherkin
Scenario: Desactivación segura de un rol (Prevención de pérdida de datos)
  Given una persona que actualmente es Asociado y tiene datos de pago registrados
  When el gestor edita su perfil, desmarca la casilla "Asociado" y guarda los cambios
  Then el backend actualiza la propiedad es_asociado a false
  And el backend NO ejecuta un comando DELETE sobre la tabla de datos del asociado
  And al recargar la vista, el formulario oculta la sección de pagos
```
