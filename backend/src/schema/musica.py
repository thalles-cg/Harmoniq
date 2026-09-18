from pydantic import BaseModel, ConfigDict

class MusicaBase(BaseModel):
  titulo: str
  letra: str | None = None
  album_id: int | None = None
  progressao_relativa: str | None = None

class MusicaCreate(MusicaBase):
  pass

class MusicaUpdate(BaseModel):
  titulo: str | None = None
  letra: str | None = None
  album_id: int | None = None
  progressao_relativa: str | None = None

class MusicaResponse(MusicaBase):
  id: int
  model_config = ConfigDict(from_attributes=True)