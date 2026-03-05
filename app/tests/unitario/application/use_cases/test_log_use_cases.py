import pytest
from unittest.mock import MagicMock, ANY
from app.application.use_cases.log_use_cases import LogUseCases
from datetime import datetime

def test_listar_logs():
    repo_mock = MagicMock()
    logs_mock = [MagicMock()]
    repo_mock.get_all_paginated.return_value = logs_mock
    repo_mock.count.return_value = 1
    use_cases = LogUseCases(repo_mock)
    
    result = use_cases.listar_logs()
    
    assert result["items"] == logs_mock
    assert result["total"] == 1
    repo_mock.get_all_paginated.assert_called_once_with(0, 10, "timestamp", "desc", "")

def test_registrar_acao():
    repo_mock = MagicMock()
    log_criado_mock = MagicMock()
    repo_mock.create.return_value = log_criado_mock
    use_cases = LogUseCases(repo_mock)
    
    result = use_cases.registrar_acao("u1", "Admin", "CRIAR", "EntidadeX", "DetalhesY", "Antigo", "Novo")
    assert result == log_criado_mock
    
    # O create deve ter sido chamado com um dict contendo as informações passadas
    repo_mock.create.assert_called_once_with({
        "userId": "u1",
        "userName": "Admin",
        "action": "CRIAR",
        "entity": "EntidadeX",
        "details": "DetalhesY",
        "dados_anteriores": "Antigo",
        "dados_novos": "Novo",
        "timestamp": ANY
    })
