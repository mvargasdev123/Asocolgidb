# Especificación: 02_guardado_usuarios

## 1. Contexto y Usuario
El módulo de Gestión de Miembros permite a los gestores de Asocolgi registrar a cualquier persona que llegue a la asociación. 

**Nota Arquitectónica (Roles Dinámicos):** 
El sistema maneja un modelo base de "Persona". Dependiendo de las casillas marcadas en el formulario, la persona adquiere roles que habilitan menús y funcionalidades adicionales:
*   **Externo:** Rol por defecto. Solo viene a consulta, no se marca ninguna casilla especial.
*   **Asociado:** Habilita campos financieros/membresía y permite generar un **Expediente**.
*   **Voluntario:** Habilita campos operativos (cargos, horas, contratos).
*   *Nota:* Una persona puede tener ambos roles (Asociado + Voluntario) simultáneamente.

## 2. Historia de Usuario
* **Como** gestor de la base de datos,
* **Quiero** poder registrar los datos de las personas a través de un formulario segmentado, definiendo si son Asociados, Voluntarios, Ambos o Externos.
* **Para** mantener un control centralizado, generar expedientes (a los asociados) y gestionar los datos eficientemente.

## 3. Requisitos Funcionales (E.A.R.S)

### 3.1 Interfaz y Flujo Básico (Ubiquitous)
* **El sistema deberá** presentar el formulario de registro en un panel lateral interactivo (Drawer) dividido en 7 secciones: Identificación, Datos Personales, Situación Social, Legal/Acogida, Contacto de Emergencia, Asociado y Voluntario.
* **El sistema deberá** expandir/mostrar los campos obligatorios de la sección 6 (Asociado) únicamente si la casilla "Registrar como Asociado" está marcada.
* **El sistema deberá** expandir/mostrar los campos de la sección 7 (Voluntario) únicamente si la casilla "Registrar como Voluntario" está marcada.

### 3.2 Proceso de Guardado y Catálogos Dinámicos (Event-driven)
* **Cuando** el usuario envíe el formulario, **el sistema deberá** guardar a la persona en la base de datos.
* **Cuando** se cree una nueva Persona, **el sistema deberá** inicializar automáticamente su "Contador de Visitas" interno en 1.
* **Cuando** un campo opcional no sea completado por el gestor, **el sistema deberá** registrarlo como nulo (`null` o vacío) en la base de datos, para que en la interfaz visual aparezca como "N/A".
* **Cuando** el usuario seleccione la opción "Otro" en un menú desplegable e introduzca un valor inédito (Ej: una nueva Nacionalidad, Técnica de Acogida o Ciudad), **el sistema deberá** guardar silenciosamente ese nuevo valor en las tablas de catálogos. Así estará disponible para futuros registros sin duplicados tipográficos.

### 3.3 Validaciones y Casos Límite (Unwanted Behavior)
* **Si** el formulario se envía sin los campos mínimos obligatorios (Nombre Completo y Número de Identificación), **entonces el sistema deberá** rechazar el registro y resaltar los campos faltantes en rojo.
* **Si** el gestor intenta guardar un usuario cuyo `numero_identificacion` ya existe en la base de datos, **entonces el sistema deberá** rechazar el registro, no sobrescribir ningún dato, y mostrar una alerta estandarizada: *"Esta persona ya existe"*, ofreciendo un botón para ir directamente al perfil de dicha persona.

## 4. Contratos y Tipos (Pydantic / Dart Classes)

**Request Estándar (Frontend -> Backend):**
*(Nota: Solo `nombre_completo` y `numero_identificacion` son estrictamente requeridos. El resto son opcionales `Optional[...]`)*

```json
{
  "identificacion": {
    "tipo_documento": "NIF/NIE",
    "numero_identificacion": "Y1234567X", 
    "nacionalidad": "España"
  },
  "datos_personales": {
    "nombre_completo": "Miguel Vargas", 
    "fecha_nacimiento": "1990-05-14",
    "genero": "M",
    "correo_electronico": "ejemplo@gmail.com",
    "direccion_residencia": "Calle Falsa 123",
    "codigo_postal": "17001",
    "ciudad": "Girona"
  },
  "situacion_social": {
    "situacion_admin": "Regular",
    "unidad_familiar": 1,
    "madre_soltera": "NA",
    "violencia_genero": "NA",
    "nivel_educativo": "Grado Medio"
  },
  "legal_acogida": {
    "tiene_padron": false,
    "fecha_padron": null,
    "motivo_consulta": "Asesoría legal",
    "derivacion": "Ninguna",
    "tecnica_acogida": "Staff X",
    "autoriza_datos": true,
    "autoriza_imagen": false
  },
  "contacto_emergencia": {
    "nombre": "María",
    "parentesco": "Madre",
    "telefono": "+34600000000"
  },
  "es_asociado": true,
  "datos_asociado": {
    "metodo_pago": "Efectivo",
    "estado_membresia": "Activo",
    "estado_pago": "Al día",
    "autoriza_whatsapp": true
  },
  "es_voluntario": false,
  "datos_voluntario": null
}
```

## 5. Criterios de Aceptación (Gherkin)

```gherkin
Scenario: Rechazo por Documento Duplicado (Caso Límite)
  Given que existe una Persona en DB con Número de Identificación "Y1234567X"
  When el gestor intenta registrar una nueva persona con el mismo "Y1234567X"
  Then el backend retorna un código HTTP 409 Conflict
  And el frontend detiene la carga y muestra el modal "Esta persona ya existe" con enlace a su perfil
```
