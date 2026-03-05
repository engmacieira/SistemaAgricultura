import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from app.main import app
from app.core.dependencies import get_current_user
from app.presentation.routers.logs import get_use_case

client = TestClient(app)

@pytest.fixture
def mock_uc():
    uc = MagicMock()
    app.dependency_overrides[get_use_case] = lambda: uc
    app.dependency_overrides[get_current_user] = lambda: {"id": "1", "name": "Admin Test", "email": "admin@teste.com", "role": "admin"}
    yield uc
    app.dependency_overrides.clear()

def test_listar_logs(mock_uc):
    logs_data = {"items": [{"id": "1", "userId": "u1", "userName": "U1", "action": "LOGIN", "entity": "auth", "details": "d", "timestamp": "2026-03-03T10:00:00"}], "total": 1, "page": 1, "pages": 1}
    mock_uc.listar_logs.return_value = logs_data
    response = client.get("/api/logs/")
    assert response.status_code == 200
    assert response.json()["items"][0]["action"] == "LOGIN"
    assert response.json()["total"] == 1
    mock_uc.listar_logs.assert_called_once()
