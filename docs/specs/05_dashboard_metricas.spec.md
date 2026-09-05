# Especificación: 05_dashboard_metricas

## 1. Contexto y Usuario
El Dashboard de Métricas es la pantalla principal o panel analítico que utilizan los gestores y la directiva de Asocolgi (Asociación de Colombianos en Girona) para comprender el impacto de la fundación, la demografía de sus miembros y el estado administrativo y financiero de los asociados.

## 2. Historia de Usuario
* **Como** directivo o gestor administrativo,
* **Quiero** visualizar estadísticas consolidadas, dinámicas y precisas en tiempo real sobre las personas registradas (roles, situación migratoria, ciudades, nacionalidades, etc.).
* **Para** poder tomar decisiones informadas, justificar la petición de subvenciones (grants) al gobierno local, y entender qué tipo de población estamos atendiendo.
* **Además**, necesito que las barras y gráficas se llenen dinámicamente con los datos reales de la base de datos y no con valores estáticos.

## 3. Requisitos Funcionales (E.A.R.S)

### 3.1 Interfaz y Flujo Básico (Ubiquitous)
* **El sistema deberá** renderizar un Dashboard organizado por bloques (Tarjetas de resumen numérico y Tarjetas de distribución porcentual/barras).
* **El sistema deberá** calcular todos los porcentajes y anchos de barra matemáticamente en base al total de registros, asegurando que ninguna barra sea estática.

### 3.2 Tarjetas de Resumen (KPIs Principales)
* **El sistema deberá** mostrar números absolutos para: Total de Personas, Total de Expedientes, Asociados Activos, Asociados Morosos/Pendientes, y Total de Voluntarios.
* **El sistema deberá** resaltar visualmente (en rojo o con un ícono de alerta) la tarjeta de "Asociados Morosos" si el número es mayor a 0.

### 3.3 Distribuciones y Gráficas (State-driven)
* **El sistema deberá** agrupar y mostrar la "Distribución por Roles" (Asociados, Voluntarios, Externos).
* **El sistema deberá** agrupar y mostrar la "Situación Administrativa" (Regular, Irregular, En trámite).
* **El sistema deberá** agrupar y mostrar la "Demografía por Género" (Hombres, Mujeres, LGTBI).
* **El sistema deberá** calcular y mostrar el Top 5 de "Nacionalidades" más frecuentes.
* **El sistema deberá** calcular y mostrar el Top 5 de "Ciudades de Residencia" (Ej: Girona, Salt, Figueres, etc.).
* **El sistema deberá** calcular y agrupar el "Top 5 Motivos de Consulta", para entender por qué la gente acude a la fundación.

### 3.4 Actualización Dinámica (Event-driven)
* **Cuando** el usuario entre a la pantalla del Dashboard, **el sistema deberá** solicitar las métricas actualizadas al Backend (Endpoint `/metrics`).
* **Cuando** el backend reciba la petición, **el sistema deberá** ejecutar consultas de agregación (COUNT, GROUP BY) en la base de datos y retornar los totales reales.

## 4. Contratos y Tipos (Pydantic / Dart Classes)

**Response Éxito (Backend -> Frontend):**
```json
{
  "kpis": {
    "total_personas": 150,
    "total_expedientes": 45,
    "asociados_activos": 30,
    "asociados_morosos": 5,
    "total_voluntarios": 20
  },
  "distribuciones": {
    "roles": {"asociados": 35, "voluntarios": 20, "externos": 105},
    "situacion_admin": {"regular": 90, "irregular": 40, "en_tramite": 20},
    "genero": {"hombres": 70, "mujeres": 75, "lgtbi": 5},
    "nacionalidades_top5": {"Colombia": 120, "Honduras": 10, "España": 5, "Venezuela": 5, "Ecuador": 10},
    "ciudades_top5": {"Girona": 80, "Salt": 50, "Banyoles": 10, "Figueres": 10},
    "motivos_consulta_top5": {"Asesoría Legal": 60, "Ayuda Alimentaria": 40, "Trámites Extranjería": 50}
  }
}
```

## 5. Criterios de Aceptación (Gherkin)

```gherkin
Scenario: Actualización real y dinámica de las barras de progreso
  Given que la base de datos tiene 10 Hombres y 10 Mujeres
  When el gestor registra una nueva "Mujer" en el sistema
  And el gestor recarga el Dashboard de Métricas
  Then el backend recalcula la distribución (10 Hombres, 11 Mujeres)
  And el frontend ajusta el ancho de la barra de progreso de "Mujeres" para que sea visualmente mayor a la de "Hombres"
```
