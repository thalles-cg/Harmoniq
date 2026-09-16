from pydantic import BaseModel, ConfigDict

class ArtistaBase(BaseModel):
  nome: str

class ArtistaCreate(ArtistaBase):
  pass

class ArtistaResponse(ArtistaBase):
  id: int

  model_config = ConfigDict(from_attributes=True)