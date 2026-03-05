from sqlalchemy.orm import Session
from typing import List, Optional
from .base_repository import BaseRepository
from ..models.usuario_model import UsuarioModel
from app.domain.entities.usuario_entity import Usuario

class UsuarioRepository(BaseRepository[UsuarioModel, Usuario]):
    def __init__(self, db: Session):
        super().__init__(db, UsuarioModel)

    def get_all_paginated(self, skip: int = 0, limit: int = 10, sort_by: str = "name", order: str = "asc") -> List[Usuario]:
        query = self.db.query(self.model).filter(self.model.is_deleted == False)
        
        # Sorting
        column = getattr(self.model, sort_by, self.model.name)
        if order.lower() == "desc":
            query = query.order_by(column.desc())
        else:
            query = query.order_by(column.asc())
            
        models = query.offset(skip).limit(limit).all()
        return [m.to_entity() for m in models]

    def count_active(self) -> int:
        return self.db.query(self.model).filter(self.model.is_deleted == False).count()

    def get_by_id(self, id: str) -> Optional[Usuario]:
        model = self.db.query(self.model).filter(self.model.id == id, self.model.is_deleted == False).first()
        return model.to_entity() if model else None

    def get_by_email(self, email: str):
        model = self.db.query(self.model).filter(self.model.email == email, self.model.is_deleted == False).first()
        return model.to_entity() if model else None
        
    def delete(self, id: str) -> bool:
        obj = self.db.query(self.model).filter(self.model.id == id).first()
        if obj:
            obj.is_deleted = True
            self.db.commit()
            return True
        return False
