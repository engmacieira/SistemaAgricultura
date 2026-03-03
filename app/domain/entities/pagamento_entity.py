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
    paymentDate: Optional[date] = None
