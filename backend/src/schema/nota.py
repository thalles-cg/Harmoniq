from pydantic import BaseModel, ConfigDict

class NotaBase(BaseModel):
  nome: str
  pitch_class: int

class NotaCreate(NotaBase):
  pass

class NotaResponse(NotaBase):
  id: int
  model_config = ConfigDict(from_attributes=True)