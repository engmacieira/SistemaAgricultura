from sqlalchemy.orm import Session
from .base_repository import BaseRepository
from ..models.usuario_model import UsuarioModel
from app.domain.entities.usuario_entity import Usuario

class UsuarioRepository(BaseRepository[UsuarioModel, Usuario]):
    def __init__(self, db: Session):
        super().__init__(db, UsuarioModel)

    def get_by_email(self, email: str):
        model = self.db.query(self.model).filter(self.model.email == email).first()
        return model.to_entity() if model else None
