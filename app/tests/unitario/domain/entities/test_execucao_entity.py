import pytest
from datetime import date
from app.domain.entities.execucao_entity import Execucao

def test_criar_execucao():
    data_hoje = date.today()
    execucao = Execucao(
        id="1",
        producerId="p1",
        producerName="João",
        serviceId="s1",
        serviceName="Aração",
        date=data_hoje,
        quantity=10.5,
        unit="ha",
        totalValue=1500.0,
        status="Em andamento"
    )
    
    assert execucao.id == "1"
    assert execucao.producerId == "p1"
    assert execucao.producerName == "João"
    assert execucao.serviceId == "s1"
    assert execucao.serviceName == "Aração"
    assert execucao.date == data_hoje
    assert execucao.quantity == 10.5
    assert execucao.unit == "ha"
    assert execucao.totalValue == 1500.0
    assert execucao.status == "Em andamento"
