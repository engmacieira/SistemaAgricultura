import getpass
import sys
import os
import uuid

# Adiciona o diretório raiz ao path para permitir importações do módulo app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.core.database import SessionLocal
from app.core.security import get_password_hash
from app.infrastructure.models.usuario_model import UsuarioModel

def create_admin():
    print("--- Criação de Usuário Administrador Inicial ---")
    
    name = input("Nome Completo: ").strip()
    email = input("E-mail: ").strip()
    
    if not name or not email:
        print("Erro: Nome e e-mail são obrigatórios.")
        return

    password = getpass.getpass("Senha: ")
    confirm_password = getpass.getpass("Confirme a Senha: ")

    if password != confirm_password:
        print("Erro: As senhas não coincidem.")
        return

    if len(password) < 6:
        print("Erro: A senha deve ter pelo menos 6 caracteres.")
        return

    db = SessionLocal()
    try:
        # Verifica se o e-mail já existe
        existing_user = db.query(UsuarioModel).filter(UsuarioModel.email == email).first()
        if existing_user:
            print(f"Erro: O e-mail '{email}' já está em uso.")
            return

        new_user = UsuarioModel(
            id=str(uuid.uuid4()),
            name=name,
            email=email,
            role="admin",
            password_hash=get_password_hash(password)
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        print(f"\nSucesso! Usuário administrador '{name}' criado com sucesso.")
        print(f"ID do Usuário: {new_user.id}")

    except Exception as e:
        db.rollback()
        print(f"Erro inesperado ao criar usuário: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_admin()
