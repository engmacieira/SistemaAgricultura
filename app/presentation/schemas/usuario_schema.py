from pydantic import BaseModel, EmailStr
from typing import Optional

class UsuarioBase(BaseModel):
    name: str
    email: EmailStr
    role: str

class UsuarioCreate(UsuarioBase):
    password: str

class UsuarioUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    password: Optional[str] = None

class UsuarioResponse(UsuarioBase):
    id: str

    class Config:
        from_attributes = True
