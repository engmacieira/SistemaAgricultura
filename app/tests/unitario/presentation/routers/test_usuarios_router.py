from unittest.mock import ANY
import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from app.main import app
from app.core.dependencies import get_current_user
from app.presentation.routers.usuarios import get_use_case

client = TestClient(app)

@pytest.fixture
def mock_uc():
    uc = MagicMock()
    app.dependency_overrides[get_use_case] = lambda: uc
    app.dependency_overrides[get_current_user] = lambda: {"id": "1", "name": "Admin Test", "email": "admin@teste.com", "role": "admin"}
    yield uc
    app.dependency_overrides.clear()

def test_listar_usuarios(mock_uc):
    mock_uc.listar_usuarios.return_value = {"items": [{"email": "admin@ex.com"}], "total": 1, "page": 1, "size": 10, "pages": 1}
    response = client.get("/usuarios/")
    assert response.status_code == 200

def test_criar_usuario(mock_uc):
    mock_uc.criar_usuario.return_value = {"id": "1", "name": "Admin", "email": "admin@ex.com", "role": "admin"}
    payload = {"name": "Admin", "email": "admin@ex.com", "role": "admin", "password": "123"}
    response = client.post("/usuarios/", json=payload)
    assert response.status_code == 201
    mock_uc.criar_usuario.assert_called_once_with(payload)

def test_criar_usuario_erro(mock_uc):
    mock_uc.criar_usuario.side_effect = ValueError("Já existe")
    payload = {"name": "Admin", "email": "admin@ex.com", "role": "admin", "password": "123"}
    response = client.post("/usuarios/", json=payload)
    assert response.status_code == 400

def test_login(mock_uc):
    mock_uc.autenticar_usuario.return_value = {"id": "1", "email": "admin@ex.com"}
    response = client.post("/usuarios/login", json={"email": "admin@ex.com", "password": "123"})
    assert response.status_code == 200
    mock_uc.autenticar_usuario.assert_called_once_with("admin@ex.com", "123")

def test_login_erro(mock_uc):
    mock_uc.autenticar_usuario.side_effect = ValueError("Credenciais inválidas")
    response = client.post("/usuarios/login", json={"email": "admin@ex.com", "password": "123"})
    assert response.status_code == 401

def test_alterar_senha(mock_uc):
    mock_uc.alterar_senha.return_value = True
    response = client.put("/usuarios/1/senha", json={"senha_atual": "old", "nova_senha": "new"})
    assert response.status_code == 200
    mock_uc.alterar_senha.assert_called_once_with("1", "old", "new")

def test_alterar_senha_erro(mock_uc):
    mock_uc.alterar_senha.side_effect = ValueError("Senha atual incorreta")
    response = client.put("/usuarios/1/senha", json={"senha_atual": "old", "nova_senha": "new"})
    assert response.status_code == 400
