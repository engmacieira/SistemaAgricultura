from sqlalchemy.orm import Session
from .base_repository import BaseRepository
from ..models.produtor_model import ProdutorModel
from ..models.execucao_model import ExecucaoModel
from app.domain.entities.produtor_entity import Produtor

class ProdutorRepository(BaseRepository[ProdutorModel, Produtor]):
    def __init__(self, db: Session):
        super().__init__(db, ProdutorModel)

    def get_by_cpf_cnpj(self, cpf_cnpj: str):
        model = self.db.query(self.model).filter(self.model.cpfCnpj == cpf_cnpj).first()
        return model.to_entity() if model else None
        
    def has_execucoes(self, produtor_id: str) -> bool:
        count = self.db.query(ExecucaoModel).filter(ExecucaoModel.producerId == produtor_id).count()
        return count > 0
