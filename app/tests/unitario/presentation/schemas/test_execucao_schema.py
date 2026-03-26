import pytest
from pydantic import ValidationError
from datetime import date
from app.presentation.schemas.execucao_schema import ExecucaoCreate, ExecucaoUpdate, ExecucaoResponse

def test_execucao_create_schema_valido():
    data = {
        "solicitacaoId": "solic-1",
        "serviceId": "s1",
        "serviceName": "Aração",
        "date": "2023-11-01",
        "quantity": 10.5,
        "unit": "ha",
        "valor_unitario": 150.0,
        "totalValue": 1575.0,
        "status": "REGISTRADA",
        "operador_maquina": "João"
    }
    schema = ExecucaoCreate(**data)
    assert schema.solicitacaoId == "solic-1"
    assert isinstance(schema.date, date)
    assert schema.quantity == 10.5
    assert schema.valor_unitario == 150.0

def test_execucao_create_schema_invalido():
    data = {
        "solicitacaoId": "solic-1"
        # Faltam campos obrigatórios
    }
    with pytest.raises(ValidationError):
        ExecucaoCreate(**data)

def test_execucao_update_schema():
    # Update permite itens opcionais
    data = {"status": "FATURADA", "operador_maquina": "Carlos"}
    schema = ExecucaoUpdate(**data)
    assert schema.status == "FATURADA"
    assert schema.operador_maquina == "Carlos"
    assert schema.serviceId is None
