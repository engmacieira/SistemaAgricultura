from pydantic import BaseModel, ConfigDict
from typing import Optional
import datetime

class ExecucaoBase(BaseModel):
    solicitacaoId: str      # ✅ Vínculo com a Fila
    serviceId: str
    serviceName: str
    date: datetime.date
    quantity: float
    unit: str
    valor_unitario: float   # ✅ Preço no dia
    totalValue: float
    status: str = "REGISTRADA"
    operador_maquina: Optional[str] = None # ✅ Quem operou

class ExecucaoCreate(ExecucaoBase):
    pass

class ExecucaoUpdate(BaseModel):
    serviceId: Optional[str] = None
    serviceName: Optional[str] = None
    date: Optional[datetime.date] = None
    quantity: Optional[float] = None
    unit: Optional[str] = None
    valor_unitario: Optional[float] = None
    totalValue: Optional[float] = None
    status: Optional[str] = None
    operador_maquina: Optional[str] = None

class ExecucaoResponse(ExecucaoBase):
    id: str

    model_config = ConfigDict(from_attributes=True)