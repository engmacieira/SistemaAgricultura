from fastapi import APIRouter, HTTPException, status
from typing import List
from ..schemas.usuario_schema import UsuarioCreate, UsuarioUpdate, UsuarioResponse

router = APIRouter(prefix="/usuarios", tags=["Usuários"])

@router.get("/", response_model=List[UsuarioResponse])
def listar_usuarios():
    """Retorna a lista de todos os usuários do sistema."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Ainda não implementado")

@router.get("/{usuario_id}", response_model=UsuarioResponse)
def obter_usuario(usuario_id: str):
    """Retorna os detalhes de um usuário específico."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Ainda não implementado")

@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def criar_usuario(usuario: UsuarioCreate):
    """Cria um novo usuário."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Ainda não implementado")

@router.put("/{usuario_id}", response_model=UsuarioResponse)
def atualizar_usuario(usuario_id: str, usuario: UsuarioUpdate):
    """Atualiza os dados de um usuário existente."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Ainda não implementado")

@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_usuario(usuario_id: str):
    """Remove um usuário do sistema."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Ainda não implementado")
