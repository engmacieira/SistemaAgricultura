from pydantic import BaseModel, ConfigDict
from typing import Optional
import datetime

class PagamentoBase(BaseModel):
    executionId: str
    producerName: str
    serviceName: str
    dueDate: datetime.date
    amount: float
    paidAmount: float = 0.0
    status: str

class PagamentoCreate(PagamentoBase):
    paymentDate: Optional[datetime.date] = None

class PagamentoUpdate(BaseModel):
    dueDate: Optional[datetime.date] = None
    paymentDate: Optional[datetime.date] = None
    amount: Optional[float] = None
    paidAmount: Optional[float] = None
    status: Optional[str] = None

class PagamentoRegister(BaseModel):
    amountToPay: float
    paymentDate: Optional[datetime.date] = None

class TransacaoPagamentoUpdate(BaseModel):
    amount: Optional[float] = None
    date: Optional[datetime.date] = None

class TransacaoPagamentoResponse(BaseModel):
    id: str
    pagamentoId: str
    amount: float
    date: datetime.date

    model_config = ConfigDict(from_attributes=True)

class PagamentoResponse(PagamentoBase):
    id: str
    paymentDate: Optional[datetime.date] = None
    is_deleted: bool = False

    model_config = ConfigDict(from_attributes=True)

class PagamentoPaginatedResponse(BaseModel):
    items: list[PagamentoResponse]
    total: int
    page: int
    pages: int

class DebitoPorProdutorResponse(BaseModel):
    producerName: str
    totalDebt: float
    paymentCount: int

class DebitosReportResponse(BaseModel):
    records: list[DebitoPorProdutorResponse]
    totalGeneral: float
