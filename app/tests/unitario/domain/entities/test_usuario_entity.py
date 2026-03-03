import pytest
from app.domain.entities.usuario_entity import Usuario

def test_criar_usuario():
    usuario = Usuario(
        id="u1",
        name="Maria",
        email="maria@exemplo.com",
        role="Admin",
        password_hash="hash123456"
    )
    
    assert usuario.id == "u1"
    assert usuario.name == "Maria"
    assert usuario.email == "maria@exemplo.com"
    assert usuario.role == "Admin"
    assert usuario.password_hash == "hash123456"
