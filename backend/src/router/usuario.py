from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from src.controller import usuario as controller
from src.database.dependencies import get_db
from src.schema import UsuarioCreate, UsuarioResponse

router = APIRouter(prefix="/usuarios", tags=["Usuários"])

@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def criar_usuario(dados: UsuarioCreate, db: Session = Depends(get_db)):
  return controller.criar(db, dados)