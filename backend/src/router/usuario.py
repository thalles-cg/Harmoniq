from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.controller import usuario as controller
from src.database.dependencies import get_db, obter_usuario_id
from src.schema import UsuarioCreate, UsuarioResponse

router = APIRouter(prefix="/usuarios", tags=["Usuários"])

@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def criar_usuario(dados: UsuarioCreate, db: Session = Depends(get_db)):
  return controller.criar(db, dados)

@router.get("/me", response_model=UsuarioResponse)
def obter_usuario_atual(usuario_id: int = Depends(obter_usuario_id), db: Session = Depends(get_db),):
  usuario = controller.buscar_por_id(db, usuario_id)

  if usuario is None:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="Usuário não encontrado",
    )

  return usuario