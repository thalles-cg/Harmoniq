from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base

class Usuario(Base):
  __tablename__ = "usuario"

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  nome: Mapped[str] = mapped_column(String(255))
  email: Mapped[str] = mapped_column(String(255))
  senha_hash: Mapped[str] = mapped_column(String(255))