from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from ..entities.servico_entity import Servico

class IServicoRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Servico]:
        pass

    @abstractmethod
    def get_by_id(self, id: str) -> Optional[Servico]:
        pass

    @abstractmethod
    def create(self, data: Dict[str, Any]) -> Servico:
        pass

    @abstractmethod
    def update(self, id: str, data: Dict[str, Any]) -> Optional[Servico]:
        pass

    @abstractmethod
    def delete(self, id: str) -> bool:
        pass

    @abstractmethod
    def get_by_name(self, name: str) -> Optional[Servico]:
        pass

    @abstractmethod
    def has_execucoes(self, servico_id: str) -> bool:
        pass
