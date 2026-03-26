from sqlalchemy import Column, String, Integer, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.domain.entities.solicitacao_entity import Solicitacao
import uuid

class SolicitacaoModel(Base):
    __tablename__ = "solicitacoes"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    producerId = Column(String, ForeignKey("produtores.id"), nullable=False)
    producerName = Column(String, nullable=False)
    data_solicitacao = Column(Date, nullable=False)
    prioridade = Column(Integer, default=1)
    status = Column(String, default="PENDENTE")
    observacoes = Column(String, nullable=True)
    is_deleted = Column(Boolean, default=False)

    # Relação 1:N com as Execuções. 
    # cascade="all, delete-orphan" garante que se a solicitação for deletada, as execuções filhas também somem (ou soft delete na aplicação).
    execucoes = relationship("ExecucaoModel", backref="solicitacao", cascade="all, delete-orphan")

    def to_entity(self) -> Solicitacao:
        return Solicitacao(
            id=self.id,
            producerId=self.producerId,
            producerName=self.producerName,
            data_solicitacao=self.data_solicitacao,
            prioridade=self.prioridade,
            status=self.status,
            observacoes=self.observacoes,
            is_deleted=self.is_deleted,
            # Se houver execuções carregadas no banco, já converte para as entidades filhas!
            execucoes=[exec.to_entity() for exec in self.execucoes] if self.execucoes else []
        )