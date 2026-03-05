from fastapi import APIRouter, Depends, HTTPException, Query, status
from app.core.dependencies import get_current_user
from sqlalchemy.orm import Session
from app.presentation.schemas.produtor_schema import ProdutorCreate, ProdutorUpdate, ProdutorResponse, PaginatedProdutorResponse
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

@router.get("/", response_model=PaginatedProdutorResponse)
def listar_produtores(
    page: int = 1, 
    size: int = 10, 
    sort_by: str = "name", 
    order: str = "asc",
    uc: ProdutorUseCases = Depends(get_use_case)
):
    """Retorna a lista de todos os produtores com paginação e ordenação."""
    return uc.listar_produtores(page=page, size=size, sort_by=sort_by, order=order)

@router.get("/{produtor_id}", response_model=ProdutorResponse)
def obter_produtor(produtor_id: str, uc: ProdutorUseCases = Depends(get_use_case)):
    """Retorna os detalhes de um produtor específico."""
    try:
        return uc.obter_produtor(produtor_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/", response_model=ProdutorResponse, status_code=status.HTTP_201_CREATED)
def criar_produtor(data: ProdutorCreate, uc: ProdutorUseCases = Depends(get_use_case), usuario_logado: dict = Depends(get_current_user)):
    """Cria um novo produtor."""
    try:
        return uc.criar_produtor(data.model_dump(), usuario_logado)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{produtor_id}", response_model=ProdutorResponse)
def atualizar_produtor(produtor_id: str, data: ProdutorUpdate, uc: ProdutorUseCases = Depends(get_use_case), usuario_logado: dict = Depends(get_current_user)):
    """Atualiza os dados de um produtor existente."""
    try:
        return uc.atualizar_produtor(produtor_id, data.model_dump(exclude_unset=True), usuario_logado)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{produtor_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_produtor(produtor_id: str, uc: ProdutorUseCases = Depends(get_use_case), usuario_logado: dict = Depends(get_current_user)):
    """Remove um produtor do sistema."""
    try:
        sucesso = uc.deletar_produtor(produtor_id, usuario_logado)
        if not sucesso:
            raise HTTPException(status_code=404, detail="Produtor não encontrado")
        return {"message": "Produtor deletado com sucesso"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

