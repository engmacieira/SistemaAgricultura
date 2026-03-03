from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.infrastructure.repositories.usuario_repository import UsuarioRepository
from app.application.use_cases.usuario_use_cases import UsuarioUseCases

router = APIRouter(prefix="/usuarios", tags=["Usuários"])

def get_use_case(db: Session = Depends(get_db)):
    return UsuarioUseCases(UsuarioRepository(db))

@router.get("/")
def listar_usuarios(uc: UsuarioUseCases = Depends(get_use_case)):
    return uc.listar_usuarios()

@router.post("/")
def criar_usuario(data: dict, uc: UsuarioUseCases = Depends(get_use_case)):
    try:
        return uc.criar_usuario(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
def login(data: dict, uc: UsuarioUseCases = Depends(get_use_case)):
    email = data.get("email")
    senha = data.get("password")
    try:
        return uc.autenticar_usuario(email, senha)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
        
@router.put("/{usuario_id}/senha")
def alterar_senha(usuario_id: str, data: dict, uc: UsuarioUseCases = Depends(get_use_case)):
    senha_atual = data.get("senha_atual")
    nova_senha = data.get("nova_senha")
    try:
        return uc.alterar_senha(usuario_id, senha_atual, nova_senha)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
