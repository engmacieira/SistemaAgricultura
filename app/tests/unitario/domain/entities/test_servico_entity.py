import pytest
from app.domain.entities.servico_entity import Servico

def test_criar_servico_com_descricao():
    servico = Servico(
        id="s1",
        name="Aração",
        description="Aração profunda do solo",
        unit="ha",
        basePrice=150.0,
        active=True
    )
    
    assert servico.id == "s1"
    assert servico.name == "Aração"
    assert servico.description == "Aração profunda do solo"
    assert servico.unit == "ha"
    assert servico.basePrice == 150.0
    assert servico.active is True

def test_criar_servico_sem_descricao():
    servico = Servico(
        id="s2",
        name="Gradeação",
        description=None,
        unit="hora",
        basePrice=120.0,
        active=False
    )
    
    assert servico.id == "s2"
    assert servico.name == "Gradeação"
    assert servico.description is None
    assert servico.unit == "hora"
    assert servico.basePrice == 120.0
    assert servico.active is False
