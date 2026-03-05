from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class Pagamento:
    id: str
    executionId: str
    producerName: str
    serviceName: str
    dueDate: date
    amount: float
    status: str
    paidAmount: float = 0.0
    paymentDate: Optional[date] = None
    is_deleted: bool = False

@dataclass
class TransacaoPagamento:
    id: str
    pagamentoId: str
    amount: float
    date: date
