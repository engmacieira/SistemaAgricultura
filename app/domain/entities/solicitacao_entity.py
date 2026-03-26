# app/domain/entities/solicitacao_entity.py
from dataclasses import dataclass, field
from datetime import date
from typing import Optional, List
from app.domain.entities.execucao_entity import Execucao # Importamos a filha

@dataclass
class Solicitacao:
    id: str
    producerId: str
    producerName: str
    data_solicitacao: date  
    prioridade: int         
    status: str             
    observacoes: Optional[str] = None
    is_deleted: bool = False
    
    # AQUI ESTÁ A MÁGICA DO DDD (Relação 1:N no Domínio)
    # Usamos field(default_factory=list) para que, ao criar uma Solicitação nova, 
    # ela nasça com uma lista vazia de execuções.
    execucoes: List[Execucao] = field(default_factory=list)