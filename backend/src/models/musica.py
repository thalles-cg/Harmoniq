from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base

class Musica(Base):
  __tablename__ = "musica"

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  titulo: Mapped[str] = mapped_column(String(255))
  letra: Mapped[str | None] = mapped_column(Text)
  album_id: Mapped[int | None] = mapped_column(ForeignKey("album.id"))
  progressao_relativa: Mapped[str | None] = mapped_column(Text)