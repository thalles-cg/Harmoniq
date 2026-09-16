from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.model import Nota
from src.schema.nota import NotaCreate, NotaUpdate
from src.service.nota import (
  atualizar_nota,
  buscar_nota,
  criar_nota,
  excluir_nota,
  listar_notas
)

def criar(db: Session, dados: NotaCreate) -> Nota:
  return criar_nota(db, dados)

def listar(db: Session) -> list[Nota]:
  return listar_notas(db)

def buscar(db: Session, nota_id: int) -> Nota:
  nota = buscar_nota(db, nota_id)
  if nota is None:
    raise HTTPException(status_code=404, detail="Nota não encontrada")

  return nota

def atualizar(db: Session, nota_id: int, dados: NotaUpdate) -> Nota:
  nota = atualizar_nota(db, nota_id, dados)
  if nota is None:
    raise HTTPException(status_code=404, detail="Nota não encontrada")

  return nota

def excluir(db: Session, nota_id: int) -> None:
  resultado = excluir_nota(db, nota_id)
  if not resultado:
    raise HTTPException(status_code=404, detail="Nota não encontrada")