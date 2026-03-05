from fastapi import APIRouter, Depends, HTTPException, status
from typing import List # Added missing import
from app.core.dependencies import get_current_user
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.infrastructure.repositories.servico_repository import ServicoRepository
from app.infrastructure.repositories.log_repository import LogRepository
from app.application.use_cases.servico_use_cases import ServicoUseCases
from app.application.use_cases.log_use_cases import LogUseCases
from app.presentation.schemas.servico_schema import ServicoCreate, ServicoUpdate, ServicoResponse, PaginatedServicoResponse # Assuming PaginatedServicoResponse exists like in Produtores

router = APIRouter(prefix="/servicos", tags=["Serviços"])

def get_use_case(db: Session = Depends(get_db)):
    repo = ServicoRepository(db)
    log_repo = LogRepository(db)
    log_uc = LogUseCases(log_repo)
    return ServicoUseCases(repo, log_uc)

@router.get("/", response_model=PaginatedServicoResponse)
def listar_servicos(
    skip: int = 0, 
    limit: int = 10, 
    sort_by: str = "name", 
    order: str = "asc",
    uc: ServicoUseCases = Depends(get_use_case)
):
    """Retorna a lista de todos os serviços agrícolas com paginação e ordenação."""
    return uc.listar_servicos(skip, limit, sort_by, order)

@router.get("/{servico_id}", response_model=ServicoResponse)
def obter_servico(servico_id: str, uc: ServicoUseCases = Depends(get_use_case)):
    """Retorna os detalhes de um serviço específico."""
    try:
        return uc.obter_servico(servico_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/", response_model=ServicoResponse, status_code=status.HTTP_201_CREATED)
def criar_servico(data: ServicoCreate, uc: ServicoUseCases = Depends(get_use_case), usuario_logado: dict = Depends(get_current_user)):
    """Cria um novo serviço agrícola."""
    try:
        return uc.criar_servico(data.model_dump(), usuario_logado) # Updated to use model_dump
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{servico_id}", response_model=ServicoResponse)
def atualizar_servico(servico_id: str, data: ServicoUpdate, uc: ServicoUseCases = Depends(get_use_case), usuario_logado: dict = Depends(get_current_user)):
    """Atualiza os dados de um serviço existente."""
    try:
        return uc.atualizar_servico(servico_id, data.model_dump(exclude_unset=True), usuario_logado) # Updated to use model_dump
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{servico_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_servico(servico_id: str, uc: ServicoUseCases = Depends(get_use_case), usuario_logado: dict = Depends(get_current_user)):
    """Remove um serviço do sistema."""
    try:
        sucesso = uc.deletar_servico(servico_id, usuario_logado)
        if not sucesso:
            raise HTTPException(status_code=404, detail="Serviço não encontrado")
        return {"message": "Serviço deletado com sucesso"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

