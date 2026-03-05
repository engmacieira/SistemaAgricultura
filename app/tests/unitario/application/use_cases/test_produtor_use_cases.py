import pytest
from unittest.mock import MagicMock, ANY
from app.application.use_cases.produtor_use_cases import ProdutorUseCases

def test_obter_produtor_erro():
    repo_mock = MagicMock()
    repo_mock.get_by_id.return_value = None
    use_cases = ProdutorUseCases(repo_mock)
    with pytest.raises(ValueError, match="Produtor não encontrado"):
        use_cases.obter_produtor("1")

def test_criar_produtor_com_log():
    repo_mock = MagicMock()
    log_mock = MagicMock()
    produtor_mock = MagicMock()
    repo_mock.get_model_by_cpf_cnpj.return_value = None
    repo_mock.create.return_value = produtor_mock
    
    use_cases = ProdutorUseCases(repo_mock, log_use_cases=log_mock)
    usuario_logado = {"id": "u1", "name": "Admin1"}
    data = {"name": "João", "cpfCnpj": "123"}
    
    result = use_cases.criar_produtor(data, usuario_logado)
    
    assert result == produtor_mock
    repo_mock.create.assert_called_once_with(data)
    log_mock.registrar_acao.assert_called_once_with(
        user_id="u1",
        user_name="Admin1",
        action="CRIAR",
        entity="Produtor",
        details="Criou o produtor 'João'",
        dados_anteriores=None,
        dados_novos=ANY
    )

def test_atualizar_produtor_com_log():
    repo_mock = MagicMock()
    log_mock = MagicMock()
    produtor_mock = MagicMock()
    produtor_mock.name = "João Antigo"
    repo_mock.get_by_id.return_value = produtor_mock
    repo_mock.update.return_value = produtor_mock
    
    use_cases = ProdutorUseCases(repo_mock, log_use_cases=log_mock)
    usuario_logado = {"id": "u1", "name": "Admin1"}
    data = {"name": "João Novo"}
    
    result = use_cases.atualizar_produtor("p1", data, usuario_logado)
    
    assert result == produtor_mock
    repo_mock.update.assert_called_once_with("p1", data)
    log_mock.registrar_acao.assert_called_once_with(
        user_id="u1",
        user_name="Admin1",
        action="EDITAR",
        entity="Produtor",
        details="Atualizou os dados do produtor 'João Antigo'",
        dados_anteriores=ANY,
        dados_novos=ANY
    )
