from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base

class Album(Base):
  __tablename__ = "album"

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  titulo: Mapped[str] = mapped_column(String(255))
  
  musicas: Mapped[list["Musica"]] = relationship(back_populates="album")