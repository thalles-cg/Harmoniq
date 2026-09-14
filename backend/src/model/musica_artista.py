from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base

class MusicaArtista(Base):
  __tablename__ = "musica_artista"

  musica_id: Mapped[int] = mapped_column(ForeignKey("musica.id"), primary_key=True)
  artista_id: Mapped[int] = mapped_column(ForeignKey("artista.id"), primary_key=True)
  
  artista: Mapped["Artista"] = relationship(back_populates="musicas")
  musica: Mapped["Musica"] = relationship(back_populates="artistas")