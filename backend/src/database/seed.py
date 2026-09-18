from sqlalchemy.orm import Session
from src.database import SessionLocal
from src.model import Acorde, AcordeNota, Musica, MusicaAcorde, Nota

def seed_notas(db: Session):
  notas = [
    {"nome": "C", "pitch_class": 0},
    {"nome": "C#", "pitch_class": 1},
    {"nome": "D", "pitch_class": 2},
    {"nome": "D#", "pitch_class": 3},
    {"nome": "E", "pitch_class": 4},
    {"nome": "F", "pitch_class": 5},
    {"nome": "F#", "pitch_class": 6},
    {"nome": "G", "pitch_class": 7},
    {"nome": "G#", "pitch_class": 8},
    {"nome": "A", "pitch_class": 9},
    {"nome": "A#", "pitch_class": 10},
    {"nome": "B", "pitch_class": 11},
  ]

  for dados in notas:
    nota = db.query(Nota).filter(Nota.nome == dados["nome"]).first()

    if nota is None:
      db.add(Nota(**dados))

  db.commit()

def seed_acordes(db: Session):
  notas = {
    nota.nome: nota
    for nota in db.query(Nota).all()
  }

  acordes = [
      # C
    {
    "nome_cifra": "C",
    "nome_extenso": "Dó Maior",
    "nota_fundamental": "C",
    "qualidade": "M",
    "notas": ["C", "E", "G"],
    },
    {
      "nome_cifra": "Cm",
      "nome_extenso": "Dó Menor",
      "nota_fundamental": "C",
      "qualidade": "m",
      "notas": ["C", "D#", "G"],
    },
    {
      "nome_cifra": "C7",
      "nome_extenso": "Dó com Sétima",
      "nota_fundamental": "C",
      "qualidade": "7",
      "notas": ["C", "E", "G", "A#"],
    },
    {
      "nome_cifra": "Cm7",
      "nome_extenso": "Dó Menor com Sétima",
      "nota_fundamental": "C",
      "qualidade": "m7",
      "notas": ["C", "D#", "G", "A#"],
    },

    # C#
    {
      "nome_cifra": "C#",
      "nome_extenso": "Dó Sustenido Maior",
      "nota_fundamental": "C#",
      "qualidade": "M",
      "notas": ["C#", "F", "G#"],
    },
    {
      "nome_cifra": "C#m",
      "nome_extenso": "Dó Sustenido Menor",
      "nota_fundamental": "C#",
      "qualidade": "m",
      "notas": ["C#", "E", "G#"],
    },
    {
      "nome_cifra": "C#7",
      "nome_extenso": "Dó Sustenido com Sétima",
      "nota_fundamental": "C#",
      "qualidade": "7",
      "notas": ["C#", "F", "G#", "B"],
    },
    {
      "nome_cifra": "C#m7",
      "nome_extenso": "Dó Sustenido Menor com Sétima",
      "nota_fundamental": "C#",
      "qualidade": "m7",
      "notas": ["C#", "E", "G#", "B"],
    },

    # D
    {
      "nome_cifra": "D",
      "nome_extenso": "Ré Maior",
      "nota_fundamental": "D",
      "qualidade": "M",
      "notas": ["D", "F#", "A"],
    },
    {
      "nome_cifra": "Dm",
      "nome_extenso": "Ré Menor",
      "nota_fundamental": "D",
      "qualidade": "m",
      "notas": ["D", "F", "A"],
    },
    {
      "nome_cifra": "D7",
      "nome_extenso": "Ré com Sétima",
      "nota_fundamental": "D",
      "qualidade": "7",
      "notas": ["D", "F#", "A", "C"],
    },
    {
      "nome_cifra": "Dm7",
      "nome_extenso": "Ré Menor com Sétima",
      "nota_fundamental": "D",
      "qualidade": "m7",
      "notas": ["D", "F", "A", "C"],
    },

    # D#
    {
      "nome_cifra": "D#",
      "nome_extenso": "Ré Sustenido Maior",
      "nota_fundamental": "D#",
      "qualidade": "M",
      "notas": ["D#", "G", "A#"],
    },
    {
      "nome_cifra": "D#m",
      "nome_extenso": "Ré Sustenido Menor",
      "nota_fundamental": "D#",
      "qualidade": "m",
      "notas": ["D#", "F#", "A#"],
    },
    {
      "nome_cifra": "D#7",
      "nome_extenso": "Ré Sustenido com Sétima",
      "nota_fundamental": "D#",
      "qualidade": "7",
      "notas": ["D#", "G", "A#", "C#"],
    },
    {
      "nome_cifra": "D#m7",
      "nome_extenso": "Ré Sustenido Menor com Sétima",
      "nota_fundamental": "D#",
      "qualidade": "m7",
      "notas": ["D#", "F#", "A#", "C#"],
    },

    # E
    {
      "nome_cifra": "E",
      "nome_extenso": "Mi Maior",
      "nota_fundamental": "E",
      "qualidade": "M",
      "notas": ["E", "G#", "B"],
    },
    {
      "nome_cifra": "Em",
      "nome_extenso": "Mi Menor",
      "nota_fundamental": "E",
      "qualidade": "m",
      "notas": ["E", "G", "B"],
    },
    {
      "nome_cifra": "E7",
      "nome_extenso": "Mi com Sétima",
      "nota_fundamental": "E",
      "qualidade": "7",
      "notas": ["E", "G#", "B", "D"],
    },
    {
      "nome_cifra": "Em7",
      "nome_extenso": "Mi Menor com Sétima",
      "nota_fundamental": "E",
      "qualidade": "m7",
      "notas": ["E", "G", "B", "D"],
    },

    # F
    {
      "nome_cifra": "F",
      "nome_extenso": "Fá Maior",
      "nota_fundamental": "F",
      "qualidade": "M",
      "notas": ["F", "A", "C"],
    },
    {
      "nome_cifra": "Fm",
      "nome_extenso": "Fá Menor",
      "nota_fundamental": "F",
      "qualidade": "m",
      "notas": ["F", "G#", "C"],
    },
    {
      "nome_cifra": "F7",
      "nome_extenso": "Fá com Sétima",
      "nota_fundamental": "F",
      "qualidade": "7",
      "notas": ["F", "A", "C", "D#"],
    },
    {
      "nome_cifra": "Fm7",
      "nome_extenso": "Fá Menor com Sétima",
      "nota_fundamental": "F",
      "qualidade": "m7",
      "notas": ["F", "G#", "C", "D#"],
    },

    # F#
    {
      "nome_cifra": "F#",
      "nome_extenso": "Fá Sustenido Maior",
      "nota_fundamental": "F#",
      "qualidade": "M",
      "notas": ["F#", "A#", "C#"],
    },
    {
      "nome_cifra": "F#m",
      "nome_extenso": "Fá Sustenido Menor",
      "nota_fundamental": "F#",
      "qualidade": "m",
      "notas": ["F#", "A", "C#"],
    },
    {
      "nome_cifra": "F#7",
      "nome_extenso": "Fá Sustenido com Sétima",
      "nota_fundamental": "F#",
      "qualidade": "7",
      "notas": ["F#", "A#", "C#", "E"],
    },
    {
      "nome_cifra": "F#m7",
      "nome_extenso": "Fá Sustenido Menor com Sétima",
      "nota_fundamental": "F#",
      "qualidade": "m7",
      "notas": ["F#", "A", "C#", "E"],
    },

    # G
    {
      "nome_cifra": "G",
      "nome_extenso": "Sol Maior",
      "nota_fundamental": "G",
      "qualidade": "M",
      "notas": ["G", "B", "D"],
    },
    {
      "nome_cifra": "Gm",
      "nome_extenso": "Sol Menor",
      "nota_fundamental": "G",
      "qualidade": "m",
      "notas": ["G", "A#", "D"],
    },
    {
      "nome_cifra": "G7",
      "nome_extenso": "Sol com Sétima",
      "nota_fundamental": "G",
      "qualidade": "7",
      "notas": ["G", "B", "D", "F"],
    },
    {
      "nome_cifra": "Gm7",
      "nome_extenso": "Sol Menor com Sétima",
      "nota_fundamental": "G",
      "qualidade": "m7",
      "notas": ["G", "A#", "D", "F"],
    },

    # G#
    {
      "nome_cifra": "G#",
      "nome_extenso": "Sol Sustenido Maior",
      "nota_fundamental": "G#",
      "qualidade": "M",
      "notas": ["G#", "C", "D#"],
    },
    {
      "nome_cifra": "G#m",
      "nome_extenso": "Sol Sustenido Menor",
      "nota_fundamental": "G#",
      "qualidade": "m",
      "notas": ["G#", "B", "D#"],
    },
    {
      "nome_cifra": "G#7",
      "nome_extenso": "Sol Sustenido com Sétima",
      "nota_fundamental": "G#",
      "qualidade": "7",
      "notas": ["G#", "C", "D#", "F#"],
    },
    {
      "nome_cifra": "G#m7",
      "nome_extenso": "Sol Sustenido Menor com Sétima",
      "nota_fundamental": "G#",
      "qualidade": "m7",
      "notas": ["G#", "B", "D#", "F#"],
    },

    # A
    {
      "nome_cifra": "A",
      "nome_extenso": "Lá Maior",
      "nota_fundamental": "A",
      "qualidade": "M",
      "notas": ["A", "C#", "E"],
    },
    {
      "nome_cifra": "Am",
      "nome_extenso": "Lá Menor",
      "nota_fundamental": "A",
      "qualidade": "m",
      "notas": ["A", "C", "E"],
    },
    {
      "nome_cifra": "A7",
      "nome_extenso": "Lá com Sétima",
      "nota_fundamental": "A",
      "qualidade": "7",
      "notas": ["A", "C#", "E", "G"],
    },
    {
      "nome_cifra": "Am7",
      "nome_extenso": "Lá Menor com Sétima",
      "nota_fundamental": "A",
      "qualidade": "m7",
      "notas": ["A", "C", "E", "G"],
    },

    # A#
    {
      "nome_cifra": "A#",
      "nome_extenso": "Lá Sustenido Maior",
      "nota_fundamental": "A#",
      "qualidade": "M",
      "notas": ["A#", "D", "F"],
    },
    {
      "nome_cifra": "A#m",
      "nome_extenso": "Lá Sustenido Menor",
      "nota_fundamental": "A#",
      "qualidade": "m",
      "notas": ["A#", "C#", "F"],
    },
    {
      "nome_cifra": "A#7",
      "nome_extenso": "Lá Sustenido com Sétima",
      "nota_fundamental": "A#",
      "qualidade": "7",
      "notas": ["A#", "D", "F", "G#"],
    },
    {
      "nome_cifra": "A#m7",
      "nome_extenso": "Lá Sustenido Menor com Sétima",
      "nota_fundamental": "A#",
      "qualidade": "m7",
      "notas": ["A#", "C#", "F", "G#"],
    },

    # B
    {
      "nome_cifra": "B",
      "nome_extenso": "Si Maior",
      "nota_fundamental": "B",
      "qualidade": "M",
      "notas": ["B", "D#", "F#"],
    },
    {
      "nome_cifra": "Bm",
      "nome_extenso": "Si Menor",
      "nota_fundamental": "B",
      "qualidade": "m",
      "notas": ["B", "D", "F#"],
    },
    {
      "nome_cifra": "B7",
      "nome_extenso": "Si com Sétima",
      "nota_fundamental": "B",
      "qualidade": "7",
      "notas": ["B", "D#", "F#", "A"],
    },
    {
      "nome_cifra": "Bm7",
      "nome_extenso": "Si Menor com Sétima",
      "nota_fundamental": "B",
      "qualidade": "m7",
      "notas": ["B", "D", "F#", "A"],
    },
  ]

  for dados in acordes:
    acorde_existente = (
      db.query(Acorde)
      .filter(Acorde.nome_cifra == dados["nome_cifra"])
      .first()
    )

    if acorde_existente is not None:
      continue

    nota_fundamental = notas[dados["nota_fundamental"]]

    acorde = Acorde(
      nome_cifra=dados["nome_cifra"],
      nome_extenso=dados["nome_extenso"],
      nota_fundamental_id=nota_fundamental.id,
      qualidade=dados["qualidade"],
    )

    db.add(acorde)
    db.flush()

    for nome_nota in dados["notas"]:
      db.add(
        AcordeNota(
          acorde_id=acorde.id,
          nota_id=notas[nome_nota].id,
        )
      )

  db.commit()

