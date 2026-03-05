from sqlalchemy.orm import Session
from .base_repository import BaseRepository
from ..models.servico_model import ServicoModel
from ..models.execucao_model import ExecucaoModel
from typing import List, Optional
from app.domain.entities.servico_entity import Servico

class ServicoRepository(BaseRepository[ServicoModel, Servico]):
    def __init__(self, db: Session):
        super().__init__(db, ServicoModel)

    def get_all_paginated(self, skip: int = 0, limit: int = 10, sort_by: str = "name", order: str = "asc") -> List[Servico]:
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

    def get_by_id(self, id: str) -> Optional[Servico]:
        model = self.db.query(self.model).filter(self.model.id == id, self.model.is_deleted == False).first()
        return model.to_entity() if model else None

    def get_by_name(self, name: str):
        model = self.db.query(self.model).filter(self.model.name == name, self.model.is_deleted == False).first()
        return model.to_entity() if model else None
        
    def delete(self, id: str) -> bool:
        obj = self.db.query(self.model).filter(self.model.id == id).first()
        if obj:
            obj.is_deleted = True
            self.db.commit()
            return True
        return False

    def has_execucoes(self, servico_id: str) -> bool:
        count = self.db.query(ExecucaoModel).filter(ExecucaoModel.serviceId == servico_id).count()
        return count > 0
