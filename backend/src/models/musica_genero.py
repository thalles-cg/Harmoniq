from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base

class MusicaGenero(Base):
  __tablename__ = "musica_genero"

  musica_id: Mapped[int] = mapped_column(ForeignKey("musica.id"), primary_key=True)
  genero_id: Mapped[int] = mapped_column(ForeignKey("genero.id"), primary_key=True)