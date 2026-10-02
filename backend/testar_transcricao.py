from src.database import SessionLocal
from src.service.transcricao import (ler_eventos_basic_pitch, consolidar_eventos_nota)

db = SessionLocal()

try:
  eventos = ler_eventos_basic_pitch(
    db,
    r".\audio-teste\4_basic_pitch.csv"
  )

  eventos_consolidados = consolidar_eventos_nota(eventos)

  for evento in eventos_consolidados:
    print(
      f"{evento.inicio:5.2f}s -"
      f"{evento.fim:5.2f}s | "
      f"{evento.nota.nome} | "
      f"{evento.fim - evento.inicio:5.2f}s"
    )
finally:
  db.close()