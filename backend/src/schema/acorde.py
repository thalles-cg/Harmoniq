from pydantic import BaseModel, ConfigDict

class AcordeBase(BaseModel):
  nome_cifra: str
  nome_extenso: str
  nota_fundamental_id: int
  qualidade: str
  notas: list[int]

class AcordeCreate(AcordeBase):
  pass

class AcordeUpdate(BaseModel):
  nome_cifra: str | None = None
  nome_extenso: str | None = None
  nota_fundamental_id: int | None = None
  qualidade: str | None = None
  notas: list[int] | None = None

class AcordeResponse(AcordeBase):
  id: int
  model_config = ConfigDict(from_attributes=True)