import pytest
from unittest.mock import MagicMock
from datetime import date
from app.application.use_cases.pagamento_use_cases import PagamentoUseCases

def test_obter_pagamento_sucesso():
    repo_mock = MagicMock()
    pg_mock = MagicMock()
    repo_mock.get_by_id.return_value = pg_mock
    use_cases = PagamentoUseCases(repo_mock)
    assert use_cases.obter_pagamento("1") == pg_mock

def test_obter_pagamento_erro():
    repo_mock = MagicMock()
    repo_mock.get_by_id.return_value = None
    use_cases = PagamentoUseCases(repo_mock)
    with pytest.raises(ValueError, match="Pagamento não encontrado"):
        use_cases.obter_pagamento("1")

def test_registrar_pagamento_ja_pago():
    repo_mock = MagicMock()
    pg_mock = MagicMock()
    pg_mock.status = "Pago"
    repo_mock.get_by_id.return_value = pg_mock
    use_cases = PagamentoUseCases(repo_mock)
    
    with pytest.raises(ValueError, match="Este pagamento já foi realizado"):
        use_cases.registrar_pagamento("1", date.today())

def test_registrar_pagamento_sucesso():
    repo_mock = MagicMock()
    pg_mock = MagicMock()
    pg_mock.status = "Pendente"
    repo_mock.get_by_id.return_value = pg_mock
    
    pg_atualizado_mock = MagicMock()
    repo_mock.update.return_value = pg_atualizado_mock
    
    use_cases = PagamentoUseCases(repo_mock)
    data_pg = date.today()
    result = use_cases.registrar_pagamento("1", data_pg)
    
    assert result == pg_atualizado_mock
    repo_mock.update.assert_called_once_with("1", {
        "status": "Pago",
        "paymentDate": data_pg
    })
