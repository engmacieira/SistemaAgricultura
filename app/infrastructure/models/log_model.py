from sqlalchemy import Column, String, DateTime
from app.core.database import Base
from app.domain.entities.log_entity import Log
import uuid
from datetime import datetime, timezone

class LogModel(Base):
    __tablename__ = "logs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    userId = Column(String, nullable=False)
    userName = Column(String, nullable=False)
    action = Column(String, nullable=False)
    entity = Column(String, nullable=False)
    details = Column(String, nullable=False)

    def to_entity(self) -> Log:
        return Log(
            id=self.id,
            timestamp=self.timestamp,
            userId=self.userId,
            userName=self.userName,
            action=self.action,
            entity=self.entity,
            details=self.details
        )
