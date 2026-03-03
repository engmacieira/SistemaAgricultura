import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from app.infrastructure.repositories.execucao_repository import ExecucaoRepository

def test_execucao_repository_init():
    db_mock = MagicMock(spec=Session)
    repo = ExecucaoRepository(db_mock)
    assert repo.db == db_mock
