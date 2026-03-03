from typing import List, Dict, Any

class ExecucaoUseCases:
    def __init__(self, execucao_repository, pagamento_repository=None):
        self.execucao_repository = execucao_repository
        self.pagamento_repository = pagamento_repository

    def listar_execucoes(self) -> List[Any]:
        return self.execucao_repository.get_all()

    def obter_execucao(self, execucao_id: str) -> Any:
        execucao = self.execucao_repository.get_by_id(execucao_id)
        if not execucao:
            raise ValueError("Execução não encontrada")
        return execucao

    def criar_execucao(self, data: Dict[str, Any]) -> Any:
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
        
        return nova_execucao

    def atualizar_execucao(self, execucao_id: str, data: Dict[str, Any]) -> Any:
        self.obter_execucao(execucao_id)
        return self.execucao_repository.update(execucao_id, data)

    def deletar_execucao(self, execucao_id: str) -> bool:
        self.obter_execucao(execucao_id)
        # Regra de negócio: Excluir pagamentos atrelados ou impedir exclusão se já estiver pago
        return self.execucao_repository.delete(execucao_id)
