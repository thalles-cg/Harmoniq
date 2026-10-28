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

def buscar_por_repertorio(db: Session, nomes_acordes: list[str], limiar_minimo: float = 1.0) -> list[dict]:
  acordes_usuario = {nome.strip() for nome in nomes_acordes if nome.strip()}

  if not acordes_usuario:
      return []

  musicas = db.query(Musica).all()
  resultados = []

  for musica in musicas:
    # Busca todas as ocorrências de acordes da música na ordem da cifra
    acordes_musica = (
      db.query(MusicaAcorde)
      .filter(MusicaAcorde.musica_id == musica.id)
      .order_by(MusicaAcorde.posicao)
      .all()
    )

    if not acordes_musica:
      continue

    todas_ocorrencias = [
      ma.acorde.nome_cifra 
      for ma in acordes_musica 
      if ma.acorde and ma.acorde.nome_cifra
    ]

    if not todas_ocorrencias:
      continue

    total_ocorrencias = len(todas_ocorrencias)
    ocorrencias_conhecidas = sum(
      1 for cifra in todas_ocorrencias if cifra in acordes_usuario
    )

    if ocorrencias_conhecidas == 0:
      continue

    # Porcentagem ponderada pela frequência das execuções
    porcentagem = (ocorrencias_conhecidas / total_ocorrencias) * 100

    if porcentagem >= limiar_minimo:
      acordes_unicos_musica = set(todas_ocorrencias)
      acordes_conhecidos = sorted(list(acordes_unicos_musica.intersection(acordes_usuario)))
      acordes_faltantes = sorted(list(acordes_unicos_musica - acordes_usuario))

      resultados.append({
        "musica": musica,
        "porcentagem": round(porcentagem, 1),
        "acordes_conhecidos": acordes_conhecidos,
        "acordes_faltantes": acordes_faltantes,
      })

  # Ordena decrescente pela porcentagem da música que pode ser tocada
  resultados.sort(key=lambda item: item["porcentagem"], reverse=True)

  return resultados

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