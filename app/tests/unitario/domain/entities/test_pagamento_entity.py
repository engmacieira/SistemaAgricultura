import pytest
from datetime import date
from app.domain.entities.pagamento_entity import Pagamento

def test_criar_pagamento_sem_data_pagamento():
    vencimento = date(2023, 12, 31)
    pagamento = Pagamento(
        id="1",
        executionId="e1",
        producerName="João",
        serviceName="Aração",
        dueDate=vencimento,
        amount=1500.0,
        status="Pendente"
    )
    
    assert pagamento.id == "1"
    assert pagamento.executionId == "e1"
    assert pagamento.producerName == "João"
    assert pagamento.serviceName == "Aração"
    assert pagamento.dueDate == vencimento
    assert pagamento.amount == 1500.0
    assert pagamento.status == "Pendente"
    assert pagamento.paymentDate is None

def test_criar_pagamento_com_data_pagamento():
    vencimento = date(2023, 12, 31)
    data_pgto = date(2023, 12, 30)
    pagamento = Pagamento(
        id="1",
        executionId="e1",
        producerName="João",
        serviceName="Aração",
        dueDate=vencimento,
        amount=1500.0,
        status="Pago",
        paymentDate=data_pgto
    )
    
    assert pagamento.paymentDate == data_pgto
    assert pagamento.status == "Pago"
