import pytest
from app.infrastructure.models.usuario_model import UsuarioModel
from app.domain.entities.usuario_entity import Usuario

def test_usuario_model_to_entity():
    model = UsuarioModel(
        id="usr1",
        name="Usuário de Teste",
        email="teste@teste.com",
        role="Admin",
        password_hash="hahahadfasdf8asdf8"
    )
    
    entity = model.to_entity()
    assert isinstance(entity, Usuario)
    assert entity.id == model.id
    assert entity.name == model.name
    assert entity.email == model.email
    assert entity.role == model.role
    assert entity.password_hash == model.password_hash
