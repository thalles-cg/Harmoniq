from sqlalchemy.orm import Session
from src.schema.usuario import UsuarioCreate
from src.service import usuario as service

def criar(db: Session, dados: UsuarioCreate):
  return service.criar_usuario(db, dados)