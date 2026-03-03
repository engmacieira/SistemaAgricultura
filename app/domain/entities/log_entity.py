from dataclasses import dataclass
from datetime import datetime

@dataclass
class Log:
    id: str
    timestamp: datetime
    userId: str
    userName: str
    action: str
    entity: str
    details: str
