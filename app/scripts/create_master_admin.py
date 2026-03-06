import sys
import os
import uuid

# Adiciona o diretório raiz ao path para permitir importações do módulo app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.core.database import SessionLocal
from app.core.security import get_password_hash
from app.infrastructure.models.usuario_model import UsuarioModel

def create_master_admin():
    """
    Cria automaticamente um usuário administrador master predefinido no banco de dados.
    
    Este script não requer interação do usuário e é ideal para o processo de 
    deploy inicial (bootstrap) do sistema, garantindo que sempre exista um
    acesso administrativo padrão.
    """
    print("--- Inicializando Seed de Usuário Administrador Master ---")
    
    # Credenciais Hardcoded do Master
    name = "Administrador"
    email = "admin@sunnytech.com"
    password = "Azulceleste#123"

    db = SessionLocal()
    try:
        # Verifica se o e-mail já existe para evitar duplicações de seed
        existing_user = db.query(UsuarioModel).filter(UsuarioModel.email == email).first()
        if existing_user:
            print(f"⚠️ Aviso: O usuário master com e-mail '{email}' já existe no banco de dados.")
            return

        # Criação da Entidade
        new_user = UsuarioModel(
            id=str(uuid.uuid4()),
            name=name,
            email=email,
            role="admin",
            password_hash=get_password_hash(password)
        )

        db.add(new_user)
        db.commit()
        
        print(f"✅ Sucesso! Usuário master '{name}' criado com sucesso.")
        print(f"🔑 E-mail de Acesso: {email}")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Erro crítico ao tentar salvar o usuário master: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_master_admin()