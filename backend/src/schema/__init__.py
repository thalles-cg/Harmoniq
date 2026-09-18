from .acorde import AcordeBase, AcordeCreate, AcordeResponse, AcordeUpdate
from .artista import ArtistaBase, ArtistaCreate, ArtistaResponse
from .musica import MusicaBase, MusicaCreate, MusicaResponse, MusicaUpdate
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
  "MusicaUpdate",
  "NotaBase",
  "NotaCreate",
  "NotaResponse",
  "NotaUpdate",
  "AcordeUpdate",
]