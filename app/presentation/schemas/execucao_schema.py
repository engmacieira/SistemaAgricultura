from pydantic import BaseModel
from typing import Optional
from datetime import date

class ExecucaoBase(BaseModel):
    producerId: str
    producerName: str
    serviceId: str
    serviceName: str
    date: date
    quantity: float
    unit: str
    totalValue: float
    status: str

class ExecucaoCreate(ExecucaoBase):
    pass

class ExecucaoUpdate(BaseModel):
    producerId: Optional[str] = None
    producerName: Optional[str] = None
    serviceId: Optional[str] = None
    serviceName: Optional[str] = None
    date: Optional[date] = None
    quantity: Optional[float] = None
    unit: Optional[str] = None
    totalValue: Optional[float] = None
    status: Optional[str] = None

class ExecucaoResponse(ExecucaoBase):
    id: str

    class Config:
        from_attributes = True
