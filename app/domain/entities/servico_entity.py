from dataclasses import dataclass
from typing import Optional

@dataclass
class Servico:
    id: str
    name: str
    description: Optional[str]
    unit: str
    basePrice: float
    active: bool
