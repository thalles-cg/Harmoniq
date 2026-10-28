from sqlalchemy.orm import Session
from src.schema.usuario import UsuarioCreate
from src.service import usuario as service

def criar(db: Session, dados: UsuarioCreate):
  return service.criar_usuario(db, dados)

def buscar_por_id(db: Session, usuario_id: int):
  return service.buscar_por_id(db, usuario_id)