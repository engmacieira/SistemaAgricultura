from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from app.core.database import get_db

from app.infrastructure.repositories.execucao_repository import ExecucaoRepository
from app.infrastructure.repositories.solicitacao_repository import SolicitacaoRepository # ✅ NOVO
from app.infrastructure.repositories.pagamento_repository import PagamentoRepository
from app.infrastructure.repositories.log_repository import LogRepository

from app.application.use_cases.execucao_use_cases import ExecucaoUseCases
from app.application.use_cases.log_use_cases import LogUseCases

from app.presentation.schemas.execucao_schema import ExecucaoCreate, ExecucaoUpdate, ExecucaoResponse
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/execucoes", tags=["Execuções"], dependencies=[Depends(get_current_user)])

# ✅ REFATORAÇÃO: Injetando a Fila de Espera no Cérebro da Execução
def get_use_case(db: Session = Depends(get_db)):
    repo = ExecucaoRepository(db)
    solic_repo = SolicitacaoRepository(db) # Passamos o repositório da mãe
    pag_repo = PagamentoRepository(db)
    log_repo = LogRepository(db)
    log_uc = LogUseCases(log_repo)
    return ExecucaoUseCases(repo, solic_repo, pag_repo, log_uc)

@router.get("/")
def listar_execucoes(
    skip: int = 0, limit: int = 10, sort_by: str = "date", order: str = "desc",
    show_completed: bool = False, uc: ExecucaoUseCases = Depends(get_use_case)
):
    return uc.listar_execucoes(skip, limit, sort_by, order, show_completed)

@router.get("/count")
def contar_execucoes(show_completed: bool = False, uc: ExecucaoUseCases = Depends(get_use_case)):
    return {"total": uc.contar_execucoes(show_completed)}

@router.get("/{execucao_id}", response_model=ExecucaoResponse)
def obter_execucao(execucao_id: str, uc: ExecucaoUseCases = Depends(get_use_case)):
    try:
        return uc.obter_execucao(execucao_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/", response_model=ExecucaoResponse, status_code=status.HTTP_201_CREATED)
def registrar_execucao(data: ExecucaoCreate, uc: ExecucaoUseCases = Depends(get_use_case), current_user: dict = Depends(get_current_user)):
    return uc.criar_execucao(data.model_dump(), current_user)

@router.put("/{execucao_id}", response_model=ExecucaoResponse)
def atualizar_execucao(execucao_id: str, data: ExecucaoUpdate, uc: ExecucaoUseCases = Depends(get_use_case), current_user: dict = Depends(get_current_user)):
    try:
        return uc.atualizar_execucao(execucao_id, data.model_dump(exclude_unset=True), current_user)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{execucao_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_execucao(execucao_id: str, uc: ExecucaoUseCases = Depends(get_use_case), current_user: dict = Depends(get_current_user)):
    try:
        uc.deletar_execucao(execucao_id, current_user)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))