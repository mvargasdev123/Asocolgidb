# Especificación: 04_gestion_comentarios

## 1. Contexto y Usuario
El módulo de Gestión de Comentarios permite a los gestores añadir anotaciones, notas o historial de interacciones al perfil de cualquier miembro (Asociado, Voluntario o Externo). Estos comentarios funcionan como un registro cronológico de la relación entre la persona y Asocolgi.

## 2. Historia de Usuario
* **Como** gestor de la base de datos,
* **Quiero** poder agregar, editar y eliminar comentarios en el perfil de una persona, eligiendo a qué categoría pertenece el comentario (Persona, Voluntario, Asociado, Expediente).
* **Para** llevar un historial detallado de las interacciones.
* **Además**, quiero que el recuadro de texto crezca automáticamente según lo que yo escriba (para que sea cómodo leer textos largos) y que el sistema le ponga automáticamente la fecha del día sin que yo tenga que teclearla.

## 3. Requisitos Funcionales (E.A.R.S)

### 3.1 Interfaz y Flujo Básico (Ubiquitous)
* **El sistema deberá** renderizar un componente de "Gestión de Comentarios" dentro del perfil de la persona.
* **El sistema deberá** tener un menú desplegable (Dropdown) con los siguientes tipos obligatorios: `Persona`, `Voluntario`, `Asociado`, `Expediente`.
* **El sistema deberá** permitir la edición y eliminación de comentarios existentes (CRUD).

### 3.2 Experiencia de Usuario (State-driven)
* **Mientras** el gestor escribe en el recuadro del nuevo comentario, **el sistema deberá** expandir dinámicamente la altura de la caja de texto (Auto-expanding TextField en Flutter) para evitar el colapso visual de comentarios largos.

### 3.3 Lógica de Guardado (Event-driven)
* **Cuando** el usuario envíe un nuevo comentario, **el sistema deberá** capturar la fecha y hora actual del servidor automáticamente y adjuntarla al registro.
* **Cuando** el comentario se guarde exitosamente, **el sistema deberá** mostrarlo en la lista cronológica del perfil.

### 3.4 Validaciones (Unwanted Behavior)
* **Si** el usuario intenta guardar un comentario con el texto completamente vacío, **entonces el sistema deberá** bloquear la acción y mantener deshabilitado el botón de envío.

## 4. Contratos y Tipos (Pydantic / Dart Classes)

**Request POST - Crear Comentario (Frontend -> Backend):**
*(Nota: El frontend no envía la fecha, la genera el servidor por seguridad).*

```json
{
  "persona_id": 142,
  "texto": "El usuario se presentó hoy para preguntar sobre los trámites de extranjería. Se le derivó al abogado...",
  "tipo": "Persona"
}
```

**Response Éxito (Backend -> Frontend):**
```json
{
  "id": 894,
  "persona_id": 142,
  "texto": "El usuario se presentó hoy para preguntar...",
  "tipo": "Persona",
  "fecha_creacion": "2026-09-05T10:30:00Z"
}
```

## 5. Criterios de Aceptación (Gherkin)

```gherkin
Scenario: Creación de comentario con fecha automática
  Given el gestor está en el perfil del usuario Miguel
  When el gestor escribe un texto válido, selecciona el tipo "Expediente" y presiona enviar
  Then el backend recibe el payload y le asigna el timestamp actual
  And el backend retorna el comentario guardado
  And el frontend pinta el comentario en la lista mostrando la fecha de hoy
```
