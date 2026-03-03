from pydantic import BaseModel, ConfigDict
from typing import Optional
import datetime

class PagamentoBase(BaseModel):
    executionId: str
    producerName: str
    serviceName: str
    dueDate: datetime.date
    amount: float
    status: str

class PagamentoCreate(PagamentoBase):
    paymentDate: Optional[datetime.date] = None

class PagamentoUpdate(BaseModel):
    dueDate: Optional[datetime.date] = None
    paymentDate: Optional[datetime.date] = None
    amount: Optional[float] = None
    status: Optional[str] = None

class PagamentoResponse(PagamentoBase):
    id: str
    paymentDate: Optional[date] = None

    model_config = ConfigDict(from_attributes=True)
