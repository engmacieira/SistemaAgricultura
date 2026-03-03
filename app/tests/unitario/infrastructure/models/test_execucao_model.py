import pytest
from datetime import date
from app.infrastructure.models.execucao_model import ExecucaoModel
from app.domain.entities.execucao_entity import Execucao

def test_execucao_model_to_entity():
    data_hoje = date.today()
    model = ExecucaoModel(
        id="1",
        producerId="p1",
        producerName="João da Silva",
        serviceId="s1",
        serviceName="Aração",
        date=data_hoje,
        quantity=10.5,
        unit="ha",
        totalValue=1500.0,
        status="Finalizado"
    )
    
    assert model.id == "1"
    assert model.producerId == "p1"
    
    entity = model.to_entity()
    assert isinstance(entity, Execucao)
    assert entity.id == model.id
    assert entity.producerId == model.producerId
    assert entity.producerName == model.producerName
    assert entity.serviceId == model.serviceId
    assert entity.serviceName == model.serviceName
    assert entity.date == model.date
    assert entity.quantity == model.quantity
    assert entity.unit == model.unit
    assert entity.totalValue == model.totalValue
    assert entity.status == model.status
