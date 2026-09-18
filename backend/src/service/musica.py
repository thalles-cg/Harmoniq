from sqlalchemy.orm import Session
from src.model import Album, Musica
from src.schema.musica import MusicaCreate, MusicaUpdate

def criar_musica(db: Session, dados: MusicaCreate) -> Musica | None:
  if dados.album_id is not None:
    album = db.query(Album).filter(
      Album.id == dados.album_id
    ).first()

    if album is None:
      return None

  nova_musica = Musica(
    titulo=dados.titulo,
    letra=dados.letra,
    album_id=dados.album_id,
    progressao_relativa=dados.progressao_relativa
  )

  db.add(nova_musica)
  db.commit()
  db.refresh(nova_musica)

  return nova_musica

def listar_musicas(db: Session) -> list[Musica]:
  return db.query(Musica).all()

def buscar_musica(db: Session, musica_id: int) -> Musica | None:
  return db.query(Musica).filter(
    Musica.id == musica_id
  ).first()

def atualizar_musica(db: Session, musica_id: int, dados: MusicaUpdate) -> Musica | None:
  musica = buscar_musica(db, musica_id)

  if musica is None:
    return None

  if dados.album_id is not None:
    album = db.query(Album).filter(
      Album.id == dados.album_id
    ).first()

    if album is None:
      return None

  if dados.titulo is not None:
    musica.titulo = dados.titulo

  if dados.letra is not None:
    musica.letra = dados.letra

  if dados.album_id is not None:
    musica.album_id = dados.album_id

  if dados.progressao_relativa is not None:
    musica.progressao_relativa = dados.progressao_relativa

  db.commit()
  db.refresh(musica)

  return musica

def excluir_musica(db: Session, musica_id: int) -> bool:
  musica = buscar_musica(db, musica_id)

  if musica is None:
    return False

  db.delete(musica)
  db.commit()

  return True