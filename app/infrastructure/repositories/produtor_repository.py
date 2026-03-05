from sqlalchemy.orm import Session
from typing import List, Optional
from .base_repository import BaseRepository
from ..models.produtor_model import ProdutorModel
from ..models.execucao_model import ExecucaoModel
from app.domain.entities.produtor_entity import Produtor

class ProdutorRepository(BaseRepository[ProdutorModel, Produtor]):
    def __init__(self, db: Session):
        super().__init__(db, ProdutorModel)

    def get_all_paginated(self, skip: int = 0, limit: int = 10, sort_by: str = "name", order: str = "asc") -> List[Produtor]:
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

    def get_by_id(self, id: str) -> Optional[Produtor]:
        model = self.db.query(self.model).filter(self.model.id == id, self.model.is_deleted == False).first()
        return model.to_entity() if model else None

    def get_by_cpf_cnpj(self, cpf_cnpj: str):
        model = self.db.query(self.model).filter(self.model.cpfCnpj == cpf_cnpj, self.model.is_deleted == False).first()
        return model.to_entity() if model else None

    def get_model_by_cpf_cnpj(self, cpf_cnpj: str) -> Optional[ProdutorModel]:
        return self.db.query(self.model).filter(self.model.cpfCnpj == cpf_cnpj).first()
        
    def delete(self, id: str) -> bool:
        obj = self.db.query(self.model).filter(self.model.id == id).first()
        if obj:
            obj.is_deleted = True
            self.db.commit()
            return True
        return False

    def get_by_filters(self, producer_id: Optional[str] = None, status: Optional[str] = None, regiao: Optional[str] = None) -> List[Produtor]:
        query = self.db.query(self.model).filter(self.model.is_deleted == False)
        
        if producer_id:
            query = query.filter(self.model.id == producer_id)
            
        if status:
            query = query.filter(self.model.status == status)
            
        if regiao:
            query = query.filter(self.model.regiao_referencia == regiao)
            
        models = query.order_by(self.model.name.asc()).all()
        return [m.to_entity() for m in models]

    def has_execucoes(self, produtor_id: str) -> bool:
        count = self.db.query(ExecucaoModel).filter(ExecucaoModel.producerId == produtor_id).count()
        return count > 0
