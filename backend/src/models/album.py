from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base

class Album(Base):
  __tablename__ = "album"

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  titulo: Mapped[str] = mapped_column(String(255))