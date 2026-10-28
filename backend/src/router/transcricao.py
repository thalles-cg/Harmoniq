from fastapi import APIRouter, File, UploadFile
from src.controller import transcricao as controller

router = APIRouter(prefix="/transcricoes", tags=["Transcrições"])

@router.post("/")
def transcrever_audio(arquivo: UploadFile = File(...)):
  return controller.transcrever(arquivo)