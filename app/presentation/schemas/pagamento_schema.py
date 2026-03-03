from pydantic import BaseModel
from typing import Optional
from datetime import date

class PagamentoBase(BaseModel):
    executionId: str
    producerName: str
    serviceName: str
    dueDate: date
    amount: float
    status: str

class PagamentoCreate(PagamentoBase):
    paymentDate: Optional[date] = None

class PagamentoUpdate(BaseModel):
    dueDate: Optional[date] = None
    paymentDate: Optional[date] = None
    amount: Optional[float] = None
    status: Optional[str] = None

class PagamentoResponse(PagamentoBase):
    id: str
    paymentDate: Optional[date] = None

    class Config:
        from_attributes = True
