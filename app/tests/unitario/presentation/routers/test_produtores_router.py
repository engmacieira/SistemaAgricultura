from unittest.mock import ANY
import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from app.main import app
from app.presentation.routers.produtores import get_use_case
from app.core.dependencies import get_current_user

client = TestClient(app)

@pytest.fixture
def mock_uc():
    uc = MagicMock()
    app.dependency_overrides[get_use_case] = lambda: uc
    app.dependency_overrides[get_current_user] = lambda: {"id": "test_user_id", "name": "Test User"}
    yield uc
    app.dependency_overrides.clear()

produtor_mock = {
    "id": "1",
    "name": "João",
    "cpfCnpj": "123",
    "property": "Prop",
    "regiao_referencia": "R",
    "telefone_contato": "1",
    "apelido_produtor": "A",
    "status": "Ativo",
    "is_deleted": False
}

def test_listar_produtores(mock_uc):
    mock_uc.listar_produtores.return_value = {"items": [produtor_mock], "total": 1, "page": 1, "size": 10, "pages": 1}
    response = client.get("/api/produtores/")
    assert response.status_code == 200
    assert response.json()["items"][0]["id"] == "1"

def test_obter_produtor(mock_uc):
    mock_uc.obter_produtor.return_value = produtor_mock
    response = client.get("/api/produtores/1")
    assert response.status_code == 200
    assert response.json()["id"] == "1"

def test_obter_produtor_erro(mock_uc):
    mock_uc.obter_produtor.side_effect = ValueError("Produtor não encontrado")
    response = client.get("/api/produtores/1")
    assert response.status_code == 404

def test_criar_produtor(mock_uc):
    mock_uc.criar_produtor.return_value = produtor_mock
    payload = {"name": "Maria", "cpfCnpj": "123", "property": "Prop", "status": "Ativo", "regiao_referencia": None, "telefone_contato": None, "apelido_produtor": None}
    response = client.post("/api/produtores/", json=payload)
    assert response.status_code == 201
    assert response.json()["id"] == "1"
    mock_uc.criar_produtor.assert_called_once_with(payload, {"id": "test_user_id", "name": "Test User"})

def test_criar_produtor_erro(mock_uc):
    mock_uc.criar_produtor.side_effect = ValueError("CPF/CNPJ já cadastrado")
    response = client.post("/api/produtores/", json={"name": "Maria", "cpfCnpj": "123", "property": "Prop", "status": "Ativo"})
    assert response.status_code == 400

def test_atualizar_produtor(mock_uc):
    mock_uc.atualizar_produtor.return_value = {**produtor_mock, "name": "Novo"}
    response = client.put("/api/produtores/1", json={"name": "Novo"})
    assert response.status_code == 200
    assert response.json()["name"] == "Novo"

def test_deletar_produtor(mock_uc):
    mock_uc.deletar_produtor.return_value = True
    response = client.delete("/api/produtores/1")
    assert response.status_code == 204

def test_deletar_produtor_falha_bool(mock_uc):
    mock_uc.deletar_produtor.return_value = False
    response = client.delete("/api/produtores/1")
    assert response.status_code == 404
