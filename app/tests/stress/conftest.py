import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from app.main import app
from app.core.database import Base, get_db
from app.core.dependencies import get_current_user

import os

# Usamos um arquivo físico temporário para poder testar concorrência real do SQLite (modo WAL, timeout)
DB_PATH = "./test_stress.db"
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False, "timeout": 30}
)

from sqlalchemy import event

@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.execute("PRAGMA synchronous=NORMAL")
    cursor.execute("PRAGMA cache_size=-64000")
    cursor.execute("PRAGMA busy_timeout=30000")
    cursor.close()

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def setup_database():
    """
    Creates the database tables for the tests and drops them when done.
    """
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

@pytest.fixture
def db_session(setup_database):
    """
    Provides a real database session to tests if they need to interact directly with DB.
    """
    session = TestingSessionLocal()
    yield session
    session.close()

@pytest.fixture
def client(setup_database):
    """
    Provides a FastAPI TestClient configured to use the test database session.
    A diferença crítica para estresse é que não passamos uma mesma sessão global
    para o client, deixamos o FastAPI criar uma sessão nova por requisição
    (exatamente como em produção).
    """
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    def override_current_user():
        return {
            "id": "1",
            "name": "Admin Test",
            "email": "admin@teste.com",
            "role": "admin"
        }

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_current_user
    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()
