from typing import List, Dict, Any
from datetime import datetime, timezone

class LogUseCases:
    def __init__(self, log_repository):
        self.log_repository = log_repository

    def listar_logs(self, skip: int = 0, limit: int = 10, sort_by: str = "timestamp", order: str = "desc", search: str = "") -> Dict[str, Any]:
        items = self.log_repository.get_all_paginated(skip, limit, sort_by, order, search)
        total = self.log_repository.count(search)
        import math
        return {
            "items": items,
            "total": total,
            "page": skip // limit,
            "pages": math.ceil(total / limit) if limit > 0 else 1
        }

    def registrar_acao(self, user_id: str, user_name: str, action: str, entity: str, details: str, dados_anteriores: str = None, dados_novos: str = None) -> Any:
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
            "dados_anteriores": dados_anteriores,
            "dados_novos": dados_novos,
            "timestamp": datetime.now(timezone.utc)
        }
        return self.log_repository.create(dados_log)
