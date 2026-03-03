from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.infrastructure.repositories.administrador_repository import AdministradorRepository
from app.application.use_cases.administrador_use_cases import AdministradorUseCases

router = APIRouter(prefix="/admin", tags=["Administrador"])

def get_use_case(db: Session = Depends(get_db)):
    return AdministradorUseCases(AdministradorRepository(db))

@router.get("/configuracoes")
def obter_configuracoes(uc: AdministradorUseCases = Depends(get_use_case)):
    return uc.obter_configuracoes()

@router.put("/configuracoes")
def atualizar_configuracoes(data: dict, uc: AdministradorUseCases = Depends(get_use_case)):
    return uc.atualizar_configuracoes(data)

@router.post("/backup")
def realizar_backup(uc: AdministradorUseCases = Depends(get_use_case)):
    try:
        return uc.realizar_backup()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/restaurar")
def restaurar_backup(data: dict, uc: AdministradorUseCases = Depends(get_use_case)):
    file_url = data.get("file_url")
    try:
        return uc.restaurar_backup(file_url)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
