import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from app.main import app
from app.presentation.routers.logs import get_use_case

client = TestClient(app)

@pytest.fixture
def mock_uc():
    uc = MagicMock()
    app.dependency_overrides[get_use_case] = lambda: uc
    yield uc
    app.dependency_overrides.clear()

def test_listar_logs(mock_uc):
    mock_uc.listar_logs.return_value = [{"id": "1", "action": "LOGIN"}]
    response = client.get("/logs/")
    assert response.status_code == 200
    assert response.json() == [{"id": "1", "action": "LOGIN"}]
    mock_uc.listar_logs.assert_called_once()
