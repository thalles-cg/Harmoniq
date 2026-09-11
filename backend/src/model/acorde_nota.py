from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base

class AcordeNota(Base):
  __tablename__ = "acorde_nota"

  nota_id: Mapped[int] = mapped_column(ForeignKey("nota.id"), primary_key=True)
  acorde_id: Mapped[int] = mapped_column(ForeignKey("acorde.id"), primary_key=True)

  nota: Mapped["Nota"] = relationship(back_populates="acordes")
  acorde: Mapped["Acorde"] = relationship(back_populates="notas")