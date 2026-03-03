from fastapi import APIRouter, HTTPException, status
from ..schemas.administrador_schema import ConfiguracaoSistema, BackupResponse

router = APIRouter(prefix="/admin", tags=["Administração"])

@router.get("/configuracoes", response_model=ConfiguracaoSistema)
def obter_configuracoes():
    """Retorna as configurações globais do sistema."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Ainda não implementado")

@router.put("/configuracoes", response_model=ConfiguracaoSistema)
def atualizar_configuracoes(config: ConfiguracaoSistema):
    """Atualiza as configurações globais do sistema."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Ainda não implementado")

@router.post("/backup", response_model=BackupResponse)
def realizar_backup():
    """Inicia o processo de backup do banco de dados."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Ainda não implementado")

@router.post("/restore", response_model=BackupResponse)
def restaurar_backup():
    """Restaura o banco de dados a partir de um backup."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Ainda não implementado")
