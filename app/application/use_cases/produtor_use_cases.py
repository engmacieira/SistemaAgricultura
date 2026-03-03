from typing import List, Dict, Any

class ProdutorUseCases:
    def __init__(self, produtor_repository, log_use_cases=None):
        self.produtor_repository = produtor_repository
        self.log_use_cases = log_use_cases

    def listar_produtores(self) -> List[Any]:
        return self.produtor_repository.get_all()

    def obter_produtor(self, produtor_id: str) -> Any:
        produtor = self.produtor_repository.get_by_id(produtor_id)
        if not produtor:
            raise ValueError("Produtor não encontrado")
        return produtor

    def criar_produtor(self, data: Dict[str, Any], usuario_logado: dict = None) -> Any:
        # Regra de negócio: Validar se CPF/CNPJ já existe no banco
        # if self.produtor_repository.get_by_cpf_cnpj(data.get("cpfCnpj")):
        #     raise ValueError("CPF/CNPJ já cadastrado para outro produtor")
            
        novo_produtor = self.produtor_repository.create(data)
        
        # Integração com Logs: Registrar a ação de criação
        if self.log_use_cases and usuario_logado:
            self.log_use_cases.registrar_acao(
                user_id=usuario_logado.get("id"),
                user_name=usuario_logado.get("name"),
                action="CRIAR",
                entity="Produtor",
                details=f"Criou o produtor '{data.get('name')}'"
            )
            
        return novo_produtor

    def atualizar_produtor(self, produtor_id: str, data: Dict[str, Any], usuario_logado: dict = None) -> Any:
        produtor_atual = self.obter_produtor(produtor_id)
        produtor_atualizado = self.produtor_repository.update(produtor_id, data)
        
        # Integração com Logs: Registrar a ação de edição
        if self.log_use_cases and usuario_logado:
            self.log_use_cases.registrar_acao(
                user_id=usuario_logado.get("id"),
                user_name=usuario_logado.get("name"),
                action="EDITAR",
                entity="Produtor",
                details=f"Atualizou os dados do produtor '{produtor_atual.name}'"
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
            self.log_use_cases.registrar_acao(
                user_id=usuario_logado.get("id"),
                user_name=usuario_logado.get("name"),
                action="EXCLUIR",
                entity="Produtor",
                details=f"Excluiu o produtor '{produtor_atual.name}'"
            )
            
        return sucesso
