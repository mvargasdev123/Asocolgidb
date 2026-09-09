# Especificación: 10_schemas_y_separacion

## 1. Contexto y Usuario

El sistema Asocolgi V2 maneja personas que pueden tener uno o más roles dentro de la organización: **Asociado**, **Voluntario**, **Ambos** (doble rol) o **Externo / Ninguno** (persona registrada sin membresía ni voluntariado).

Esta especificación establece la separación limpia de esquemas, endpoints y servicios CRUD para **Asociados** (`/asociados`) y **Voluntarios** (`/voluntarios`), la auditoría de todos los esquemas Pydantic/OpenAPI (ej. `ExpedienteCreateRequest`), y las reglas de negocio para la emisión de **Expedientes Legales**.

---

## 2. Historias de Usuario

* **Como** gestor de la base de datos,
* **Quiero** crear, editar y consultar personas asignando de forma independiente o simultánea los roles de Asociado y/o Voluntario,
* **Para** mantener la información limpia y acceder a listados/CRUDs dedicados para cada perfil.

* **Como** responsable del área legal,
* **Quiero** garantizar que una persona solo pueda tener un expediente activo en estado `"En tramite"`,
* **Para** prevenir duplicidad de expedientes legales simultáneos para un mismo beneficiario.

* **Como** administrador de datos,
* **Quiero** que al actualizar una persona o importar archivos Excel (`BD`, `ASO`, `VOL`, `EXP`) no se borre ni sobreescriba ningún campo previamente existente,
* **Para** garantizar la integridad total de la información.

---

## 3. Requisitos Funcionales (E.A.R.S)

### 3.1 Gestión de Roles y Estados de Persona

#### Caso 1: Edición de Persona Existente
* **Cuando** el usuario edita una persona existente y marca la casilla "Registrar como Voluntario" (o "Registrar como Asociado"), **el sistema deberá** desplegar los campos correspondientes del rol y crear/actualizar los datos de voluntario/asociado sin eliminar la información del rol ya existente.
* **Mientras** una persona tenga marcadas ambas casillas (`es_asociado = True` y `es_voluntario = True`), **el sistema deberá** mostrar ambos perfiles en la vista de detalle y asignarle los badges `[Asociado]` y `[Voluntario]`.

#### Caso 2: Creación de Nueva Persona
* **Cuando** se registra una nueva persona desde cero, **el sistema deberá** permitir marcar opcionalmente una o ambas casillas ("Registrar como Asociado", "Registrar como Voluntario") y registrar los datos personales junto con las entidades asociadas en una sola transacción atómica.

#### Caso 3: Importación desde Excel
* **Cuando** se importa un archivo Excel con pestañas `BD`, `ASO`, `VOL` y `EXP`, **el sistema deberá** vincular mediante el número de documento la información de las 4 pestañas a la misma `Persona`, creando las entidades `DatosAsociado`, `DatosVoluntario` y `Expediente` correspondientes sin perder ningún dato.

---

### 3.2 Regla de Negocio en Expedientes Legales

* **Si** se intenta crear un nuevo `Expediente` para una persona que ya cuenta con un expediente existente en estado `"En tramite"`, **entonces el sistema deberá** rechazar la solicitud devolviendo un código HTTP `400 Bad Request` con el mensaje: `"La persona ya cuenta con un expediente legal en trámite"`.
* **Si** el expediente previo de la persona se encuentra en cualquiera de los estados finales/intermedios (`"Favorable"`, `"Requerimiento"`, `"Archivado"`, `"Denegado"`, `"Recurso"`), **entonces el sistema deberá** permitir la creación del nuevo expediente legal.

---

### 3.3 Preservación Estricta de Campos (Zero Data Loss)

* **El sistema deberá** aplicar fusiones (*updates*) parciales utilizando la configuración de reemplazo de campos no nulos, garantizando que una actualización parcial (PATCH) jamás sobreescriba con `NULL` ni borre información de campos no enviados en la petición.

---

## 4. Contratos y Esquemas (Pydantic / OpenAPI)

### 4.1 Estados Permitidos para Expediente Legal
Los estados válidos para la propiedad `estado` en `Expediente` son:
1. `"En tramite"` *(Estado activo restrictivo)*
2. `"Favorable"`
3. `"Requerimiento"`
4. `"Archivado"`
5. `"Denegado"`
6. `"Recurso"`

### 4.2 Esquema de Creación de Expediente (`ExpedienteCreateRequest`)
```json
{
  "tipo_tramite": "Renovación NIE",
  "fecha_presentacion": "2026-09-06",
  "numero_expediente_asignado": "EXP-2026-0001",
  "representante_legal": "Dr. Carlos Ruiz",
  "consultorio_juridico": "Consultorio Central",
  "aporte_social": "Sí",
  "solicitante_extranjeria": false,
  "antecedentes_traducidos_y_apostillados": true,
  "fecha_resolucion": null
}
```

---

## 5. Criterios de Aceptación (Gherkin)

```gherkin
Scenario: Bloqueo de segundo expediente si ya existe uno en trámite
  Given una persona que posee un expediente en estado "En tramite"
  When el usuario intenta crear un nuevo expediente para esa misma persona
  Then el backend responde con un error HTTP 400
  And la respuesta indica "La persona ya cuenta con un expediente legal en trámite"

Scenario: Creación permitida de expediente tras resolución del previo
  Given una persona cuyo expediente anterior está en estado "Favorable" o "Requerimiento"
  When el usuario crea un nuevo expediente para esa persona
  Then el backend crea el nuevo expediente exitosamente con un número de registro único
  And responde con un código HTTP 201 Created

Scenario: Asignación de rol de Voluntario a un Asociado existente sin pérdida de datos
  Given una persona registrada como "Asociado"
  When el usuario edita la persona, marca "Registrar como Voluntario" y guarda los datos
  Then el backend crea el registro DatosVoluntario manteniendo intacto el registro DatosAsociado
  And la persona ahora posee ambos roles en el sistema
```
