from typing import List, Dict, Any

class ExecucaoUseCases:
    # ✅ NOVO: Injetamos o solicitacao_repository para podermos alterar a fila de espera
    def __init__(self, execucao_repository, solicitacao_repository=None, pagamento_repository=None, log_use_cases=None):
        self.execucao_repository = execucao_repository
        self.solicitacao_repository = solicitacao_repository 
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
        # 1. Registra a execução real no banco
        nova_execucao = self.execucao_repository.create(data)
        
        # 2. ✅ REGRA DE NEGÓCIO: Se a execução foi feita, a Solicitação da fila deve ser "Concluída"
        nome_produtor = "Desconhecido"
        if self.solicitacao_repository:
            solicitacao = self.solicitacao_repository.get_by_id(nova_execucao.solicitacaoId)
            if solicitacao:
                nome_produtor = solicitacao.producerName
                if solicitacao.status != 'CONCLUIDO':
                    self.solicitacao_repository.update(solicitacao.id, {"status": "CONCLUIDO"})

        # 3. Gerar o pagamento automaticamente (Faturamento)
        if self.pagamento_repository:
            from datetime import date, timedelta
            pagamento_data = {
                "executionId": nova_execucao.id,
                "producerName": nome_produtor, # Puxamos da solicitação mãe!
                "serviceName": nova_execucao.serviceName,
                "dueDate": date.today() + timedelta(days=30),
                "amount": nova_execucao.totalValue,
                "status": "Pendente",
                "paidAmount": 0.0
            }
            self.pagamento_repository.create(pagamento_data)

        # 4. Log
        if self.log_use_cases and usuario_logado:
            import json
            self.log_use_cases.registrar_acao(
                user_id=usuario_logado["id"],
                user_name=usuario_logado["name"],
                action="CRIAR",
                entity="Execução",
                details=f"Registrou a execução do serviço '{nova_execucao.serviceName}'",
                dados_anteriores=None,
                dados_novos=json.dumps(data, default=str)
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

        if execucao_atualizada and self.log_use_cases and usuario_logado:
            self.log_use_cases.registrar_acao(
                user_id=usuario_logado["id"],
                user_name=usuario_logado["name"],
                action="ATUALIZAR",
                entity="Execução",
                details=f"Atualizou a execução do serviço '{execucao_atualizada.serviceName}'",
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