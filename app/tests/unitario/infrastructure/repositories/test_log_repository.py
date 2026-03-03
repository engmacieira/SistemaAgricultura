import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from app.infrastructure.repositories.log_repository import LogRepository

def test_log_repository_init():
    db_mock = MagicMock(spec=Session)
    repo = LogRepository(db_mock)
    assert repo.db == db_mock
