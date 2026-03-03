import pytest
from unittest.mock import MagicMock, patch
from app.application.use_cases.usuario_use_cases import UsuarioUseCases

def test_obter_usuario_erro():
    repo_mock = MagicMock()
    repo_mock.get_by_id.return_value = None
    use_cases = UsuarioUseCases(repo_mock)
    with pytest.raises(ValueError, match="Usuário não encontrado"):
        use_cases.obter_usuario("1")

def test_autenticar_usuario_nao_encontrado():
    repo_mock = MagicMock()
    repo_mock.get_by_email.return_value = None
    use_cases = UsuarioUseCases(repo_mock)
    
    with pytest.raises(ValueError, match="Credenciais inválidas"):
        use_cases.autenticar_usuario("inexistente@ex.com", "123")
        
@patch("app.application.use_cases.usuario_use_cases.verify_password")
def test_autenticar_usuario_sucesso(mock_verify):
    repo_mock = MagicMock()
    usuario_mock = MagicMock()
    usuario_mock.id = "1"
    usuario_mock.name = "Admin"
    usuario_mock.email = "admin@ex.com"
    usuario_mock.role = "admin"
    usuario_mock.password_hash = "hashed_password"
    
    repo_mock.get_by_email.return_value = usuario_mock
    mock_verify.return_value = True
    
    use_cases = UsuarioUseCases(repo_mock)
    
    result = use_cases.autenticar_usuario("admin@ex.com", "123")
    
    assert result == {
        "id": "1",
        "name": "Admin",
        "email": "admin@ex.com",
        "role": "admin"
    }
    repo_mock.get_by_email.assert_called_once_with("admin@ex.com")
    mock_verify.assert_called_once_with("123", "hashed_password")

def test_criar_usuario_email_existente():
    repo_mock = MagicMock()
    usuario_existente = MagicMock()
    repo_mock.get_by_email.return_value = usuario_existente
    use_cases = UsuarioUseCases(repo_mock)
    
    with pytest.raises(ValueError, match="Email já cadastrado"):
        use_cases.criar_usuario({"email": "admin@ex.com"})
        
def test_criar_usuario_sucesso():
    repo_mock = MagicMock()
    repo_mock.get_by_email.return_value = None
    novo_usuario_mock = MagicMock()
    repo_mock.create.return_value = novo_usuario_mock
    use_cases = UsuarioUseCases(repo_mock)
    
    data = {"email": "novo@ex.com", "name": "Novo"}
    result = use_cases.criar_usuario(data)
    
    assert result == novo_usuario_mock
    repo_mock.get_by_email.assert_called_once_with("novo@ex.com")
    repo_mock.create.assert_called_once_with(data)
