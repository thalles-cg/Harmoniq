from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base

class MusicaInterrupcao(Base):
    __tablename__ = "musica_interrupcao"

    musica_id: Mapped[int] = mapped_column(ForeignKey("musica.id"), primary_key=True)
    posicao: Mapped[int] = mapped_column(Integer,primary_key=True)

    musica: Mapped["Musica"] = relationship(back_populates="interrupcoes")
