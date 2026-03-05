import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from app.main import app
from app.core.dependencies import get_current_user
from app.presentation.routers.administrador import get_use_case

client = TestClient(app)

@pytest.fixture
def mock_uc():
    uc = MagicMock()
    app.dependency_overrides[get_use_case] = lambda: uc
    app.dependency_overrides[get_current_user] = lambda: {"id": "1", "name": "Admin Test", "email": "admin@teste.com", "role": "admin"}
    yield uc
    app.dependency_overrides.clear()

configuracao_mock = {"unidades_medida": ["hr", "ha"]}
backup_mock = {"status": "ok", "message": "Backup realizado", "timestamp": "2026-03-05T10:00:00Z", "file_url": "url.sql"}

def test_obter_configuracoes(mock_uc):
    mock_uc.obter_configuracoes.return_value = configuracao_mock
    response = client.get("/admin/configuracoes")
    assert response.status_code == 200
    assert response.json() == configuracao_mock

def test_atualizar_configuracoes(mock_uc):
    mock_uc.atualizar_configuracoes.return_value = configuracao_mock
    response = client.put("/admin/configuracoes", json=configuracao_mock)
    assert response.status_code == 200
    assert response.json() == configuracao_mock

def test_realizar_backup(mock_uc):
    mock_uc.realizar_backup.return_value = backup_mock
    response = client.post("/admin/backup")
    assert response.status_code == 200
    assert response.json() == backup_mock

def test_realizar_backup_erro(mock_uc):
    mock_uc.realizar_backup.side_effect = ValueError("Erro")
    response = client.post("/admin/backup")
    assert response.status_code == 400
    assert response.json() == {"detail": "Erro"}

def test_restaurar_backup(mock_uc):
    mock_uc.restaurar_backup.return_value = {**backup_mock, "status": "restaurado"}
    response = client.post("/admin/restaurar", json={"file_url": "url.sql"})
    assert response.status_code == 200
    assert response.json()["status"] == "restaurado"
    mock_uc.restaurar_backup.assert_called_once_with("url.sql")

def test_restaurar_backup_erro(mock_uc):
    mock_uc.restaurar_backup.side_effect = ValueError("Falha")
    response = client.post("/admin/restaurar", json={"file_url": "url.sql"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Falha"}
