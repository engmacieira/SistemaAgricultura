import pytest
from fastapi import status
from datetime import date

def test_registrar_execucao(client):
    # 1. Cria a solicitacao mãe
    solic_resp = client.post("/api/solicitacoes/", json={
        "producerId": "p1", "producerName": "João", "data_solicitacao": str(date.today())
    })
    solic_id = solic_resp.json()["id"]

    payload = {
        "solicitacaoId": solic_id,
        "serviceId": "serv-1",
        "serviceName": "Aragem",
        "date": str(date.today()),
        "quantity": 10.0,
        "unit": "Hectare",
        "valor_unitario": 250.0,
        "totalValue": 2500.0,
        "status": "REGISTRADA"
    }
    response = client.post("/api/execucoes/", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["solicitacaoId"] == solic_id
    assert "id" in data

def test_listar_execucoes(client):
    solic_resp = client.post("/api/solicitacoes/", json={
        "producerId": "p2", "producerName": "Maria", "data_solicitacao": str(date.today())
    })
    solic_id = solic_resp.json()["id"]

    payload = {
        "solicitacaoId": solic_id,
        "serviceId": "serv-2",
        "serviceName": "Plantio",
        "date": str(date.today()),
        "quantity": 5.0,
        "unit": "Hectare",
        "valor_unitario": 300.0,
        "totalValue": 1500.0,
        "status": "REGISTRADA"
    }
    client.post("/api/execucoes/", json=payload)
    
    response = client.get("/api/execucoes/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

def test_obter_execucao(client):
    solic_resp = client.post("/api/solicitacoes/", json={
        "producerId": "p3", "producerName": "Carlos", "data_solicitacao": str(date.today())
    })
    solic_id = solic_resp.json()["id"]

    payload = {
        "solicitacaoId": solic_id,
        "serviceId": "serv-3",
        "serviceName": "Colheita",
        "date": str(date.today()),
        "quantity": 20.0,
        "unit": "Hora",
        "valor_unitario": 150.0,
        "totalValue": 3000.0,
        "status": "REGISTRADA"
    }
    create_res = client.post("/api/execucoes/", json=payload)
    execucao_id = create_res.json()["id"]
    
    response = client.get(f"/api/execucoes/{execucao_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == execucao_id

def test_atualizar_execucao(client):
    solic_resp = client.post("/api/solicitacoes/", json={
        "producerId": "p4", "producerName": "Pedro", "data_solicitacao": str(date.today())
    })
    solic_id = solic_resp.json()["id"]

    payload = {
        "solicitacaoId": solic_id,
        "serviceId": "serv-4",
        "serviceName": "Pulverização",
        "date": str(date.today()),
        "quantity": 100.0,
        "unit": "Litro",
        "valor_unitario": 50.0,
        "totalValue": 5000.0,
        "status": "REGISTRADA"
    }
    create_res = client.post("/api/execucoes/", json=payload)
    execucao_id = create_res.json()["id"]
    
    update_payload = {"status": "FATURADA", "totalValue": 5000.0}
    response = client.put(f"/api/execucoes/{execucao_id}", json=update_payload)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "FATURADA"

def test_deletar_execucao(client):
    solic_resp = client.post("/api/solicitacoes/", json={
        "producerId": "p5", "producerName": "Deletar", "data_solicitacao": str(date.today())
    })
    solic_id = solic_resp.json()["id"]

    payload = {
        "solicitacaoId": solic_id,
        "serviceId": "serv-5",
        "serviceName": "Temporario",
        "date": str(date.today()),
        "quantity": 1.0,
        "unit": "Un",
        "valor_unitario": 10.0,
        "totalValue": 10.0,
        "status": "REGISTRADA"
    }
    create_res = client.post("/api/execucoes/", json=payload)
    execucao_id = create_res.json()["id"]
    
    response = client.delete(f"/api/execucoes/{execucao_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # By default, listing shouldn't show it
    get_res = client.get("/api/execucoes/")
    items = get_res.json()
    assert isinstance(items, list)
    assert not any(item["id"] == execucao_id for item in items)
