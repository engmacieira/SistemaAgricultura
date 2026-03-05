import pytest
from fastapi import status
from datetime import date, timedelta

def test_obter_debitos_por_produtor(client):
    # Setup: Create execution to generate a payment
    exec_payload = {
        "producerId": "prod-debt-1",
        "producerName": "Produtor Devedor",
        "serviceId": "serv-1",
        "serviceName": "Aragem",
        "date": str(date.today()),
        "quantity": 2.0,
        "unit": "Hectare",
        "totalValue": 250.0,
        "status": "Concluído"
    }
    client.post("/api/execucoes/", json=exec_payload)
    
    response = client.get("/api/pagamentos/debitos-por-produtor")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "records" in data
    assert "totalGeneral" in data
    assert any(r["producerName"] == "Produtor Devedor" for r in data["records"])

def test_obter_historico_pagamento(client):
    # Setup: Create and pay partially
    exec_payload = {
        "producerId": "prod-hist",
        "producerName": "Produtor Historico",
        "serviceId": "serv-1",
        "serviceName": "Aragem",
        "date": str(date.today()),
        "quantity": 1.0,
        "unit": "Hectare",
        "totalValue": 100.0,
        "status": "Concluído"
    }
    client.post("/api/execucoes/", json=exec_payload)
    
    list_res = client.get("/api/pagamentos/")
    pagamento = next(p for p in list_res.json()["items"] if p["producerName"] == "Produtor Historico")
    pagamento_id = pagamento["id"]
    
    # Pay 50
    client.post(f"/api/pagamentos/{pagamento_id}/pagar", json={"amountToPay": 50.0})
    
    response = client.get(f"/api/pagamentos/{pagamento_id}/historico")
    assert response.status_code == status.HTTP_200_OK
    history = response.json()
    assert len(history) >= 1
    assert history[0]["amount"] == 50.0

def test_deletar_pagamento(client):
    # Setup
    exec_payload = {
        "producerId": "prod-del",
        "producerName": "Produtor Deletar",
        "serviceId": "serv-1",
        "serviceName": "Aragem",
        "date": str(date.today()),
        "quantity": 1.0,
        "unit": "Hectare",
        "totalValue": 100.0,
        "status": "Concluído"
    }
    client.post("/api/execucoes/", json=exec_payload)
    
    list_res = client.get("/api/pagamentos/")
    pagamento = next(p for p in list_res.json()["items"] if p["producerName"] == "Produtor Deletar")
    pagamento_id = pagamento["id"]
    
    # Delete
    del_res = client.delete(f"/api/pagamentos/{pagamento_id}")
    assert del_res.status_code == status.HTTP_204_NO_CONTENT
    
    # Verify it's gone
    get_res = client.get(f"/api/pagamentos/{pagamento_id}")
    assert get_res.status_code == status.HTTP_404_NOT_FOUND

def test_pagar_valor_invalido_ou_ja_pago(client):
    # Setup
    exec_payload = {
        "producerId": "prod-err",
        "producerName": "Produtor Erro",
        "serviceId": "serv-1",
        "serviceName": "Aragem",
        "date": str(date.today()),
        "quantity": 1.0,
        "unit": "Hectare",
        "totalValue": 100.0,
        "status": "Concluído"
    }
    client.post("/api/execucoes/", json=exec_payload)
    list_res = client.get("/api/pagamentos/")
    pagamento = next(p for p in list_res.json()["items"] if p["producerName"] == "Produtor Erro")
    pagamento_id = pagamento["id"]
    
    # Valida valor zero
    pay_res = client.post(f"/api/pagamentos/{pagamento_id}/pagar", json={"amountToPay": 0.0})
    assert pay_res.status_code == status.HTTP_400_BAD_REQUEST
    
    # Paga tudo
    client.post(f"/api/pagamentos/{pagamento_id}/pagar", json={"amountToPay": 100.0})
    
    # Tenta pagar novamente
    pay_res = client.post(f"/api/pagamentos/{pagamento_id}/pagar", json={"amountToPay": 10.0})
    assert pay_res.status_code == status.HTTP_400_BAD_REQUEST

def test_crud_transacoes(client):
    # Setup
    exec_payload = {
        "producerId": "prod-trans",
        "producerName": "Produtor Transacao",
        "serviceId": "serv-1",
        "serviceName": "Aragem",
        "date": str(date.today()),
        "quantity": 1.0,
        "unit": "Hectare",
        "totalValue": 100.0,
        "status": "Concluído"
    }
    client.post("/api/execucoes/", json=exec_payload)
    list_res = client.get("/api/pagamentos/")
    pagamento = next(p for p in list_res.json()["items"] if p["producerName"] == "Produtor Transacao")
    pagamento_id = pagamento["id"]
    
    # Create transaction via /pagar
    client.post(f"/api/pagamentos/{pagamento_id}/pagar", json={"amountToPay": 40.0})
    
    hist_res = client.get(f"/api/pagamentos/{pagamento_id}/historico")
    trans_id = hist_res.json()[0]["id"]
    
    # Update transaction
    upd_res = client.put(f"/api/pagamentos/transacoes/{trans_id}", json={"amount": 50.0})
    assert upd_res.status_code == status.HTTP_200_OK
    
    # Delete transaction
    del_res = client.delete(f"/api/pagamentos/transacoes/{trans_id}")
    assert del_res.status_code == status.HTTP_204_NO_CONTENT
