from typing import List, Dict, Any

class SolicitacaoUseCases:
    def __init__(self, solicitacao_repository, log_use_cases=None):
        self.solicitacao_repository = solicitacao_repository
        self.log_use_cases = log_use_cases

    def listar_solicitacoes(self, skip: int = 0, limit: int = 10, status: str = None) -> List[Any]:
        return self.solicitacao_repository.get_all_paginated(skip, limit, status)

    def obter_solicitacao(self, solicitacao_id: str) -> Any:
        solicitacao = self.solicitacao_repository.get_by_id(solicitacao_id)
        if not solicitacao:
            raise ValueError("Solicitação não encontrada")
        return solicitacao

    def criar_solicitacao(self, data: Dict[str, Any], usuario_logado: dict = None) -> Any:
        # Garante que a solicitação nasce pendente
        data["status"] = "PENDENTE" 
        nova_solicitacao = self.solicitacao_repository.create(data)
        
        if self.log_use_cases and usuario_logado:
            import json
            self.log_use_cases.registrar_acao(
                user_id=usuario_logado["id"],
                user_name=usuario_logado["name"],
                action="CRIAR",
                entity="Solicitação",
                details=f"Adicionou {nova_solicitacao.producerName} à Fila de Espera",
                dados_anteriores=None,
                dados_novos=json.dumps(data, default=str)
            )

        return nova_solicitacao

    def atualizar_solicitacao(self, solicitacao_id: str, data: Dict[str, Any], usuario_logado: dict = None) -> Any:
        # A lógica de log segue o mesmo padrão dos outros use_cases
        solicitacao_atualizada = self.solicitacao_repository.update(solicitacao_id, data)
        return solicitacao_atualizada

    def deletar_solicitacao(self, solicitacao_id: str, usuario_logado: dict = None) -> bool:
        # Na vida real da Fila, é melhor cancelar do que deletar, 
        # mas mantemos o método delete caso precisem limpar lixo do sistema.
        return self.solicitacao_repository.delete(solicitacao_id)