from fastapi import APIRouter, HTTPException, status
from typing import List
from ..schemas.servico_schema import ServicoCreate, ServicoUpdate, ServicoResponse

router = APIRouter(prefix="/servicos", tags=["Serviços"])

@router.get("/", response_model=List[ServicoResponse])
def listar_servicos():
    """Retorna a lista de todos os serviços agrícolas."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Ainda não implementado")

@router.get("/{servico_id}", response_model=ServicoResponse)
def obter_servico(servico_id: str):
    """Retorna os detalhes de um serviço específico."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Ainda não implementado")

@router.post("/", response_model=ServicoResponse, status_code=status.HTTP_201_CREATED)
def criar_servico(servico: ServicoCreate):
    """Cria um novo serviço agrícola."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Ainda não implementado")

@router.put("/{servico_id}", response_model=ServicoResponse)
def atualizar_servico(servico_id: str, servico: ServicoUpdate):
    """Atualiza os dados de um serviço existente."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Ainda não implementado")

@router.delete("/{servico_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_servico(servico_id: str):
    """Remove um serviço do sistema."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Ainda não implementado")
