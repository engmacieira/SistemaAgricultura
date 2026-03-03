from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from ..entities.pagamento_entity import Pagamento

class IPagamentoRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Pagamento]:
        pass

    @abstractmethod
    def get_by_id(self, id: str) -> Optional[Pagamento]:
        pass

    @abstractmethod
    def create(self, data: Dict[str, Any]) -> Pagamento:
        pass

    @abstractmethod
    def update(self, id: str, data: Dict[str, Any]) -> Optional[Pagamento]:
        pass

    @abstractmethod
    def delete(self, id: str) -> bool:
        pass
