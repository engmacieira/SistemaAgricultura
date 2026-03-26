from pydantic import BaseModel, ConfigDict
from typing import Optional, List
import datetime
from .execucao_schema import ExecucaoResponse # Importamos a filha para exibir junto!

class SolicitacaoBase(BaseModel):
    producerId: str
    producerName: str
    data_solicitacao: datetime.date
    prioridade: int = 1
    status: str = "PENDENTE"
    observacoes: Optional[str] = None

class SolicitacaoCreate(BaseModel):
    producerId: str
    producerName: str
    data_solicitacao: datetime.date
    prioridade: Optional[int] = 1
    observacoes: Optional[str] = None

class SolicitacaoUpdate(BaseModel):
    prioridade: Optional[int] = None
    status: Optional[str] = None
    observacoes: Optional[str] = None

class SolicitacaoResponse(SolicitacaoBase):
    id: str
    # O SQLAlchemy trará as execuções filhas, e o Pydantic vai convertê-las para nós!
    execucoes: List[ExecucaoResponse] = []

    model_config = ConfigDict(from_attributes=True)