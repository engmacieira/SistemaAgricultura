from pydantic import BaseModel, ConfigDict
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

    model_config = ConfigDict(from_attributes=True)
