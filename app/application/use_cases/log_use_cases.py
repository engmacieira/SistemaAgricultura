from typing import List, Dict, Any
from datetime import datetime

class LogUseCases:
    def __init__(self, log_repository):
        self.log_repository = log_repository

    def listar_logs(self) -> List[Any]:
        return self.log_repository.get_all()

    def registrar_acao(self, user_id: str, user_name: str, action: str, entity: str, details: str) -> Any:
        """
        Caso de uso para registrar qualquer ação no sistema.
        Deve ser chamado por outros Use Cases (ex: ao criar um produtor, chama registrar_acao)
        """
        dados_log = {
            "userId": user_id,
            "userName": user_name,
            "action": action,
            "entity": entity,
            "details": details,
            "timestamp": datetime.utcnow()
        }
        return self.log_repository.create(dados_log)
