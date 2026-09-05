# Skill: Clean Architecture (Frontend y Backend)

## Descripción
Esta habilidad define la estructura estricta de carpetas y separación de responsabilidades (Separation of Concerns) que todos los agentes deben seguir para evitar el código espagueti.

## Reglas para el Backend (Python/FastAPI)
El backend debe separarse estrictamente en estas capas:
1.  **`domain/` (Capa Central):** Aquí viven los modelos de datos (SQLModel/Pydantic) y las interfaces (Contratos). No debe importar nada de las capas exteriores.
2.  **`application/` (Casos de Uso):** Aquí va la lógica de negocio pura (ej. la regla de aumentar en +1 el contador de visitas).
3.  **`infrastructure/` (Datos):** La única capa autorizada para hablar con la Base de Datos (Supabase) o servicios externos (SMTP para enviar el Excel). Aquí viven los Repositorios.
4.  **`api/` (Controladores):** Aquí viven los Endpoints de FastAPI (`@app.get()`, `@app.post()`). Su único trabajo es recibir la petición HTTP y pasársela a `application/`.

## Reglas para el Frontend (Flutter/BLoC)
El frontend debe separarse en:
1.  **`domain/`:** Modelos de datos equivalentes a los del backend.
2.  **`data/`:** Repositorios que hacen los llamados HTTP a nuestra API.
3.  **`presentation/`:** 
    *   **`bloc/`:** Archivos de manejo de estado (Eventos y Estados).
    *   **`widgets/`:** Componentes de UI reutilizables (Ej. la caja de texto auto-expansible).
    *   **`pages/`:** Las pantallas completas que ensamblan los widgets.
