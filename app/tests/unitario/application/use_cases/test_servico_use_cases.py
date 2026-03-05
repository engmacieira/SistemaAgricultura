import pytest
from unittest.mock import MagicMock, ANY
from app.application.use_cases.servico_use_cases import ServicoUseCases

def test_obter_servico_erro():
    repo_mock = MagicMock()
    repo_mock.get_by_id.return_value = None
    use_cases = ServicoUseCases(repo_mock)
    with pytest.raises(ValueError, match="Serviço não encontrado"):
        use_cases.obter_servico("1")

def test_criar_servico_com_log():
    repo_mock = MagicMock()
    log_mock = MagicMock()
    servico_mock = MagicMock()
    repo_mock.create.return_value = servico_mock
    
    use_cases = ServicoUseCases(repo_mock, log_use_cases=log_mock)
    usuario = {"id": "u1", "name": "Admin1"}
    data = {"name": "Aração", "basePrice": 100}
    
    result = use_cases.criar_servico(data, usuario)
    
    assert result == servico_mock
    repo_mock.create.assert_called_once_with(data)
    log_mock.registrar_acao.assert_called_once_with(
        user_id="u1",
        user_name="Admin1",
        action="CRIAR",
        entity="Serviço",
        details="Criou o serviço 'Aração'",
        dados_anteriores=None,
        dados_novos=ANY
    )

def test_deletar_servico():
    repo_mock = MagicMock()
    servico_mock = MagicMock()
    servico_mock.name = "Aração"
    repo_mock.get_by_id.return_value = servico_mock
    repo_mock.delete.return_value = True
    
    use_cases = ServicoUseCases(repo_mock)
    result = use_cases.deletar_servico("1")
    
    assert result is True
    repo_mock.get_by_id.assert_called_once_with("1")
    repo_mock.delete.assert_called_once_with("1")
