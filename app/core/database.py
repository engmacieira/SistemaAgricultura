from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from pathlib import Path

APP_NAME = "SistemaAgricultura"

if os.name == 'nt':  # Se for Windows
    BASE_DIR = Path(os.getenv('LOCALAPPDATA', os.path.expanduser('~'))) / APP_NAME
else:  # Se for Linux ou Mac
    BASE_DIR = Path(os.path.expanduser('~')) / f".{APP_NAME.lower()}"

BASE_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = BASE_DIR / "app.db"

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DB_PATH}")

# Mitigação de Concorrência SQLite (Stress/Load)
# Aumentamos o timeout para esperar mais por locks (default é 5)
# Usamos connect_args={"check_same_thread": False, "timeout": 15}
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False, "timeout": 30}
)

# Precisamos injetar as configurações PRAGMA no momento em que a conexão é feita
# O WAL mode (Write-Ahead Logging) melhora MUITO a concorrência do SQLite.
from sqlalchemy import event

@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.execute("PRAGMA synchronous=NORMAL")
    # Tenta usar um pool de memória pro cache para ir mais rápido
    cursor.execute("PRAGMA cache_size=-64000") # 64MB cache
    cursor.execute("PRAGMA busy_timeout=30000") # 30s timeout nativo dbapi
    cursor.close()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
