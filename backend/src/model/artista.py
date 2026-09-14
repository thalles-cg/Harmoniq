from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base

class Artista(Base):
  __tablename__ = "artista"

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  nome: Mapped[str] = mapped_column(String(255))
  
  musicas: Mapped[list["MusicaArtista"]] = relationship(back_populates="artista")