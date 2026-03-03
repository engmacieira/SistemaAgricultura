from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from ..entities.produtor_entity import Produtor

class IProdutorRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Produtor]:
        pass

    @abstractmethod
    def get_by_id(self, id: str) -> Optional[Produtor]:
        pass

    @abstractmethod
    def create(self, data: Dict[str, Any]) -> Produtor:
        pass

    @abstractmethod
    def update(self, id: str, data: Dict[str, Any]) -> Optional[Produtor]:
        pass

    @abstractmethod
    def delete(self, id: str) -> bool:
        pass

    @abstractmethod
    def get_by_cpf_cnpj(self, cpf_cnpj: str) -> Optional[Produtor]:
        pass

    @abstractmethod
    def has_execucoes(self, produtor_id: str) -> bool:
        pass
