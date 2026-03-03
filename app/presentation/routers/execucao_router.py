from fastapi import APIRouter, HTTPException, status
from typing import List
from ..schemas.execucao_schema import ExecucaoCreate, ExecucaoUpdate, ExecucaoResponse

router = APIRouter(prefix="/execucoes", tags=["Execuções"])

@router.get("/", response_model=List[ExecucaoResponse])
def listar_execucoes():
    """Retorna a lista de todas as execuções e agendamentos."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Ainda não implementado")

@router.get("/{execucao_id}", response_model=ExecucaoResponse)
def obter_execucao(execucao_id: str):
    """Retorna os detalhes de uma execução específica."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Ainda não implementado")

@router.post("/", response_model=ExecucaoResponse, status_code=status.HTTP_201_CREATED)
def criar_execucao(execucao: ExecucaoCreate):
    """Registra uma nova execução ou agendamento."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Ainda não implementado")

@router.put("/{execucao_id}", response_model=ExecucaoResponse)
def atualizar_execucao(execucao_id: str, execucao: ExecucaoUpdate):
    """Atualiza os dados de uma execução existente."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Ainda não implementado")

@router.delete("/{execucao_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_execucao(execucao_id: str):
    """Remove uma execução do sistema."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Ainda não implementado")
