from typing import List, Dict, Any

class ServicoUseCases:
    def __init__(self, servico_repository, log_use_cases=None):
        self.servico_repository = servico_repository
        self.log_use_cases = log_use_cases

    def listar_servicos(self, skip: int = 0, limit: int = 10, sort_by: str = "name", order: str = "asc") -> Dict[str, Any]:
        items = self.servico_repository.get_all_paginated(skip, limit, sort_by, order)
        total = self.servico_repository.count_active()
        return {
            "items": items, 
            "total": total,
            "page": (skip // limit) + 1 if limit > 0 else 1,
            "size": limit,
            "pages": (total + limit - 1) // limit if limit > 0 else 1
        }

    def obter_servico(self, servico_id: str) -> Any:
        servico = self.servico_repository.get_by_id(servico_id)
        if not servico:
            raise ValueError("Serviço não encontrado")
        return servico

    def criar_servico(self, data: Dict[str, Any], usuario_logado: dict = None) -> Any:
        # Regra de negócio: Validar se o nome do serviço já existe
        # if self.servico_repository.get_by_name(data.get("name")):
        #     raise ValueError("Já existe um serviço cadastrado com este nome")
            
        novo_servico = self.servico_repository.create(data)
        
        # Integração com Logs
        if self.log_use_cases and usuario_logado:
            import json
            def to_dict(obj):
                if hasattr(obj, 'model_dump'):
                    return obj.model_dump()
                if hasattr(obj, '__dict__'):
                    d = obj.__dict__.copy()
                    d.pop('_sa_instance_state', None)
                    return d
                return obj
            self.log_use_cases.registrar_acao(
                user_id=usuario_logado.get("id"),
                user_name=usuario_logado.get("name"),
                action="CRIAR",
                entity="Serviço",
                details=f"Criou o serviço '{data.get('name')}'",
                dados_anteriores=None,
                dados_novos=json.dumps(to_dict(novo_servico), default=str)
            )
            
        return novo_servico

    def atualizar_servico(self, servico_id: str, data: Dict[str, Any], usuario_logado: dict = None) -> Any:
        servico_atual = self.obter_servico(servico_id)
        servico_atualizado = self.servico_repository.update(servico_id, data)
        
        # Integração com Logs
        if self.log_use_cases and usuario_logado:
            import json
            def to_dict(obj):
                if hasattr(obj, 'model_dump'):
                    return obj.model_dump()
                if hasattr(obj, '__dict__'):
                    d = obj.__dict__.copy()
                    d.pop('_sa_instance_state', None)
                    return d
                return obj
            self.log_use_cases.registrar_acao(
                user_id=usuario_logado.get("id"),
                user_name=usuario_logado.get("name"),
                action="EDITAR",
                entity="Serviço",
                details=f"Atualizou o serviço '{servico_atual.name}'",
                dados_anteriores=json.dumps(to_dict(servico_atual), default=str),
                dados_novos=json.dumps(to_dict(servico_atualizado), default=str)
            )
            
        return servico_atualizado

    def deletar_servico(self, servico_id: str, usuario_logado: dict = None) -> bool:
        servico_atual = self.obter_servico(servico_id)
        
        # Regra de negócio: verificar se o serviço já foi utilizado em alguma execução
        # if self.servico_repository.has_execucoes(servico_id):
        #     raise ValueError("Não é possível excluir um serviço que já possui execuções vinculadas. Considere inativá-lo.")
            
        sucesso = self.servico_repository.delete(servico_id)
        
        # Integração com Logs
        if sucesso and self.log_use_cases and usuario_logado:
            import json
            def to_dict(obj):
                if hasattr(obj, 'model_dump'):
                    return obj.model_dump()
                if hasattr(obj, '__dict__'):
                    d = obj.__dict__.copy()
                    d.pop('_sa_instance_state', None)
                    return d
                return obj
            self.log_use_cases.registrar_acao(
                user_id=usuario_logado.get("id"),
                user_name=usuario_logado.get("name"),
                action="EXCLUIR",
                entity="Serviço",
                details=f"Excluiu o serviço '{servico_atual.name}'",
                dados_anteriores=json.dumps(to_dict(servico_atual), default=str),
                dados_novos=None
            )
            
        return sucesso
