from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base

class Nota(Base):
  __tablename__ = "nota"

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  nome: Mapped[str] = mapped_column(String(20))
  pitch_class: Mapped[int] = mapped_column(Integer)

  acordes: Mapped[list["AcordeNota"]] = relationship(back_populates="nota")