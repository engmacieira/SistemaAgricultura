from typing import List, Dict, Any

class ExecucaoUseCases:
    def __init__(self, execucao_repository, pagamento_repository=None, log_use_cases=None):
        self.execucao_repository = execucao_repository
        self.pagamento_repository = pagamento_repository
        self.log_use_cases = log_use_cases

    def listar_execucoes(self, skip: int = 0, limit: int = 10, sort_by: str = "date", order: str = "desc", show_completed: bool = False) -> List[Any]:
        return self.execucao_repository.get_all_paginated(skip, limit, sort_by, order, show_completed)

    def contar_execucoes(self, show_completed: bool = False) -> int:
        return self.execucao_repository.count_filtered(show_completed)

    def obter_execucao(self, execucao_id: str) -> Any:
        execucao = self.execucao_repository.get_by_id(execucao_id)
        if not execucao:
            raise ValueError("Execução não encontrada")
        return execucao

    def criar_execucao(self, data: Dict[str, Any], usuario_logado: dict = None) -> Any:
        nova_execucao = self.execucao_repository.create(data)
        
        # Regra de negócio: Gerar o pagamento automaticamente se houver repositório
        if self.pagamento_repository:
            from datetime import date, timedelta
            pagamento_data = {
                "executionId": nova_execucao.id,
                "producerName": nova_execucao.producerName,
                "serviceName": nova_execucao.serviceName,
                "amount": nova_execucao.totalValue,
                "dueDate": date.today() + timedelta(days=30),
                "status": "Pendente"
            }
            self.pagamento_repository.create(pagamento_data)
        
        if self.log_use_cases and usuario_logado:
            import json
            def to_dict(obj):
                if hasattr(obj, 'model_dump'): return obj.model_dump()
                if hasattr(obj, '__dict__'):
                    d = obj.__dict__.copy()
                    d.pop('_sa_instance_state', None)
                    return d
                return obj
            self.log_use_cases.registrar_acao(
                user_id=usuario_logado["id"],
                user_name=usuario_logado["name"],
                action="CRIAR",
                entity="Execução",
                details=f"Agendou a execução do serviço '{nova_execucao.serviceName}' para '{nova_execucao.producerName}'",
                dados_anteriores=None,
                dados_novos=json.dumps(to_dict(nova_execucao), default=str)
            )

        return nova_execucao

    def atualizar_execucao(self, execucao_id: str, data: Dict[str, Any], usuario_logado: dict = None) -> Any:
        execucao_antiga = self.obter_execucao(execucao_id)
        
        import json
        def to_dict(obj):
            if hasattr(obj, 'model_dump'): return obj.model_dump()
            if hasattr(obj, '__dict__'):
                d = obj.__dict__.copy()
                d.pop('_sa_instance_state', None)
                return d
            return obj
            
        dados_antigos_dict = to_dict(execucao_antiga)
        execucao_atualizada = self.execucao_repository.update(execucao_id, data)
        
        if self.log_use_cases and usuario_logado:
            self.log_use_cases.registrar_acao(
                user_id=usuario_logado["id"],
                user_name=usuario_logado["name"],
                action="EDITAR",
                entity="Execução",
                details=f"Atualizou a execução {execucao_id} do serviço '{execucao_atualizada.serviceName}'",
                dados_anteriores=json.dumps(dados_antigos_dict, default=str),
                dados_novos=json.dumps(to_dict(execucao_atualizada), default=str)
            )

        return execucao_atualizada

    def deletar_execucao(self, execucao_id: str, usuario_logado: dict = None) -> bool:
        execucao_antiga = self.obter_execucao(execucao_id)
        
        import json
        def to_dict(obj):
            if hasattr(obj, 'model_dump'): return obj.model_dump()
            if hasattr(obj, '__dict__'):
                d = obj.__dict__.copy()
                d.pop('_sa_instance_state', None)
                return d
            return obj
            
        dados_antigos_dict = to_dict(execucao_antiga)
        
        # Regra de negócio: Excluir pagamentos atrelados ou impedir exclusão se já estiver pago
        sucesso = self.execucao_repository.delete(execucao_id)
        
        if sucesso and self.log_use_cases and usuario_logado:
            self.log_use_cases.registrar_acao(
                user_id=usuario_logado["id"],
                user_name=usuario_logado["name"],
                action="EXCLUIR",
                entity="Execução",
                details=f"Excluiu a execução {execucao_id} do serviço '{dados_antigos_dict.get('serviceName')}'",
                dados_anteriores=json.dumps(dados_antigos_dict, default=str),
                dados_novos=None
            )
            
        return sucesso
