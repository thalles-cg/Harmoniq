from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.controller import autenticacao as controller
from src.database.dependencies import get_db
from src.schema import LoginRequest

router = APIRouter(prefix="/auth", tags=["Autenticação"])

@router.post("/login")
def login(dados: LoginRequest, db: Session = Depends(get_db)):
  resultado = controller.autenticar(
    db,
    dados.email,
    dados.senha
  )

  if resultado is None:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="E-mail ou senha inválidos"
    )

  return resultado