from typing import List, Dict, Any
from app.core.security import verify_password, get_password_hash

class UsuarioUseCases:
    def __init__(self, usuario_repository, hasher_service=None):
        self.usuario_repository = usuario_repository
        self.hasher_service = hasher_service # Serviço para hash de senhas (ex: bcrypt)

    def autenticar_usuario(self, email: str, password: str) -> Any:
        usuario = self.usuario_repository.get_by_email(email)
        if not usuario:
            raise ValueError("Credenciais inválidas")
            
        if not verify_password(password, usuario.password_hash):
            raise ValueError("Credenciais inválidas")
            
        # Converter para dicionário e remover campos sensíveis
        usuario_dict = {
            "id": usuario.id,
            "name": usuario.name,
            "email": usuario.email,
            "role": usuario.role
        }
        return usuario_dict

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
        
        if "password" in data:
            data["password_hash"] = get_password_hash(data.pop("password"))
        
        return self.usuario_repository.create(data)

    def atualizar_usuario(self, usuario_id: str, data: Dict[str, Any]) -> Any:
        self.obter_usuario(usuario_id)
        return self.usuario_repository.update(usuario_id, data)

    def alterar_senha(self, usuario_id: str, senha_atual: str, nova_senha: str) -> bool:
        """Caso de uso específico para a tela de Perfil do usuário"""
        usuario = self.obter_usuario(usuario_id)
        
        # Verificar senha atual
        if not verify_password(senha_atual, usuario.password_hash):
            raise ValueError("Senha atual incorreta")
            
        nova_senha_hash = get_password_hash(nova_senha)
        return self.usuario_repository.update(usuario_id, {"password_hash": nova_senha_hash})

    def deletar_usuario(self, usuario_id: str) -> bool:
        self.obter_usuario(usuario_id)
        # Regra: Não permitir excluir o último administrador do sistema
        return self.usuario_repository.delete(usuario_id)
