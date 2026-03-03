import pytest
from unittest.mock import patch, MagicMock
from app.core.database import get_db

@patch("app.core.database.SessionLocal")
def test_get_db(mock_session_local):
    """Testa se get_db retorna (yield) a sessão e a fecha depois."""
    mock_db = MagicMock()
    mock_session_local.return_value = mock_db
    
    # get_db é um generator (yield)
    gen = get_db()
    
    # Pega o primeiro valor yieldeado (o mock_db)
    db = next(gen)
    assert db == mock_db
    
    # Ao iterar para o próximo, o bloco finally de get_db deve ser executado chamando db.close()
    with pytest.raises(StopIteration):
        next(gen)
        
    mock_db.close.assert_called_once()
