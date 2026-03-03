import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from app.main import app
from app.presentation.routers.execucoes import get_use_case

client = TestClient(app)

@pytest.fixture
def mock_uc():
    uc = MagicMock()
    app.dependency_overrides[get_use_case] = lambda: uc
    yield uc
    app.dependency_overrides.clear()

def test_listar_execucoes(mock_uc):
    mock_uc.listar_execucoes.return_value = [{"id": "1", "status": "Pendente"}]
    response = client.get("/execucoes/")
    assert response.status_code == 200
    assert response.json() == [{"id": "1", "status": "Pendente"}]

def test_obter_execucao(mock_uc):
    mock_uc.obter_execucao.return_value = {"id": "1"}
    response = client.get("/execucoes/1")
    assert response.status_code == 200
    assert response.json() == {"id": "1"}

def test_obter_execucao_nao_encontrado(mock_uc):
    mock_uc.obter_execucao.side_effect = ValueError("Execução não encontrada")
    response = client.get("/execucoes/1")
    assert response.status_code == 404
    assert response.json() == {"detail": "Execução não encontrada"}

def test_registrar_execucao(mock_uc):
    from datetime import date
    payload = {
        "producerId": "p1",
        "producerName": "Produtor 1",
        "serviceId": "s1",
        "serviceName": "Servico 1",
        "date": "2026-03-03",
        "quantity": 10.0,
        "unit": "Hectare",
        "totalValue": 1000.0,
        "status": "Pendente"
    }
    # O Pydantic converte a string para date object no model_dump()
    expected_payload = payload.copy()
    expected_payload["date"] = date(2026, 3, 3)
    
    mock_uc.criar_execucao.return_value = {"id": "1", **payload}
    response = client.post("/execucoes/", json=payload)
    assert response.status_code == 200
    assert response.json()["id"] == "1"
    mock_uc.criar_execucao.assert_called_once_with(expected_payload)

def test_atualizar_execucao(mock_uc):
    mock_uc.atualizar_execucao.return_value = {"id": "1", "status": "Cancelado"}
    response = client.put("/execucoes/1", json={"status": "Cancelado"})
    assert response.status_code == 200
    assert response.json() == {"id": "1", "status": "Cancelado"}
    mock_uc.atualizar_execucao.assert_called_once_with("1", {"status": "Cancelado"})

def test_atualizar_execucao_erro(mock_uc):
    mock_uc.atualizar_execucao.side_effect = ValueError("Nao encontrado")
    response = client.put("/execucoes/1", json={"status": "Cancelado"})
    assert response.status_code == 404

def test_deletar_execucao(mock_uc):
    mock_uc.deletar_execucao.return_value = True
    response = client.delete("/execucoes/1")
    assert response.status_code == 200
    assert response.json() == {"message": "Execução deletada com sucesso"}

def test_deletar_execucao_falha(mock_uc):
    mock_uc.deletar_execucao.return_value = False
    response = client.delete("/execucoes/1")
    assert response.status_code == 404
