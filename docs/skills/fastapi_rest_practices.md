# Skill: Buenas Prácticas API REST (FastAPI)

## Descripción
Lineamientos estrictos para escribir el backend de manera que sea rápido, escalable y profesional.

## Reglas
1.  **Uso de Pydantic V2:** Todos los payloads entrantes y salientes deben estar estrictamente tipados. Nada de recibir diccionarios genéricos (`dict`).
2.  **Inyección de Dependencias (DI):** Nunca instanciar la base de datos dentro de la ruta. Usar `Depends()` de FastAPI para inyectar la sesión de base de datos o el usuario actual. Esto permite hacer testing (QA) fácilmente.
3.  **Códigos HTTP Estándar:**
    *   `200 OK` para lecturas.
    *   `201 Created` para guardados nuevos (Spec 02).
    *   `400 Bad Request` para errores de validación de formato.
    *   `401 Unauthorized` si no hay token de login.
    *   `409 Conflict` si se intenta crear un DNI duplicado (Specs 02, 03 y 08).
4.  **Asincronismo Real:** Las rutas deben ser `async def` y las llamadas a base de datos deben usar el motor asíncrono para soportar múltiples conexiones simultáneas sin bloquear el servidor.
