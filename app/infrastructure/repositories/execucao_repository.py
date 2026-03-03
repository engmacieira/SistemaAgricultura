from sqlalchemy.orm import Session
from .base_repository import BaseRepository
from ..models.execucao_model import ExecucaoModel
from app.domain.entities.execucao_entity import Execucao

class ExecucaoRepository(BaseRepository[ExecucaoModel, Execucao]):
    def __init__(self, db: Session):
        super().__init__(db, ExecucaoModel)
