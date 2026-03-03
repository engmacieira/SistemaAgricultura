from pydantic import BaseModel
from typing import Optional

class ProdutorBase(BaseModel):
    name: str
    cpfCnpj: str
    property: str
    totalArea: float
    status: str

class ProdutorCreate(ProdutorBase):
    pass

class ProdutorUpdate(BaseModel):
    name: Optional[str] = None
    cpfCnpj: Optional[str] = None
    property: Optional[str] = None
    totalArea: Optional[float] = None
    status: Optional[str] = None

class ProdutorResponse(ProdutorBase):
    id: str

    class Config:
        from_attributes = True
