from unittest.mock import ANY
import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from app.main import app
from app.core.dependencies import get_current_user
from app.presentation.routers.execucoes import get_use_case

client = TestClient(app)

@pytest.fixture
def mock_uc():
    uc = MagicMock()
    app.dependency_overrides[get_use_case] = lambda: uc
    app.dependency_overrides[get_current_user] = lambda: {"id": "1", "name": "Admin Test", "email": "admin@teste.com", "role": "admin"}
    yield uc
    app.dependency_overrides.clear()

execucao_mock = {
    "id": "1",
    "solicitacaoId": "sol-1",
    "serviceId": "s1",
    "serviceName": "S1",
    "date": "2026-03-03",
    "quantity": 10.0,
    "unit": "H",
    "valor_unitario": 10.0,
    "totalValue": 100.0,
    "status": "REGISTRADA",
}

def test_listar_execucoes(mock_uc):
    mock_uc.listar_execucoes.return_value = [execucao_mock]
    response = client.get("/api/execucoes/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert data[0]["id"] == "1"

def test_obter_execucao(mock_uc):
    mock_uc.obter_execucao.return_value = execucao_mock
    response = client.get("/api/execucoes/1")
    assert response.status_code == 200
    assert response.json()["id"] == "1"

def test_obter_execucao_nao_encontrado(mock_uc):
    mock_uc.obter_execucao.side_effect = ValueError("Execução não encontrada")
    response = client.get("/api/execucoes/1")
    assert response.status_code == 404
    assert response.json() == {"detail": "Execução não encontrada"}

def test_registrar_execucao(mock_uc):
    from datetime import date
    payload = {
        "solicitacaoId": "sol-1",
        "serviceId": "s1",
        "serviceName": "Servico 1",
        "date": "2026-03-03",
        "quantity": 10.0,
        "unit": "Hectare",
        "valor_unitario": 100.0,
        "totalValue": 1000.0,
        "status": "REGISTRADA"
    }
    # O Pydantic converte a string para date object no model_dump()
    expected_payload = payload.copy()
    expected_payload["date"] = date(2026, 3, 3)
    
    # Adiciona campos opcionais padroes que o schema pode ter (operador_maquina: None)
    expected_payload["operador_maquina"] = None
    
    mock_uc.criar_execucao.return_value = {"id": "1", **payload, "operador_maquina": None}
    response = client.post("/api/execucoes/", json=payload)
    assert response.status_code == 201
    assert response.json()["id"] == "1"
    mock_uc.criar_execucao.assert_called_once_with(expected_payload, ANY)

def test_atualizar_execucao(mock_uc):
    mock_uc.atualizar_execucao.return_value = {**execucao_mock, "status": "FATURADA"}
    response = client.put("/api/execucoes/1", json={"status": "FATURADA"})
    assert response.status_code == 200
    assert response.json()["id"] == "1"
    mock_uc.atualizar_execucao.assert_called_once_with("1", {"status": "FATURADA"}, {"id": "1", "name": "Admin Test", "email": "admin@teste.com", "role": "admin"})

def test_atualizar_execucao_erro(mock_uc):
    mock_uc.atualizar_execucao.side_effect = ValueError("Nao encontrado")
    response = client.put("/api/execucoes/1", json={"status": "FATURADA"})
    assert response.status_code == 404

def test_deletar_execucao(mock_uc):
    mock_uc.deletar_execucao.return_value = True
    response = client.delete("/api/execucoes/1")
    assert response.status_code == 204

def test_deletar_execucao_falha(mock_uc):
    mock_uc.deletar_execucao.side_effect = ValueError("Execução não encontrada")
    response = client.delete("/api/execucoes/1")
    assert response.status_code == 404
