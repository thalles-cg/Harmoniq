from src.database import SessionLocal
from src.service.transcricao import ler_eventos_basic_pitch

db = SessionLocal()

try:
  eventos = ler_eventos_basic_pitch(
    db,
    r".\audio-teste\4_basic_pitch.csv"
  )

  for evento in eventos:
    print(
      f"{evento.inicio:5.2f}s - "
      f"{evento.fim:5.2f}s | "
      f"{evento.nota.nome} | "
      f"pitch class {evento.nota.pitch_class}"
    )
finally:
  db.close()