import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from app.main import app
from app.presentation.routers.produtores import get_use_case

client = TestClient(app)

@pytest.fixture
def mock_uc():
    uc = MagicMock()
    app.dependency_overrides[get_use_case] = lambda: uc
    yield uc
    app.dependency_overrides.clear()

def test_listar_produtores(mock_uc):
    mock_uc.listar_produtores.return_value = [{"id": "1", "name": "João"}]
    response = client.get("/produtores/")
    assert response.status_code == 200
    assert response.json() == [{"id": "1", "name": "João"}]

def test_obter_produtor(mock_uc):
    mock_uc.obter_produtor.return_value = {"id": "1", "name": "João"}
    response = client.get("/produtores/1")
    assert response.status_code == 200
    assert response.json() == {"id": "1", "name": "João"}

def test_obter_produtor_erro(mock_uc):
    mock_uc.obter_produtor.side_effect = ValueError("Produtor não encontrado")
    response = client.get("/produtores/1")
    assert response.status_code == 404

def test_criar_produtor(mock_uc):
    mock_uc.criar_produtor.return_value = {"id": "1"}
    response = client.post("/produtores/", json={"name": "Maria"})
    assert response.status_code == 200
    assert response.json() == {"id": "1"}
    # Verifica mock passando dados e o usuário injetado nas rotas: {"id": "system", "name": "Sistema"}
    mock_uc.criar_produtor.assert_called_once_with({"name": "Maria"}, {"id": "system", "name": "Sistema"})

def test_criar_produtor_erro(mock_uc):
    mock_uc.criar_produtor.side_effect = ValueError("CPF/CNPJ já cadastrado")
    response = client.post("/produtores/", json={"name": "Maria"})
    assert response.status_code == 400

def test_atualizar_produtor(mock_uc):
    mock_uc.atualizar_produtor.return_value = {"id": "1", "name": "Novo"}
    response = client.put("/produtores/1", json={"name": "Novo"})
    assert response.status_code == 200
    assert response.json() == {"id": "1", "name": "Novo"}

def test_deletar_produtor(mock_uc):
    mock_uc.deletar_produtor.return_value = True
    response = client.delete("/produtores/1")
    assert response.status_code == 200
    assert response.json() == {"message": "Produtor deletado com sucesso"}

def test_deletar_produtor_falha_bool(mock_uc):
    mock_uc.deletar_produtor.return_value = False
    response = client.delete("/produtores/1")
    assert response.status_code == 404
