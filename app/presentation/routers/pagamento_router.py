from fastapi import APIRouter, HTTPException, status
from typing import List
from ..schemas.pagamento_schema import PagamentoCreate, PagamentoUpdate, PagamentoResponse

router = APIRouter(prefix="/pagamentos", tags=["Pagamentos"])

@router.get("/", response_model=List[PagamentoResponse])
def listar_pagamentos():
    """Retorna a lista de todos os pagamentos."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Ainda não implementado")

@router.get("/{pagamento_id}", response_model=PagamentoResponse)
def obter_pagamento(pagamento_id: str):
    """Retorna os detalhes de um pagamento específico."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Ainda não implementado")

@router.post("/", response_model=PagamentoResponse, status_code=status.HTTP_201_CREATED)
def criar_pagamento(pagamento: PagamentoCreate):
    """Registra um novo pagamento (ou previsão de pagamento)."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Ainda não implementado")

@router.put("/{pagamento_id}", response_model=PagamentoResponse)
def atualizar_pagamento(pagamento_id: str, pagamento: PagamentoUpdate):
    """Atualiza os dados de um pagamento existente (ex: registrar como pago)."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Ainda não implementado")

@router.delete("/{pagamento_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_pagamento(pagamento_id: str):
    """Remove um pagamento do sistema."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Ainda não implementado")
