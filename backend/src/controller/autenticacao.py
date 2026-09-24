from sqlalchemy.orm import Session
from src.service import autenticacao as service

def autenticar(db: Session, email: str, senha: str):
  return service.autenticar_usuario(db, email, senha)