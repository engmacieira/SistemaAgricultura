from pydantic import BaseModel, ConfigDict
from typing import Optional, List

class ProdutorBase(BaseModel):
    name: str
    cpfCnpj: str
    property: str
    regiao_referencia: Optional[str] = None
    telefone_contato: Optional[str] = None
    apelido_produtor: Optional[str] = None
    status: str

class ProdutorCreate(ProdutorBase):
    pass

class ProdutorUpdate(BaseModel):
    name: Optional[str] = None
    cpfCnpj: Optional[str] = None
    property: Optional[str] = None
    regiao_referencia: Optional[str] = None
    telefone_contato: Optional[str] = None
    apelido_produtor: Optional[str] = None
    status: Optional[str] = None

class ProdutorResponse(ProdutorBase):
    id: str
    is_deleted: bool

    model_config = ConfigDict(from_attributes=True)

class PaginatedProdutorResponse(BaseModel):
    items: List[ProdutorResponse]
    total: int
    page: int
    size: int
    pages: int
