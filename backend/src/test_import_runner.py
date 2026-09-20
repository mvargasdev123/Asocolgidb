import os
import sys

# Agregar el directorio src al path de python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Usar local_test.db para aislar las pruebas de forma 100% segura
os.environ["DATABASE_URL"] = "sqlite:///local_test.db"

from sqlmodel import SQLModel, create_engine, Session, select
import domain.models
from domain.models.persona import Persona
from domain.models.roles import DatosAsociado, DatosVoluntario
from domain.models.expediente import Expediente
from application.excel_service import ejecutar_importacion_definitiva

def main():
    db_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "local_test.db")
    if os.path.exists(db_file):
        os.remove(db_file)
        print("🗑️ Base de datos de pruebas anterior eliminada.")

    engine = create_engine("sqlite:///local_test.db", echo=False)
    SQLModel.metadata.create_all(engine)
    print("✅ Base de datos local_test.db creada limpiamente.")

    excel_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "Modelo basededatos Asocolgi2026.xlsx")
    if not os.path.exists(excel_path):
        print(f"❌ No se encontró el archivo Excel en {excel_path}")
        return

    with open(excel_path, "rb") as f:
        file_bytes = f.read()

    print(f"📦 Leyendo {excel_path} ({len(file_bytes)} bytes)...")
    
    with Session(engine) as session:
        resultado = ejecutar_importacion_definitiva(file_bytes, decisiones={}, session=session)
        print("\n📊 Resultado de ejecutar_importacion_definitiva:")
        print(resultado)

        # Conteo final en la base de datos de pruebas
        total_personas = len(session.exec(select(Persona)).all())
        total_asociados = len(session.exec(select(DatosAsociado)).all())
        total_voluntarios = len(session.exec(select(DatosVoluntario)).all())
        total_expedientes = len(session.exec(select(Expediente)).all())

        print("\n🔍 RECUENTO EN BASE DE DATOS DE PRUEBAS:")
        print(f"  - Total Personas: {total_personas}")
        print(f"  - Total Asociados (DatosAsociado): {total_asociados}")
        print(f"  - Total Voluntarios (DatosVoluntario): {total_voluntarios}")
        print(f"  - Total Expedientes (Expediente): {total_expedientes}")

if __name__ == "__main__":
    main()
