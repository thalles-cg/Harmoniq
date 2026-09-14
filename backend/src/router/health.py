from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from src.database.dependencies import get_db

router = APIRouter()

@router.get("/health")
def health():
  return {"status": "ok"}

@router.get("/health/database")
def health_database(db: Session = Depends(get_db)):
  db.execute(text("SELECT 1"))

  return {
    "status": "ok",
    "database": "connected",
  }