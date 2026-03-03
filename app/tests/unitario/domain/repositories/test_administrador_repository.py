import pytest
from unittest.mock import Mock
from app.domain.repositories.administrador_repository import IAdministradorRepository

def test_administrador_repository_interface():
    # Cria um mock que implementa a interface
    repo_mock = Mock(spec=IAdministradorRepository)
    
    # Configura o retorno esperado
    config_esperada = {"tema": "escuro"}
    repo_mock.get_configuracoes.return_value = config_esperada
    repo_mock.update_configuracoes.return_value = config_esperada
    
    # Testa os métodos
    resultado_get = repo_mock.get_configuracoes()
    resultado_update = repo_mock.update_configuracoes({"tema": "escuro"})
    
    # Asserções
    assert resultado_get == config_esperada
    assert resultado_update == config_esperada
    repo_mock.get_configuracoes.assert_called_once()
    repo_mock.update_configuracoes.assert_called_once_with({"tema": "escuro"})
