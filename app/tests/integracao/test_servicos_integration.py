import pytest
from fastapi import status

def test_criar_servico(client):
    payload = {
        "name": "Aragem",
        "description": "Serviço de aragem de terra",
        "unit": "Hectare",
        "basePrice": 250.0,
        "active": True
    }
    response = client.post("/servicos/", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == payload["name"]
    assert "id" in data

def test_listar_servicos(client):
    payload = {
        "name": "Plantio",
        "description": "Serviço de plantio",
        "unit": "Hectare",
        "basePrice": 300.0,
        "active": True
    }
    client.post("/servicos/", json=payload)
    
    response = client.get("/servicos/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data.get("items", []), list)
    assert len(data.get("items", [])) >= 1

def test_obter_servico(client):
    payload = {
        "name": "Colheita",
        "description": "Serviço de colheita",
        "unit": "Hora",
        "basePrice": 150.0,
        "active": True
    }
    create_res = client.post("/servicos/", json=payload)
    servico_id = create_res.json()["id"]
    
    response = client.get(f"/servicos/{servico_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == servico_id

def test_atualizar_servico(client):
    payload = {
        "name": "Pulverização",
        "description": "Serviço de pulverização",
        "unit": "Litro",
        "basePrice": 50.0,
        "active": True
    }
    create_res = client.post("/servicos/", json=payload)
    servico_id = create_res.json()["id"]
    
    update_payload = {"basePrice": 55.0}
    response = client.put(f"/servicos/{servico_id}", json=update_payload)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["basePrice"] == 55.0

def test_deletar_servico(client):
    payload = {
        "name": "Serviço Temporário",
        "description": "Para deletar",
        "unit": "Unidade",
        "basePrice": 10.0,
        "active": False
    }
    create_res = client.post("/servicos/", json=payload)
    servico_id = create_res.json()["id"]
    
    response = client.delete(f"/servicos/{servico_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    get_res = client.get(f"/servicos/{servico_id}")
    assert get_res.status_code == status.HTTP_404_NOT_FOUND
