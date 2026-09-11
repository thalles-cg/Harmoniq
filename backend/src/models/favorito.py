from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base

class Favorito(Base):
  __tablename__ = "favorito"

  usuario_id: Mapped[int] = mapped_column(ForeignKey("usuario.id"), primary_key=True)
  musica_id: Mapped[int] = mapped_column(ForeignKey("musica.id"), primary_key=True)