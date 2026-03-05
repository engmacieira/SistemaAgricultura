from sqlalchemy import Column, String, Boolean
from app.core.database import Base
from app.domain.entities.usuario_entity import Usuario
import uuid

class UsuarioModel(Base):
    __tablename__ = "usuarios"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    role = Column(String, default="user")
    password_hash = Column(String, nullable=False)
    is_deleted = Column(Boolean, default=False)

    def to_entity(self) -> Usuario:
        return Usuario(
            id=self.id,
            name=self.name,
            email=self.email,
            role=self.role,
            password_hash=self.password_hash,
            is_deleted=self.is_deleted
        )
