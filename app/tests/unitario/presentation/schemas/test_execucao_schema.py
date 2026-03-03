import pytest
from pydantic import ValidationError
from datetime import date
from app.presentation.schemas.execucao_schema import ExecucaoCreate, ExecucaoUpdate, ExecucaoResponse

def test_execucao_create_schema_valido():
    data = {
        "producerId": "p1",
        "producerName": "João",
        "serviceId": "s1",
        "serviceName": "Aração",
        "date": "2023-11-01",
        "quantity": 10.5,
        "unit": "ha",
        "totalValue": 150.0,
        "status": "Pendente"
    }
    schema = ExecucaoCreate(**data)
    assert schema.producerId == "p1"
    assert isinstance(schema.date, date)
    assert schema.quantity == 10.5

def test_execucao_create_schema_invalido():
    data = {
        "producerId": "p1"
        # Faltam campos obrigatórios
    }
    with pytest.raises(ValidationError):
        ExecucaoCreate(**data)

def test_execucao_update_schema():
    # Update permite itens opcionais
    data = {"status": "Concluído"}
    schema = ExecucaoUpdate(**data)
    assert schema.status == "Concluído"
    assert schema.producerId is None
