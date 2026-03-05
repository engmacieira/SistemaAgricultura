import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from app.main import app
from app.core.database import Base, get_db
from app.core.dependencies import get_current_user

# Use an in-memory SQLite database for testing to avoid touching production data
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def setup_database():
    """
    Creates the database tables for the tests and drops them when done.
    """
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session(setup_database):
    """
    Provides a real database session to tests if they need to interact directly with DB.
    """
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def client(db_session):
    """
    Provides a FastAPI TestClient configured to use the test database session.
    """
    def override_get_db():
        try:
            yield db_session
        finally:
            pass # Session is closed by the db_session fixture
            
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
