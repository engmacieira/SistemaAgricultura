from pydantic import BaseModel
from datetime import datetime

class LogBase(BaseModel):
    userId: str
    userName: str
    action: str
    entity: str
    details: str

class LogCreate(LogBase):
    pass

class LogResponse(LogBase):
    id: str
    timestamp: datetime

    class Config:
        from_attributes = True
