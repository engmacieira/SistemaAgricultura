import pytest
from unittest.mock import MagicMock, ANY
from app.application.use_cases.log_use_cases import LogUseCases
from datetime import datetime

def test_listar_logs():
    repo_mock = MagicMock()
    logs_mock = [MagicMock()]
    repo_mock.get_all.return_value = logs_mock
    use_cases = LogUseCases(repo_mock)
    
    assert use_cases.listar_logs() == logs_mock
    repo_mock.get_all.assert_called_once()

def test_registrar_acao():
    repo_mock = MagicMock()
    log_criado_mock = MagicMock()
    repo_mock.create.return_value = log_criado_mock
    use_cases = LogUseCases(repo_mock)
    
    result = use_cases.registrar_acao("u1", "Admin", "CRIAR", "EntidadeX", "DetalhesY")
    assert result == log_criado_mock
    
    # O create deve ter sido chamado com um dict contendo as informações passadas
    repo_mock.create.assert_called_once_with({
        "userId": "u1",
        "userName": "Admin",
        "action": "CRIAR",
        "entity": "EntidadeX",
        "details": "DetalhesY",
        "timestamp": ANY
    })
