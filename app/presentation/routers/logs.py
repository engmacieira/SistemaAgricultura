from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.infrastructure.repositories.log_repository import LogRepository
from app.application.use_cases.log_use_cases import LogUseCases

router = APIRouter(prefix="/logs", tags=["Logs"])

def get_use_case(db: Session = Depends(get_db)):
    return LogUseCases(LogRepository(db))

@router.get("/")
def listar_logs(uc: LogUseCases = Depends(get_use_case)):
    return uc.listar_logs()
