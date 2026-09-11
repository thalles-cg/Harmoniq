from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base

class Intervalo(Base):
  __tablename__ = "intervalo"

  acorde_id: Mapped[int] = mapped_column(ForeignKey("acorde.id"), primary_key=True)
  intervalo: Mapped[int] = mapped_column(Integer, primary_key=True)