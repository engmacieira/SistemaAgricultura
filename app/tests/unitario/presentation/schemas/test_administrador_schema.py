import pytest
from pydantic import ValidationError
from app.presentation.schemas.administrador_schema import ConfiguracaoSistema, BackupResponse

def test_configuracao_sistema_schema_valido():
    data = {"unidades_medida": ["ha", "kg", "ton"]}
    schema = ConfiguracaoSistema(**data)
    assert schema.unidades_medida == ["ha", "kg", "ton"]

def test_configuracao_sistema_schema_invalido():
    data = {"unidades_medida": "nao_e_lista"} # Pydantic tentará converter strings para lista, mas falha se for objeto incorreto esperado, porém string vira lista de chars.
    with pytest.raises(ValidationError):
        ConfiguracaoSistema(unidades_medida=123)

def test_backup_response_schema():
    data = {
        "status": "sucesso",
        "message": "OK",
        "timestamp": "2023-11-01T12:00:00"
    }
    schema = BackupResponse(**data)
    assert schema.status == "sucesso"
    assert schema.file_url is None # Opcional
