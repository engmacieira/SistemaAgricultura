from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.infrastructure.repositories.administrador_repository import AdministradorRepository
from app.application.use_cases.administrador_use_cases import AdministradorUseCases
from app.presentation.schemas.administrador_schema import ConfiguracaoSistema, BackupResponse

router = APIRouter(prefix="/admin", tags=["Administração"])

def get_use_case(db: Session = Depends(get_db)):
    from app.infrastructure.services.backup_service import BackupService
    backup_service = BackupService()
    return AdministradorUseCases(AdministradorRepository(db), backup_service=backup_service)

@router.get("/configuracoes", response_model=ConfiguracaoSistema)
def obter_configuracoes(uc: AdministradorUseCases = Depends(get_use_case)):
    """Retorna as configurações globais do sistema."""
    return uc.obter_configuracoes()

@router.put("/configuracoes", response_model=ConfiguracaoSistema)
def atualizar_configuracoes(data: ConfiguracaoSistema, uc: AdministradorUseCases = Depends(get_use_case)):
    """Atualiza as configurações globais do sistema."""
    return uc.atualizar_configuracoes(data.model_dump())

@router.post("/backup", response_model=BackupResponse)
def realizar_backup(uc: AdministradorUseCases = Depends(get_use_case)):
    """Inicia o processo de backup do banco de dados."""
    try:
        return uc.realizar_backup()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/restaurar", response_model=BackupResponse)
def restaurar_backup(data: dict, uc: AdministradorUseCases = Depends(get_use_case)):
    """Restaura o banco de dados a partir de um backup."""
    file_url = data.get("file_url")
    try:
        return uc.restaurar_backup(file_url)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

