import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from app.main import app
from app.presentation.routers.servicos import get_use_case

client = TestClient(app)

@pytest.fixture
def mock_uc():
    uc = MagicMock()
    app.dependency_overrides[get_use_case] = lambda: uc
    yield uc
    app.dependency_overrides.clear()

def test_listar_servicos(mock_uc):
    mock_uc.listar_servicos.return_value = [{"id": "1", "name": "Aração"}]
    response = client.get("/servicos/")
    assert response.status_code == 200
    assert response.json() == [{"id": "1", "name": "Aração"}]

def test_obter_servico(mock_uc):
    mock_uc.obter_servico.return_value = {"id": "1", "name": "Aração"}
    response = client.get("/servicos/1")
    assert response.status_code == 200

def test_obter_servico_erro(mock_uc):
    mock_uc.obter_servico.side_effect = ValueError("Not found")
    response = client.get("/servicos/1")
    assert response.status_code == 404

def test_criar_servico(mock_uc):
    mock_uc.criar_servico.return_value = {"id": "1", "name": "Aração"}
    response = client.post("/servicos/", json={"name": "Aração"})
    assert response.status_code == 200

def test_criar_servico_erro(mock_uc):
    mock_uc.criar_servico.side_effect = ValueError("Existe")
    response = client.post("/servicos/", json={"name": "Aração"})
    assert response.status_code == 400

def test_atualizar_servico(mock_uc):
    mock_uc.atualizar_servico.return_value = {"id": "1"}
    response = client.put("/servicos/1", json={"name": "Novo"})
    assert response.status_code == 200

def test_deletar_servico(mock_uc):
    mock_uc.deletar_servico.return_value = True
    response = client.delete("/servicos/1")
    assert response.status_code == 200
    mock_uc.deletar_servico.assert_called_once_with("1", {"id": "system", "name": "Sistema"})

def test_deletar_servico_erro(mock_uc):
    mock_uc.deletar_servico.side_effect = ValueError("Tem execuções")
    response = client.delete("/servicos/1")
    assert response.status_code == 400
