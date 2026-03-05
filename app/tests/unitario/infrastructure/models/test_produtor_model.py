import pytest
from app.infrastructure.models.produtor_model import ProdutorModel
from app.domain.entities.produtor_entity import Produtor

def test_produtor_model_to_entity():
    model = ProdutorModel(
        id="prod1",
        name="Produtor Teste",
        cpfCnpj="000.000.000-00",
        property="Fazenda Esperança",
        regiao_referencia="R", telefone_contato="1", apelido_produtor="A",
        status="Ativo"
    )
    
    entity = model.to_entity()
    assert isinstance(entity, Produtor)
    assert entity.id == model.id
    assert entity.name == model.name
    assert entity.cpfCnpj == model.cpfCnpj
    assert getattr(entity, 'property') == getattr(model, 'property')
    assert entity.regiao_referencia == model.regiao_referencia
    assert entity.status == model.status
