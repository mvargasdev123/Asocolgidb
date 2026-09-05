from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from api.auth_router import router as auth_router
from api.persona_router import router as persona_router
from api.comentario_router import router as comentario_router
from infrastructure.database import create_db_and_tables

app = FastAPI(
    title="Asocolgi V2 API",
    description="Backend refactorizado con Clean Architecture para Asocolgi",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Manejador global de excepciones (Rule 10: Prevención de Fallos en Cascada)
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # No mostramos el stacktrace crudo al frontend (Regla estricta)
    # Loggeamos el error real internamente
    import logging
    logging.error(f"Error inesperado: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"status": "error", "message": "Ocurrió un error interno en el servidor. Inténtelo más tarde."}
    )

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(auth_router)
app.include_router(persona_router)
app.include_router(comentario_router)

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Asocolgi V2 API is running"}
