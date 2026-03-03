from sqlalchemy import Column, String, JSON
from app.core.database import Base
from app.domain.entities.administrador_entity import Configuracao
import uuid

class ConfiguracaoModel(Base):
    __tablename__ = "configuracoes"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    chave = Column(String, unique=True, nullable=False)
    valor = Column(JSON, nullable=False)

    def to_entity(self) -> Configuracao:
        return Configuracao(
            id=self.id,
            chave=self.chave,
            valor=self.valor
        )
