import pytest
from unittest.mock import Mock
from datetime import date
from app.domain.repositories.pagamento_repository import IPagamentoRepository
from app.domain.entities.pagamento_entity import Pagamento

def test_pagamento_repository_interface():
    repo_mock = Mock(spec=IPagamentoRepository)
    
    pagamento_esperado = Pagamento(
        id="1", executionId="e1", producerName="João", serviceName="Aração",
        dueDate=date.today(), amount=1500.0, status="Pendente"
    )
    
    repo_mock.get_all.return_value = [pagamento_esperado]
    repo_mock.get_by_id.return_value = pagamento_esperado
    repo_mock.create.return_value = pagamento_esperado
    repo_mock.update.return_value = pagamento_esperado
    repo_mock.delete.return_value = True
    
    assert repo_mock.get_all() == [pagamento_esperado]
    assert repo_mock.get_by_id("1") == pagamento_esperado
    assert repo_mock.create({"amount": 1500.0}) == pagamento_esperado
    assert repo_mock.update("1", {"status": "Pago"}) == pagamento_esperado
    assert repo_mock.delete("1") is True
    
    repo_mock.get_all.assert_called_once()
    repo_mock.get_by_id.assert_called_once_with("1")
    repo_mock.create.assert_called_once_with({"amount": 1500.0})
    repo_mock.update.assert_called_once_with("1", {"status": "Pago"})
    repo_mock.delete.assert_called_once_with("1")
