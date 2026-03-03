from fastapi import APIRouter, HTTPException, status
from typing import List
from ..schemas.log_schema import LogCreate, LogResponse

router = APIRouter(prefix="/logs", tags=["Logs"])

@router.get("/", response_model=List[LogResponse])
def listar_logs():
    """Retorna a lista de logs de auditoria do sistema."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Ainda não implementado")

@router.post("/", response_model=LogResponse, status_code=status.HTTP_201_CREATED)
def registrar_log(log: LogCreate):
    """Registra uma nova ação no log do sistema."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Ainda não implementado")
