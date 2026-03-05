import pytest
from unittest.mock import MagicMock
from app.application.use_cases.execucao_use_cases import ExecucaoUseCases

def test_obter_execucao_sucesso():
    repo_mock = MagicMock()
    execucao_mock = MagicMock()
    repo_mock.get_by_id.return_value = execucao_mock
    use_cases = ExecucaoUseCases(repo_mock)
    
    result = use_cases.obter_execucao("1")
    assert result == execucao_mock
    repo_mock.get_by_id.assert_called_once_with("1")

def test_listar_execucoes():
    repo_mock = MagicMock()
    repo_mock.get_all_paginated.return_value = []
    use_cases = ExecucaoUseCases(repo_mock)
    
    result = use_cases.listar_execucoes()
    assert result == []
    repo_mock.get_all_paginated.assert_called_once()

def test_obter_execucao_nao_encontrado():
    repo_mock = MagicMock()
    repo_mock.get_by_id.return_value = None
    use_cases = ExecucaoUseCases(repo_mock)
    
    with pytest.raises(ValueError, match="Execução não encontrada"):
        use_cases.obter_execucao("1")

def test_criar_execucao():
    repo_mock = MagicMock()
    data = {"producerId": "1", "serviceId": "2", "totalValue": 100}
    nova_exec_mock = MagicMock()
    repo_mock.create.return_value = nova_exec_mock
    use_cases = ExecucaoUseCases(repo_mock)
    
    result = use_cases.criar_execucao(data)
    assert result == nova_exec_mock
    repo_mock.create.assert_called_once_with(data)

def test_atualizar_execucao():
    repo_mock = MagicMock()
    exec_mock = MagicMock()
    repo_mock.get_by_id.return_value = exec_mock
    repo_mock.update.return_value = exec_mock
    use_cases = ExecucaoUseCases(repo_mock)
    
    result = use_cases.atualizar_execucao("1", {"status": "Concluído"})
    assert result == exec_mock
    repo_mock.get_by_id.assert_called_once_with("1")
    repo_mock.update.assert_called_once_with("1", {"status": "Concluído"})
