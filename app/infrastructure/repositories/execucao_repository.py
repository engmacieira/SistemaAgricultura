from sqlalchemy.orm import Session
from typing import List, Optional
from .base_repository import BaseRepository
from ..models.execucao_model import ExecucaoModel
from app.domain.entities.execucao_entity import Execucao
from app.domain.repositories.execucao_repository import IExecucaoRepository

class ExecucaoRepository(BaseRepository[ExecucaoModel, Execucao], IExecucaoRepository):
    def __init__(self, db: Session):
        self.db = db
        super().__init__(db, ExecucaoModel)

    def get_all(self) -> List[Execucao]:
        models = self.db.query(self.model).filter(self.model.is_deleted == False).all()
        return [m.to_entity() for m in models]

    def get_by_id(self, id: str) -> Optional[Execucao]:
        model = self.db.query(self.model).filter(self.model.id == id, self.model.is_deleted == False).first()
        return model.to_entity() if model else None

    # ✅ NOVO MÉTODO: Buscar todas as execuções de um pedido específico
    def get_by_solicitacao_id(self, solicitacao_id: str) -> List[Execucao]:
        models = self.db.query(self.model).filter(
            self.model.solicitacaoId == solicitacao_id,
            self.model.is_deleted == False
        ).order_by(self.model.date.desc()).all()
        return [m.to_entity() for m in models]

    def get_all_paginated(self, skip: int = 0, limit: int = 10, sort_by: str = "date", order: str = "desc", show_completed: bool = False) -> List[Execucao]:
        query = self.db.query(self.model).filter(self.model.is_deleted == False)
        
        if not show_completed:
            query = query.filter(self.model.status != "Concluído")
            
        # Sorting
        column = getattr(self.model, sort_by, self.model.date)
        if order.lower() == "desc":
            query = query.order_by(column.desc())
        else:
            query = query.order_by(column.asc())
            
        models = query.offset(skip).limit(limit).all()
        return [m.to_entity() for m in models]

    def count_filtered(self, show_completed: bool = False) -> int:
        query = self.db.query(self.model).filter(self.model.is_deleted == False)
        if not show_completed:
            query = query.filter(self.model.status != "Concluído")
        return query.count()

    def get_by_date_range(self, start_date: str, end_date: str) -> List[Execucao]:
        from datetime import datetime
        start = datetime.strptime(start_date, "%Y-%m-%d").date()
        end = datetime.strptime(end_date, "%Y-%m-%d").date()
        
        models = self.db.query(self.model).filter(
            self.model.date >= start,
            self.model.date <= end,
            self.model.is_deleted == False
        ).order_by(self.model.date.asc()).all()
        
        return [m.to_entity() for m in models]

    def delete(self, id: str) -> bool:
        # Assumindo que o delete físico/lógico é tratado pelo base_repository
        return super().delete(id)