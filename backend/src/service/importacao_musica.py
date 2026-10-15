from sqlalchemy.orm import Session
from src.model import (
  Acorde,
  Artista,
  Musica,
  MusicaAcorde,
  MusicaArtista,
  MusicaInterrupcao,
)

def importar_musica(
  db: Session,
  titulo: str,
  artista_nome: str,
  acordes_posicionados: list[tuple[int, str]],
  interrupcoes: list[int] | None = None,
):
  titulo = titulo.strip()
  artista_nome = artista_nome.strip()
  interrupcoes = interrupcoes or []

  if not titulo or not artista_nome:
    raise ValueError("Título e artista são obrigatórios.")

  if not acordes_posicionados:
    raise ValueError("Informe pelo menos um acorde.")

  acordes_banco = {
    acorde.nome_cifra: acorde
    for acorde in db.query(Acorde).all()
  }

  acordes_invalidos = sorted({
    nome_acorde
    for _, nome_acorde in acordes_posicionados
    if nome_acorde not in acordes_banco
  })

  if acordes_invalidos:
    raise ValueError(
      "Acordes não cadastrados: "
      + ", ".join(acordes_invalidos)
    )

  artista = (
    db.query(Artista)
    .filter(Artista.nome == artista_nome)
    .first()
  )

  if artista is not None:
    musica_existente = (
      db.query(Musica)
      .join(MusicaArtista)
      .filter(
        Musica.titulo == titulo,
        MusicaArtista.artista_id == artista.id,
      )
      .first()
    )

    if musica_existente is not None:
      raise ValueError(
        "Essa música já está cadastrada para esse artista."
      )

  try:
    if artista is None:
      artista = Artista(nome=artista_nome)
      db.add(artista)
      db.flush()

    musica = Musica(titulo=titulo)
    db.add(musica)
    db.flush()

    db.add(
      MusicaArtista(
        musica_id=musica.id,
        artista_id=artista.id,
      )
    )

    for posicao, nome_acorde in acordes_posicionados:
      db.add(
        MusicaAcorde(
          musica_id=musica.id,
          posicao=posicao,
          acorde_id=acordes_banco[nome_acorde].id,
        )
      )

    for posicao in interrupcoes:
      db.add(
        MusicaInterrupcao(
          musica_id=musica.id,
          posicao=posicao,
        )
      )

    db.commit()
    db.refresh(musica)

    return musica

  except Exception:
    db.rollback()
    raise
