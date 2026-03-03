import pytest
from app.infrastructure.models.produtor_model import ProdutorModel
from app.domain.entities.produtor_entity import Produtor

def test_produtor_model_to_entity():
    model = ProdutorModel(
        id="prod1",
        name="Produtor Teste",
        cpfCnpj="000.000.000-00",
        property="Fazenda Esperança",
        totalArea=300.5,
        status="Ativo"
    )
    
    entity = model.to_entity()
    assert isinstance(entity, Produtor)
    assert entity.id == model.id
    assert entity.name == model.name
    assert entity.cpfCnpj == model.cpfCnpj
    assert getattr(entity, 'property') == getattr(model, 'property')
    assert entity.totalArea == model.totalArea
    assert entity.status == model.status
