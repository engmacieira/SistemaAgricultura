# app/domain/entities/pagamento_entity.py
from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class Pagamento:
    id: str
    executionId: str        # Faturando a execução real
    producerName: str
    serviceName: str
    dueDate: date           # Vencimento
    amount: float           # Valor total a pagar
    status: str             # 'PENDENTE', 'PARCIAL', 'PAGO'
    paidAmount: float = 0.0
    paymentDate: Optional[date] = None
    is_deleted: bool = False

@dataclass
class TransacaoPagamento:
    id: str
    pagamentoId: str
    amount: float
    date: date