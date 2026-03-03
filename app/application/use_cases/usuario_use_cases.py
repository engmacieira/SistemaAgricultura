from typing import List, Dict, Any

class UsuarioUseCases:
    def __init__(self, usuario_repository, hasher_service=None):
        self.usuario_repository = usuario_repository
        self.hasher_service = hasher_service # Serviço para hash de senhas (ex: bcrypt)

    def autenticar_usuario(self, email: str, senha_plana: str) -> Any:
        usuario = self.usuario_repository.get_by_email(email)
        if not usuario:
            raise ValueError("Credenciais inválidas")
            
        # if not self.hasher_service.verify(senha_plana, usuario.password_hash):
        #     raise ValueError("Credenciais inválidas")
            
        return usuario

    def listar_usuarios(self) -> List[Any]:
        return self.usuario_repository.get_all()

    def obter_usuario(self, usuario_id: str) -> Any:
        usuario = self.usuario_repository.get_by_id(usuario_id)
        if not usuario:
            raise ValueError("Usuário não encontrado")
        return usuario

    def criar_usuario(self, data: Dict[str, Any]) -> Any:
        # Verificar se email já existe
        if self.usuario_repository.get_by_email(data.get("email")):
            raise ValueError("Email já cadastrado")
            
        # Hash da senha antes de salvar
        # data["password"] = self.hasher_service.hash(data["password"])
        
        return self.usuario_repository.create(data)

    def atualizar_usuario(self, usuario_id: str, data: Dict[str, Any]) -> Any:
        self.obter_usuario(usuario_id)
        return self.usuario_repository.update(usuario_id, data)

    def alterar_senha(self, usuario_id: str, senha_atual: str, nova_senha: str) -> bool:
        """Caso de uso específico para a tela de Perfil do usuário"""
        usuario = self.obter_usuario(usuario_id)
        
        # Verificar senha atual
        # if not self.hasher_service.verify(senha_atual, usuario.password_hash):
        #     raise ValueError("Senha atual incorreta")
            
        # nova_senha_hash = self.hasher_service.hash(nova_senha)
        # return self.usuario_repository.update(usuario_id, {"password": nova_senha_hash})
        return True

    def deletar_usuario(self, usuario_id: str) -> bool:
        self.obter_usuario(usuario_id)
        # Regra: Não permitir excluir o último administrador do sistema
        return self.usuario_repository.delete(usuario_id)
