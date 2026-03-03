import pytest
from unittest.mock import MagicMock
from app.application.use_cases.administrador_use_cases import AdministradorUseCases

def test_obter_configuracoes():
    repo_mock = MagicMock()
    repo_mock.get_configuracoes.return_value = {"tema": "escuro"}
    use_cases = AdministradorUseCases(repo_mock)
    
    assert use_cases.obter_configuracoes() == {"tema": "escuro"}
    repo_mock.get_configuracoes.assert_called_once()

def test_atualizar_configuracoes():
    repo_mock = MagicMock()
    repo_mock.update_configuracoes.return_value = {"tema": "claro"}
    use_cases = AdministradorUseCases(repo_mock)
    
    assert use_cases.atualizar_configuracoes({"tema": "claro"}) == {"tema": "claro"}
    repo_mock.update_configuracoes.assert_called_once_with({"tema": "claro"})

def test_realizar_backup_sem_servico():
    use_cases = AdministradorUseCases(MagicMock(), backup_service=None)
    with pytest.raises(ValueError, match="Serviço de backup não configurado"):
        use_cases.realizar_backup()

def test_restaurar_backup_sem_servico():
    use_cases = AdministradorUseCases(MagicMock(), backup_service=None)
    with pytest.raises(ValueError, match="Serviço de backup não configurado"):
        use_cases.restaurar_backup("url_mock")
