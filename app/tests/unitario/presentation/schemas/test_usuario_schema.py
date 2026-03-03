import pytest
from pydantic import ValidationError
from app.presentation.schemas.usuario_schema import UsuarioCreate, UsuarioUpdate

def test_usuario_create_schema_valido():
    data = {
        "name": "Admin",
        "email": "admin@exemplo.com", # EmailStr valida formato
        "role": "Admin",
        "password": "senha"
    }
    schema = UsuarioCreate(**data)
    assert schema.name == "Admin"
    assert schema.email == "admin@exemplo.com"

def test_usuario_create_schema_email_invalido():
    data = {
        "name": "Admin",
        "email": "email-invalido-sem-arroba",
        "role": "Admin",
        "password": "senha"
    }
    with pytest.raises(ValidationError):
        UsuarioCreate(**data)

def test_usuario_update_schema():
    data = {"role": "User"}
    schema = UsuarioUpdate(**data)
    assert schema.role == "User"
    assert schema.name is None
