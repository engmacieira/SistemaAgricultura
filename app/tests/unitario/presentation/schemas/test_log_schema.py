import pytest
from pydantic import ValidationError
from datetime import datetime
from app.presentation.schemas.log_schema import LogCreate, LogResponse

def test_log_create_schema_valido():
    data = {
        "userId": "u1",
        "userName": "Admin",
        "action": "CRIAR",
        "entity": "Produtor",
        "details": "Detalhes"
    }
    schema = LogCreate(**data)
    assert schema.action == "CRIAR"

def test_log_create_schema_invalido():
    with pytest.raises(ValidationError):
        LogCreate(userId="u1") # faltam campos

def test_log_response_schema():
    data = {
        "id": "1",
        "userId": "u1",
        "userName": "Admin",
        "action": "CRIAR",
        "entity": "Produtor",
        "details": "Detalhes",
        "timestamp": "2023-11-01T12:00:00Z"
    }
    schema = LogResponse(**data)
    assert schema.id == "1"
    assert isinstance(schema.timestamp, datetime)
