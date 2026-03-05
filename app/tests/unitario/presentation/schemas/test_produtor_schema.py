import pytest
from pydantic import ValidationError
from app.presentation.schemas.produtor_schema import ProdutorCreate, ProdutorUpdate

def test_produtor_create_schema_valido():
    data = {
        "name": "João",
        "cpfCnpj": "123.456.789-00",
        "property": "Fazenda",
        "regiao_referencia": "Norte",
        "status": "Ativo"
    }
    schema = ProdutorCreate(**data)
    assert schema.name == "João"
    assert schema.regiao_referencia == "Norte"

def test_produtor_create_schema_invalido():
    with pytest.raises(ValidationError):
        ProdutorCreate(name="João") # falta cpfCnpj e rest

def test_produtor_update_schema():
    data = {"status": "Inativo"}
    schema = ProdutorUpdate(**data)
    assert schema.status == "Inativo"
    assert schema.name is None
