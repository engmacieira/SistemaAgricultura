from pydantic import BaseModel, ConfigDict
from typing import Optional

class ServicoBase(BaseModel):
    name: str
    description: str
    unit: str
    basePrice: float
    active: bool

class ServicoCreate(ServicoBase):
    pass

class ServicoUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    unit: Optional[str] = None
    basePrice: Optional[float] = None
    active: Optional[bool] = None

class ServicoResponse(ServicoBase):
    id: str

    model_config = ConfigDict(from_attributes=True)
