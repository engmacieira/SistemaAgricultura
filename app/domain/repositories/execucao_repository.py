from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from ..entities.execucao_entity import Execucao

class IExecucaoRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Execucao]:
        pass

    @abstractmethod
    def get_all_paginated(self, skip: int = 0, limit: int = 10, sort_by: str = "date", order: str = "desc", show_completed: bool = False) -> List[Execucao]:
        pass

    @abstractmethod
    def count_filtered(self, show_completed: bool = False) -> int:
        pass

    @abstractmethod
    def get_by_id(self, id: str) -> Optional[Execucao]:
        pass

    # ✅ NOVO MÉTODO: Buscar as filhas (execuções) de uma mãe (solicitação)
    @abstractmethod
    def get_by_solicitacao_id(self, solicitacao_id: str) -> List[Execucao]:
        pass

    @abstractmethod
    def create(self, data: Dict[str, Any]) -> Execucao:
        pass

    @abstractmethod
    def update(self, id: str, data: Dict[str, Any]) -> Optional[Execucao]:
        pass

    @abstractmethod
    def delete(self, id: str) -> bool:
        pass