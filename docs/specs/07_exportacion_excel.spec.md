# Especificación: 07_exportacion_excel

## 1. Contexto y Usuario
El módulo de Exportación permite extraer la información de la base de datos a un archivo Excel (.xlsx).
**Nota de Seguridad Estricta:** Para prevenir el robo rápido de la base de datos por personal no autorizado que tenga acceso temporal al sistema, los archivos generados **jamás** se descargarán directamente al navegador/computadora.

## 2. Historia de Usuario
* **Como** gestor de la base de datos,
* **Quiero** poder solicitar la exportación de la base de datos, eligiendo si quiero descargar todo, solo Asociados, solo Voluntarios o solo Expedientes.
* **Para** tener un respaldo o trabajar los datos externamente.
* **Además**, por seguridad, quiero que el sistema envíe este Excel como archivo adjunto al correo oficial de administración, en lugar de descargarlo en mi PC.

## 3. Requisitos Funcionales (E.A.R.S)

### 3.1 Interfaz y Opciones (Ubiquitous)
* **El sistema deberá** mostrar un modal o pantalla de exportación con 4 opciones de selección: "Base de Datos Completa", "Solo Asociados", "Solo Voluntarios" y "Solo Expedientes".

### 3.2 Proceso de Generación y Envío (Event-driven)
* **Cuando** el usuario seleccione la opción deseada y presione "Exportar", **el sistema deberá** solicitar la generación al Backend y mostrar un spinner de carga con el texto: "Generando y enviando al correo...".
* **Cuando** el Backend reciba la petición, **el sistema deberá** generar un archivo `.xlsx` en memoria RAM (sin guardarlo físicamente en el servidor) con las columnas correspondientes.
* **Cuando** el archivo esté generado en memoria, **el sistema deberá** enviarlo mediante SMTP (con la plantilla correspondiente) al correo administrativo: `asocolgibasededatos@gmail.com`.
* **Cuando** el correo se envíe con éxito, **el sistema deberá** retornar un mensaje de éxito al frontend: "Archivo enviado al correo oficial".

## 4. Contratos y Tipos

**Request (Frontend -> Backend):**
```json
{
  "tipo_exportacion": "asociados" // Valores: "completa", "asociados", "voluntarios", "expedientes"
}
```

## 5. Criterios de Aceptación (Gherkin)
```gherkin
Scenario: Exportación segura vía Email
  Given que el gestor quiere exportar a los Voluntarios
  When hace clic en "Exportar"
  Then el backend procesa los datos y genera el Excel en memoria
  And el backend envía el Excel por email a la cuenta oficial
  And el frontend NO lanza ninguna descarga directa en el navegador
  And el frontend muestra el mensaje "Enviado al correo"
```
