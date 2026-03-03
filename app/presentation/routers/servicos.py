from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.infrastructure.repositories.servico_repository import ServicoRepository
from app.infrastructure.repositories.log_repository import LogRepository
from app.application.use_cases.servico_use_cases import ServicoUseCases
from app.application.use_cases.log_use_cases import LogUseCases

router = APIRouter(prefix="/servicos", tags=["Serviços"])

def get_use_case(db: Session = Depends(get_db)):
    repo = ServicoRepository(db)
    log_repo = LogRepository(db)
    log_uc = LogUseCases(log_repo)
    return ServicoUseCases(repo, log_uc)

@router.get("/")
def listar_servicos(uc: ServicoUseCases = Depends(get_use_case)):
    return uc.listar_servicos()

@router.get("/{servico_id}")
def obter_servico(servico_id: str, uc: ServicoUseCases = Depends(get_use_case)):
    try:
        return uc.obter_servico(servico_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/")
def criar_servico(data: dict, uc: ServicoUseCases = Depends(get_use_case)):
    usuario_logado = {"id": "system", "name": "Sistema"} # TODO: Pegar do token JWT
    try:
        return uc.criar_servico(data, usuario_logado)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{servico_id}")
def atualizar_servico(servico_id: str, data: dict, uc: ServicoUseCases = Depends(get_use_case)):
    usuario_logado = {"id": "system", "name": "Sistema"} # TODO: Pegar do token JWT
    try:
        return uc.atualizar_servico(servico_id, data, usuario_logado)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{servico_id}")
def deletar_servico(servico_id: str, uc: ServicoUseCases = Depends(get_use_case)):
    usuario_logado = {"id": "system", "name": "Sistema"} # TODO: Pegar do token JWT
    try:
        sucesso = uc.deletar_servico(servico_id, usuario_logado)
        if not sucesso:
            raise HTTPException(status_code=404, detail="Serviço não encontrado")
        return {"message": "Serviço deletado com sucesso"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
