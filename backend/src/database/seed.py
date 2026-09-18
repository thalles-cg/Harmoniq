from sqlalchemy.orm import Session
from src.database import SessionLocal
from src.model import Nota

NOTAS = [
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

def seed_notas(db: Session) -> None:
  for dados in NOTAS:
    nota = db.query(Nota).filter(
      Nota.pitch_class == dados["pitch_class"]
    ).first()

    if nota is None:
      db.add(Nota(**dados))

  db.commit()

def main() -> None:
  db = SessionLocal()

  try:
    seed_notas(db)
  finally:
    db.close()

if __name__ == "__main__":
  main()