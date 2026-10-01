from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.model import Acorde
from src.schema.acorde import AcordeCreate, AcordeResponse, AcordeUpdate

from src.service.acorde import (
  atualizar_acorde,
  buscar_acorde,
  criar_acorde,
  excluir_acorde,
  listar_acordes,
)

def _montar_resposta(acorde: Acorde) -> AcordeResponse:
  return AcordeResponse(
    id=acorde.id,
    nome_cifra=acorde.nome_cifra,
    nome_extenso=acorde.nome_extenso,
    nota_fundamental_id=acorde.nota_fundamental_id,
    nota_fundamental=acorde.nota_fundamental.nome,
    qualidade=acorde.qualidade,
    notas=[relacao.nota_id for relacao in acorde.notas],
  )

def criar(db: Session, dados: AcordeCreate) -> AcordeResponse:
  acorde = criar_acorde(db, dados)

  if acorde is None:
    raise HTTPException(
      status_code=400,
      detail="Não foi possível criar o acorde."
    )

  return _montar_resposta(acorde)

def listar(db: Session) -> list[AcordeResponse]:
  acordes = listar_acordes(db)
  return [_montar_resposta(acorde) for acorde in acordes]

def buscar(db: Session, acorde_id: int) -> AcordeResponse:
  acorde = buscar_acorde(db, acorde_id)

  if acorde is None:
    raise HTTPException(
      status_code=404,
      detail="Acorde não encontrado"
    )

  return _montar_resposta(acorde)

def atualizar(db: Session, acorde_id: int, dados: AcordeUpdate) -> AcordeResponse:
  acorde = atualizar_acorde(db, acorde_id, dados)

  if acorde is None:
    raise HTTPException(
      status_code=404,
      detail="Acorde não encontrado ou dados inválidos"
    )

  return _montar_resposta(acorde)

def excluir(db: Session, acorde_id: int) -> None:
  resultado = excluir_acorde(db, acorde_id)

  if not resultado:
    raise HTTPException(
      status_code=404,
      detail="Acorde não encontrado"
    )

