from abc import ABC, abstractmethod
from typing import List, Dict, Any
from ..entities.log_entity import Log

class ILogRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Log]:
        pass

    @abstractmethod
    def create(self, data: Dict[str, Any]) -> Log:
        pass
