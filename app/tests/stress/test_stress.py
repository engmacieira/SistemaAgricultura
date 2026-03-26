import pytest
from fastapi import status
import asyncio
from concurrent.futures import ThreadPoolExecutor

@pytest.fixture
def auth_client(client):
    return client

def worker_solicitacao(client, i):
    payload = {
        "producerId": f"P-{i}",
        "producerName": f"Produtor Stress {i}",
        "data_solicitacao": "2024-06-01",
        "prioridade": 1,
        "observacoes": f"Teste de stress {i}"
    }
    response = client.post("/api/solicitacoes/", json=payload)
    return response

def test_escrita_concorrente_solicitacoes(auth_client):
    """
    Dispara 50 requisições simultâneas para POST /api/solicitacoes/ criando dezenas de
    pedidos na fila de espera ao mesmo tempo. Verifica se o SQLite lança o erro de DB Locked.
    """
    num_requests = 50
    resultados = []

    with ThreadPoolExecutor(max_workers=num_requests) as executor:
        futures = [executor.submit(worker_solicitacao, auth_client, i) for i in range(num_requests)]

        for future in futures:
            try:
                resultados.append(future.result())
            except Exception as e:
                resultados.append(e)

    # Verifica quantas deram sucesso e quantas falharam (se for Database Locked, status_code >= 500)
    sucessos = sum(1 for r in resultados if hasattr(r, "status_code") and r.status_code == status.HTTP_201_CREATED)
    falhas = len(resultados) - sucessos

    print(f"\n[STRESS TEST] Solicitacoes - Sucessos: {sucessos}/{num_requests}, Falhas: {falhas}")

    # Com as mitigações corretas de banco no disco (WAL e timeout),
    # esperamos 100% de sucesso (nenhum DB Locked).
    assert sucessos == num_requests, f"Falhas de DB Locked: {falhas}"

def worker_execucao(client, solicitacao_id, i):
    payload = {
        "solicitacaoId": solicitacao_id,
        "serviceId": f"S-{i}",
        "serviceName": f"Serviço Stress {i}",
        "date": "2024-06-02",
        "quantity": 2.5,
        "unit": "Ha",
        "valor_unitario": 100.0,
        "totalValue": 250.0,
        "status": "REGISTRADA",
        "operador_maquina": "Operador Stress"
    }
    return client.post("/api/execucoes/", json=payload)

def test_cascata_transacoes_execucoes(auth_client):
    """
    Dispara 20 requisições simultâneas para POST /api/execucoes/.
    Este é o fluxo mais pesado, pois cada requisição altera a mãe, gera a execução,
    gera um pagamento e ainda cria log. Verifica o comportamento de concorrência.
    """
    num_requests = 20
    solicitacoes_ids = []

    # 1. Preparação: Criar as solicitações (de forma síncrona, não concorrente, para garantir a base)
    for i in range(num_requests):
        resp = auth_client.post("/api/solicitacoes/", json={
            "producerId": f"P-Prep-{i}",
            "producerName": f"Produtor {i}",
            "data_solicitacao": "2024-06-01"
        })
        assert resp.status_code == status.HTTP_201_CREATED
        solicitacoes_ids.append(resp.json()["id"])

    resultados = []

    # 2. Execução Concorrente da Cascata
    with ThreadPoolExecutor(max_workers=num_requests) as executor:
        futures = [executor.submit(worker_execucao, auth_client, solicitacoes_ids[i], i) for i in range(num_requests)]

        for future in futures:
            try:
                resultados.append(future.result())
            except Exception as e:
                resultados.append(e)

    # 3. Análise dos Resultados
    sucessos = sum(1 for r in resultados if hasattr(r, "status_code") and r.status_code == status.HTTP_201_CREATED)
    falhas = len(resultados) - sucessos

    print(f"\n[STRESS TEST] Execucoes - Sucessos: {sucessos}/{num_requests}, Falhas: {falhas}")

    # Com as mitigações corretas (WAL e timeout),
    # esperamos 100% de sucesso (nenhum DB Locked).
    assert sucessos == num_requests, f"Falhas de DB Locked na cascata: {falhas}"

    # 4. Verificação de Integridade de Negócio Pós-Estresse
    # Para cada execução criada (que retornou 201), a solicitação mãe DEVIA mudar de PENDENTE.
    for r in resultados:
        if hasattr(r, "status_code") and r.status_code == status.HTTP_201_CREATED:
            exec_data = r.json()
            solic_id = exec_data["solicitacaoId"]

            solic_resp = auth_client.get(f"/api/solicitacoes/{solic_id}")
            assert solic_resp.status_code == 200
            solic_data = solic_resp.json()

            # A solicitação não pode estar pendente se ela tem uma execução!
            assert solic_data["status"] != "PENDENTE", f"Inconsistência! Solicitação {solic_id} continuou PENDENTE após receber uma execução via concorrência."
