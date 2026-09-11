from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base

class Acorde(Base):
  __tablename__ = "acorde"

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  nome_cifra: Mapped[str] = mapped_column(String(50))
  nome_extenso: Mapped[str] = mapped_column(String(100))
  nota_fundamental: Mapped[str] = mapped_column(String(10))
  qualidade: Mapped[str] = mapped_column(String(50))
  pitch_class: Mapped[int] = mapped_column(Integer)