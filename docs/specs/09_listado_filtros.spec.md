# Especificación: 09_listado_y_navegacion

## 1. Contexto y Usuario
La Vista de Listado es el buscador principal de personas y expedientes. Se relaciona íntimamente con el Dashboard de Métricas (Spec 05), ya que las tarjetas del dashboard actúan como accesos directos pre-filtrados a esta lista.

## 2. Historia de Usuario
* **Como** gestor de la base de datos,
* **Quiero** poder buscar personas y aplicar filtros rápidos (por Asociado, Voluntario, Hombres, Mujeres).
* **Para** encontrar registros eficientemente sin tener que leer toda la base de datos.
* **Además**, quiero que al presionar un número en el Dashboard (ej. "Asociados Morosos"), me lleve a esta lista con esos filtros ya aplicados automáticamente.

## 3. Requisitos Funcionales (E.A.R.S)

### 3.1 Filtros y Búsqueda (Ubiquitous)
* **El sistema deberá** contar con una barra de búsqueda por texto libre (Nombre o Número de Identificación).
* **El sistema deberá** proveer botones de filtro rápido tipo "Chips". Inicialmente: `Solo Asociados`, `Solo Voluntarios`, `Hombres`, `Mujeres`. (La arquitectura debe permitir agregar más filtros fácilmente en el futuro).

### 3.2 Navegación con Parámetros (Event-driven)
* **Cuando** el usuario haga clic en una tarjeta específica del Dashboard de Métricas (Ej: "Voluntarios" o "Asociados Pendientes"), **el sistema deberá** navegar hacia la pantalla de Listado enviando parámetros en la ruta o estado.
* **Cuando** la pantalla de Listado reciba esos parámetros (Ej: `?role=asociado&pago=moroso`), **el sistema deberá** aplicar visualmente los filtros correspondientes y solicitar al backend la lista filtrada de inmediato.

### 3.3 Interfaz de Resultados (Ubiquitous)
* **El sistema deberá** mostrar los resultados de la búsqueda de forma paginada para no saturar la memoria de la aplicación si la base de datos crece a miles de registros.

## 4. Contratos y Tipos (Pydantic / Dart Classes)

**Request de Búsqueda GET (Frontend -> Backend):**
```http
GET /usuarios?query=miguel&roles=asociado&estado_pago=moroso&limit=50&offset=0
```

## 5. Criterios de Aceptación (Gherkin)
```gherkin
Scenario: Navegación desde Dashboard a Lista Filtrada
  Given el gestor se encuentra en el Dashboard de Métricas
  When el gestor hace clic en la tarjeta roja de "Asociados Morosos" (cantidad: 5)
  Then la aplicación navega a la vista del Listado
  And el filtro "Asociados" y "Morosos" aparecen activos automáticamente
  And la tabla muestra exactamente a las 5 personas morosas
```
