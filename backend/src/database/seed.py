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
  # Qualidades utilizadas pelo vocabulário expandido do BTC.
  # Os números representam intervalos em semitons.
  qualidades = {
    "min": {
      "sufixo": "m",
      "descricao": "Menor",
      "intervalos": [0, 3, 7],
    },
    "maj": {
      "sufixo": "",
      "descricao": "Maior",
      "intervalos": [0, 4, 7],
    },
    "dim": {
      "sufixo": "dim",
      "descricao": "Diminuto",
      "intervalos": [0, 3, 6],
    },
    "aug": {
      "sufixo": "aug",
      "descricao": "Aumentado",
      "intervalos": [0, 4, 8],
    },
    "min6": {
      "sufixo": "m6",
      "descricao": "Menor com Sexta",
      "intervalos": [0, 3, 7, 9],
    },
    "maj6": {
      "sufixo": "6",
      "descricao": "Maior com Sexta",
      "intervalos": [0, 4, 7, 9],
    },
    "min7": {
      "sufixo": "m7",
      "descricao": "Menor com Sétima",
      "intervalos": [0, 3, 7, 10],
    },
    "minmaj7": {
      "sufixo": "m(maj7)",
      "descricao": "Menor com Sétima Maior",
      "intervalos": [0, 3, 7, 11],
    },
    "maj7": {
      "sufixo": "maj7",
      "descricao": "Maior com Sétima Maior",
      "intervalos": [0, 4, 7, 11],
    },
    "7": {
      "sufixo": "7",
      "descricao": "Maior com Sétima Menor",
      "intervalos": [0, 4, 7, 10],
    },
    "dim7": {
      "sufixo": "dim7",
      "descricao": "Sétima Diminuta",
      "intervalos": [0, 3, 6, 9],
    },
    "hdim7": {
      "sufixo": "m7(b5)",
      "descricao": "Meio-Diminuto",
      "intervalos": [0, 3, 6, 10],
    },
    "sus2": {
      "sufixo": "sus2",
      "descricao": "Segunda Suspensa",
      "intervalos": [0, 2, 7],
    },
    "sus4": {
      "sufixo": "sus4",
      "descricao": "Quarta Suspensa",
      "intervalos": [0, 5, 7],
    },
    "power": {
      "sufixo": "5",
      "descricao": "Quinta (Power Chord)",
      "intervalos": [0, 7],
    },
    "9": {
      "sufixo": "9",
      "descricao": "Com Nona Maior",
      "intervalos": [0, 4, 7, 10, 14],
    },
    "min9": {
      "sufixo": "m9",
      "descricao": "Menor com Nona",
      "intervalos": [0, 3, 7, 10, 14], 
    },
  }

  nomes_notas = {
    "C": "Dó",
    "C#": "Dó Sustenido",
    "D": "Ré",
    "D#": "Ré Sustenido",
    "E": "Mi",
    "F": "Fá",
    "F#": "Fá Sustenido",
    "G": "Sol",
    "G#": "Sol Sustenido",
    "A": "Lá",
    "A#": "Lá Sustenido",
    "B": "Si",
  }

  notas = {
    nota.nome: nota
    for nota in db.query(Nota).all()
  }

  acordes_existentes = {
    acorde.nome_cifra: acorde
    for acorde in db.query(Acorde).all()
  }

  if len(notas) != 12:
    raise ValueError(
      "É necessário cadastrar as 12 notas antes dos acordes."
    )

  try:
    for nome_fundamental, nome_extenso in nomes_notas.items():
      fundamental = notas[nome_fundamental]

      for qualidade, dados in qualidades.items():
        nome_cifra = nome_fundamental + dados["sufixo"]

        acorde = acordes_existentes.get(nome_cifra)

        if acorde is None:
          acorde = Acorde(
            nome_cifra=nome_cifra,
            nome_extenso=f"{nome_extenso} {dados['descricao']}",
            nota_fundamental_id=fundamental.id,
            qualidade=qualidade,
          )

          db.add(acorde)
          db.flush()

          acordes_existentes[nome_cifra] = acorde

        else:
          acorde.qualidade = qualidade
          acorde.nome_extenso = (
            f"{nome_extenso} {dados['descricao']}"
          )
          acorde.nota_fundamental_id = fundamental.id

        pitch_classes = {
          (fundamental.pitch_class + intervalo) % 12
          for intervalo in dados["intervalos"]
        }

        notas_acorde = [
          nota
          for nota in notas.values()
          if nota.pitch_class in pitch_classes
        ]

        notas_atuais = {
          relacao.nota_id: relacao
          for relacao in db.query(AcordeNota)
            .filter(AcordeNota.acorde_id == acorde.id)
            .all()
        }

        ids_esperados = {
          nota.id for nota in notas_acorde
        }

        for nota_id, relacao in notas_atuais.items():
          if nota_id not in ids_esperados:
            db.delete(relacao)

        for nota in notas_acorde:
          if nota.id not in notas_atuais:
            db.add(
              AcordeNota(
                acorde_id=acorde.id,
                nota_id=nota.id,
              )
            )

    db.commit()

  except Exception:
    db.rollback()
    raise

def seed():
  db = SessionLocal()

  try:
    seed_notas(db)
    seed_acordes(db)
  finally:
    db.close()

if __name__ == "__main__":
  seed()