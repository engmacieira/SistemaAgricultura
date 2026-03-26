import pytest
from fastapi import status
from datetime import date

def test_listar_execucoes_paginacao_filtros(client):
    # 1. Criar Solicitacao
    solic_resp = client.post("/api/solicitacoes/", json={
        "producerId": "p-gap", "producerName": "Produtor Gap", "data_solicitacao": str(date.today())
    })
    solic_id = solic_resp.json()["id"]

    # 2. Setup: Create some executions
    for i in range(3):
        payload = {
            "solicitacaoId": solic_id,
            "serviceId": "serv-1",
            "serviceName": f"Aragem {i}",
            "date": str(date.today()),
            "quantity": 1.0,
            "unit": "Hectare",
            "valor_unitario": 100.0,
            "totalValue": 100.0,
            "status": "REGISTRADA"
        }
        client.post("/api/execucoes/", json=payload)
    
    # Test pagination
    response = client.get("/api/execucoes/?limit=2")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    
    # Test filter completed
    response_comp = client.get("/api/execucoes/?show_completed=true")
    assert response_comp.status_code == status.HTTP_200_OK
    assert isinstance(response_comp.json(), list)

def test_soft_delete_execucao(client):
    # 1. Criar Solicitacao
    solic_resp = client.post("/api/solicitacoes/", json={
        "producerId": "p-del-ex", "producerName": "Produtor Del Ex", "data_solicitacao": str(date.today())
    })
    solic_id = solic_resp.json()["id"]

    # 2. Setup
    payload = {
        "solicitacaoId": solic_id,
        "serviceId": "serv-1",
        "serviceName": "Aragem",
        "date": str(date.today()),
        "quantity": 1.0,
        "unit": "Hectare",
        "valor_unitario": 100.0,
        "totalValue": 100.0,
        "status": "REGISTRADA"
    }
    create_res = client.post("/api/execucoes/", json=payload)
    exec_id = create_res.json()["id"]
    
    # Delete
    del_res = client.delete(f"/api/execucoes/{exec_id}")
    assert del_res.status_code == status.HTTP_204_NO_CONTENT
    
    # Verify it's gone from list
    list_res = client.get("/api/execucoes/")
    assert not any(e["id"] == exec_id for e in list_res.json())
    
    # Verify it's gone from GET
    get_res = client.get(f"/api/execucoes/{exec_id}")
    assert get_res.status_code == status.HTTP_404_NOT_FOUND
