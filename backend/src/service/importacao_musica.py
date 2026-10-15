from sqlalchemy.orm import Session
from src.model import (
  Acorde,
  Artista,
  Musica,
  MusicaAcorde,
  MusicaArtista,
)

def importar_musica(db: Session, titulo: str, artista_nome: str, acordes: list[str]):
  titulo = titulo.strip()
  artista_nome = artista_nome.strip()

  if not titulo or not artista_nome:
    raise ValueError("Título e artista são obrigatórios.")

  if not acordes:
    raise ValueError("Informe pelo menos um acorde.")

  acordes_banco = {
    acorde.nome_cifra: acorde
    for acorde in db.query(Acorde).all()
  }

  acordes_invalidos = sorted({
    nome for nome in acordes
    if nome not in acordes_banco
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

    for posicao, nome_acorde in enumerate(acordes, start=1):
      db.add(
        MusicaAcorde(
          musica_id=musica.id,
          posicao=posicao,
          acorde_id=acordes_banco[nome_acorde].id,
        )
      )

    db.commit()
    db.refresh(musica)

    return musica

  except Exception:
    db.rollback()
    raise
