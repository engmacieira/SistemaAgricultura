from sqlalchemy import Column, String, Float, Date, ForeignKey
from app.core.database import Base
from app.domain.entities.execucao_entity import Execucao
import uuid

class ExecucaoModel(Base):
    __tablename__ = "execucoes"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    producerId = Column(String, ForeignKey("produtores.id"), nullable=False)
    producerName = Column(String, nullable=False)
    serviceId = Column(String, ForeignKey("servicos.id"), nullable=False)
    serviceName = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    quantity = Column(Float, nullable=False)
    unit = Column(String, nullable=False)
    totalValue = Column(Float, nullable=False)
    status = Column(String, default="Pendente")

    def to_entity(self) -> Execucao:
        return Execucao(
            id=self.id,
            producerId=self.producerId,
            producerName=self.producerName,
            serviceId=self.serviceId,
            serviceName=self.serviceName,
            date=self.date,
            quantity=self.quantity,
            unit=self.unit,
            totalValue=self.totalValue,
            status=self.status
        )
