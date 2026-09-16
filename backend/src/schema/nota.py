from pydantic import BaseModel, ConfigDict

class NotaBase(BaseModel):
  nome: str
  pitch_class: int

class NotaCreate(NotaBase):
  pass

class NotaUpdate(BaseModel):
  nome: str | None = None
  pitch_class: int | None = None

class NotaResponse(NotaBase):
  id: int
  model_config = ConfigDict(from_attributes=True)