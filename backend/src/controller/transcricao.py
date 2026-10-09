from pathlib import Path
from tempfile import NamedTemporaryFile
from fastapi import HTTPException, UploadFile, status
from src.service.btc_service import transcrever_audio

EXTENSOES_PERMITIDAS = {".mp3", ".wav", ".flac", ".ogg", ".m4a"}

def transcrever(arquivo: UploadFile) -> list[dict]:
  extensao = Path(arquivo.filename or "").suffix.lower()

  if extensao not in EXTENSOES_PERMITIDAS:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail="Formato de áudio não suportado.",
    )

  caminho_temporario = None

  try:
    with NamedTemporaryFile(
      suffix=extensao,
      delete=False,
    ) as temporario:
      caminho_temporario = Path(temporario.name)

      while bloco := arquivo.file.read(1024 * 1024):
        temporario.write(bloco)

    return transcrever_audio(caminho_temporario)

  except HTTPException:
    raise

  except Exception as erro:
    raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail="Não foi possível transcrever o áudio.",
    ) from erro

  finally:
    if caminho_temporario is not None:
      caminho_temporario.unlink(missing_ok=True)

    arquivo.file.close()