from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base

class Musica(Base):
  __tablename__ = "musica"

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  titulo: Mapped[str] = mapped_column(String(255))
  letra: Mapped[str | None] = mapped_column(Text)
  album_id: Mapped[int | None] = mapped_column(ForeignKey("album.id"))
  progressao_relativa: Mapped[str | None] = mapped_column(Text)
  tom: Mapped[str | None] = mapped_column(String(3), nullable=True)
  
  album: Mapped["Album | None"] = relationship(back_populates="musicas")
  artistas: Mapped[list["MusicaArtista"]] = relationship(back_populates="musica")
  generos: Mapped[list["MusicaGenero"]] = relationship(back_populates="musica")
  acordes: Mapped[list["MusicaAcorde"]] = relationship(back_populates="musica")
  interrupcoes: Mapped[list["MusicaInterrupcao"]] = relationship(back_populates="musica")
  favoritos: Mapped[list["Favorito"]] = relationship(back_populates="musica")