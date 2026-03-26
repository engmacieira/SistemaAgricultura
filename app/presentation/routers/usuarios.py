from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.infrastructure.repositories.usuario_repository import UsuarioRepository
from app.application.use_cases.usuario_use_cases import UsuarioUseCases
from app.core.security import create_access_token
from app.presentation.schemas.usuario_schema import UsuarioCreate, UsuarioUpdate, UsuarioResponse

from app.core.dependencies import get_current_user

router = APIRouter(prefix="/usuarios", tags=["Usuários"])

# Some endpoints like login should remain public
# We apply dependency to specific ones or at the router level but exclude login

def get_use_case(db: Session = Depends(get_db)):
    return UsuarioUseCases(UsuarioRepository(db))

@router.get("/", response_model=dict)
def listar_usuarios(
    skip: int = 0, 
    limit: int = 10, 
    sort_by: str = "name", 
    order: str = "asc",
    uc: UsuarioUseCases = Depends(get_use_case),
    current_user: dict = Depends(get_current_user)
):
    """Retorna a lista de todos os usuários do sistema com paginação e ordenação."""
    return uc.listar_usuarios(skip, limit, sort_by, order)

@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def criar_usuario(data: UsuarioCreate, uc: UsuarioUseCases = Depends(get_use_case), current_user: dict = Depends(get_current_user)):
    """Cria um novo usuário."""
    try:
        return uc.criar_usuario(data.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
def login(data: dict, uc: UsuarioUseCases = Depends(get_use_case)):
    """Realiza o login e retorna o token de acesso."""
    email = data.get("email")
    password = data.get("password")
    try:
        user_dict = uc.autenticar_usuario(email, password)
        access_token = create_access_token(data={"sub": str(user_dict["id"])})
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user_dict
        }
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
        
@router.put("/{usuario_id}/senha")
def alterar_senha(usuario_id: str, data: dict, uc: UsuarioUseCases = Depends(get_use_case)):
    """Permite um usuário alterar sua própria senha."""
    senha_atual = data.get("senha_atual")
    nova_senha = data.get("nova_senha")
    try:
        return uc.alterar_senha(usuario_id, senha_atual, nova_senha)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{usuario_id}", response_model=UsuarioResponse)
def obter_usuario(usuario_id: str, uc: UsuarioUseCases = Depends(get_use_case), current_user: dict = Depends(get_current_user)):
    """Retorna os detalhes de um usuário específico."""
    try:
        return uc.obter_usuario(usuario_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_usuario(usuario_id: str, uc: UsuarioUseCases = Depends(get_use_case), current_user: dict = Depends(get_current_user)):
    """Remove um usuário do sistema (soft delete)."""
    try:
        if not uc.deletar_usuario(usuario_id):
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# Crie esse schema simples para não vazar a senha no endpoint público
class UsuarioSelect(BaseModel):
    name: str
    email: str

# ⚠️ ATENÇÃO: Essa rota NÃO pode ter o Depends(get_current_user)
@router.get("/public/lista", response_model=List[UsuarioSelect])
def listar_usuarios_para_login(db: Session = Depends(get_db)):
    """Rota pública para alimentar o Select da tela de Login"""
    from app.infrastructure.models.usuario_model import UsuarioModel # Ajuste o import se necessário
    
    usuarios = db.query(UsuarioModel).filter(UsuarioModel.is_deleted == False).all()
    return [{"name": u.name, "email": u.email} for u in usuarios]

