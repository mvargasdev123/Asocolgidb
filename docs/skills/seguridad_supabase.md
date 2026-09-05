# Skill: Seguridad en Supabase y Bases de Datos

## Descripción
Esta habilidad contiene las reglas críticas para evitar filtraciones de datos, inyecciones y accesos no autorizados, aprendiendo de los errores de versiones anteriores.

## Las 10 Reglas de Oro
1.  **Secretos Fuera de Git:** Jamás colocar URLs de Supabase, Passwords, o JWT Secrets en el código fuente. Usar un archivo `.env` local que esté forzosamente en el `.gitignore`.
2.  **Activar RLS (Row Level Security):** Ninguna tabla de Supabase debe tener acceso público irrestricto. Toda tabla debe requerir autenticación.
3.  **Roles y Permisos:** Un usuario "Externo" no puede consultar la tabla de "Asociados". El RLS debe filtrar esto.
4.  **No Borrado Permanente (Soft Delete):** Cuando un usuario pierda el rol de "Asociado", no se hace un `DELETE` en SQL. Se desactiva la bandera (`es_asociado = false`) para proteger la integridad histórica y financiera.
5.  **Sanitización:** Validar TODAS las entradas (FastAPI/Pydantic hace gran parte de esto) para evitar SQL Injection.
6.  **Rate Limiting (Bloqueos):** Si se detectan 5 intentos fallidos de login, bloquear temporalmente el acceso (15 seg, luego 30 seg, luego 5 min).
7.  **Cifrado de Datos Sensibles:** Datos altamente confidenciales del expediente (si los hubiera) deben estar cifrados.
8.  **Forzar HTTPS:** La API solo responderá a peticiones seguras.
9.  **Auditoría (Logs):** Mantener registro de quién modificó qué en los expedientes (Spec 04 de comentarios cubre parte de esto).
10. **Prevención de Fallos en Cascada:** Manejar los errores de base de datos con bloques `try/except` globales en FastAPI para devolver un `HTTP 500` limpio en lugar de colgar el servidor.
