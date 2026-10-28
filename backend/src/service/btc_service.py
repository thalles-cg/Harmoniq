import json
import os
import subprocess
import tempfile
from pathlib import Path

HARMONIQ_DIR = Path(__file__).resolve().parents[3]
BTC_DIR = HARMONIQ_DIR / "btc"
BTC_PYTHON = BTC_DIR / ".venv" / "Scripts" / "python.exe"
BTC_SCRIPT = BTC_DIR / "transcrever_audio.py"

def transcrever_audio(caminho_audio: str | Path) -> list[dict]:
  audio = Path(caminho_audio).resolve()

  if not audio.is_file():
    raise FileNotFoundError(f"Áudio não encontrado: {audio}")

  if not BTC_PYTHON.is_file():
    raise FileNotFoundError(
      f"Python do ambiente BTC não encontrado: {BTC_PYTHON}"
    )

  if not BTC_SCRIPT.is_file():
    raise FileNotFoundError(
      f"Script de transcrição não encontrado: {BTC_SCRIPT}"
    )

  with tempfile.TemporaryDirectory(prefix="harmoniq_") as temp:
    arquivo_json = Path(temp) / "resultado.json"

    resultado = subprocess.run(
      [
        str(BTC_PYTHON),
        str(BTC_SCRIPT),
        "--audio",
        str(audio),
        "--output-json",
        str(arquivo_json),
      ],
      cwd=BTC_DIR,
      capture_output=True,
      text=True,
      encoding="utf-8",
      errors="replace",
      timeout=600,
    )

    if resultado.returncode != 0:
      raise RuntimeError(
        "Falha ao transcrever o áudio com o BTC.\n"
        f"Saída:\n{resultado.stdout}\n"
        f"Erros:\n{resultado.stderr}"
      )

    if not arquivo_json.is_file():
      raise RuntimeError(
        "O processo BTC terminou sem gerar o JSON esperado."
      )

    return json.loads(arquivo_json.read_text(encoding="utf-8"))