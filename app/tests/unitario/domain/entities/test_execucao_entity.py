import pytest
from datetime import date
from app.domain.entities.execucao_entity import Execucao

def test_criar_execucao():
    data_hoje = date.today()
    execucao = Execucao(
        id="1",
        solicitacaoId="solic-1",  # ✅ Novo: Vínculo com a Fila
        serviceId="s1",
        serviceName="Aração",
        date=data_hoje,
        quantity=10.5,
        unit="ha",
        valor_unitario=150.0,     # ✅ Novo: Valor no dia
        totalValue=1575.0,        # 10.5 * 150.0
        status="REGISTRADA",
        operador_maquina="João"    # ✅ Novo: Quem operou
    )
    
    assert execucao.id == "1"
    assert execucao.solicitacaoId == "solic-1"
    assert execucao.serviceId == "s1"
    assert execucao.serviceName == "Aração"
    assert execucao.date == data_hoje
    assert execucao.quantity == 10.5
    assert execucao.unit == "ha"
    assert execucao.valor_unitario == 150.0
    assert execucao.totalValue == 1575.0
    assert execucao.status == "REGISTRADA"
    assert execucao.operador_maquina == "João"
