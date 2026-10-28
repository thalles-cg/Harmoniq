from sqlalchemy.orm import Session
from src.service import autenticacao as autenticacao_service
from src.service import token as token_service

def autenticar(db: Session, email: str, senha: str):
  usuario = autenticacao_service.autenticar_usuario(
    db,
    email,
    senha
  )

  if usuario is None:
    return None

  access_token = token_service.criar_token_acesso(usuario.id)

  return {
    "access_token": access_token,
    "token_type": "bearer"
  }