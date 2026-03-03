from sqlalchemy import Column, String, Float, Date, ForeignKey
from app.core.database import Base
from app.domain.entities.pagamento_entity import Pagamento
import uuid

class PagamentoModel(Base):
    __tablename__ = "pagamentos"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    executionId = Column(String, ForeignKey("execucoes.id"), nullable=False)
    producerName = Column(String, nullable=False)
    serviceName = Column(String, nullable=False)
    dueDate = Column(Date, nullable=False)
    paymentDate = Column(Date, nullable=True)
    amount = Column(Float, nullable=False)
    status = Column(String, default="Pendente")

    def to_entity(self) -> Pagamento:
        return Pagamento(
            id=self.id,
            executionId=self.executionId,
            producerName=self.producerName,
            serviceName=self.serviceName,
            dueDate=self.dueDate,
            amount=self.amount,
            status=self.status,
            paymentDate=self.paymentDate
        )
