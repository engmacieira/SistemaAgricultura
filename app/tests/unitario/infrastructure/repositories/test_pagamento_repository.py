import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from app.infrastructure.repositories.pagamento_repository import PagamentoRepository

def test_pagamento_repository_init():
    db_mock = MagicMock(spec=Session)
    repo = PagamentoRepository(db_mock)
    assert repo.db == db_mock
