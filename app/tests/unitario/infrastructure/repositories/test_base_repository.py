import pytest
from unittest.mock import Mock, MagicMock
from sqlalchemy.orm import Session
from app.infrastructure.repositories.base_repository import BaseRepository

class DummyEntity:
    pass

class DummyModel:
    id = "dummy"
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
    def to_entity(self):
        return DummyEntity()

def test_base_repository_get_all():
    db_mock = MagicMock(spec=Session)
    repo = BaseRepository(db_mock, DummyModel)
    
    query_mock = MagicMock()
    model_instance = DummyModel(id="1")
    query_mock.all.return_value = [model_instance]
    db_mock.query.return_value = query_mock
    
    result = repo.get_all()
    
    assert len(result) == 1
    assert isinstance(result[0], DummyEntity)
    db_mock.query.assert_called_once_with(DummyModel)
    query_mock.all.assert_called_once()

def test_base_repository_get_by_id():
    db_mock = MagicMock(spec=Session)
    repo = BaseRepository(db_mock, DummyModel)
    
    query_mock = MagicMock()
    model_instance = DummyModel(id="2")
    query_mock.filter.return_value = query_mock
    query_mock.first.return_value = model_instance
    db_mock.query.return_value = query_mock
    
    result = repo.get_by_id("2")
    
    assert isinstance(result, DummyEntity)
    db_mock.query.assert_called_once_with(DummyModel)
    query_mock.filter.assert_called_once()
    query_mock.first.assert_called_once()

def test_base_repository_create():
    db_mock = MagicMock(spec=Session)
    repo = BaseRepository(db_mock, DummyModel)
    
    data = {"id": "3"}
    result = repo.create(data)
    
    assert isinstance(result, DummyEntity)
    db_mock.add.assert_called_once()
    db_mock.commit.assert_called_once()
    db_mock.refresh.assert_called_once()

def test_base_repository_update_existing():
    db_mock = MagicMock(spec=Session)
    repo = BaseRepository(db_mock, DummyModel)
    
    query_mock = MagicMock()
    model_instance = DummyModel(id="4")
    query_mock.filter.return_value = query_mock
    query_mock.first.return_value = model_instance
    db_mock.query.return_value = query_mock
    
    result = repo.update("4", {"nome": "Teste"})
    
    assert getattr(model_instance, "nome") == "Teste"
    assert isinstance(result, DummyEntity)
    db_mock.commit.assert_called_once()
    db_mock.refresh.assert_called_once()

def test_base_repository_delete():
    db_mock = MagicMock(spec=Session)
    repo = BaseRepository(db_mock, DummyModel)
    
    query_mock = MagicMock()
    model_instance = DummyModel(id="5")
    query_mock.filter.return_value = query_mock
    query_mock.first.return_value = model_instance
    db_mock.query.return_value = query_mock
    
    result = repo.delete("5")
    
    assert result is True
    db_mock.delete.assert_called_once_with(model_instance)
    db_mock.commit.assert_called_once()
