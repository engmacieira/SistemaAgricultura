from sqlalchemy import Column, String, Float
from app.core.database import Base
from app.domain.entities.produtor_entity import Produtor
import uuid

class ProdutorModel(Base):
    __tablename__ = "produtores"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    cpfCnpj = Column(String, unique=True, nullable=False)
    property = Column(String, nullable=False)
    totalArea = Column(Float, nullable=False)
    status = Column(String, default="Ativo")

    def to_entity(self) -> Produtor:
        return Produtor(
            id=self.id,
            name=self.name,
            cpfCnpj=self.cpfCnpj,
            property=self.property,
            totalArea=self.totalArea,
            status=self.status
        )
