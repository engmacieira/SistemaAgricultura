from sqlalchemy import Column, String, Float, Boolean
from app.core.database import Base
from app.domain.entities.produtor_entity import Produtor
import uuid

class ProdutorModel(Base):
    __tablename__ = "produtores"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    cpfCnpj = Column(String, unique=True, nullable=False)
    property = Column(String, nullable=False)
    regiao_referencia = Column(String, nullable=True)
    telefone_contato = Column(String, nullable=True)
    apelido_produtor = Column(String, nullable=True)
    status = Column(String, default="Ativo")
    is_deleted = Column(Boolean, default=False)

    def to_entity(self) -> Produtor:
        return Produtor(
            id=self.id,
            name=self.name,
            cpfCnpj=self.cpfCnpj,
            property=self.property,
            regiao_referencia=self.regiao_referencia,
            telefone_contato=self.telefone_contato,
            apelido_produtor=self.apelido_produtor,
            status=self.status,
            is_deleted=self.is_deleted
        )
