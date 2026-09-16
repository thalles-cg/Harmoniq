from sqlalchemy.orm import Session
from src.model import Nota
from src.schema.nota import NotaCreate, NotaUpdate

def criar_nota(db: Session, nota: NotaCreate) -> Nota:
  nova_nota = Nota(
    nome=nota.nome,
    pitch_class=nota.pitch_class
  )

  db.add(nova_nota)
  db.commit()
  db.refresh(nova_nota)

  return nova_nota

def listar_notas(db: Session) -> list[Nota]:
  return db.query(Nota).all()

def buscar_nota(db: Session, nota_id: int) -> Nota | None:
  return db.get(Nota, nota_id)

def atualizar_nota(db: Session, nota_id: int, dados: NotaUpdate) -> Nota | None:
  nota = db.get(Nota, nota_id)
  if nota is None:
    return None

  dados_atualizacao = dados.model_dump(exclude_unset=True)
  for campo, valor in dados_atualizacao.items():
    setattr(nota, campo, valor)

  db.commit()
  db.refresh(nota)

  return nota

def excluir_nota(db: Session, nota_id: int) -> bool:
  nota = db.get(Nota, nota_id)
  if nota is None:
    return False

  db.delete(nota)
  db.commit()

  return True