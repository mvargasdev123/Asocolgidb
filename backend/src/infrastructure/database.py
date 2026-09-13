import os
from sqlmodel import SQLModel, create_engine, Session, text
import domain.models  # Importante para que SQLModel registre todas las tablas y relaciones

# Se lee la URL de la base de datos de las variables de entorno. 
# Para QA (testing) usaremos sqlite:///:memory: por defecto si no está definida
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///local.db")

# Para SQLite necesitamos connect_args. Para PostgreSQL no hace falta, 
# pero la dejaremos vacía en caso de postgres.
connect_args = {"check_same_thread": False} if "sqlite" in DATABASE_URL else {}

engine = create_engine(DATABASE_URL, echo=False, connect_args=connect_args)

def migrate_db_schema():
    """Migración suave dinámica para SQLite: añade cualquier columna faltante definida en SQLModel metadata."""
    if "sqlite" not in DATABASE_URL:
        return
    with engine.connect() as conn:
        for table_name, table_obj in SQLModel.metadata.tables.items():
            try:
                res = conn.execute(text(f"PRAGMA table_info({table_name})")).fetchall()
                existing_cols = {r[1].lower() for r in res}
                if not existing_cols:
                    continue
                for col in table_obj.columns:
                    if col.name.lower() not in existing_cols:
                        col_type = str(col.type)
                        conn.execute(text(f"ALTER TABLE {table_name} ADD COLUMN {col.name} {col_type}"))
            except Exception:
                pass
        conn.commit()

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    migrate_db_schema()
    try:
        with Session(engine) as session:
            from domain.models.usuario import Usuario
            import bcrypt
            user_exist = session.exec(select(Usuario).where(Usuario.email == "asocolgibasededatos@gmail.com")).first()
            if not user_exist:
                hashed = bcrypt.hashpw("AsocolgiDB2026".encode('utf-8'), bcrypt.gensalt(12)).decode('utf-8')
                admin_user = Usuario(
                    email="asocolgibasededatos@gmail.com",
                    hashed_password=hashed,
                    es_admin=True,
                    activo=True
                )
                session.add(admin_user)
                session.commit()
    except Exception as e:
        print(f"Aviso al sembrar usuario administrador: {e}")

def get_session():
    with Session(engine) as session:
        yield session

