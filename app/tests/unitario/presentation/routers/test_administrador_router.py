import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from app.main import app
from app.presentation.routers.administrador import get_use_case

client = TestClient(app)

@pytest.fixture
def mock_uc():
    uc = MagicMock()
    app.dependency_overrides[get_use_case] = lambda: uc
    yield uc
    app.dependency_overrides.clear()

def test_obter_configuracoes(mock_uc):
    mock_uc.obter_configuracoes.return_value = {"tema": "escuro"}
    response = client.get("/admin/configuracoes")
    assert response.status_code == 200
    assert response.json() == {"tema": "escuro"}

def test_atualizar_configuracoes(mock_uc):
    mock_uc.atualizar_configuracoes.return_value = {"tema": "claro"}
    response = client.put("/admin/configuracoes", json={"tema": "claro"})
    assert response.status_code == 200
    assert response.json() == {"tema": "claro"}

def test_realizar_backup(mock_uc):
    mock_uc.realizar_backup.return_value = {"status": "ok"}
    response = client.post("/admin/backup")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_realizar_backup_erro(mock_uc):
    mock_uc.realizar_backup.side_effect = ValueError("Erro")
    response = client.post("/admin/backup")
    assert response.status_code == 400
    assert response.json() == {"detail": "Erro"}

def test_restaurar_backup(mock_uc):
    mock_uc.restaurar_backup.return_value = {"status": "restaurado"}
    response = client.post("/admin/restaurar", json={"file_url": "url.sql"})
    assert response.status_code == 200
    assert response.json() == {"status": "restaurado"}
    mock_uc.restaurar_backup.assert_called_once_with("url.sql")

def test_restaurar_backup_erro(mock_uc):
    mock_uc.restaurar_backup.side_effect = ValueError("Falha")
    response = client.post("/admin/restaurar", json={"file_url": "url.sql"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Falha"}
