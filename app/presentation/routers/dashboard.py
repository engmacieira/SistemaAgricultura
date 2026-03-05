from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.application.use_cases.dashboard_use_cases import DashboardUseCases
from app.application.schemas.dashboard_schemas import DashboardData

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/", response_model=DashboardData)
def get_dashboard_data(db: Session = Depends(get_db)):
    try:
        use_cases = DashboardUseCases(db)
        return use_cases.get_dashboard_data()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
