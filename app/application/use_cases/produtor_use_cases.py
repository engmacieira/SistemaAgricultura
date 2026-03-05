from typing import List, Dict, Any

class ProdutorUseCases:
    def __init__(self, produtor_repository, log_use_cases=None):
        self.produtor_repository = produtor_repository
        self.log_use_cases = log_use_cases

    def listar_produtores(self, page: int = 1, size: int = 10, sort_by: str = "name", order: str = "asc") -> Dict[str, Any]:
        skip = (page - 1) * size
        items = self.produtor_repository.get_all_paginated(skip=skip, limit=size, sort_by=sort_by, order=order)
        total = self.produtor_repository.count_active()
        pages = (total + size - 1) // size
        
        return {
            "items": items,
            "total": total,
            "page": page,
            "size": size,
            "pages": pages
        }

    def obter_produtor(self, produtor_id: str) -> Any:
        produtor = self.produtor_repository.get_by_id(produtor_id)
        if not produtor:
            raise ValueError("Produtor não encontrado")
        return produtor

    def criar_produtor(self, data: Dict[str, Any], usuario_logado: dict = None) -> Any:
        # Regra de negócio: Validar se CPF/CNPJ já existe no banco
        existente = self.produtor_repository.get_model_by_cpf_cnpj(data.get("cpfCnpj"))
        
        if existente:
            if not existente.is_deleted:
                raise ValueError("Este CPF/CNPJ já está cadastrado para outro produtor.")
            
            # Reativar produtor que foi excluído
            produtor_id = existente.id
            data["is_deleted"] = False
            novo_produtor = self.produtor_repository.update(produtor_id, data)
        else:
            novo_produtor = self.produtor_repository.create(data)
        
        # Integração com Logs: Registrar a ação de criação
        if self.log_use_cases and usuario_logado:
            import json
            # Helper function to convert mapped objects to dict
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
                entity="Produtor",
                details=f"Criou o produtor '{data.get('name')}'",
                dados_anteriores=None,
                dados_novos=json.dumps(to_dict(novo_produtor), default=str)
            )
            
        return novo_produtor

    def atualizar_produtor(self, produtor_id: str, data: Dict[str, Any], usuario_logado: dict = None) -> Any:
        produtor_atual = self.obter_produtor(produtor_id)
        produtor_atualizado = self.produtor_repository.update(produtor_id, data)
        
        # Integração com Logs: Registrar a ação de edição
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
                entity="Produtor",
                details=f"Atualizou os dados do produtor '{produtor_atual.name}'",
                dados_anteriores=json.dumps(to_dict(produtor_atual), default=str),
                dados_novos=json.dumps(to_dict(produtor_atualizado), default=str)
            )
            
        return produtor_atualizado

    def deletar_produtor(self, produtor_id: str, usuario_logado: dict = None) -> bool:
        produtor_atual = self.obter_produtor(produtor_id)
        
        # Regra de negócio: verificar se o produtor tem execuções pendentes antes de excluir
        # if self.produtor_repository.has_execucoes(produtor_id):
        #     raise ValueError("Não é possível excluir um produtor com execuções vinculadas")
            
        sucesso = self.produtor_repository.delete(produtor_id)
        
        # Integração com Logs: Registrar a ação de exclusão
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
                entity="Produtor",
                details=f"Excluiu o produtor '{produtor_atual.name}'",
                dados_anteriores=json.dumps(to_dict(produtor_atual), default=str),
                dados_novos=None
            )
            
        return sucesso
