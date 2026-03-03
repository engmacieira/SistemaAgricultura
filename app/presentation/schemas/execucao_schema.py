from pydantic import BaseModel, ConfigDict
from typing import Optional
import datetime

class ExecucaoBase(BaseModel):
    producerId: str
    producerName: str
    serviceId: str
    serviceName: str
    date: datetime.date
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
    date: Optional[datetime.date] = None
    quantity: Optional[float] = None
    unit: Optional[str] = None
    totalValue: Optional[float] = None
    status: Optional[str] = None

class ExecucaoResponse(ExecucaoBase):
    id: str

    model_config = ConfigDict(from_attributes=True)
