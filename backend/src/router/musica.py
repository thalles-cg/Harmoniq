from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from src.controller import musica as controller
from src.database.dependencies import get_db
from src.schema import MusicaCreate, MusicaResponse, MusicaUpdate, MusicaBuscaSequenciaResponse

router = APIRouter(prefix="/musicas", tags=["Músicas"])

@router.post("/", response_model=MusicaResponse, status_code=status.HTTP_201_CREATED)
def criar_musica(dados: MusicaCreate, db: Session = Depends(get_db)):
  return controller.criar(db, dados)

@router.get("/", response_model=list[MusicaResponse])
def listar_musicas(db: Session = Depends(get_db)):
  return controller.listar(db)

@router.get("/busca/repertorio", response_model=list[MusicaResponse])
def buscar_por_repertorio(acordes: list[str] = Query(...), db: Session = Depends(get_db)):
  return controller.buscar_repertorio(db, acordes)

@router.get("/busca/sequencia", response_model=list[MusicaBuscaSequenciaResponse])
def buscar_por_sequencia(graus: list[str] = Query(...), db: Session = Depends(get_db)):
  return controller.buscar_sequencia(db, graus)

@router.get("/{musica_id}", response_model=MusicaResponse)
def buscar_musica(musica_id: int, db: Session = Depends(get_db)):
  return controller.buscar(db, musica_id)

@router.patch("/{musica_id}", response_model=MusicaResponse)
def atualizar_musica(musica_id: int, dados: MusicaUpdate, db: Session = Depends(get_db)):
  return controller.atualizar(db, musica_id, dados)

@router.delete("/{musica_id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_musica(musica_id: int, db: Session = Depends(get_db)):
  controller.excluir(db, musica_id)