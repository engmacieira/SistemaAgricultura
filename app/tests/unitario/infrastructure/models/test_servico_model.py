import pytest
from app.infrastructure.models.servico_model import ServicoModel
from app.domain.entities.servico_entity import Servico

def test_servico_model_to_entity():
    model = ServicoModel(
        id="serv1",
        name="Teste Serviço",
        description="Descrição do Serviço",
        unit="Hora",
        basePrice=50.0,
        active=True
    )
    
    entity = model.to_entity()
    assert isinstance(entity, Servico)
    assert entity.id == model.id
    assert entity.name == model.name
    assert entity.description == model.description
    assert entity.unit == model.unit
    assert entity.basePrice == model.basePrice
    assert entity.active == model.active
