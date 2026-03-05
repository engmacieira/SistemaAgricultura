import pytest
from fastapi import status
from datetime import date, timedelta

def test_listar_pagamentos(client):
    # Normalmente pagamentos são criados via UseCase de Execução, 
    # mas vamos assumir que podemos listar mesmo que vazio no início
    response = client.get("/api/pagamentos/")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json()["items"], list)

def test_registrar_pagamento_fluxo(client):
    # 1. Criar uma execução (que deve gerar um pagamento via logic do sistema)
    exec_payload = {
        "producerId": "prod-p1",
        "producerName": "João Pagador",
        "serviceId": "serv-p1",
        "serviceName": "Aragem",
        "date": str(date.today()),
        "quantity": 10.0,
        "unit": "Hectare",
        "totalValue": 1000.0,
        "status": "Concluído"
    }
    client.post("/api/execucoes/", json=exec_payload)
    
    # 2. Listar pagamentos para pegar o ID
    list_res = client.get("/api/pagamentos/")
    pagamentos = list_res.json().get("items", [])
    assert len(pagamentos) >= 1
    pagamento_id = pagamentos[0]["id"]
    
    # 3. Obter pagamento específico
    get_res = client.get(f"/api/pagamentos/{pagamento_id}")
    assert get_res.status_code == status.HTTP_200_OK
    assert get_res.json()["id"] == pagamento_id
    
    # 4. Registrar o pagamento (pagar)
    pay_res = client.post(f"/api/pagamentos/{pagamento_id}/pagar", json={"amountToPay": 1000.0})
    assert pay_res.status_code == status.HTTP_201_CREATED
    assert pay_res.json()["status"] == "Pago"
    assert pay_res.json()["paymentDate"] is not None

def test_atualizar_pagamento(client):
    # 1. Criar uma execução (que deve gerar um pagamento)
    exec_payload = {
        "producerId": "prod-p2",
        "producerName": "Maria Pagadora",
        "serviceId": "serv-p2",
        "serviceName": "Colheita",
        "date": str(date.today()),
        "quantity": 5.0,
        "unit": "Hectare",
        "totalValue": 500.0,
        "status": "Concluído"
    }
    client.post("/api/execucoes/", json=exec_payload)
    
    # 2. Listar pagamentos para pegar o ID
    list_res = client.get("/api/pagamentos/")
    pagamentos = list_res.json().get("items", [])
    pagamento_id = next(p["id"] for p in pagamentos if p["producerName"] == "Maria Pagadora")
    
    # 3. Atualizar o pagamento via PUT (como o frontend faz)
    update_payload = {
        "dueDate": str(date.today() + timedelta(days=15)),
        "status": "Atrasado",
        "amount": 600.0
    }
    response = client.put(f"/api/pagamentos/{pagamento_id}", json=update_payload)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "Atrasado"
    assert data["amount"] == 600.0

def test_obter_pagamento_inexistente(client):
    response = client.get("/api/pagamentos/id-fantasma")
    assert response.status_code == status.HTTP_404_NOT_FOUND
