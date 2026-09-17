from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from src.controller import acorde as controller
from src.database.dependencies import get_db
from src.schema import AcordeCreate, AcordeResponse, AcordeUpdate

router = APIRouter(prefix="/acordes", tags=["Acordes"])

@router.post("/", response_model=AcordeResponse, status_code=status.HTTP_201_CREATED)
def criar_acorde(dados: AcordeCreate, db: Session = Depends(get_db)):
  return controller.criar(db, dados)

@router.get("/", response_model=list[AcordeResponse])
def listar_acordes(db: Session = Depends(get_db)):
  return controller.listar(db)

@router.get("/{acorde_id}", response_model=AcordeResponse)
def buscar_acorde(acorde_id: int, db: Session = Depends(get_db)):
  return controller.buscar(db, acorde_id)

@router.patch("/{acorde_id}", response_model=AcordeResponse)
def atualizar_acorde(acorde_id: int, dados: AcordeUpdate,db: Session = Depends(get_db)):
  return controller.atualizar(db, acorde_id, dados)

@router.delete("/{acorde_id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_acorde(acorde_id: int, db: Session = Depends(get_db)):
  controller.excluir(db, acorde_id)

