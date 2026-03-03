from abc import ABC, abstractmethod
from typing import Dict, Any
from app.domain.entities.administrador_entity import Configuracao

class IAdministradorRepository(ABC):
    @abstractmethod
    def get_configuracoes(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    def update_configuracoes(self, data: Dict[str, Any]) -> Dict[str, Any]:
        pass
