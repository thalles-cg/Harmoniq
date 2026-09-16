from pydantic import BaseModel, ConfigDict

class MusicaBase(BaseModel):
  titulo: str
  letra: str | None = None
  album_id: int | None = None

class MusicaCreate(MusicaBase):
  pass

class MusicaResponse(MusicaBase):
  id: int

  model_config = ConfigDict(from_attributes=True)