from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base

class MusicaAcorde(Base):
  __tablename__ = "musica_acorde"

  musica_id: Mapped[int] = mapped_column(ForeignKey("musica.id"), primary_key=True)
  acorde_id: Mapped[int] = mapped_column(ForeignKey("acorde.id"), primary_key=True)
  posicao: Mapped[int] = mapped_column(Integer)

  acorde: Mapped["Acorde"] = relationship(back_populates="musicas")
  musica: Mapped["Musica"] = relationship(back_populates="acordes")