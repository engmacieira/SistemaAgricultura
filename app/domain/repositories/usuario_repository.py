from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from ..entities.usuario_entity import Usuario

class IUsuarioRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Usuario]:
        pass

    @abstractmethod
    def get_by_id(self, id: str) -> Optional[Usuario]:
        pass

    @abstractmethod
    def create(self, data: Dict[str, Any]) -> Usuario:
        pass

    @abstractmethod
    def update(self, id: str, data: Dict[str, Any]) -> Optional[Usuario]:
        pass

    @abstractmethod
    def delete(self, id: str) -> bool:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[Usuario]:
        pass
