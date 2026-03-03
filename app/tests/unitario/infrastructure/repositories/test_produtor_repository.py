import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from app.infrastructure.repositories.produtor_repository import ProdutorRepository
from app.infrastructure.models.produtor_model import ProdutorModel
from app.domain.entities.produtor_entity import Produtor

def test_produtor_repository_get_by_cpf_cnpj():
    db_mock = MagicMock(spec=Session)
    repo = ProdutorRepository(db_mock)
    
    query_mock = MagicMock()
    model_mock = MagicMock(spec=ProdutorModel)
    entidade_mock = Produtor(id="1", name="João", cpfCnpj="123", property="A", totalArea=10, status="A")
    model_mock.to_entity.return_value = entidade_mock
    
    query_mock.filter.return_value = query_mock
    query_mock.first.return_value = model_mock
    db_mock.query.return_value = query_mock
    
    result = repo.get_by_cpf_cnpj("123")
    
    assert result == entidade_mock
    db_mock.query.assert_called_with(ProdutorModel)
    query_mock.filter.assert_called_once()

def test_produtor_repository_has_execucoes():
    db_mock = MagicMock(spec=Session)
    repo = ProdutorRepository(db_mock)
    
    query_mock = MagicMock()
    query_mock.filter.return_value = query_mock
    query_mock.count.return_value = 5 # possui execuções
    db_mock.query.return_value = query_mock
    
    result = repo.has_execucoes("p1")
    
    assert result is True
    query_mock.count.assert_called_once()
