import subprocess
from pathlib import Path
from tempfile import NamedTemporaryFile
from fastapi import HTTPException, UploadFile, status
from src.service.btc_service import transcrever_audio

EXTENSOES_PERMITIDAS = {".mp3", ".wav", ".flac", ".ogg", ".m4a", ".webm", ".weba", ".mp4", ".opus"}

def converter_para_wav(caminho_entrada: Path) -> Path:
  """Converte qualquer áudio para WAV 22.05kHz Mono para garantir compatibilidade com o BTC."""
  caminho_wav = caminho_entrada.with_suffix(".wav")

  cmd = [
    "ffmpeg",
    "-y",
    "-i", str(caminho_entrada),
    "-ar", "22050",
    "-ac", "1",
    str(caminho_wav)
  ]

  resultado = subprocess.run(cmd, capture_output=True, text=True)

  if resultado.returncode != 0:
    raise RuntimeError(
      "Certifique-se de que o FFmpeg está instalado e configurado no PATH do sistema.\n"
      f"Erro na conversão: {resultado.stderr}"
    )

  return caminho_wav

def transcrever(arquivo: UploadFile) -> list[dict]:
  extensao = Path(arquivo.filename or "").suffix.lower()

  if extensao not in EXTENSOES_PERMITIDAS:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail="Formato de áudio não suportado.",
    )

  caminho_temporario = None
  caminho_wav = None

  try:
    with NamedTemporaryFile(suffix=extensao, delete=False) as temporario:
      caminho_temporario = Path(temporario.name)
      while bloco := arquivo.file.read(1024 * 1024):
        temporario.write(bloco)

    # Se o áudio não for .wav, converte para .wav antes de enviar ao BTC
    if extensao != ".wav":
      caminho_wav = converter_para_wav(caminho_temporario)
      arquivo_final = caminho_wav
    else:
      arquivo_final = caminho_temporario

    return transcrever_audio(arquivo_final)

  except HTTPException:
    raise

  except Exception as erro:
    print("\n" + "=" * 50)
    print("DETALHES DO ERRO DE TRANSCRIÇÃO:")
    print(str(erro))
    print("=" * 50 + "\n")

    raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail=f"Falha na transcrição: {str(erro)}",
    ) from erro

  finally:
    if caminho_temporario is not None:
      caminho_temporario.unlink(missing_ok=True)
    if caminho_wav is not None:
      caminho_wav.unlink(missing_ok=True)

    arquivo.file.close()