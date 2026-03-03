import pytest
from fastapi import status
from datetime import date

def test_registrar_execucao(client):
    # Primeiro criamos um produtor e um serviço para ter IDs válidos (se necessário pela lógica do UC)
    # Mas o router aceita um dict genérico, então vamos testar a interface
    payload = {
        "producerId": "prod-1",
        "producerName": "João Silva",
        "serviceId": "serv-1",
        "serviceName": "Aragem",
        "date": str(date.today()),
        "quantity": 10.0,
        "unit": "Hectare",
        "totalValue": 2500.0,
        "status": "Concluído"
    }
    response = client.post("/execucoes/", json=payload)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["producerName"] == payload["producerName"]
    assert "id" in data

def test_listar_execucoes(client):
    payload = {
        "producerId": "prod-2",
        "producerName": "Maria Oliveira",
        "serviceId": "serv-2",
        "serviceName": "Plantio",
        "date": str(date.today()),
        "quantity": 5.0,
        "unit": "Hectare",
        "totalValue": 1500.0,
        "status": "Pendente"
    }
    client.post("/execucoes/", json=payload)
    
    response = client.get("/execucoes/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

def test_obter_execucao(client):
    payload = {
        "producerId": "prod-3",
        "producerName": "Carlos Santos",
        "serviceId": "serv-3",
        "serviceName": "Colheita",
        "date": str(date.today()),
        "quantity": 20.0,
        "unit": "Hora",
        "totalValue": 3000.0,
        "status": "Em Andamento"
    }
    create_res = client.post("/execucoes/", json=payload)
    execucao_id = create_res.json()["id"]
    
    response = client.get(f"/execucoes/{execucao_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == execucao_id

def test_atualizar_execucao(client):
    payload = {
        "producerId": "prod-4",
        "producerName": "Pedro Rocha",
        "serviceId": "serv-4",
        "serviceName": "Pulverização",
        "date": str(date.today()),
        "quantity": 100.0,
        "unit": "Litro",
        "totalValue": 5000.0,
        "status": "Concluído"
    }
    create_res = client.post("/execucoes/", json=payload)
    execucao_id = create_res.json()["id"]
    
    update_payload = {"status": "Cancelado", "totalValue": 0.0}
    response = client.put(f"/execucoes/{execucao_id}", json=update_payload)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "Cancelado"
    assert data["totalValue"] == 0.0

def test_deletar_execucao(client):
    payload = {
        "producerId": "prod-5",
        "producerName": "Deletar",
        "serviceId": "serv-5",
        "serviceName": "Temporario",
        "date": str(date.today()),
        "quantity": 1.0,
        "unit": "Un",
        "totalValue": 10.0,
        "status": "Pendente"
    }
    create_res = client.post("/execucoes/", json=payload)
    execucao_id = create_res.json()["id"]
    
    response = client.delete(f"/execucoes/{execucao_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "Execução deletada com sucesso"
    
    get_res = client.get(f"/execucoes/{execucao_id}")
    assert get_res.status_code == status.HTTP_404_NOT_FOUND
