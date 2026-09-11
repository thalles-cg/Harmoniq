from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base

class Acorde(Base):
  __tablename__ = "acorde"

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  nome: Mapped[str] = mapped_column(String(255))