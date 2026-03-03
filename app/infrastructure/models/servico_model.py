from sqlalchemy import Column, String, Float, Boolean
from app.core.database import Base
from app.domain.entities.servico_entity import Servico
import uuid

class ServicoModel(Base):
    __tablename__ = "servicos"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    unit = Column(String, nullable=False)
    basePrice = Column(Float, nullable=False)
    active = Column(Boolean, default=True)

    def to_entity(self) -> Servico:
        return Servico(
            id=self.id,
            name=self.name,
            description=self.description,
            unit=self.unit,
            basePrice=self.basePrice,
            active=self.active
        )
