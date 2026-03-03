from fastapi import APIRouter, HTTPException, status
from typing import List
from ..schemas.produtor_schema import ProdutorCreate, ProdutorUpdate, ProdutorResponse

router = APIRouter(prefix="/produtores", tags=["Produtores"])

@router.get("/", response_model=List[ProdutorResponse])
def listar_produtores():
    """Retorna a lista de todos os produtores."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Ainda não implementado")

@router.get("/{produtor_id}", response_model=ProdutorResponse)
def obter_produtor(produtor_id: str):
    """Retorna os detalhes de um produtor específico."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Ainda não implementado")

@router.post("/", response_model=ProdutorResponse, status_code=status.HTTP_201_CREATED)
def criar_produtor(produtor: ProdutorCreate):
    """Cria um novo produtor."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Ainda não implementado")

@router.put("/{produtor_id}", response_model=ProdutorResponse)
def atualizar_produtor(produtor_id: str, produtor: ProdutorUpdate):
    """Atualiza os dados de um produtor existente."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Ainda não implementado")

@router.delete("/{produtor_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_produtor(produtor_id: str):
    """Remove um produtor do sistema."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Ainda não implementado")
