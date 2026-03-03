import pytest
from unittest.mock import Mock
from app.domain.repositories.usuario_repository import IUsuarioRepository
from app.domain.entities.usuario_entity import Usuario

def test_usuario_repository_interface():
    repo_mock = Mock(spec=IUsuarioRepository)
    
    usuario_esperado = Usuario(
        id="u1", name="Admin", email="admin@exemplo.com", role="Admin",
        password_hash="hash"
    )
    
    repo_mock.get_all.return_value = [usuario_esperado]
    repo_mock.get_by_id.return_value = usuario_esperado
    repo_mock.create.return_value = usuario_esperado
    repo_mock.update.return_value = usuario_esperado
    repo_mock.delete.return_value = True
    repo_mock.get_by_email.return_value = usuario_esperado
    
    assert repo_mock.get_all() == [usuario_esperado]
    assert repo_mock.get_by_id("u1") == usuario_esperado
    assert repo_mock.create({"name": "Admin"}) == usuario_esperado
    assert repo_mock.update("u1", {"role": "User"}) == usuario_esperado
    assert repo_mock.delete("u1") is True
    assert repo_mock.get_by_email("admin@exemplo.com") == usuario_esperado
    
    repo_mock.get_all.assert_called_once()
    repo_mock.get_by_id.assert_called_once_with("u1")
    repo_mock.create.assert_called_once_with({"name": "Admin"})
    repo_mock.update.assert_called_once_with("u1", {"role": "User"})
    repo_mock.delete.assert_called_once_with("u1")
    repo_mock.get_by_email.assert_called_once_with("admin@exemplo.com")
