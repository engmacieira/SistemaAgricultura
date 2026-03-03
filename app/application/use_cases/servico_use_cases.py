from typing import List, Dict, Any

class ServicoUseCases:
    def __init__(self, servico_repository, log_use_cases=None):
        self.servico_repository = servico_repository
        self.log_use_cases = log_use_cases

    def listar_servicos(self) -> List[Any]:
        return self.servico_repository.get_all()

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
            self.log_use_cases.registrar_acao(
                user_id=usuario_logado.get("id"),
                user_name=usuario_logado.get("name"),
                action="CRIAR",
                entity="Serviço",
                details=f"Criou o serviço '{data.get('name')}'"
            )
            
        return novo_servico

    def atualizar_servico(self, servico_id: str, data: Dict[str, Any], usuario_logado: dict = None) -> Any:
        servico_atual = self.obter_servico(servico_id)
        servico_atualizado = self.servico_repository.update(servico_id, data)
        
        # Integração com Logs
        if self.log_use_cases and usuario_logado:
            self.log_use_cases.registrar_acao(
                user_id=usuario_logado.get("id"),
                user_name=usuario_logado.get("name"),
                action="EDITAR",
                entity="Serviço",
                details=f"Atualizou o serviço '{servico_atual.name}'"
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
            self.log_use_cases.registrar_acao(
                user_id=usuario_logado.get("id"),
                user_name=usuario_logado.get("name"),
                action="EXCLUIR",
                entity="Serviço",
                details=f"Excluiu o serviço '{servico_atual.name}'"
            )
            
        return sucesso
