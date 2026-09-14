from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base

class Acorde(Base):
  __tablename__ = "acorde"

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  nome_cifra: Mapped[str] = mapped_column(String(50))
  nome_extenso: Mapped[str] = mapped_column(String(100))
  nota_fundamental_id: Mapped[int] = mapped_column(ForeignKey("nota.id"))
  qualidade: Mapped[str] = mapped_column(String(50))

  notas: Mapped[list["AcordeNota"]] = relationship(back_populates="acorde")
  musicas: Mapped[list["MusicaAcorde"]] = relationship(back_populates="acorde")
  usuarios: Mapped[list["UsuarioAcorde"]] = relationship(back_populates="acorde")
  nota_fundamental: Mapped["Nota"] = relationship(foreign_keys=[nota_fundamental_id])