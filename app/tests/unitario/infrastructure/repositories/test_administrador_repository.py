import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from app.infrastructure.repositories.administrador_repository import AdministradorRepository
from app.infrastructure.models.administrador_model import ConfiguracaoModel

def test_administrador_repository_get_configuracoes():
    db_mock = MagicMock(spec=Session)
    repo = AdministradorRepository(db_mock)
    
    query_mock = MagicMock()
    config_mock = MagicMock(spec=ConfiguracaoModel)
    config_mock.valor = {"tema": "escuro"}
    query_mock.filter.return_value = query_mock
    query_mock.first.return_value = config_mock
    db_mock.query.return_value = query_mock
    
    result = repo.get_configuracoes()
    
    assert result == {"tema": "escuro"}

def test_administrador_repository_update_configuracoes_existing():
    db_mock = MagicMock(spec=Session)
    repo = AdministradorRepository(db_mock)
    
    query_mock = MagicMock()
    config_mock = MagicMock(spec=ConfiguracaoModel)
    config_mock.valor = {"tema": "claro"}
    query_mock.filter.return_value = query_mock
    query_mock.first.return_value = config_mock
    db_mock.query.return_value = query_mock
    
    result = repo.update_configuracoes({"tema": "escuro"})
    
    assert config_mock.valor == {"tema": "escuro"}
    assert result == {"tema": "escuro"}
    db_mock.commit.assert_called_once()
    db_mock.refresh.assert_called_once_with(config_mock)

def test_administrador_repository_update_configuracoes_new():
    db_mock = MagicMock(spec=Session)
    repo = AdministradorRepository(db_mock)
    
    query_mock = MagicMock()
    query_mock.filter.return_value = query_mock
    query_mock.first.return_value = None # Simula não encontrar registro
    db_mock.query.return_value = query_mock
    
    # Ao adicionar, devemos fazer o db.add de uma instância real ou mock
    result = repo.update_configuracoes({"tema": "escuro"})
    
    assert db_mock.add.called
    assert db_mock.commit.called
    assert db_mock.refresh.called
