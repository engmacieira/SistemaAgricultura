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

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
