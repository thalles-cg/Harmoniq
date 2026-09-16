from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from src.controller import nota as controller
from src.database.dependencies import get_db
from src.schema import NotaCreate, NotaResponse, NotaUpdate

router = APIRouter(prefix="/notas", tags=["Notas"])

@router.post("/", response_model=NotaResponse, status_code=status.HTTP_201_CREATED)
def criar_nota(dados: NotaCreate, db: Session = Depends(get_db)):
  return controller.criar(db, dados)

@router.get("/", response_model=list[NotaResponse])
def listar_notas(db: Session = Depends(get_db)):
  return controller.listar(db)

@router.get("/{nota_id}", response_model=NotaResponse)
def buscar_nota(nota_id: int, db: Session = Depends(get_db)):
  return controller.buscar(db, nota_id)

@router.patch("/{nota_id}", response_model=NotaResponse)
def atualizar_nota(nota_id: int, dados: NotaUpdate, db: Session = Depends(get_db)):
  return controller.atualizar(db, nota_id, dados)

@router.delete("/{nota_id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_nota(nota_id: int, db: Session = Depends(get_db)):
  controller.excluir(db, nota_id)