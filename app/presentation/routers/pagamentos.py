from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.infrastructure.repositories.pagamento_repository import PagamentoRepository
from app.application.use_cases.pagamento_use_cases import PagamentoUseCases

router = APIRouter(prefix="/pagamentos", tags=["Pagamentos"])

def get_use_case(db: Session = Depends(get_db)):
    return PagamentoUseCases(PagamentoRepository(db))

@router.get("/")
def listar_pagamentos(uc: PagamentoUseCases = Depends(get_use_case)):
    return uc.listar_pagamentos()

@router.get("/{pagamento_id}")
def obter_pagamento(pagamento_id: str, uc: PagamentoUseCases = Depends(get_use_case)):
    try:
        return uc.obter_pagamento(pagamento_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/{pagamento_id}/pagar")
def registrar_pagamento(pagamento_id: str, uc: PagamentoUseCases = Depends(get_use_case)):
    try:
        return uc.registrar_pagamento(pagamento_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
