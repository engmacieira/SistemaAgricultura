from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.infrastructure.repositories.execucao_repository import ExecucaoRepository
from app.infrastructure.repositories.pagamento_repository import PagamentoRepository
from app.application.use_cases.execucao_use_cases import ExecucaoUseCases
from app.presentation.schemas.execucao_schema import ExecucaoCreate, ExecucaoUpdate

router = APIRouter(prefix="/execucoes", tags=["Execuções"])

def get_use_case(db: Session = Depends(get_db)):
    repo = ExecucaoRepository(db)
    pag_repo = PagamentoRepository(db)
    return ExecucaoUseCases(repo, pag_repo)

@router.get("/")
def listar_execucoes(uc: ExecucaoUseCases = Depends(get_use_case)):
    return uc.listar_execucoes()

@router.get("/{execucao_id}")
def obter_execucao(execucao_id: str, uc: ExecucaoUseCases = Depends(get_use_case)):
    try:
        return uc.obter_execucao(execucao_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/")
def registrar_execucao(data: ExecucaoCreate, uc: ExecucaoUseCases = Depends(get_use_case)):
    return uc.criar_execucao(data.model_dump())

@router.put("/{execucao_id}")
def atualizar_execucao(execucao_id: str, data: ExecucaoUpdate, uc: ExecucaoUseCases = Depends(get_use_case)):
    try:
        return uc.atualizar_execucao(execucao_id, data.model_dump(exclude_unset=True))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{execucao_id}")
def deletar_execucao(execucao_id: str, uc: ExecucaoUseCases = Depends(get_use_case)):
    sucesso = uc.deletar_execucao(execucao_id)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Execução não encontrada")
    return {"message": "Execução deletada com sucesso"}
