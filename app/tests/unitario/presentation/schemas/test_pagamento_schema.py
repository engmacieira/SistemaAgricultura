import pytest
from pydantic import ValidationError
from datetime import date
from app.presentation.schemas.pagamento_schema import PagamentoCreate, PagamentoUpdate, PagamentoResponse

def test_pagamento_create_schema_valido():
    data = {
        "executionId": "e1",
        "producerName": "João",
        "serviceName": "Aração",
        "dueDate": "2023-12-31",
        "amount": 1500.0,
        "status": "Pendente"
    }
    schema = PagamentoCreate(**data)
    assert schema.executionId == "e1"
    assert isinstance(schema.dueDate, date)

def test_pagamento_create_schema_invalido():
    # Falta amount e dueDate (date incorreto dispara erro)
    data = {
        "executionId": "e1",
        "producerName": "João",
        "serviceName": "Aração",
        "dueDate": "data-invalida",
        "status": "Pendente"
    }
    with pytest.raises(ValidationError):
        PagamentoCreate(**data)

def test_pagamento_update_schema():
    data = {"status": "Pago", "paymentDate": "2023-11-15"}
    schema = PagamentoUpdate(**data)
    assert schema.status == "Pago"
    assert isinstance(schema.paymentDate, date)
