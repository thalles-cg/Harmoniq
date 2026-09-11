from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base

class UsuarioAcorde(Base):
  __tablename__ = "usuario_acorde"

  usuario_id: Mapped[int] = mapped_column(ForeignKey("usuario.id"), primary_key=True)
  acorde_id: Mapped[int] = mapped_column(ForeignKey("acorde.id"), primary_key=True)