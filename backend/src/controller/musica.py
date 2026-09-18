from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.model import Musica
from src.schema.musica import MusicaCreate, MusicaUpdate

from src.service.musica import (
  atualizar_musica,
  buscar_musica,
  criar_musica,
  excluir_musica,
  listar_musicas,
)

def criar(db: Session, dados: MusicaCreate) -> Musica:
  musica = criar_musica(db, dados)

  if musica is None:
    raise HTTPException(
      status_code=400,
      detail="Não foi possível criar a música."
    )

  return musica

def listar(db: Session) -> list[Musica]:
  return listar_musicas(db)

def buscar(db: Session, musica_id: int) -> Musica:
  musica = buscar_musica(db, musica_id)

  if musica is None:
    raise HTTPException(
      status_code=404,
      detail="Música não encontrada"
    )

  return musica

def atualizar(db: Session, musica_id: int, dados: MusicaUpdate) -> Musica:
  musica = atualizar_musica(db, musica_id, dados)

  if musica is None:
    raise HTTPException(
      status_code=404,
      detail="Música não encontrada ou dados inválidos"
    )

  return musica

def excluir(db: Session, musica_id: int) -> None:
  resultado = excluir_musica(db, musica_id)

  if not resultado:
    raise HTTPException(
      status_code=404,
      detail="Música não encontrada"
    )