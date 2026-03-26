import pytest
from unittest.mock import MagicMock
from app.application.use_cases.execucao_use_cases import ExecucaoUseCases

@pytest.fixture
def dependencias():
    return {
        "exec_repo": MagicMock(),
        "solic_repo": MagicMock(),
        "pag_repo": MagicMock(),
        "log_uc": MagicMock()
    }

def test_criar_execucao_deve_concluir_solicitacao_e_gerar_pagamento(dependencias):
    # Setup
    use_cases = ExecucaoUseCases(
        dependencias["exec_repo"], 
        dependencias["solic_repo"], 
        dependencias["pag_repo"], 
        dependencias["log_uc"]
    )
    
    dados_execucao = {
        "solicitacaoId": "solic-1",
        "serviceId": "serv-1",
        "serviceName": "Plantio",
        "date": "2023-10-02",
        "quantity": 3.0,
        "unit": "Horas",
        "valor_unitario": 100.0,
        "totalValue": 300.0
    }
    
    # Configurando os retornos fingidos (Mocks)
    mock_exec_criada = MagicMock()
    mock_exec_criada.id = "exec-1"
    mock_exec_criada.solicitacaoId = "solic-1"
    mock_exec_criada.serviceName = "Plantio"
    mock_exec_criada.totalValue = 300.0
    dependencias["exec_repo"].create.return_value = mock_exec_criada
    
    mock_solicitacao_mae = MagicMock()
    mock_solicitacao_mae.id = "solic-1"
    mock_solicitacao_mae.producerName = "Fazenda Esperança"
    mock_solicitacao_mae.status = "PENDENTE"
    dependencias["solic_repo"].get_by_id.return_value = mock_solicitacao_mae

    usuario = {"id": "user-1", "name": "Operador"}

    # Ação
    resultado = use_cases.criar_execucao(dados_execucao, usuario)

    # Validações Essenciais (A Regra de Ouro)
    
    # 1. Atualizou a fila para CONCLUIDO?
    dependencias["solic_repo"].update.assert_called_once_with("solic-1", {"status": "CONCLUIDO"})
    
    # 2. Gerou o pagamento financeiro usando o nome do produtor da fila?
    dependencias["pag_repo"].create.assert_called_once()
    args_pagamento = dependencias["pag_repo"].create.call_args[0][0]
    assert args_pagamento["producerName"] == "Fazenda Esperança"
    assert args_pagamento["amount"] == 300.0
    assert args_pagamento["executionId"] == "exec-1"