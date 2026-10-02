import csv
from dataclasses import dataclass
from sqlalchemy.orm import Session
from src.model import Nota

@dataclass
class EventoNota:
  nota: Nota
  inicio: float
  fim: float

def ler_eventos_basic_pitch(db: Session, caminho_csv: str) -> list[EventoNota]:
  """
  Lê os eventos de notas gerados pelo Basic Pitch,
  converte cada MIDI para o pitch_class correspondente
  e associa o evento à Nota existente no banco de dados.
  """

  eventos: list[EventoNota] = []

  with open(caminho_csv, newline="", encoding="utf-8") as arquivo:
    leitor = csv.DictReader(arquivo)

    for linha in leitor:
      midi_pitch = int(linha["pitch_midi"])
      pitch_class = midi_pitch % 12

      nota = (
        db.query(Nota)
        .filter(Nota.pitch_class == pitch_class)
        .first()
      )

      if nota is None:
        continue

      eventos.append(
        EventoNota(
          nota=nota,
          inicio=float(linha["start_time_s"]),
          fim=float(linha["end_time_s"]),
        )
      )

  return sorted(eventos, key=lambda evento: evento.inicio)