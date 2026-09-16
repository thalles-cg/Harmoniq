from pydantic import BaseModel, ConfigDict

class AcordeBase(BaseModel):
  nome_cifra: str
  nome_extenso: str
  nota_fundamental_id: int
  qualidade: str
  notas: list[int]

class AcordeCreate(AcordeBase):
  pass

class AcordeResponse(AcordeBase):
  id: int
  model_config = ConfigDict(from_attributes=True)