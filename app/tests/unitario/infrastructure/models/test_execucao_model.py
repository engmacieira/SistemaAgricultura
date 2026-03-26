import pytest
from datetime import date
from app.infrastructure.models.execucao_model import ExecucaoModel
from app.domain.entities.execucao_entity import Execucao

def test_execucao_model_to_entity():
    data_hoje = date.today()
    model = ExecucaoModel(
        id="1",
        solicitacaoId="solic-1",
        serviceId="s1",
        serviceName="Aração",
        date=data_hoje,
        quantity=10.5,
        unit="ha",
        valor_unitario=150.0,
        totalValue=1575.0,
        status="REGISTRADA",
        operador_maquina="João"
    )
    
    assert model.id == "1"
    assert model.solicitacaoId == "solic-1"
    
    entity = model.to_entity()
    assert isinstance(entity, Execucao)
    assert entity.id == model.id
    assert entity.solicitacaoId == model.solicitacaoId
    assert entity.serviceId == model.serviceId
    assert entity.serviceName == model.serviceName
    assert entity.date == model.date
    assert entity.quantity == model.quantity
    assert entity.unit == model.unit
    assert entity.valor_unitario == model.valor_unitario
    assert entity.totalValue == model.totalValue
    assert entity.status == model.status
    assert entity.operador_maquina == model.operador_maquina
