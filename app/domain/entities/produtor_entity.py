from dataclasses import dataclass
from typing import Optional

@dataclass
class Produtor:
    id: str
    name: str
    cpfCnpj: str
    property: str
    totalArea: float
    status: str
