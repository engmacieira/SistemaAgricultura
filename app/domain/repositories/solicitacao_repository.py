from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from ..entities.solicitacao_entity import Solicitacao

class ISolicitacaoRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Solicitacao]:
        pass

    @abstractmethod
    def get_all_paginated(self, skip: int = 0, limit: int = 10, status: Optional[str] = None) -> List[Solicitacao]:
        """Busca a fila de espera, podendo filtrar por status (ex: PENDENTE)"""
        pass

    @abstractmethod
    def get_by_id(self, id: str) -> Optional[Solicitacao]:
        """Deve trazer a Solicitação já com a lista de Execuções embutida"""
        pass

    @abstractmethod
    def create(self, data: Dict[str, Any]) -> Solicitacao:
        pass

    @abstractmethod
    def update(self, id: str, data: Dict[str, Any]) -> Optional[Solicitacao]:
        pass

    @abstractmethod
    def delete(self, id: str) -> bool:
        pass