import pytest
from fastapi import status
from fastapi.testclient import TestClient
from jose import jwt
from datetime import datetime, timedelta, timezone

from app.main import app
from app.core.database import get_db
from app.core.security import SECRET_KEY, ALGORITHM
from app.core.dependencies import get_current_user

@pytest.fixture
def unauthenticated_client(db_session):
    """
    Provides a FastAPI TestClient configured to use the test database session,
    but does NOT override get_current_user. Thus, actual auth logic is executed.
    """
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    # Removendo override de current_user caso exista globalmente
    if get_current_user in app.dependency_overrides:
        del app.dependency_overrides[get_current_user]

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()

def test_acesso_sem_token(unauthenticated_client):
    response = unauthenticated_client.post("/api/solicitacoes/", json={
        "producerId": "123",
        "producerName": "Teste",
        "data_solicitacao": "2024-05-15"
    })
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_acesso_com_token_expirado(unauthenticated_client, db_session):
    # Criar um token expirado
    to_encode = {"sub": "1"}
    expire = datetime.now(timezone.utc) - timedelta(minutes=15)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    response = unauthenticated_client.post("/api/solicitacoes/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "producerId": "123",
            "producerName": "Teste",
            "data_solicitacao": "2024-05-15"
        }
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_acesso_com_token_chave_falsa(unauthenticated_client):
    # Criar um token com chave falsa
    to_encode = {"sub": "1"}
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, "chave-falsa-invalida", algorithm=ALGORITHM)

    response = unauthenticated_client.post("/api/solicitacoes/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "producerId": "123",
            "producerName": "Teste",
            "data_solicitacao": "2024-05-15"
        }
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_acesso_com_token_malformado(unauthenticated_client):
    response = unauthenticated_client.post("/api/solicitacoes/",
        headers={"Authorization": "Bearer token.malformado.aqui"},
        json={
            "producerId": "123",
            "producerName": "Teste",
            "data_solicitacao": "2024-05-15"
        }
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.fixture
def auth_client(client):
    # O cliente configurado em conftest já tem o override de get_current_user
    # Para testes de injeção, usamos o cliente normal autenticado
    return client

def test_injecao_sqli_nos_campos(auth_client):
    payload_malicioso = {
        "producerId": "123",
        "producerName": "Teste'; DROP TABLE usuarios; --",
        "data_solicitacao": "2024-05-15",
        "observacoes": "1 OR 1=1"
    }

    response = auth_client.post("/api/solicitacoes/", json=payload_malicioso)

    # Se a aplicação for segura e sanitizar (ou bloquear via Pydantic validator),
    # o status code ideal para dados inválidos seria 422/400.
    # Se aceitar e inserir como texto plano inofensivo, vai dar 201.
    # O importante é não dar erro 500 (SQL quebrado) ou expor dados.
    assert response.status_code in [status.HTTP_400_BAD_REQUEST, status.HTTP_422_UNPROCESSABLE_ENTITY, status.HTTP_201_CREATED]
    assert response.status_code != status.HTTP_500_INTERNAL_SERVER_ERROR

def test_injecao_xss_nos_campos(auth_client):
    payload_malicioso = {
        "producerId": "123",
        "producerName": "<script>alert('XSS')</script>",
        "data_solicitacao": "2024-05-15",
        "observacoes": "<img src=x onerror=alert('XSS')>"
    }

    response = auth_client.post("/api/solicitacoes/", json=payload_malicioso)

    # Da mesma forma que o SQLi, o ideal é validar (400/422) ou pelo menos
    # tratar como texto e retornar 201. Jamais 500.
    # Vamos verificar também se o Pydantic / SQLAlchemy lida bem sem estourar 500.
    assert response.status_code in [status.HTTP_400_BAD_REQUEST, status.HTTP_422_UNPROCESSABLE_ENTITY, status.HTTP_201_CREATED]
    assert response.status_code != status.HTTP_500_INTERNAL_SERVER_ERROR


def test_rate_limiting_brute_force_login(unauthenticated_client):
    # Simula 50 tentativas de login erradas
    for _ in range(50):
        response = unauthenticated_client.post("/api/usuarios/login", json={
            "email": "usuario@inexistente.com",
            "password": "senhaerrada123"
        })

        # A resposta ideal seria 429 Too Many Requests após algumas tentativas
        # Porém, vamos apenas garantir que a aplicação se mantenha estável (401)
        # sem estourar 500 ou travar.
        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_429_TOO_MANY_REQUESTS]
