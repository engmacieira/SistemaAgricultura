import pytest
from fastapi import status
from datetime import date

def test_listar_logs_vazio(client):
    response = client.get("/logs/")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json().get("items", []), list)

def test_geracao_log_automatica(client):
    # Ao criar um produtor, um log deve ser gerado (pela lógica do use case)
    payload = {
        "name": "Produtor Log",
        "cpfCnpj": "99999999999",
        "property": "Fazenda Lógica",
        "totalArea": 50.0,
        "status": "Ativo"
    }
    client.post("/produtores/", json=payload)
    
    response = client.get("/logs/")
    assert response.status_code == status.HTTP_200_OK
    logs = response.json()
    assert len(logs) >= 1
    
    # Verificar se o último log é sobre a criação do produtor
    ultimo_log = logs.get("items", [])[-1]
    assert ultimo_log["entity"] == "Produtor"
    action = ultimo_log["action"].upper()
    assert "CRIAR" in action or "CREATE" in action or "CRIADO" in action
