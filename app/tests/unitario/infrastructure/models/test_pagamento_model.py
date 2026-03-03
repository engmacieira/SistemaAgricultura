import pytest
from datetime import date
from app.infrastructure.models.pagamento_model import PagamentoModel
from app.domain.entities.pagamento_entity import Pagamento

def test_pagamento_model_to_entity():
    vencimento = date(2023, 12, 31)
    pagamento = date(2023, 12, 30)
    model = PagamentoModel(
        id="pg1",
        executionId="exec1",
        producerName="João",
        serviceName="Aração",
        dueDate=vencimento,
        paymentDate=pagamento,
        amount=150.0,
        status="Pago"
    )
    
    entity = model.to_entity()
    assert isinstance(entity, Pagamento)
    assert entity.id == model.id
    assert entity.executionId == model.executionId
    assert entity.producerName == model.producerName
    assert entity.serviceName == model.serviceName
    assert entity.dueDate == model.dueDate
    assert entity.paymentDate == model.paymentDate
    assert entity.amount == model.amount
    assert entity.status == model.status
