import pytest
from app.infrastructure.models.administrador_model import ConfiguracaoModel
from app.domain.entities.administrador_entity import Configuracao

def test_configuracao_model_to_entity():
    # Cria uma instância do model
    model = ConfiguracaoModel(
        id="123",
        chave="tema",
        valor={"cor": "escuro"}
    )
    
    # Testa os atributos do model
    assert model.id == "123"
    assert model.chave == "tema"
    assert model.valor == {"cor": "escuro"}
    
    # Testa a conversão para entity
    entity = model.to_entity()
    assert isinstance(entity, Configuracao)
    assert entity.id == "123"
    assert entity.chave == "tema"
    assert entity.valor == {"cor": "escuro"}
