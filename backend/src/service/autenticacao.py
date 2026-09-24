from sqlalchemy import select
from sqlalchemy.orm import Session
from pwdlib import PasswordHash
from src.model.usuario import Usuario

password_hash = PasswordHash.recommended()

def autenticar_usuario(db: Session, email: str, senha: str) -> Usuario | None:
  usuario = db.scalar(
    select(Usuario).where(Usuario.email == email)
  )

  if usuario is None:
    return None

  if not password_hash.verify(senha, usuario.senha_hash):
    return None

  return usuario