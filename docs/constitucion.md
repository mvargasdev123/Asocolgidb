# CONSTITUCIÓN DEL PROYECTO (Reglas Inquebrantables)

Este documento contiene los "Mandamientos" técnicos y de seguridad del proyecto Asocolgi_V2. Ningún desarrollador humano ni asistente de IA está autorizado a romper estas reglas bajo ninguna circunstancia. Si una especificación o requerimiento choca con estas reglas, la regla de la Constitución prevalece y el requerimiento debe rediseñarse.

---

## 🏛️ PARTE I: Mandamientos Arquitectónicos y de Flujo (SDD)

1. **La Spec es la Ley:** No se escribe ni una sola línea de código sin una especificación (Spec E.A.R.S) previamente aprobada. Si el código y la Spec difieren, el código se considera erróneo.
2. **Separación Estricta (Cero Lógica en UI):** El Frontend (Flutter) es "tonto". Un Widget tiene estrictamente prohibido hacer cálculos complejos, filtrados pesados o peticiones HTTP. Su único trabajo es pintar la interfaz y delegar acciones al BLoC.
3. **Desarrollo Guiado por Pruebas (TDD):** Queda prohibido implementar una lógica de negocio en backend o frontend sin antes haber escrito un test (unitario o de integración) que compruebe su funcionamiento.
4. **Resiliencia (Cero Errores en Cascada):** Si una parte del backend falla (ej. la base de datos no responde), la aplicación no debe crashear entera. El backend atrapará el error y devolverá un JSON amigable (Ej: `503 Service Unavailable`). El frontend atrapará ese JSON y mostrará una alerta suave.

---

## 🛡️ PARTE II: Mandamientos de Seguridad Estricta (OWASP)

Estas reglas protegen los datos de la fundación y sus integrantes contra atacantes y fugas de datos.

### A. Gestión de Secretos y Acceso
5. **Cero Secretos en Código:** Las claves API, contraseñas, JWT Secrets y URL de base de datos **jamás** pisarán el código fuente ni el historial de Git. Todo se maneja por variables de entorno inyectadas en ejecución.
6. **Autenticación Fuerte:** El Backend debe forzar la validación de tokens (Autenticación) en cualquier endpoint privado. Jamás confiar en que el Frontend "ya bloqueó" la vista.
7. **Contraseñas Hasheadas:** Toda contraseña se guarda cifrada con algoritmos fuertes (ej. *Bcrypt* o delegando en Supabase Auth). Jamás se guardarán en texto plano.
8. **Seguridad de Base de Datos (RLS):** Toda tabla en Supabase debe tener configurada obligatoriamente *Row Level Security (RLS)*. Nadie accede a datos que no le corresponden, incluso si obtienen la clave anónima pública de Supabase.

### B. Validación y Protección de Entradas
9. **Validación Extrema (Pydantic):** Todo dato que entre al Backend debe ser validado. Si un campo no está definido en el esquema o es del tipo incorrecto, la petición se rechaza (Previene *Mass Assignment* y manipulación de campos).
10. **Prevención de Inyección SQL:** Prohibido concatenar *strings* para hacer consultas a la base de datos. Toda consulta pasará por el ORM (SQLModel/SQLAlchemy) que sanitiza las consultas automáticamente.
11. **Escapar el Contenido del Usuario (Anti-XSS):** Todo texto ingresado por el usuario se asume malicioso. Si alguien escribe `<script>hack()</script>` en su nombre, el sistema lo tratará como texto simple y no lo ejecutará al mostrarlo en pantalla.
12. **Restricción de Subida de Archivos:** Todo Excel, PDF o imagen subido al servidor debe ser analizado. Se limitará su tamaño (Mb) y se verificará su extensión real (MIME type) para evitar que suban ejecutables camuflados.

### C. Red y Tráfico
13. **Forzar HTTPS:** Toda comunicación entre Frontend y Backend, y entre Backend y Supabase, se hará obligatoriamente a través de canales encriptados TLS/HTTPS.
14. **Defensa contra Bots y Fuerza Bruta:** Los endpoints de inicio de sesión y recuperación de contraseña deben tener límites de peticiones (*Rate Limiting*) para bloquear ataques de fuerza bruta.
15. **Paginación Obligatoria:** Limitar siempre el número de respuestas de la API. (Jamás hacer un `SELECT *` de 100,000 registros de golpe porque colapsaría la memoria del servidor).

### D. Monitoreo y Mantenimiento
16. **Monitoreo Silencioso:** Las consultas de DB lentas y los errores graves del servidor serán registrados en un log interno (cifrando datos personales si aparecen en el error), pero jamás expuestos al cliente.
17. **Escaneo de Dependencias:** Se mantendrán vigiladas las librerías de Python (`requirements.txt`) y Dart (`pubspec.yaml`) para actualizarlas si reportan vulnerabilidades conocidas.
