from sqlalchemy.orm import Session
from typing import List, Optional
from .base_repository import BaseRepository
from ..models.solicitacao_model import SolicitacaoModel
from app.domain.entities.solicitacao_entity import Solicitacao
from app.domain.repositories.solicitacao_repository import ISolicitacaoRepository

class SolicitacaoRepository(BaseRepository[SolicitacaoModel, Solicitacao], ISolicitacaoRepository):
    def __init__(self, db: Session):
        self.db = db
        super().__init__(db, SolicitacaoModel)

    def get_all(self) -> List[Solicitacao]:
        models = self.db.query(self.model).filter(self.model.is_deleted == False).all()
        return [m.to_entity() for m in models]

    def get_all_paginated(self, skip: int = 0, limit: int = 10, status: Optional[str] = None) -> List[Solicitacao]:
        query = self.db.query(self.model).filter(self.model.is_deleted == False)
        
        # Filtro útil para a secretaria ver apenas o que está PENDENTE na fila
        if status:
            query = query.filter(self.model.status == status)
            
        # Ordenamos pela data do pedido e prioridade (Urgentes primeiro)
        query = query.order_by(self.model.data_solicitacao.asc(), self.model.prioridade.desc())
            
        models = query.offset(skip).limit(limit).all()
        return [m.to_entity() for m in models]

    def get_by_id(self, id: str) -> Optional[Solicitacao]:
        # O SQLAlchemy, através do relationship que criámos no Model, já vai trazer
        # as execuções filhas automaticamente aqui! Magia pura.
        model = self.db.query(self.model).filter(self.model.id == id, self.model.is_deleted == False).first()
        return model.to_entity() if model else None

    # Os métodos create, update e delete já são herdados do teu BaseRepository,
    # então não precisamos de reescrevê-los aqui a não ser que haja lógica extra.