# Especificación: 08_importacion_excel

## 1. Contexto y Usuario
El módulo de Importación permite popular la base de datos masivamente subiendo un archivo Excel con un formato específico (columnas predefinidas).

## 2. Historia de Usuario
* **Como** gestor de la base de datos,
* **Quiero** poder subir un Excel para crear cientos de usuarios de golpe.
* **Para** ahorrar tiempo de registro manual.
* **Además**, si el Excel tiene personas que ya existen, quiero que el sistema me avise y me deje elegir si ignorarlas o si sobreescribirlas, sin que la app colapse.

## 3. Requisitos Funcionales (E.A.R.S)

### 3.1 Proceso de Dry-Run (Análisis Previo) (Event-driven)
* **Cuando** el usuario suba el archivo Excel, **el sistema deberá** enviarlo al Backend en modo "Análisis" (Dry-Run), **SIN** guardar nada aún en la base de datos.
* **Cuando** el Backend analice el archivo, **el sistema deberá** cruzar el Número de Identificación de cada fila con la base de datos actual.
* **El sistema deberá** retornar un reporte al Frontend con 3 listas: "Usuarios Nuevos", "Usuarios Duplicados" y "Errores de Formato".

### 3.2 Interfaz de Resolución de Conflictos (State-driven)
* **Si** existen "Usuarios Duplicados" en el reporte, **entonces el sistema deberá** mostrar una tabla en la interfaz donde indique: "Hubo coincidencia con la fila X".
* **El sistema deberá** proveer al usuario, para cada duplicado (o para todos en lote), las opciones: "Omitir (No importar esta fila)" o "Sobreescribir (Reemplazar datos viejos con los del Excel)".

### 3.3 Importación Definitiva (Event-driven)
* **Cuando** el usuario resuelva los conflictos y presione "Confirmar Importación", **el sistema deberá** enviar las instrucciones finales al Backend.
* **El sistema deberá** registrar a los nuevos, ignorar los marcados como omitidos, y actualizar los marcados como sobreescribir.
* **Cuando** una celda opcional del Excel venga vacía, **el sistema deberá** guardarla como `null` en la base de datos (que luego se interpretará como "N/A" en la vista).

## 4. Contratos y Tipos

**Response del Análisis (Backend -> Frontend):**
```json
{
  "total_filas": 50,
  "nuevos_listos_para_guardar": 45,
  "errores": [],
  "duplicados": [
    {
      "fila_excel": 12,
      "identificacion": "Y1234567X",
      "nombre_excel": "Miguel Vargas",
      "accion_recomendada": "resolver"
    }
  ]
}
```

## 5. Criterios de Aceptación (Gherkin)
```gherkin
Scenario: Resolución de Coincidencias en Importación
  Given un archivo Excel con 1 usuario nuevo y 1 usuario que ya existe en DB
  When el gestor sube el archivo
  Then el frontend muestra un modal de confirmación diciendo "1 Nuevo, 1 Duplicado"
  And el gestor marca "Omitir" en el duplicado y presiona "Importar"
  Then el backend solo guarda al usuario nuevo y no altera al existente
```
