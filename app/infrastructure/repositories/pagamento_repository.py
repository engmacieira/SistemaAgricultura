from sqlalchemy.orm import Session
from .base_repository import BaseRepository
from ..models.pagamento_model import PagamentoModel
from app.domain.entities.pagamento_entity import Pagamento

class PagamentoRepository(BaseRepository[PagamentoModel, Pagamento]):
    def __init__(self, db: Session):
        super().__init__(db, PagamentoModel)
