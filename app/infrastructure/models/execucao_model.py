from sqlalchemy import Column, String, Float, Date, ForeignKey, Boolean
from app.core.database import Base
from app.domain.entities.execucao_entity import Execucao
import uuid

class ExecucaoModel(Base):
    __tablename__ = "execucoes"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    solicitacaoId = Column(String, ForeignKey("solicitacoes.id"), nullable=False) # Vínculo com a Fila
    serviceId = Column(String, ForeignKey("servicos.id"), nullable=False)
    serviceName = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    quantity = Column(Float, nullable=False)
    unit = Column(String, nullable=False)
    valor_unitario = Column(Float, nullable=False) # Preço no dia do serviço
    totalValue = Column(Float, nullable=False)
    status = Column(String, default="REGISTRADA")
    operador_maquina = Column(String, nullable=True) # Quem pilotou o trator
    is_deleted = Column(Boolean, default=False)

    def to_entity(self) -> Execucao:
        return Execucao(
            id=self.id,
            solicitacaoId=self.solicitacaoId,
            serviceId=self.serviceId,
            serviceName=self.serviceName,
            date=self.date,
            quantity=self.quantity,
            unit=self.unit,
            valor_unitario=self.valor_unitario,
            totalValue=self.totalValue,
            status=self.status,
            operador_maquina=self.operador_maquina,
            is_deleted=self.is_deleted
        )