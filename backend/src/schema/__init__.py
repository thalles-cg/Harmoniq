from .acorde import AcordeBase, AcordeCreate, AcordeResponse
from .artista import ArtistaBase, ArtistaCreate, ArtistaResponse
from .musica import MusicaBase, MusicaCreate, MusicaResponse
from .nota import NotaBase, NotaCreate, NotaResponse, NotaUpdate

__all__ = [
  "AcordeBase",
  "AcordeCreate",
  "AcordeResponse",
  "ArtistaBase",
  "ArtistaCreate",
  "ArtistaResponse",
  "MusicaBase",
  "MusicaCreate",
  "MusicaResponse",
  "NotaBase",
  "NotaCreate",
  "NotaResponse",
  "NotaUpdate",
  "AcordeUpdate",
]