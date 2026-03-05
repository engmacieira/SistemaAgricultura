from sqlalchemy.orm import Session
from .base_repository import BaseRepository
from ..models.log_model import LogModel
from app.domain.entities.log_entity import Log

class LogRepository(BaseRepository[LogModel, Log]):
    def __init__(self, db: Session):
        super().__init__(db, LogModel)

    def get_all_paginated(self, skip: int = 0, limit: int = 10, sort_by: str = "timestamp", order: str = "desc", search: str = "") -> list[Log]:
        from sqlalchemy import or_
        query = self.db.query(self.model)
        
        if search:
            search_filter = f"%{search}%"
            query = query.filter(
                or_(
                    self.model.userName.ilike(search_filter),
                    self.model.entity.ilike(search_filter),
                    self.model.details.ilike(search_filter)
                )
            )

        # Sorting
        column = getattr(self.model, sort_by, self.model.timestamp)
        if order.lower() == "desc":
            query = query.order_by(column.desc())
        else:
            query = query.order_by(column.asc())
            
        models = query.offset(skip).limit(limit).all()
        return [m.to_entity() for m in models]

    def count(self, search: str = "") -> int:
        from sqlalchemy import or_
        query = self.db.query(self.model)
        
        if search:
            search_filter = f"%{search}%"
            query = query.filter(
                or_(
                    self.model.userName.ilike(search_filter),
                    self.model.entity.ilike(search_filter),
                    self.model.details.ilike(search_filter)
                )
            )
            
        return query.count()
