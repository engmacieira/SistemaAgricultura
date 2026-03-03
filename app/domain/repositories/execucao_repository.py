from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from ..entities.execucao_entity import Execucao

class IExecucaoRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Execucao]:
        pass

    @abstractmethod
    def get_by_id(self, id: str) -> Optional[Execucao]:
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
