# Especificación: 06_gestion_expedientes

## 1. Contexto y Usuario
El módulo de Gestión de Expedientes permite a los gestores de Asocolgi administrar los trámites legales o administrativos de los miembros que tienen el rol de **Asociado**. Un expediente centraliza el tipo de trámite, su estado actual y los comentarios o actualizaciones relacionadas a dicho proceso.

## 2. Historia de Usuario
* **Como** gestor de la base de datos,
* **Quiero** poder ver una lista de todos los expedientes, filtrarlos por su estado, y entrar al detalle de un expediente específico.
* **Para** actualizar su estado (ej. de "En trámite" a "Favorable") y añadir notas/comentarios sobre el progreso del trámite.
* **Además**, necesito que el sistema genere automáticamente un Número de Registro único (Ej: `EXP-2026-0005`) al crear un expediente.

## 3. Requisitos Funcionales (E.A.R.S)

### 3.1 Interfaz y Flujo Básico (Ubiquitous)
* **El sistema deberá** tener una pantalla principal de lista de expedientes que muestre KPIs superiores (Total Expedientes, Expedientes Activos) y botones de filtro por estado.
* **El sistema deberá** tener una pantalla de Detalles del Expediente dividida en dos paneles: a la izquierda los detalles y botones de estado, y a la derecha el chat/historial de comentarios.

### 3.2 Lógica de Estados (Event-driven / State-driven)
* **Cuando** el gestor presione uno de los botones de "Gestión de Estado" (En trámite, Favorable, Requerimiento, Archivado, Denegado, Recurso), **el sistema deberá** actualizar instantáneamente el estado del expediente en la base de datos.
* **Mientras** un expediente tenga el estado "Archivado", "Denegado" o "Favorable", **el sistema deberá** restar ese expediente del contador de "Expedientes Activos" en los KPIs de la vista principal.

### 3.3 Relación con Comentarios (Ubiquitous)
* **El sistema deberá** cargar en el panel derecho única y exclusivamente los comentarios asociados a esta persona que tengan la categoría/tipo `Expediente` (reutilizando la arquitectura de la Spec 04).

### 3.4 Creación y Autogeneración (Event-driven)
* **Cuando** se cree un nuevo expediente para un Asociado, **el sistema deberá** autogenerar el "Nº Registro" usando el formato `EXP-[AÑO]-[SECUENCIA_4_DIGITOS]` (Ej: `EXP-2026-0001`).
* **Si** el usuario al que se le intenta crear el expediente NO tiene la casilla de "Asociado" marcada, **entonces el sistema deberá** bloquear la creación.

## 4. Contratos y Tipos (Pydantic / Dart Classes)

**Modelo de Expediente (Backend -> Frontend):**
```json
{
  "id": 12,
  "persona_id": 142,
  "numero_registro": "EXP-2026-0005",
  "tipo_tramite": "Arraigo Social",
  "fecha_presentacion": "2026-08-11",
  "estado": "Favorable"
}
```

## 5. Criterios de Aceptación (Gherkin)

```gherkin
Scenario: Cambio de estado de un expediente
  Given un expediente actualmente en estado "En trámite"
  When el gestor hace clic en el botón "Favorable"
  Then el backend recibe la petición de actualización PATCH
  And el sistema cambia el badge de estado a verde (Favorable)
  And el KPI de "Expedientes Activos" disminuye en 1
```
