from unittest.mock import ANY
import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from app.main import app
from app.core.dependencies import get_current_user
from app.presentation.routers.pagamentos import get_use_case

client = TestClient(app)

@pytest.fixture
def mock_uc():
    uc = MagicMock()
    app.dependency_overrides[get_use_case] = lambda: uc
    app.dependency_overrides[get_current_user] = lambda: {"id": "1", "name": "Admin Test", "email": "admin@teste.com", "role": "admin"}
    yield uc
    app.dependency_overrides.clear()

pagamento_mock = {
    "id": "1",
    "executionId": "e1",
    "producerName": "P1",
    "serviceName": "S1",
    "dueDate": "2026-03-03",
    "amount": 100.0,
    "paidAmount": 100.0,
    "status": "Pago",
    "paymentDate": "2026-03-03",
    "is_deleted": False
}

def test_listar_pagamentos(mock_uc):
    mock_uc.listar_pagamentos.return_value = [pagamento_mock]
    mock_uc.contar_pagamentos.return_value = 1
    response = client.get("/pagamentos/")
    assert response.status_code == 200
    assert response.json()["items"][0]["id"] == "1"
    assert response.json()["total"] == 1

def test_obter_pagamento(mock_uc):
    mock_uc.obter_pagamento.return_value = pagamento_mock
    response = client.get("/pagamentos/1")
    assert response.status_code == 200
    assert response.json()["id"] == "1"

def test_obter_pagamento_erro(mock_uc):
    mock_uc.obter_pagamento.side_effect = ValueError("Pagamento não encontrado")
    response = client.get("/pagamentos/1")
    assert response.status_code == 404

def test_registrar_pagamento(mock_uc):
    mock_uc.registrar_pagamento.return_value = {"id": "1", "status": "Pago"}
    response = client.post("/pagamentos/1/pagar", json={"amountToPay": 100.0})
    assert response.status_code == 201
    assert response.json() == {"id": "1", "status": "Pago"}
    mock_uc.registrar_pagamento.assert_called_once_with("1", 100.0, None, {"id": "1", "name": "Admin Test", "email": "admin@teste.com", "role": "admin"})

def test_registrar_pagamento_erro(mock_uc):
    mock_uc.registrar_pagamento.side_effect = ValueError("Este pagamento já foi realizado")
    response = client.post("/pagamentos/1/pagar", json={"amountToPay": 100.0})
    assert response.status_code == 400
    assert response.json() == {"detail": "Este pagamento já foi realizado"}
