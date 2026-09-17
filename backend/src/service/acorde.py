from sqlalchemy.orm import Session
from src.model import Acorde, AcordeNota, Nota
from src.schema.acorde import AcordeCreate, AcordeUpdate

def criar_acorde(db: Session, dados: AcordeCreate) -> Acorde | None:
  nota_fundamental = db.query(Nota).filter(
    Nota.id == dados.nota_fundamental_id
  ).first()

  if nota_fundamental is None:
    return None

  notas = db.query(Nota).filter(
    Nota.id.in_(dados.notas)
  ).all()

  if len(notas) != len(dados.notas):
    return None

  novo_acorde = Acorde(
    nome_cifra=dados.nome_cifra,
    nome_extenso=dados.nome_extenso,
    nota_fundamental_id=dados.nota_fundamental_id,
    qualidade=dados.qualidade
  )

  db.add(novo_acorde)
  db.flush()

  for nota_id in dados.notas:
    nova_relacao = AcordeNota(
      nota_id=nota_id,
      acorde_id=novo_acorde.id
    )
    db.add(nova_relacao)

  db.commit()
  db.refresh(novo_acorde)

  return novo_acorde


def listar_acordes(db: Session) -> list[Acorde]:
  return db.query(Acorde).all()


def buscar_acorde(db: Session, acorde_id: int) -> Acorde | None:
  return db.query(Acorde).filter(
    Acorde.id == acorde_id
  ).first()


def atualizar_acorde(db: Session, acorde_id: int, dados: AcordeUpdate) -> Acorde | None:
  acorde = buscar_acorde(db, acorde_id)

  if acorde is None:
    return None

  if dados.nota_fundamental_id is not None:
    nota_fundamental = db.query(Nota).filter(
      Nota.id == dados.nota_fundamental_id
    ).first()

    if nota_fundamental is None:
      return None

    acorde.nota_fundamental_id = dados.nota_fundamental_id

  if dados.nome_cifra is not None:
    acorde.nome_cifra = dados.nome_cifra

  if dados.nome_extenso is not None:
    acorde.nome_extenso = dados.nome_extenso

  if dados.qualidade is not None:
    acorde.qualidade = dados.qualidade

  if dados.notas is not None:
    notas = db.query(Nota).filter(
      Nota.id.in_(dados.notas)
    ).all()

    if len(notas) != len(dados.notas):
      return None

    db.query(AcordeNota).filter(
      AcordeNota.acorde_id == acorde.id
    ).delete()

    for nota_id in dados.notas:
      nova_relacao = AcordeNota(
        nota_id=nota_id,
        acorde_id=acorde.id
      )
      db.add(nova_relacao)

  db.commit()
  db.refresh(acorde)

  return acorde


def excluir_acorde(db: Session, acorde_id: int) -> bool:
  acorde = buscar_acorde(db, acorde_id)

  if acorde is None:
    return False

  db.query(AcordeNota).filter(
    AcordeNota.acorde_id == acorde_id
  ).delete()

  db.delete(acorde)
  db.commit()

  return True