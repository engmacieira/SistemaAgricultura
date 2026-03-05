from typing import List
from app.presentation.schemas.pagamento_schema import (
    PagamentoUpdate, 
    PagamentoRegister, 
    TransacaoPagamentoResponse,
    PagamentoPaginatedResponse,
    DebitosReportResponse,
    TransacaoPagamentoUpdate,
    PagamentoResponse # Added missing import
)
from fastapi import APIRouter, Depends, HTTPException, status # Added status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.infrastructure.repositories.pagamento_repository import PagamentoRepository
from app.infrastructure.repositories.log_repository import LogRepository
from app.application.use_cases.pagamento_use_cases import PagamentoUseCases
from app.application.use_cases.log_use_cases import LogUseCases
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/pagamentos", tags=["Pagamentos"])

def get_use_case(db: Session = Depends(get_db)):
    return PagamentoUseCases(
        PagamentoRepository(db),
        LogUseCases(LogRepository(db))
    )

@router.get("/", response_model=PagamentoPaginatedResponse)
def listar_pagamentos(
    skip: int = 0, 
    limit: int = 10, 
    sort_by: str = "dueDate", 
    order: str = "desc",
    search: str = "",
    uc: PagamentoUseCases = Depends(get_use_case)
):
    """Retorna a lista de todos os pagamentos com paginação e busca."""
    items = uc.listar_pagamentos(skip, limit, sort_by, order, search)
    total = uc.contar_pagamentos(search)
    import math
    return {
        "items": items,
        "total": total,
        "page": skip // limit,
        "pages": math.ceil(total / limit)
    }

@router.get("/debitos-por-produtor", response_model=DebitosReportResponse)
def obter_debitos_por_produtor(search: str = "", uc: PagamentoUseCases = Depends(get_use_case)):
    """Retorna o relatório de débitos agrupados por produtor."""
    records = uc.obter_debitos_por_produtor(search)
    total_general = sum(r["totalDebt"] for r in records)
    return {
        "records": records,
        "totalGeneral": total_general
    }

@router.get("/{pagamento_id}", response_model=PagamentoResponse)
def obter_pagamento(pagamento_id: str, uc: PagamentoUseCases = Depends(get_use_case)):
    """Retorna os detalhes de um pagamento específico."""
    try:
        return uc.obter_pagamento(pagamento_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{pagamento_id}/historico", response_model=List[TransacaoPagamentoResponse])
def obter_historico(pagamento_id: str, uc: PagamentoUseCases = Depends(get_use_case)):
    """Retorna o histórico de transações de um pagamento específico."""
    try:
        return uc.obter_historico(pagamento_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/{pagamento_id}", response_model=PagamentoResponse)
def atualizar_pagamento(pagamento_id: str, data: PagamentoUpdate, uc: PagamentoUseCases = Depends(get_use_case), current_user: dict = Depends(get_current_user)):
    """Atualiza os dados de um pagamento existente (ex: alterar data de vencimento ou desconto)."""
    try:
        return uc.atualizar_pagamento(pagamento_id, data.model_dump(exclude_unset=True), current_user)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/{pagamento_id}/pagar", status_code=status.HTTP_201_CREATED)
def registrar_pagamento(pagamento_id: str, data: PagamentoRegister, uc: PagamentoUseCases = Depends(get_use_case), current_user: dict = Depends(get_current_user)):
    """Registra uma nova transação de pagamento/baixa para um pagamento existente."""
    try:
        return uc.registrar_pagamento(pagamento_id, data.amountToPay, data.paymentDate, current_user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{pagamento_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_pagamento(pagamento_id: str, uc: PagamentoUseCases = Depends(get_use_case), current_user: dict = Depends(get_current_user)):
    """Remove um pagamento do sistema."""
    try:
        uc.deletar_pagamento(pagamento_id, current_user)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/transacoes/{transaction_id}")
def atualizar_transacao(transaction_id: str, data: TransacaoPagamentoUpdate, uc: PagamentoUseCases = Depends(get_use_case)):
    """Atualiza uma transação de pagamento existente."""
    try:
        return uc.atualizar_transacao(transaction_id, data.model_dump(exclude_unset=True))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/transacoes/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_transacao(transaction_id: str, uc: PagamentoUseCases = Depends(get_use_case)):
    """Remove uma transação de pagamento específica."""
    if not uc.excluir_transacao(transaction_id):
        raise HTTPException(status_code=404, detail="Transação não encontrada")

