# AGENTS.md — Protocolo Operativo y Especificaciones (SDD)

Este repositorio opera bajo una metodología estricta de **Spec-Driven Development (SDD)** y Desarrollo Asistido por IA. Toda modificación, refactorización o nueva característica debe derivarse de especificaciones formales y pasar por fases de validación secuenciales antes de considerarse completa.

---

## 1. El Proyecto: Asocolgi_V2
Este proyecto es el sistema integral de gestión para la **Asociación de Colombianos en Girona (Asocolgi)**. Su objetivo es registrar y administrar la información de las personas vinculadas a la fundación (Asociados, Voluntarios, Externos), gestionar sus expedientes, métricas demográficas y estados administrativos (Regular, Moroso, En trámite). 

El sistema consta de:
* Una base de datos relacional alojada en **Supabase**.
* Una API robusta construida con **FastAPI**.
* Una interfaz de usuario multiplataforma construida con **Flutter**.

---

## 2. Arquitectura y Stack Tecnológico

El proyecto está dividido en un Monorepo con la siguiente pila tecnológica:

* **Backend:** Python 3 (entorno virtual `.venv`), pip, FastAPI, SQLModel (ORM), Pytest.
* **Frontend:** Dart, Flutter, BLoC (State Management).
* **Base de Datos:** PostgreSQL (Supabase) con RLS estricto.
* **Despliegue y Contenedores:** **Docker** (Todo el proyecto se contenedorizará para su despliegue final).
* **Patrón Arquitectónico Global:** Clean Architecture.

---

## 3. Flujo de Trabajo Operativo (Protocolo SDD)

La IA y los desarrolladores deben ejecutar cualquier interacción siguiendo estrictamente este orden:

1. **Lectura de la petición:** Leer el prompt del usuario. Si hay ambigüedades, hacer preguntas y dar feedback hasta que el requerimiento sea 100% claro.
2. **Localización y Análisis del Spec:** Dirigirse a `docs/specs/<nombre_feature>.spec.md`. Leer requisitos, contratos y criterios Gherkin. Si hay lagunas lógicas, **detener la ejecución** y solicitar aclaraciones.
3. **Generación del Plan de Acción:** Crear un checklist (`implementation_plan.md`) desglosando interfaces, lógica, integración y UI.
4. **Test-Driven Development (TDD):** 
   * Escribir pruebas que fallen (Red phase) basadas en los Criterios de Aceptación.
   * Implementar la lógica mínima necesaria (Green phase).
   * Refactorizar asegurando tipos y limpieza (Refactor phase).
5. **Verificación Integral:** Ejecutar Linters, Type-Checking y confirmar que la Suite de Tests pasa al 100%.

---

## 4. Arquitectura y Restricciones del Sistema

### Restricciones del Backend (FastAPI)
* **Estructura Modular por Capas:** Tal como se manejaba anteriormente, el backend DEBE estar dividido en carpetas lógicas: `routers/` (rutas API), `models/` (modelos de BD), `schemas/` (Pydantic DTOs), `services/` (lógica de negocio) y `core/` (configuraciones).
* **Aislamiento de Capas:** Los *Routers* (endpoints) NUNCA deben contener lógica de negocio. Solo reciben la petición, validan, llaman a un *Service* y retornan la respuesta.
* **Manejo Estricto de Errores (Regla de Oro):** El Backend SIEMPRE debe devolver los errores en un formato JSON estandarizado (ej. `{"status": "error", "message": "Mensaje legible"}`). Queda **estrictamente prohibido** exponer errores crudos de la base de datos (Stacktraces o errores SQL) al cliente web por motivos de seguridad.
* **Contratos Estrictos (DTOs):** Toda entrada y salida debe estar validada por esquemas de Pydantic. No se retornan modelos de base de datos crudos (`SQLModel`) directamente al cliente.

### Restricciones del Frontend (Flutter)
* **Clean Architecture Estructurada por "Features":** La organización de carpetas será agrupada por funcionalidad (Ej: `lib/features/auth/domain`, `lib/features/auth/presentation`).
* **Regla de Errores en UI:** El Frontend nunca mostrará errores en bruto del servidor al usuario. Los errores deben ser capturados y transformados en mensajes amigables (ej. un *Snackbar* que diga "Credenciales incorrectas").
* **UI "Tonta":** Los Widgets no toman decisiones lógicas ni hacen peticiones HTTP. Solo disparan eventos al BLoC y reaccionan a los cambios de estado.

### Restricciones de Base de Datos
* **Seguridad RLS:** Ninguna tabla será pública. Todas deben tener Row Level Security activado en Supabase.
* **Acceso Exclusivo:** El frontend en Flutter NUNCA se conecta directo a Supabase. Toda lectura/escritura de datos pasa obligatoriamente por la API de FastAPI.

---

## 5. Convenciones de Código y Nomenclatura

* **Archivos y Directorios:** 
  * Backend (Python): `snake_case` (ej. `user_service.py`).
  * Frontend (Dart): `snake_case` para archivos (ej. `login_screen.dart`).
* **Nombres de Clases / Interfaces:** `PascalCase` (ej. `UserRepository`).
* **Modularización y POO:** Código limpio, modular y fuertemente orientado a objetos. **Un archivo, una responsabilidad**. 
* **Tests:** Nombres explícitos que describan escenario y resultado:
  * Python: `test_debe_retornar_error_cuando_payload_es_invalido()`
  * Dart: `test('Debe retornar error cuando payload es inválido', () {...})`
* **Documentación:** Comentarios en español, profesionales explicando el *Por Qué* de la lógica compleja.

---

## 6. Formato de Especificación (`/specs`) y Toolkit 

Todo `.spec.md` debe contener: Contexto, Contratos (Esquemas), Casos Límite y Criterios de Aceptación (Gherkin).

### Comandos Oficiales (Toolkit)
Ejecutar estos comandos según el entorno activo para comprobar la salud del proyecto:

* **Backend (Python):**
  * Activar entorno: `source .venv/bin/activate` (Linux/Mac) o `.venv\Scripts\activate` (Win)
  * Servidor local: `uvicorn main:app --reload` (o el equivalente definido en la carpeta raíz del backend)
  * Tests: `pytest -v`
* **Frontend (Flutter):**
  * Generar código (BLoC/Freezed): `dart run build_runner build --delete-conflicting-outputs`
  * Tests: `flutter test`
* **Contenedores:**
  * Al finalizar, el proyecto se levantará usando `docker-compose up --build`.
