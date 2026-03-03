from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class Configuracao:
    id: str
    chave: str
    valor: Dict[str, Any]
