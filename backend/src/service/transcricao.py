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

def consolidar_eventos_nota(eventos: list[EventoNota]) -> list[EventoNota]:
  """
  Consolida eventos sobrepostos ou consecutivos da mesma nota
  em um único intervalo de tempo.
  """

  eventos_por_nota: dict[int, list[EventoNota]] = {}

  for evento in eventos:
    eventos_por_nota.setdefault(evento.nota.id, []).append(evento)

  eventos_consolidados: list[EventoNota] = []

  for eventos_nota in eventos_por_nota.values():
    eventos_nota.sort(key=lambda evento: evento.inicio)

    atual = eventos_nota[0]

    for proximo in eventos_nota[1:]:
      if proximo.inicio <= atual.fim:
        atual = EventoNota(
          nota=atual.nota,
          inicio=atual.inicio,
          fim=max(atual.fim, proximo.fim),
        )
      else:
        eventos_consolidados.append(atual)
        atual = proximo

    eventos_consolidados.append(atual)

  return sorted(eventos_consolidados, key=lambda evento: evento.inicio)