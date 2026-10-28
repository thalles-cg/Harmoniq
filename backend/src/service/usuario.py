from sqlalchemy.orm import Session
from pwdlib import PasswordHash
from src.model.usuario import Usuario
from src.schema.usuario import UsuarioCreate

password_hash = PasswordHash.recommended()

def criar_usuario(db: Session, dados: UsuarioCreate) -> Usuario:
  senha_hash = password_hash.hash(dados.senha)

  usuario = Usuario(
    nome=dados.nome,
    email=dados.email,
    senha_hash=senha_hash
  )

  db.add(usuario)
  db.commit()
  db.refresh(usuario)

  return usuario

def buscar_por_id(db: Session, usuario_id: int) -> Usuario | None:
  return db.get(Usuario, usuario_id)