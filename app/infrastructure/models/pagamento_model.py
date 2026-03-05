from sqlalchemy import Column, String, Float, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.domain.entities.pagamento_entity import Pagamento, TransacaoPagamento
import uuid

class TransacaoPagamentoModel(Base):
    __tablename__ = "transacoes_pagamento"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    pagamentoId = Column(String, ForeignKey("pagamentos.id"), nullable=False)
    amount = Column(Float, nullable=False)
    date = Column(Date, nullable=False)

    def to_entity(self) -> TransacaoPagamento:
        return TransacaoPagamento(
            id=self.id,
            pagamentoId=self.pagamentoId,
            amount=self.amount,
            date=self.date
        )

class PagamentoModel(Base):
    __tablename__ = "pagamentos"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    executionId = Column(String, ForeignKey("execucoes.id"), nullable=False)
    producerName = Column(String, nullable=False)
    serviceName = Column(String, nullable=False)
    dueDate = Column(Date, nullable=False)
    paymentDate = Column(Date, nullable=True)
    amount = Column(Float, nullable=False)
    paidAmount = Column(Float, default=0.0, nullable=False)
    status = Column(String, default="Pendente")
    is_deleted = Column(Boolean, default=False)

    transactions = relationship("TransacaoPagamentoModel", backref="pagamento")

    def to_entity(self) -> Pagamento:
        return Pagamento(
            id=self.id,
            executionId=self.executionId,
            producerName=self.producerName,
            serviceName=self.serviceName,
            dueDate=self.dueDate,
            amount=self.amount,
            paidAmount=self.paidAmount,
            status=self.status,
            paymentDate=self.paymentDate,
            is_deleted=self.is_deleted
        )
