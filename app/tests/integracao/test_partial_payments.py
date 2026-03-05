import pytest
from fastapi import status
from datetime import date

def test_partial_payment_flow(client):
    # 1. Create an execution (this should trigger payment creation)
    exec_payload = {
        "producerId": "prod-partial",
        "producerName": "João Parcial",
        "serviceId": "serv-p1",
        "serviceName": "Aragem Especial",
        "date": str(date.today()),
        "quantity": 10.0,
        "unit": "Hectare",
        "totalValue": 1000.0,
        "status": "Concluído"
    }
    client.post("/api/execucoes/", json=exec_payload)
    
    # 2. Find the payment ID
    list_res = client.get("/api/pagamentos/")
    pagamentos = list_res.json().get("items", [])
    pagamento = next(p for p in pagamentos if p["producerName"] == "João Parcial")
    pagamento_id = pagamento["id"]
    
    assert pagamento["amount"] == 1000.0
    assert pagamento["paidAmount"] == 0.0
    assert pagamento["status"] == "Pendente"
    
    # 3. Register a partial payment (500)
    pay_payload = {
        "amountToPay": 500.0
    }
    pay_res = client.post(f"/api/pagamentos/{pagamento_id}/pagar", json=pay_payload)
    assert pay_res.status_code == status.HTTP_201_CREATED
    data = pay_res.json()
    assert data["paidAmount"] == 500.0
    assert data["status"] == "Parcial"
    
    # 4. Register another partial payment (300) -> Total 800
    pay_payload = {
        "amountToPay": 300.0
    }
    pay_res = client.post(f"/api/pagamentos/{pagamento_id}/pagar", json=pay_payload)
    data = pay_res.json()
    assert data["paidAmount"] == 800.0
    assert data["status"] == "Parcial"
    
    # 5. Pay the rest (200) -> Total 1000 -> Status: Pago
    pay_payload = {
        "amountToPay": 200.0
    }
    pay_res = client.post(f"/api/pagamentos/{pagamento_id}/pagar", json=pay_payload)
    data = pay_res.json()
    assert data["paidAmount"] == 1000.0
    assert data["status"] == "Pago"

def test_payment_overpay(client):
    # Create execution
    exec_payload = {
        "producerId": "prod-overpay",
        "producerName": "Maria Rica",
        "serviceId": "serv-p2",
        "serviceName": "Colheita",
        "date": str(date.today()),
        "quantity": 1.0,
        "unit": "Hectare",
        "totalValue": 100.0,
        "status": "Concluído"
    }
    client.post("/api/execucoes/", json=exec_payload)
    
    # Find payment
    list_res = client.get("/api/pagamentos/")
    pagamentos = list_res.json().get("items", [])
    pagamento = next(p for p in pagamentos if p["producerName"] == "Maria Rica")
    pagamento_id = pagamento["id"]
    
    # Overpay (150 for a 100 bill)
    pay_payload = {
        "amountToPay": 150.0
    }
    pay_res = client.post(f"/api/pagamentos/{pagamento_id}/pagar", json=pay_payload)
    data = pay_res.json()
    assert data["paidAmount"] == 100.0 # Clamped to total
    assert data["status"] == "Pago"
