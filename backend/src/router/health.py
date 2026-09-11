from fastapi import APIRouter
from sqlalchemy import text
from src.database import engine

router = APIRouter()

@router.get("/health")
def health():
  return {"status": "ok"}

@router.get("/health/database")
def health_deep():
  with engine.connect() as connection:
    connection.execute(text("SELECT 1"))

  return {
    "status": "ok",
    "database": "connected",
  }