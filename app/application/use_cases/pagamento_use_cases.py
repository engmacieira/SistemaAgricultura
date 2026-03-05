from typing import List, Dict, Any, Optional
from typing import List, Optional, Any
from datetime import date

class PagamentoUseCases:
    def __init__(self, pagamento_repository, log_use_cases=None):
        self.pagamento_repository = pagamento_repository
        self.log_use_cases = log_use_cases

    def listar_pagamentos(self, skip: int = 0, limit: int = 10, sort_by: str = "dueDate", order: str = "desc", search: str = "") -> List[Any]:
        return self.pagamento_repository.get_all_paginated(skip, limit, sort_by, order, search)

    def contar_pagamentos(self, search: str = "") -> int:
        return self.pagamento_repository.count_filtered(search)

    def obter_debitos_por_produtor(self, search: str = "") -> List[Dict[str, Any]]:
        return self.pagamento_repository.get_debts_by_producer(search)

    def obter_pagamento(self, pagamento_id: str) -> Any:
        pagamento = self.pagamento_repository.get_by_id(pagamento_id)
        if not pagamento:
            raise ValueError("Pagamento não encontrado")
        return pagamento

    def criar_pagamento(self, data: Dict[str, Any], usuario_logado: dict = None) -> Any:
        novo_pagamento = self.pagamento_repository.create(data)

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
                entity="Pagamento",
                details=f"Criou o pagamento para '{novo_pagamento.producerName}'",
                dados_anteriores=None,
                dados_novos=json.dumps(to_dict(novo_pagamento), default=str)
            )

        return novo_pagamento

    def atualizar_pagamento(self, pagamento_id: str, data: Dict[str, Any], usuario_logado: dict = None) -> Any:
        pagamento_antigo = self.obter_pagamento(pagamento_id)
        
        import json
        def to_dict(obj):
            if hasattr(obj, 'model_dump'): return obj.model_dump()
            if hasattr(obj, '__dict__'):
                d = obj.__dict__.copy()
                d.pop('_sa_instance_state', None)
                return d
            return obj
            
        dados_antigos_dict = to_dict(pagamento_antigo)
        pagamento_atualizado = self.pagamento_repository.update(pagamento_id, data)
        
        if self.log_use_cases and usuario_logado:
            self.log_use_cases.registrar_acao(
                user_id=usuario_logado["id"],
                user_name=usuario_logado["name"],
                action="EDITAR",
                entity="Pagamento",
                details=f"Atualizou o pagamento {pagamento_id} para '{pagamento_atualizado.producerName}'",
                dados_anteriores=json.dumps(dados_antigos_dict, default=str),
                dados_novos=json.dumps(to_dict(pagamento_atualizado), default=str)
            )
            
        return pagamento_atualizado

    def registrar_pagamento(self, pagamento_id: str, amount_to_pay: float, data_pagamento: Optional[date] = None, usuario_logado: dict = None) -> Any:
        # Caso de uso específico para a ação de 'Registrar Pagamento' do frontend
        pagamento = self.obter_pagamento(pagamento_id)
        
        import json
        def to_dict(obj):
            if hasattr(obj, 'model_dump'): return obj.model_dump()
            if hasattr(obj, '__dict__'):
                d = obj.__dict__.copy()
                d.pop('_sa_instance_state', None)
                return d
            return obj
            
        dados_antigos_dict = to_dict(pagamento)
        
        if pagamento.status == "Pago":
            raise ValueError("Este pagamento já foi realizado integralmente.")
            
        if amount_to_pay <= 0:
            raise ValueError("O valor do pagamento deve ser maior que zero.")

        # Update paid amount
        novo_valor_pago = (pagamento.paidAmount or 0.0) + amount_to_pay
        
        # Determine status
        if novo_valor_pago >= pagamento.amount:
            status = "Pago"
            if novo_valor_pago > pagamento.amount:
                # We could keep the extra, but for now let's clamp
                novo_valor_pago = pagamento.amount
        else:
            status = "Parcial"

        # Use data_pagamento if provided, otherwise use today's date
        final_data_pagamento = data_pagamento if data_pagamento is not None else date.today()

        # Record the transaction
        self.pagamento_repository.create_transaction({
            "pagamentoId": pagamento_id,
            "amount": amount_to_pay,
            "date": final_data_pagamento
        })

        dados_atualizados = {
            "status": status,
            "paidAmount": novo_valor_pago,
            "paymentDate": final_data_pagamento
        }
        pagamento_atualizado = self.pagamento_repository.update(pagamento_id, dados_atualizados)
        
        if self.log_use_cases and usuario_logado:
            self.log_use_cases.registrar_acao(
                user_id=usuario_logado["id"],
                user_name=usuario_logado["name"],
                action="EDITAR",
                entity="Pagamento",
                details=f"Registrou pagamento parcial/total para '{pagamento_atualizado.producerName}' no valor de {amount_to_pay}",
                dados_anteriores=json.dumps(dados_antigos_dict, default=str),
                dados_novos=json.dumps(to_dict(pagamento_atualizado), default=str)
            )

        return pagamento_atualizado

    def obter_historico(self, pagamento_id: str) -> List[Any]:
        return self.pagamento_repository.get_history(pagamento_id)

    def deletar_pagamento(self, pagamento_id: str, usuario_logado: dict = None) -> bool:
        pagamento_antigo = self.obter_pagamento(pagamento_id)
        
        import json
        def to_dict(obj):
            if hasattr(obj, 'model_dump'): return obj.model_dump()
            if hasattr(obj, '__dict__'):
                d = obj.__dict__.copy()
                d.pop('_sa_instance_state', None)
                return d
            return obj
            
        dados_antigos_dict = to_dict(pagamento_antigo)
        sucesso = self.pagamento_repository.delete(pagamento_id)
        
        if sucesso and self.log_use_cases and usuario_logado:
            self.log_use_cases.registrar_acao(
                user_id=usuario_logado["id"],
                user_name=usuario_logado["name"],
                action="EXCLUIR",
                entity="Pagamento",
                details=f"Excluiu o pagamento {pagamento_id} de '{dados_antigos_dict.get('producerName')}'",
                dados_anteriores=json.dumps(dados_antigos_dict, default=str),
                dados_novos=None
            )
            
        return sucesso
    def atualizar_transacao(self, transaction_id: str, data: Dict[str, Any]) -> Any:
        return self.pagamento_repository.update_transaction(transaction_id, data)

    def excluir_transacao(self, transaction_id: str) -> bool:
        return self.pagamento_repository.delete_transaction(transaction_id)
