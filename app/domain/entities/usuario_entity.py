from dataclasses import dataclass

@dataclass
class Usuario:
    id: str
    name: str
    email: str
    role: str
    password_hash: str
