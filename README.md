<div align="center">

# 🇨🇴 Asocolgi v2 - Sistema de Gestión Integral 🇪🇸
### Asociación Colombiana en Galicia

[![FastAPI](https://img.shields.io/badge/FastAPI-005587?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python_3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flutter](https://img.shields.io/badge/Flutter_Web-02569B?style=for-the-badge&logo=flutter&logoColor=white)](https://flutter.dev/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![SQLModel](https://img.shields.io/badge/SQLModel-009688?style=for-the-badge&logo=sqlite&logoColor=white)](https://sqlmodel.tiangolo.com/)
[![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)](https://supabase.com/)
[![Clean Architecture](https://img.shields.io/badge/Architecture-Clean%20%2B%20BLoC-orange?style=for-the-badge)](https://bloclibrary.dev/)

*Plataforma web de alto rendimiento para el registro, seguimiento de expedientes legales de extranjería, control de miembros (Asociados y Voluntarios), análisis estadístico e importación/exportación bidireccional en Excel.*

</div>

---

## 📌 Tabla de Contenidos
- [Visión General](#-visión-general)
- [Características Principales](#-características-principales)
- [Arquitectura del Sistema](#-arquitectura-del-sistema)
- [Módulos del Backend (FastAPI)](#-módulos-del-backend-fastapi)
- [Módulos del Frontend (Flutter Web)](#-módulos-del-frontend-flutter-web)
- [Referencia de la API RESTful](#-referencia-de-la-api-restful)
- [Motor de Importación y Exportación Excel](#-motor-de-importación-y-exportación-excel)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Guía de Instalación, Docker y Despliegue](#-guía-de-instalación-docker-y-despliegue)
- [Estrategia de Infraestructura y Servidores](#-estrategia-de-infraestructura-y-servidores)
- [Pruebas y Verificación](#-pruebas-y-verificación)

---

## 🚀 Visión General

**Asocolgi v2** es la solución tecnológica centralizada para la **Asociación Colombiana en Galicia**. Diseñada bajo estándares de arquitectura limpia y escalable, la plataforma permite gestionar el padrón de beneficiarios, el ciclo de vida de asociados y voluntarios, expedientes jurídicos de extranjería, comentarios auditables etiquetados por contexto y la generación automatizada de informes en formato **Excel (`.xlsx`)** estructurados en 4 hojas sincronizadas (`BD`, `ASO`, `VOL`, `EXP`).

---

## ✨ Características Principales

### 👥 Gestión Multiroles y Padrón Unificado
- **Personas Beneficiarias**: Registro completo de identificación (NIF/NIE/Pasaporte), datos personales, residencia y situación social (situación administrativa, unidad familiar, violencia de género, nivel educativo).
- **Asociados**: Gestión de cuotas, métodos de pago, fecha de vinculación y cálculo automático de antigüedad.
- **Voluntarios**: Asignación de cargos, campo de acción, horas semanales, fecha de alta/baja y registro documental (CV, carta de compromiso, formulario).

### ⚖️ Expedientes Legales de Extranjería
- Tramitación jurídica de expedientes (Renovaciones, Arraigo, Asilo, Nacionalidad, etc.).
- Asignación de representantes legales y consultorios jurídicos.
- Control de fechas clave (Fecha de presentación y resolución), aporte social y verificación de documentación apostillada/traducida.

### 🔍 Buscador en Tiempo Real y Filtros Combinados
- Filtro en tiempo real por término de búsqueda (Nombre completo o Número de identificación).
- Menús desplegables de filtrado multi-categoría:
  - **Género**: Todos, Hombres, Mujeres.
  - **Rol**: Todos, Asociados, Voluntarios, Externos.
  - **Situación Administrativa**: Todas, Regulares, Irregulares, En trámite.

### 📊 Panel de Métricas e Indicadores
- Resumen visual interactivo con tarjetas de totales.
- Desglose estadístico por género, estatus de membresía y distribución geográfica.

### 💬 Comentarios Etiquetados por Contexto
- Comentarios vinculados al perfil del usuario pero clasificados automáticamente por pestaña/origen (`Persona`, `Asociado`, `Voluntario`, `Expediente`).

### 📅 Estandarización de Fechas (MM/DD/YYYY)
- Manejo estandarizado en formato `Mes/Día/Año` (`MM/DD/YYYY`) en la interfaz visual, API REST e importación/exportación de Excel.

---

## 🏛️ Arquitectura del Sistema

El proyecto implementa **Clean Architecture** dividida en Backend y Frontend desacoplados.

```mermaid
flowchart TD
    subgraph Frontend["Client Layer (Flutter Web & Nginx)"]
        UI["Presentation Layer\n(Pages, Widgets, Drawers)"]
        BLoC["State Management\n(Flutter BLoC Pattern)"]
        RepoFront["Data Layer\n(Repositories & Dio HTTP Client)"]
        UI --> BLoC
        BLoC --> RepoFront
    end

    subgraph Backend["Server Layer (FastAPI & Docker)"]
        Router["API Routers\n(FastAPI Controllers & Dependencies)"]
        Service["Application Layer\n(Business Services & Excel Engine)"]
        Domain["Domain Layer\n(SQLModel Entities & Pydantic Schemas)"]
        RepoBack["Infrastructure Layer\n(SQLModel Repositories)"]
        
        Router --> Service
        Service --> Domain
        Service --> RepoBack
    end

    subgraph Storage["Data & Files Layer"]
        DB[(SQLite / Supabase PostgreSQL)]
        ExcelEngine["OpenPyXL Engine\n(BD, ASO, VOL, EXP Sheets)"]
    end

    RepoFront <-->|"JSON REST API / JWT Auth"| Router
    RepoBack <--> DB
    Service <--> ExcelEngine
```

---

## ⚙️ Módulos del Backend (FastAPI)

El backend está construido con **Python 3.12**, **FastAPI** y **SQLModel**, estructurado en las siguientes capas dentro de `backend/src/`:

```
backend/src/
├── api/             # Controladores HTTP y endpoints REST
├── application/     # Lógica de negocio y procesamiento de servicios
├── domain/          # Entidades ORM (SQLModel) y esquemas DTO (Pydantic)
└── infrastructure/  # Repositorios de datos y conexión a BD
```

### 1. Capa de API (`src/api/`)
- **[persona_router.py](file:///home/miguel/Documentos/Mam%C3%A1%20cosas/Asocolgi_v2/backend/src/api/persona_router.py)**: Endpoints para listado con filtros (`q`, `genero`, `rol`, `situacion_admin`), creación, lectura y actualización de personas.
- **[asociado_router.py](file:///home/miguel/Documentos/Mam%C3%A1%20cosas/Asocolgi_v2/backend/src/api/asociado_router.py)**: Gestión de membresías y datos de asociados.
- **[voluntario_router.py](file:///home/miguel/Documentos/Mam%C3%A1%20cosas/Asocolgi_v2/backend/src/api/voluntario_router.py)**: Gestión de información operativa de voluntarios.
- **[expediente_router.py](file:///home/miguel/Documentos/Mam%C3%A1%20cosas/Asocolgi_v2/backend/src/api/expediente_router.py)**: CRUD de expedientes de extranjería y trámites jurídicos.
- **[comentario_router.py](file:///home/miguel/Documentos/Mam%C3%A1%20cosas/Asocolgi_v2/backend/src/api/comentario_router.py)**: Endpoints para agregar y consultar comentarios por tipo.
- **[excel_router.py](file:///home/miguel/Documentos/Mam%C3%A1%20cosas/Asocolgi_v2/backend/src/api/excel_router.py)**: Endpoint `POST /excel/importar` y `GET /excel/exportar` para la gestión de archivos Excel.
- **[metrics_router.py](file:///home/miguel/Documentos/Mam%C3%A1%20cosas/Asocolgi_v2/backend/src/api/metrics_router.py)**: Estadísticas consolidadas del sistema.
- **[auth_router.py](file:///home/miguel/Documentos/Mam%C3%A1%20cosas/Asocolgi_v2/backend/src/api/auth_router.py)**: Autenticación de usuarios, emisión de tokens JWT y recuperación de credenciales.
- **[dependencies.py](file:///home/miguel/Documentos/Mam%C3%A1%20cosas/Asocolgi_v2/backend/src/api/dependencies.py)**: Inyección de dependencias de sesión de BD y usuario autenticado.

### 2. Capa de Aplicación (`src/application/`)
- **[excel_service.py](file:///home/miguel/Documentos/Mam%C3%A1%20cosas/Asocolgi_v2/backend/src/application/excel_service.py)**: Motor completo de procesamiento de plantillas Excel en 4 hojas (`BD`, `ASO`, `VOL`, `EXP`). Incluye limpiadores de datos, normalización de formatos de fecha `MM/DD/YYYY` y mapeo relacional.
- **[persona_service.py](file:///home/miguel/Documentos/Mam%C3%A1%20cosas/Asocolgi_v2/backend/src/application/persona_service.py)**: Orquestación de creación/modificación de perfiles de personas con sus datos personales, legales y roles asociados.
- **[expediente_service.py](file:///home/miguel/Documentos/Mam%C3%A1%20cosas/Asocolgi_v2/backend/src/application/expediente_service.py)**: Lógica de creación de expedientes con generación de número de registro único.
- **[auth_service.py](file:///home/miguel/Documentos/Mam%C3%A1%20cosas/Asocolgi_v2/backend/src/application/auth_service.py)**: Hash de contraseñas (Passlib/Bcrypt), validación JWT y control de intentos fallidos.

### 3. Capa de Dominio (`src/domain/`)
- **Modelos ORM (`domain/models/`)**:
  - `Persona`: Modelo principal con datos personales, dirección y situación social.
  - `DatosAsociado` & `DatosVoluntario`: Tablas relacionales por rol de usuario.
  - `Expediente`: Modelo de trámites legales.
  - `Comentario`: Notas con etiqueta de origen (`Persona`, `Expediente`, `Asociado`, `Voluntario`).
  - `Usuario`: Credenciales de administradores y operadores del software.
  - `Catalogos`: Tablas de referencia (Nacionalidades, Ciudades, Nivel Educativo, etc.).
- **Esquemas DTO (`domain/schemas/`)**:
  - Validadores Pydantic con conversor flexible de fechas `parse_flexible_date` para transformar entradas diversas a objetos `date`.

### 4. Capa de Infraestructura (`src/infrastructure/`)
- **[database.py](file:///home/miguel/Documentos/Mam%C3%A1%20cosas/Asocolgi_v2/backend/src/infrastructure/database.py)**: Configuración del motor SQLModel (SQLite/PostgreSQL/Supabase) y migración dinámica de esquema.
- **Repositorios**: Abstracción de operaciones contra la base de datos (`persona_repository.py`, `expediente_repository.py`, etc.).

---

## 🎨 Módulos del Frontend (Flutter Web)

El frontend está desarrollado con **Flutter Web** siguiendo el patrón **BLoC** (Business Logic Component) y **Clean Architecture** organizado en `frontend/lib/`:

```
frontend/lib/
├── core/         # Componentes transversales (Red, Tema, Utilidades)
└── features/     # Módulos funcionales desacoplados (Auth, Dashboard, Members, Expedientes)
```

### 1. Módulo de Miembros y Personas (`features/members/`)
- **[registration_drawer.dart](file:///home/miguel/Documentos/Mam%C3%A1%20cosas/Asocolgi_v2/frontend/lib/features/members/presentation/widgets/registration_drawer.dart)**: Panel lateral deslizable divido en 8 secciones temáticas para consulta y registro detallado de personas, asociados y voluntarios. Incluye selector de fechas `MM/DD/YYYY` y cálculo automático de antigüedad.
- **[comments_section_widget.dart](file:///home/miguel/Documentos/Mam%C3%A1%20cosas/Asocolgi_v2/frontend/lib/features/members/presentation/widgets/comments_section_widget.dart)**: Interfaz de gestión de comentarios por pestañas etiquetadas.

### 2. Módulo de Dashboard y Búsqueda (`features/dashboard/`)
- **[dashboard_page.dart](file:///home/miguel/Documentos/Mam%C3%A1%20cosas/Asocolgi_v2/frontend/lib/features/dashboard/presentation/pages/dashboard_page.dart)**: Vista principal que integra la barra de búsqueda en tiempo real, selectores de filtro combinados (Género, Rol, Situación) y tabla interactiva de personas.
- **[dashboard_metrics_view.dart](file:///home/miguel/Documentos/Mam%C3%A1%20cosas/Asocolgi_v2/frontend/lib/features/dashboard/presentation/pages/dashboard_metrics_view.dart)**: Tarjetas de indicadores clave de rendimiento (KPIs).

### 3. Módulo de Expedientes Legales (`features/expedientes/`)
- **[expedientes_list_page.dart](file:///home/miguel/Documentos/Mam%C3%A1%20cosas/Asocolgi_v2/frontend/lib/features/expedientes/presentation/pages/expedientes_list_page.dart)**: Listado de expedientes tramitados con código de colores según el estado (`En trámite`, `Resuelto`, `Archivado`).
- **[expediente_detail_page.dart](file:///home/miguel/Documentos/Mam%C3%A1%20cosas/Asocolgi_v2/frontend/lib/features/expedientes/presentation/pages/expediente_detail_page.dart)**: Detalle del expediente con información del representante legal, aportes y fechas clave.

### 4. Núcleo (`core/`)
- **[date_formatter.dart](file:///home/miguel/Documentos/Mam%C3%A1%20cosas/Asocolgi_v2/frontend/lib/core/utils/date_formatter.dart)**: Formateador central de fechas para garantizar el estándar `MM/DD/YYYY`.
- **[dio_client.dart](file:///home/miguel/Documentos/Mam%C3%A1%20cosas/Asocolgi_v2/frontend/lib/core/network/dio_client.dart)**: Cliente HTTP con interceptores JWT automáticos.

---

## 🔌 Referencia de la API RESTful

| Método | Endpoint | Descripción | Auth Requerida |
| :--- | :--- | :--- | :---: |
| `POST` | `/api/v1/auth/login` | Inicio de sesión y obtención de Token JWT (20 min expiración) | ❌ |
| `POST` | `/api/v1/auth/refresh` | Renovar Token de acceso por otros 20 min si está activo | 🔒 |
| `GET` | `/api/v1/personas/` | Listar personas con búsqueda (`q`) y filtros (`genero`, `rol`, `situacion_admin`) | 🔒 |
| `POST` | `/api/v1/personas/` | Registrar nueva persona con datos personales y de rol | 🔒 |
| `GET` | `/api/v1/personas/{id}` | Obtener detalle completo de una persona | 🔒 |
| `PUT` | `/api/v1/personas/{id}` | Actualizar datos de persona | 🔒 |
| `GET` | `/api/v1/expedientes/` | Listar expedientes jurídicos registrados | 🔒 |
| `POST` | `/api/v1/expedientes/` | Crear expediente para una persona | 🔒 |
| `GET` | `/api/v1/comentarios/persona/{id}` | Listar comentarios etiquetados de una persona | 🔒 |
| `POST` | `/api/v1/comentarios/` | Agregar comentario con etiqueta de contexto | 🔒 |
| `POST` | `/api/v1/excel/importar` | Importar datos masivos desde archivo `.xlsx` | 🔒 |
| `GET` | `/api/v1/excel/exportar` | Descargar base de datos completa en `.xlsx` (4 hojas) | 🔒 |
| `GET` | `/api/v1/metrics/dashboard` | Obtener métricas consolidadas del sistema | 🔒 |

---

## 📊 Motor de Importación y Exportación Excel

El sistema incluye un motor propio en **`excel_service.py`** que procesa y genera la plantilla oficial de la asociación ([Modelo basededatos Asocolgi2026.xlsx](file:///home/miguel/Documentos/Mam%C3%A1%20cosas/Asocolgi_v2/Modelo%20basededatos%20Asocolgi2026.xlsx)):

```
┌─────────────────────────────────────────────────────────────────┐
│              Modelo basededatos Asocolgi2026.xlsx               │
├───────────────┬────────────────┬────────────────┬───────────────┤
│    Hoja 1     │     Hoja 2     │     Hoja 3     │    Hoja 4     │
│     [BD]      │     [ASO]      │     [VOL]      │     [EXP]     │
│ (31 Columnas) │  (7 Columnas)  │  (8 Columnas)  │ (12 Columnas) │
└───────────────┴────────────────┴────────────────┴───────────────┘
```

1. **Hoja BD (Base de Datos General)**: 31 columnas con toda la información de filiación, domicilio, situación administrativa y comentarios de persona.
2. **Hoja ASO (Asociados)**: 7 columnas enfocadas en número de socio, cuota, método de pago, fecha de vinculación y comentarios de asociado.
3. **Hoja VOL (Voluntarios)**: 8 columnas con cargo, tipo de voluntariado, fecha de alta/baja y comentarios de voluntario.
4. **Hoja EXP (Expedientes)**: 12 columnas con historial de trámites legales, representante asignado y comentarios de expediente.

---

## 📁 Estructura del Proyecto

```text
Asocolgi_v2/
├── README.md                          # Documentación principal del repositorio
├── docker-compose.yml                 # Orquestador Docker (Backend + Frontend)
├── Modelo basededatos Asocolgi2026.xlsx # Plantilla Excel de referencia
├── backend/                           # API Backend (Python / FastAPI)
│   ├── Dockerfile                     # Imagen Docker de FastAPI
│   ├── .dockerignore                  # Exclusiones de Docker para Backend
│   ├── requirements.txt               # Dependencias Python (FastAPI, SQLModel, psycopg2)
│   ├── src/
│   │   ├── api/                       # Routers HTTP REST
│   │   ├── application/               # Servicios de Lógica de Negocio y Excel
│   │   ├── domain/                    # Modelos SQLModel y Esquemas Pydantic
│   │   ├── infrastructure/            # Repositorios y Conexión a Base de Datos
│   │   └── main.py                    # Punto de entrada de la aplicación FastAPI
│   └── tests/                         # Suite de Pruebas Unitarias e Integración (Pytest)
└── frontend/                          # Cliente Web (Flutter / Dart)
    ├── Dockerfile                     # Imagen Docker Multietapa (Build Web + Nginx)
    ├── nginx.conf                     # Servidor Web estático Nginx para producción
    ├── .dockerignore                  # Exclusiones de Docker para Frontend
    ├── lib/
    │   ├── core/                      # Red, Formateadores y Temas
    │   ├── features/                  # Módulos por Dominio (Auth, Dashboard, Members, Expedientes)
    │   └── main.dart                  # Punto de entrada de Flutter
    └── pubspec.yaml                   # Dependencias de Flutter
```

---

## 🛠️ Guía de Instalación, Docker y Despliegue

### Requisitos Previos
- **Docker** y **Docker Compose**
- *Opción sin Docker*: Python 3.12+, Flutter SDK 3.22+, Git.

---

### 🐳 Despliegue Rápido con Docker Compose (Recomendado)

Para levantar el **Backend** y **Frontend** en un solo comando:

```bash
# Construir e iniciar contenedores
docker compose up --build
```

- **Frontend (Flutter Web)**: `http://localhost:8080`
- **Backend (FastAPI / Swagger)**: `http://localhost:8000/docs`

Para detener los contenedores:
```bash
docker compose down
```

---

### 💻 Instalación Manual Local (Sin Docker)

#### 1. Configuración del Backend (FastAPI)

```bash
cd backend

# Crear y activar entorno virtual
python3 -m venv .venv
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Iniciar servidor
uvicorn src.main:app --reload --port 8000
```
Disponible en `http://localhost:8000` (Swagger docs en `/docs`).

#### 2. Configuración del Frontend (Flutter Web)

```bash
cd frontend

# Descargar paquetes
flutter pub get

# Iniciar en navegador Chrome
flutter run -d chrome
```

---

## ☁️ Estrategia de Infraestructura y Servidores

Para garantizar un despliegue **ultra-económico, fácil de mantener y de alto rendimiento**, se recomienda la siguiente arquitectura en la nube:

### 1. Base de Datos Administrada (**Supabase**)
- **Tecnología**: PostgreSQL en la nube.
- **Ventajas**: Plan gratuito generoso, respaldos automáticos, certificado SSL y cero mantenimiento de servidores de BD.
- **Integración**: Solo basta con definir la variable de entorno `DATABASE_URL` en el backend:
  ```bash
  DATABASE_URL=postgresql://postgres:[PASSWORD]@db.[PROJECT_REF].supabase.co:5432/postgres
  ```

### 2. Alojamiento del Backend (**Render.com** / **Koyeb** / **VPS**)
- El `Dockerfile` del backend permite desplegar automáticamente en plataformas PaaS gratuitas o en un servidor VPS básico en **OVHcloud** (3€ - 5€/mes).

### 3. Alojamiento del Frontend (**Vercel** / **Cloudflare Pages**)
- Los archivos compilados de Flutter Web se pueden desplegar gratuitamente en **Vercel** o **Cloudflare Pages**, beneficiándose de red CDN mundial y SSL automático.

### 4. Dominio Institucional (`asocolgi.org` en OVHcloud)
- No se requiere una cuenta costosa de AWS.
- El dominio `asocolgi.org` alojado en **OVHcloud** se vincula simplemente configurando los **Registros DNS (A / CNAME)** en el panel de OVH para apuntar al servidor o servicio donde esté alojada la plataforma.

---

## 🔬 Pruebas y Verificación

### Backend (Pytest)
```bash
cd backend
PYTHONPATH=src pytest tests/
```

### Frontend (Dart Analysis)
```bash
cd frontend
dart analyze --no-fatal-warnings lib/
```

---

<div align="center">

Desarrollado con ❤️ para la **Asociación Colombiana en Girona(Asocolgi)**.

</div>
