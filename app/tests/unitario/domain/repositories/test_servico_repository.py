import pytest
from unittest.mock import Mock
from app.domain.repositories.servico_repository import IServicoRepository
from app.domain.entities.servico_entity import Servico

def test_servico_repository_interface():
    repo_mock = Mock(spec=IServicoRepository)
    
    servico_esperado = Servico(
        id="s1", name="Aração", description="Desc", unit="ha",
        basePrice=150.0, active=True
    )
    
    repo_mock.get_all.return_value = [servico_esperado]
    repo_mock.get_by_id.return_value = servico_esperado
    repo_mock.create.return_value = servico_esperado
    repo_mock.update.return_value = servico_esperado
    repo_mock.delete.return_value = True
    repo_mock.get_by_name.return_value = servico_esperado
    repo_mock.has_execucoes.return_value = True
    
    assert repo_mock.get_all() == [servico_esperado]
    assert repo_mock.get_by_id("s1") == servico_esperado
    assert repo_mock.create({"name": "Aração"}) == servico_esperado
    assert repo_mock.update("s1", {"active": False}) == servico_esperado
    assert repo_mock.delete("s1") is True
    assert repo_mock.get_by_name("Aração") == servico_esperado
    assert repo_mock.has_execucoes("s1") is True
    
    repo_mock.get_all.assert_called_once()
    repo_mock.get_by_id.assert_called_once_with("s1")
    repo_mock.create.assert_called_once_with({"name": "Aração"})
    repo_mock.update.assert_called_once_with("s1", {"active": False})
    repo_mock.delete.assert_called_once_with("s1")
    repo_mock.get_by_name.assert_called_once_with("Aração")
    repo_mock.has_execucoes.assert_called_once_with("s1")