def seed_musicas(db: Session):
  acordes = {
    acorde.nome_cifra: acorde
    for acorde in db.query(Acorde).all()
  }

  musicas = [
    {
      "titulo": "Chega de Saudade",
      "acordes": ["C", "Am", "Dm", "G7"],
    },
    {
      "titulo": "Garota de Ipanema",
      "acordes": ["F", "G7", "Gm7", "C7"],
    },
    {
      "titulo": "Desafinado",
      "acordes": ["F", "G7", "Gm7", "C7"],
    },
    {
      "titulo": "Corcovado",
      "acordes": ["C", "Am", "Dm", "G7"],
    },
  ]

  for dados in musicas:
    musica_existente = (
      db.query(Musica)
      .filter(Musica.titulo == dados["titulo"])
      .first()
    )

    if musica_existente is not None:
      continue

    musica = Musica(
      titulo=dados["titulo"],
    )

    db.add(musica)
    db.flush()

    for posicao, nome_acorde in enumerate(dados["acordes"], start=1):
      db.add(
        MusicaAcorde(
          musica_id=musica.id,
          posicao=posicao,
          acorde_id=acordes[nome_acorde].id,
        )
      )

  db.commit()

def seed():
  db = SessionLocal()

  try:
    seed_notas(db)
    seed_acordes(db)
    seed_musicas(db)
  finally:
    db.close()

if __name__ == "__main__":
  seed()