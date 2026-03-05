import pytest
from app.domain.entities.produtor_entity import Produtor

def test_criar_produtor():
    produtor = Produtor(
        id="p1",
        name="João da Silva",
        cpfCnpj="123.456.789-00",
        property="Fazenda Esperança",
        regiao_referencia="R", telefone_contato="1", apelido_produtor="A",
        status="Ativo"
    )
    
    assert produtor.id == "p1"
    assert produtor.name == "João da Silva"
    assert produtor.cpfCnpj == "123.456.789-00"
    assert getattr(produtor, "property") == "Fazenda Esperança"
    assert produtor.regiao_referencia == "R"
    assert produtor.status == "Ativo"
