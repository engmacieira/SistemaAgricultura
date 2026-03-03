import pytest
from datetime import datetime
from app.domain.entities.log_entity import Log

def test_criar_log():
    agora = datetime.now()
    log = Log(
        id="log1",
        timestamp=agora,
        userId="u1",
        userName="Admin",
        action="CREATE",
        entity="Produtor",
        details="Criou novo produtor João"
    )
    
    assert log.id == "log1"
    assert log.timestamp == agora
    assert log.userId == "u1"
    assert log.userName == "Admin"
    assert log.action == "CREATE"
    assert log.entity == "Produtor"
    assert log.details == "Criou novo produtor João"
