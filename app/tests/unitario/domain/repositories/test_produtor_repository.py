import pytest
from unittest.mock import Mock
from app.domain.repositories.produtor_repository import IProdutorRepository
from app.domain.entities.produtor_entity import Produtor

def test_produtor_repository_interface():
    repo_mock = Mock(spec=IProdutorRepository)
    
    produtor_esperado = Produtor(
        id="p1", name="João", cpfCnpj="123", property="Fazenda",
        regiao_referencia="R", telefone_contato="1", apelido_produtor="A", status="Ativo"
    )
    
    repo_mock.get_all.return_value = [produtor_esperado]
    repo_mock.get_by_id.return_value = produtor_esperado
    repo_mock.create.return_value = produtor_esperado
    repo_mock.update.return_value = produtor_esperado
    repo_mock.delete.return_value = True
    repo_mock.get_by_cpf_cnpj.return_value = produtor_esperado
    repo_mock.has_execucoes.return_value = False
    
    assert repo_mock.get_all() == [produtor_esperado]
    assert repo_mock.get_by_id("p1") == produtor_esperado
    assert repo_mock.create({"name": "João"}) == produtor_esperado
    assert repo_mock.update("p1", {"status": "Inativo"}) == produtor_esperado
    assert repo_mock.delete("p1") is True
    assert repo_mock.get_by_cpf_cnpj("123") == produtor_esperado
    assert repo_mock.has_execucoes("p1") is False
    
    repo_mock.get_all.assert_called_once()
    repo_mock.get_by_id.assert_called_once_with("p1")
    repo_mock.create.assert_called_once_with({"name": "João"})
    repo_mock.update.assert_called_once_with("p1", {"status": "Inativo"})
    repo_mock.delete.assert_called_once_with("p1")
    repo_mock.get_by_cpf_cnpj.assert_called_once_with("123")
    repo_mock.has_execucoes.assert_called_once_with("p1")
