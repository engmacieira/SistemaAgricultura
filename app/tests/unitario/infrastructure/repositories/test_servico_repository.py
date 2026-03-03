import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from app.infrastructure.repositories.servico_repository import ServicoRepository
from app.infrastructure.models.servico_model import ServicoModel
from app.domain.entities.servico_entity import Servico

def test_servico_repository_get_by_name():
    db_mock = MagicMock(spec=Session)
    repo = ServicoRepository(db_mock)
    
    query_mock = MagicMock()
    model_mock = MagicMock(spec=ServicoModel)
    entidade_mock = Servico(id="s1", name="Aração", description="D", unit="H", basePrice=10, active=True)
    model_mock.to_entity.return_value = entidade_mock
    
    query_mock.filter.return_value = query_mock
    query_mock.first.return_value = model_mock
    db_mock.query.return_value = query_mock
    
    result = repo.get_by_name("Aração")
    
    assert result == entidade_mock
    db_mock.query.assert_called_with(ServicoModel)

def test_servico_repository_has_execucoes():
    db_mock = MagicMock(spec=Session)
    repo = ServicoRepository(db_mock)
    
    query_mock = MagicMock()
    query_mock.filter.return_value = query_mock
    query_mock.count.return_value = 0 # não possui execuções
    db_mock.query.return_value = query_mock
    
    result = repo.has_execucoes("s1")
    
    assert result is False
    query_mock.count.assert_called_once()
