from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.infrastructure.repositories.log_repository import LogRepository
from app.application.use_cases.log_use_cases import LogUseCases
from app.presentation.schemas.log_schema import PaginatedLogResponse, LogCreate, LogResponse
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/logs", tags=["Logs"])

def get_use_case(db: Session = Depends(get_db)):
    return LogUseCases(LogRepository(db))

@router.get("/", response_model=PaginatedLogResponse)
def listar_logs(
    skip: int = 0, 
    limit: int = 10, 
    sort_by: str = "timestamp", 
    order: str = "desc",
    search: str = "",
    uc: LogUseCases = Depends(get_use_case),
    usuario_logado: dict = Depends(get_current_user)
):
    """Retorna a lista de logs de auditoria do sistema com suporte a paginação."""
    return uc.listar_logs(skip, limit, sort_by, order, search)

