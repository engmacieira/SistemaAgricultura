import pytest
from datetime import date
from app.domain.entities.solicitacao_entity import Solicitacao
from app.domain.entities.execucao_entity import Execucao

def test_criar_solicitacao_valida():
    solicitacao = Solicitacao(
        id="solic-123",
        producerId="prod-123",
        producerName="João da Silva",
        data_solicitacao=date.today(),
        prioridade=1,
        status="PENDENTE",
        observacoes="Precisa de trator"
    )
    
    assert solicitacao.id == "solic-123"
    assert solicitacao.status == "PENDENTE"
    assert solicitacao.is_deleted is False
    assert isinstance(solicitacao.execucoes, list)
    assert len(solicitacao.execucoes) == 0  # Garante que nasce sem execuções

def test_adicionar_execucao_na_solicitacao():
    solicitacao = Solicitacao(
        id="solic-123",
        producerId="prod-123",
        producerName="João",
        data_solicitacao=date.today(),
        prioridade=1,
        status="PENDENTE"
    )
    
    execucao = Execucao(
        id="exec-1",
        solicitacaoId=solicitacao.id,
        serviceId="serv-1",
        serviceName="Aração",
        date=date.today(),
        quantity=2.0,
        unit="Horas",
        valor_unitario=150.0,
        totalValue=300.0,
        status="REGISTRADA"
    )
    
    solicitacao.execucoes.append(execucao)
    
    assert len(solicitacao.execucoes) == 1
    assert solicitacao.execucoes[0].serviceName == "Aração"