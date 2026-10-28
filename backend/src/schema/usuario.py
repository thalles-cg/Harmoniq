from pydantic import BaseModel, ConfigDict

class UsuarioBase(BaseModel):
  nome: str
  email: str

class UsuarioCreate(UsuarioBase):
  senha: str

class UsuarioResponse(UsuarioBase):
  id: int

  model_config = ConfigDict(from_attributes=True)