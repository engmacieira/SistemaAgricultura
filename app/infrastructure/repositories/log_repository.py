from sqlalchemy.orm import Session
from .base_repository import BaseRepository
from ..models.log_model import LogModel
from app.domain.entities.log_entity import Log

class LogRepository(BaseRepository[LogModel, Log]):
    def __init__(self, db: Session):
        super().__init__(db, LogModel)
