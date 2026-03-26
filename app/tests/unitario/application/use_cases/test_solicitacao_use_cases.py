import pytest
from unittest.mock import MagicMock
from app.application.use_cases.solicitacao_use_cases import SolicitacaoUseCases

@pytest.fixture
def mock_solicitacao_repo():
    return MagicMock()

@pytest.fixture
def mock_log_uc():
    return MagicMock()

def test_criar_solicitacao_deve_nascer_pendente(mock_solicitacao_repo, mock_log_uc):
    use_cases = SolicitacaoUseCases(mock_solicitacao_repo, mock_log_uc)
    
    dados_entrada = {
        "producerId": "123",
        "producerName": "Maria",
        "data_solicitacao": "2023-10-01",
        "status": "QUALQUER_COISA" # Tentando burlar o sistema
    }
    
    # O mock finge que criou e retorna um objeto (mock) com os dados
    mock_retorno = MagicMock()
    mock_retorno.producerName = "Maria"
    mock_solicitacao_repo.create.return_value = mock_retorno
    
    usuario_logado = {"id": "user-1", "name": "Admin"}
    
    resultado = use_cases.criar_solicitacao(dados_entrada, usuario_logado)
    
    # Validação 1: O Use Case DEVE ter forçado o status para PENDENTE antes de mandar pro repo
    mock_solicitacao_repo.create.assert_called_once()
    argumento_chamado = mock_solicitacao_repo.create.call_args[0][0]
    assert argumento_chamado["status"] == "PENDENTE"
    
    # Validação 2: Deve ter gerado log
    mock_log_uc.registrar_acao.assert_called_once()