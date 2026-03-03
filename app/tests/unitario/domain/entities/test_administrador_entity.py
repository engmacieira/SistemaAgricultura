import pytest
from app.domain.entities.administrador_entity import Configuracao

def test_criar_configuracao():
    config = Configuracao(
        id="123",
        chave="tema",
        valor={"cor": "escuro"}
    )
    assert config.id == "123"
    assert config.chave == "tema"
    assert config.valor == {"cor": "escuro"}
