import pytest
from pydantic import ValidationError
from app.presentation.schemas.servico_schema import ServicoCreate, ServicoUpdate

def test_servico_create_schema_valido():
    data = {
        "name": "Aração",
        "description": "Desc",
        "unit": "ha",
        "basePrice": 150.0,
        "active": True
    }
    schema = ServicoCreate(**data)
    assert schema.name == "Aração"
    assert schema.basePrice == 150.0

def test_servico_create_schema_invalido():
    data = {
        "name": "Aração",
        "basePrice": "um_texto_invalido_para_float"
    }
    with pytest.raises(ValidationError):
        ServicoCreate(**data)

def test_servico_update_schema():
    data = {"active": False}
    schema = ServicoUpdate(**data)
    assert schema.active is False
    assert schema.name is None
