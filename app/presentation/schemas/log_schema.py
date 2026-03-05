from pydantic import BaseModel, ConfigDict
from datetime import datetime

class LogBase(BaseModel):
    userId: str
    userName: str
    action: str
    entity: str
    details: str
    dados_anteriores: str | None = None
    dados_novos: str | None = None

class LogCreate(LogBase):
    pass

class LogResponse(LogBase):
    id: str
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)

class PaginatedLogResponse(BaseModel):
    items: list[LogResponse]
    total: int
    page: int
    pages: int
