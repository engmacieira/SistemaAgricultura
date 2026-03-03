from sqlalchemy.orm import Session
from .base_repository import BaseRepository
from ..models.servico_model import ServicoModel
from ..models.execucao_model import ExecucaoModel
from app.domain.entities.servico_entity import Servico

class ServicoRepository(BaseRepository[ServicoModel, Servico]):
    def __init__(self, db: Session):
        super().__init__(db, ServicoModel)

    def get_by_name(self, name: str):
        model = self.db.query(self.model).filter(self.model.name == name).first()
        return model.to_entity() if model else None
        
    def has_execucoes(self, servico_id: str) -> bool:
        count = self.db.query(ExecucaoModel).filter(ExecucaoModel.serviceId == servico_id).count()
        return count > 0
