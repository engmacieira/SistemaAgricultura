import pytest
from unittest.mock import Mock
from datetime import date
from app.domain.repositories.execucao_repository import IExecucaoRepository
from app.domain.entities.execucao_entity import Execucao

def test_execucao_repository_interface():
    repo_mock = Mock(spec=IExecucaoRepository)
    
    execucao_esperada = Execucao(
        id="1", producerId="p1", producerName="João", serviceId="s1",
        serviceName="Aração", date=date.today(), quantity=10, unit="ha",
        totalValue=1500.0, status="Pendente"
    )
    
    repo_mock.get_all.return_value = [execucao_esperada]
    repo_mock.get_by_id.return_value = execucao_esperada
    repo_mock.create.return_value = execucao_esperada
    repo_mock.update.return_value = execucao_esperada
    repo_mock.delete.return_value = True
    
    assert repo_mock.get_all() == [execucao_esperada]
    assert repo_mock.get_by_id("1") == execucao_esperada
    assert repo_mock.create({"status": "Pendente"}) == execucao_esperada
    assert repo_mock.update("1", {"status": "Concluído"}) == execucao_esperada
    assert repo_mock.delete("1") is True
    
    repo_mock.get_all.assert_called_once()
    repo_mock.get_by_id.assert_called_once_with("1")
    repo_mock.create.assert_called_once_with({"status": "Pendente"})
    repo_mock.update.assert_called_once_with("1", {"status": "Concluído"})
    repo_mock.delete.assert_called_once_with("1")
