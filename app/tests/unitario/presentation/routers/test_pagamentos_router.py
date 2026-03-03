import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from app.main import app
from app.presentation.routers.pagamentos import get_use_case

client = TestClient(app)

@pytest.fixture
def mock_uc():
    uc = MagicMock()
    app.dependency_overrides[get_use_case] = lambda: uc
    yield uc
    app.dependency_overrides.clear()

def test_listar_pagamentos(mock_uc):
    mock_uc.listar_pagamentos.return_value = [{"id": "1", "amount": 100}]
    response = client.get("/pagamentos/")
    assert response.status_code == 200
    assert response.json() == [{"id": "1", "amount": 100}]

def test_obter_pagamento(mock_uc):
    mock_uc.obter_pagamento.return_value = {"id": "1"}
    response = client.get("/pagamentos/1")
    assert response.status_code == 200
    assert response.json() == {"id": "1"}

def test_obter_pagamento_erro(mock_uc):
    mock_uc.obter_pagamento.side_effect = ValueError("Pagamento não encontrado")
    response = client.get("/pagamentos/1")
    assert response.status_code == 404

def test_registrar_pagamento(mock_uc):
    mock_uc.registrar_pagamento.return_value = {"id": "1", "status": "Pago"}
    response = client.post("/pagamentos/1/pagar")
    assert response.status_code == 200
    assert response.json() == {"id": "1", "status": "Pago"}
    mock_uc.registrar_pagamento.assert_called_once_with("1")

def test_registrar_pagamento_erro(mock_uc):
    mock_uc.registrar_pagamento.side_effect = ValueError("Este pagamento já foi realizado")
    response = client.post("/pagamentos/1/pagar")
    assert response.status_code == 400
    assert response.json() == {"detail": "Este pagamento já foi realizado"}
