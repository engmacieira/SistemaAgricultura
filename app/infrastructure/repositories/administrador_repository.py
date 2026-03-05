from sqlalchemy.orm import Session
from .base_repository import BaseRepository
from ..models.administrador_model import ConfiguracaoModel
from app.domain.entities.administrador_entity import Configuracao

class AdministradorRepository(BaseRepository[ConfiguracaoModel, Configuracao]):
    def __init__(self, db: Session):
        super().__init__(db, ConfiguracaoModel)

    def get_configuracoes(self):
        config = self.db.query(self.model).filter(self.model.chave == "geral").first()
        return config.valor if config else {"unidades_medida": []}

    def update_configuracoes(self, data: dict):
        config = self.db.query(self.model).filter(self.model.chave == "geral").first()
        if config:
            config.valor = data
            self.db.commit()
            self.db.refresh(config)
            return config.valor
        else:
            nova_config = self.model(chave="geral", valor=data)
            self.db.add(nova_config)
            self.db.commit()
            self.db.refresh(nova_config)
            return nova_config.valor
