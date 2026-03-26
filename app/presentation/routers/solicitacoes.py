from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from sqlalchemy.orm import Session
from app.core.database import get_db

from app.infrastructure.repositories.solicitacao_repository import SolicitacaoRepository
from app.infrastructure.repositories.log_repository import LogRepository
from app.application.use_cases.solicitacao_use_cases import SolicitacaoUseCases
from app.application.use_cases.log_use_cases import LogUseCases

from app.presentation.schemas.solicitacao_schema import SolicitacaoCreate, SolicitacaoUpdate, SolicitacaoResponse
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/solicitacoes", tags=["Fila de Espera (Solicitações)"], dependencies=[Depends(get_current_user)])

def get_use_case(db: Session = Depends(get_db)):
    repo = SolicitacaoRepository(db)
    log_repo = LogRepository(db)
    log_uc = LogUseCases(log_repo)
    return SolicitacaoUseCases(repo, log_uc)

@router.get("/", response_model=List[SolicitacaoResponse])
def listar_solicitacoes(
    skip: int = 0, limit: int = 50, status_filtro: Optional[str] = None,
    uc: SolicitacaoUseCases = Depends(get_use_case)
):
    return uc.listar_solicitacoes(skip, limit, status_filtro)

@router.get("/{solicitacao_id}", response_model=SolicitacaoResponse)
def obter_solicitacao(solicitacao_id: str, uc: SolicitacaoUseCases = Depends(get_use_case)):
    try:
        return uc.obter_solicitacao(solicitacao_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/", response_model=SolicitacaoResponse, status_code=status.HTTP_201_CREATED)
def criar_solicitacao(data: SolicitacaoCreate, uc: SolicitacaoUseCases = Depends(get_use_case), current_user: dict = Depends(get_current_user)):
    return uc.criar_solicitacao(data.model_dump(), current_user)

@router.put("/{solicitacao_id}", response_model=SolicitacaoResponse)
def atualizar_solicitacao(solicitacao_id: str, data: SolicitacaoUpdate, uc: SolicitacaoUseCases = Depends(get_use_case), current_user: dict = Depends(get_current_user)):
    try:
        return uc.atualizar_solicitacao(solicitacao_id, data.model_dump(exclude_unset=True), current_user)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{solicitacao_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_solicitacao(solicitacao_id: str, uc: SolicitacaoUseCases = Depends(get_use_case), current_user: dict = Depends(get_current_user)):
    if not uc.deletar_solicitacao(solicitacao_id, current_user):
        raise HTTPException(status_code=404, detail="Solicitação não encontrada.")