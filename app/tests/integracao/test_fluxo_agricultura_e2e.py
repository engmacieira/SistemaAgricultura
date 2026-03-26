import pytest
from fastapi import status
from datetime import date

def test_fluxo_completo_agricultura(client):
    # 1. CRIAR UMA SOLICITAÇÃO (Fila de Espera)
    payload_solicitacao = {
        "producerId": "prod-100",
        "producerName": "Fazenda Modelo",
        "data_solicitacao": str(date.today()),
        "prioridade": 2,
        "observacoes": "Urgente para plantio de milho"
    }
    
    response_solic = client.post("/api/solicitacoes/", json=payload_solicitacao)
    assert response_solic.status_code == status.HTTP_201_CREATED
    solicitacao = response_solic.json()
    solicitacao_id = solicitacao["id"]
    assert solicitacao["status"] == "PENDENTE"
    assert solicitacao["producerName"] == "Fazenda Modelo"

    # 2. REGISTRAR UMA EXECUÇÃO (Ordem de Serviço) VINCULADA À SOLICITAÇÃO
    payload_execucao = {
        "solicitacaoId": solicitacao_id,
        "serviceId": "serv-50",
        "serviceName": "Aração Profunda",
        "date": str(date.today()),
        "quantity": 5.5,
        "unit": "Hectares",
        "valor_unitario": 200.0,
        "totalValue": 1100.0,
        "status": "REGISTRADA",
        "operador_maquina": "Marcos Tratorista"
    }
    
    response_exec = client.post("/api/execucoes/", json=payload_execucao)
    assert response_exec.status_code == status.HTTP_201_CREATED
    execucao = response_exec.json()
    assert execucao["solicitacaoId"] == solicitacao_id
    
    # 3. VERIFICAR SE A SOLICITAÇÃO MUDOU O STATUS PARA "CONCLUIDO"
    response_get_solic = client.get(f"/api/solicitacoes/{solicitacao_id}")
    assert response_get_solic.status_code == status.HTTP_200_OK
    solicitacao_atualizada = response_get_solic.json()
    assert solicitacao_atualizada["status"] == "CONCLUIDO"
    
    # 4. VERIFICAR SE O PAGAMENTO FOI GERADO AUTOMATICAMENTE
    response_pagamentos = client.get("/api/pagamentos/") # Verificando o prefixo correto do router de pagamentos
    # Opa, vamos conferir o prefixo no router de pagamentos
    # Se falhar aqui, ajustamos o prefixo.
    assert response_pagamentos.status_code == status.HTTP_200_OK
    pagamentos = response_pagamentos.json()
    
    # Procura o pagamento vinculado a esta execução
    # Dependendo da estrutura do retorno do get pagamentos (pode ser paginado)
    if isinstance(pagamentos, dict) and "items" in pagamentos:
        lista_pagamentos = pagamentos["items"]
    else:
        lista_pagamentos = pagamentos

    pagamento_encontrado = None
    for p in lista_pagamentos:
        if p.get("executionId") == execucao["id"]:
            pagamento_encontrado = p
            break
            
    assert pagamento_encontrado is not None, "O pagamento não foi gerado automaticamente"
    assert pagamento_encontrado["producerName"] == "Fazenda Modelo"
    assert pagamento_encontrado["amount"] == 1100.0
