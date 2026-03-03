from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.infrastructure.repositories.produtor_repository import ProdutorRepository
from app.infrastructure.repositories.log_repository import LogRepository
from app.application.use_cases.produtor_use_cases import ProdutorUseCases
from app.application.use_cases.log_use_cases import LogUseCases

router = APIRouter(prefix="/produtores", tags=["Produtores"])

def get_use_case(db: Session = Depends(get_db)):
    repo = ProdutorRepository(db)
    log_repo = LogRepository(db)
    log_uc = LogUseCases(log_repo)
    return ProdutorUseCases(repo, log_uc)

@router.get("/")
def listar_produtores(uc: ProdutorUseCases = Depends(get_use_case)):
    return uc.listar_produtores()

@router.get("/{produtor_id}")
def obter_produtor(produtor_id: str, uc: ProdutorUseCases = Depends(get_use_case)):
    try:
        return uc.obter_produtor(produtor_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/")
def criar_produtor(data: dict, uc: ProdutorUseCases = Depends(get_use_case)):
    usuario_logado = {"id": "system", "name": "Sistema"} # TODO: Pegar do token JWT
    try:
        return uc.criar_produtor(data, usuario_logado)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{produtor_id}")
def atualizar_produtor(produtor_id: str, data: dict, uc: ProdutorUseCases = Depends(get_use_case)):
    usuario_logado = {"id": "system", "name": "Sistema"} # TODO: Pegar do token JWT
    try:
        return uc.atualizar_produtor(produtor_id, data, usuario_logado)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{produtor_id}")
def deletar_produtor(produtor_id: str, uc: ProdutorUseCases = Depends(get_use_case)):
    usuario_logado = {"id": "system", "name": "Sistema"} # TODO: Pegar do token JWT
    try:
        sucesso = uc.deletar_produtor(produtor_id, usuario_logado)
        if not sucesso:
            raise HTTPException(status_code=404, detail="Produtor não encontrado")
        return {"message": "Produtor deletado com sucesso"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
