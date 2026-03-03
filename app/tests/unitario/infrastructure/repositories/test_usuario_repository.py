import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from app.infrastructure.repositories.usuario_repository import UsuarioRepository
from app.infrastructure.models.usuario_model import UsuarioModel
from app.domain.entities.usuario_entity import Usuario

def test_usuario_repository_get_by_email():
    db_mock = MagicMock(spec=Session)
    repo = UsuarioRepository(db_mock)
    
    query_mock = MagicMock()
    model_mock = MagicMock(spec=UsuarioModel)
    entidade_mock = Usuario(id="u1", name="Admin", email="admin@ex.com", role="A", password_hash="h")
    model_mock.to_entity.return_value = entidade_mock
    
    query_mock.filter.return_value = query_mock
    query_mock.first.return_value = model_mock
    db_mock.query.return_value = query_mock
    
    result = repo.get_by_email("admin@ex.com")
    
    assert result == entidade_mock
    db_mock.query.assert_called_with(UsuarioModel)
    query_mock.filter.assert_called_once()
