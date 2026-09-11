from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base

class Genero(Base):
  __tablename__ = "genero"

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  nome: Mapped[str] = mapped_column(String(255))
  
  musicas: Mapped[list["MusicaGenero"]] = relationship(back_populates="genero")