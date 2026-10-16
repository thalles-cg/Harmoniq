from sqlalchemy import case, func
from sqlalchemy.orm import Session
from src.model import Acorde, Album, Musica, MusicaAcorde, MusicaInterrupcao
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

def buscar_por_repertorio(db: Session, nomes_acordes: list[str]) -> list[Musica]:
  nomes_acordes = list({
    nome.strip()
    for nome in nomes_acordes
    if nome.strip()
  })

  if not nomes_acordes:
    return []

  musicas = (
    db.query(Musica)
    .join(MusicaAcorde, MusicaAcorde.musica_id == Musica.id)
    .join(Acorde, Acorde.id == MusicaAcorde.acorde_id)
    .group_by(Musica.id)
    .having(func.count(func.distinct(Acorde.id)) > 0)
    .having(
      func.sum(
        case(
          (Acorde.nome_cifra.not_in(nomes_acordes), 1),
          else_=0
        )
      ) == 0
    )
    .all()
  )

  return musicas


def buscar_por_sequencia(db: Session, nomes_acordes: list[str]) -> list[Musica]:
  nomes_acordes = [
    nome.strip()
    for nome in nomes_acordes
    if nome.strip()
  ]

  if not nomes_acordes:
    return []

  musicas = db.query(Musica).all()
  resultado = []

  for musica in musicas:
    acordes = (
      db.query(MusicaAcorde)
      .filter(MusicaAcorde.musica_id == musica.id)
      .order_by(MusicaAcorde.posicao)
      .all()
    )

    interrupcoes = {
      interrupcao.posicao
      for interrupcao in db.query(MusicaInterrupcao)
      .filter(MusicaInterrupcao.musica_id == musica.id)
      .all()
    }

    acordes_por_posicao = {
      acorde.posicao: acorde.acorde.nome_cifra
      for acorde in acordes
    }

    tamanho_sequencia = len(nomes_acordes)

    for posicao_inicial in acordes_por_posicao:
      posicoes = range(
        posicao_inicial,
        posicao_inicial + tamanho_sequencia
      )

      if any(posicao in interrupcoes for posicao in posicoes):
        continue

      sequencia_encontrada = [
        acordes_por_posicao.get(posicao)
        for posicao in posicoes
      ]

      if sequencia_encontrada == nomes_acordes:
        resultado.append(musica)
        break

  return resultado


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