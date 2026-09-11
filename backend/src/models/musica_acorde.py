from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base

class MusicaAcorde(Base):
  __tablename__ = "musica_acorde"

  musica_id: Mapped[int] = mapped_column(ForeignKey("musica.id"), primary_key=True)
  acorde_id: Mapped[int] = mapped_column(ForeignKey("acorde.id"), primary_key=True)