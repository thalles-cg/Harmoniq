from src.database import SessionLocal
from src.service.transcricao import (ler_eventos_basic_pitch, consolidar_eventos_nota, identificar_regioes_notas)

db = SessionLocal()

try:
  eventos = ler_eventos_basic_pitch(
    db,
    r".\audio-teste\4_basic_pitch.csv"
  )

  eventos_consolidados = consolidar_eventos_nota(eventos)
  regioes = identificar_regioes_notas(eventos_consolidados)

  for regiao in regioes:
    notas = ", ".join(
      nota.nome
      for nota in regiao.notas
    )

    print(
      f"{regiao.inicio:5.2f}s - "
      f"{regiao.fim:5.2f}s | "
      f"{notas}"
    )
    
finally:
  db.close()