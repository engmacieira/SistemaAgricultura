import pytest
from unittest.mock import Mock
from datetime import datetime
from app.domain.repositories.log_repository import ILogRepository
from app.domain.entities.log_entity import Log

def test_log_repository_interface():
    repo_mock = Mock(spec=ILogRepository)
    
    log_esperado = Log(
        id="1", timestamp=datetime.now(), userId="u1", userName="Admin",
        action="CREATE", entity="User", details="Details"
    )
    
    repo_mock.get_all.return_value = [log_esperado]
    repo_mock.create.return_value = log_esperado
    
    assert repo_mock.get_all() == [log_esperado]
    assert repo_mock.create({"action": "CREATE"}) == log_esperado
    
    repo_mock.get_all.assert_called_once()
    repo_mock.create.assert_called_once_with({"action": "CREATE"})
