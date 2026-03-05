from dataclasses import dataclass
from typing import Optional

@dataclass
class Produtor:
    id: str
    name: str
    cpfCnpj: str
    property: str
    regiao_referencia: str
    telefone_contato: str
    apelido_produtor: str
    status: str
    is_deleted: bool = False
