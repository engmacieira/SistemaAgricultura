import pytest
from datetime import datetime
from app.infrastructure.models.log_model import LogModel
from app.domain.entities.log_entity import Log

def test_log_model_to_entity():
    agora = datetime.now()
    model = LogModel(
        id="log1",
        timestamp=agora,
        userId="u2",
        userName="Admin",
        action="CREATE",
        entity="Produtor",
        details="Detalhes do log"
    )
    
    assert model.action == "CREATE"
    assert model.entity == "Produtor"
    
    entity = model.to_entity()
    assert isinstance(entity, Log)
    assert entity.id == model.id
    assert entity.timestamp == model.timestamp
    assert entity.userId == model.userId
    assert entity.userName == model.userName
    assert entity.action == model.action
    assert entity.entity == model.entity
    assert getattr(entity, 'details', None) == model.details
